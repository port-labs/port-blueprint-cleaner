import asyncio
from typing import Any, AsyncIterator, List
from urllib.parse import quote_plus


import httpx
from loguru import logger

from port_cleaner.core.auth import PortAuthentication
from port_cleaner.utils.helpers import stream_async_iterators_tasks, handle_status_code
from port_cleaner.utils.models import Entity, RequestOptions

PORT_MAX_CONCURRENCY = 50


class EntityClientMixin:
    def __init__(self, auth: PortAuthentication, client: httpx.AsyncClient):
        self.auth = auth
        self.client = client
        self.semaphore = asyncio.Semaphore(
            PORT_MAX_CONCURRENCY
        )

    async def delete_entity(
        self,
        entity: Entity,
        request_options: RequestOptions,
        user_agent_type: str | None = None,
        should_raise: bool = True,
    ) -> None:
        async with self.semaphore:
            logger.info(
                f"Delete entity: {entity.identifier} of blueprint: {entity.blueprint}"
            )
            response = await self.client.delete(
                f"{self.auth.api_url}/blueprints/{entity.blueprint}/entities/{quote_plus(entity.identifier)}",
                headers=await self.auth.headers(user_agent_type),
                params={
                    "delete_dependents": str(
                        request_options["delete_dependent_entities"]
                    ).lower()
                },
            )

            if response.is_error:
                if response.status_code == 404:
                    logger.info(
                        f"Failed to delete entity: {entity.identifier} of blueprint: {entity.blueprint},"
                        f" as it was already deleted from port"
                    )
                    return
                logger.error(
                    f"Error deleting "
                    f"entity: {entity.identifier} of "
                    f"blueprint: {entity.blueprint}"
                )

            handle_status_code(response, should_raise)

    async def batch_delete_entities(
        self,
        entities: list[Entity],
        request_options: RequestOptions,
        user_agent_type: str | None = None,
        should_raise: bool = True,
    ) -> None:
        results = await asyncio.gather(
            *(
                self.delete_entity(
                    entity,
                    request_options,
                    user_agent_type,
                    should_raise=should_raise,
                )
                for entity in entities
            ),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Failed to delete entity: {str(result)}")
        return results

    async def search_paginated_entities(
        self,
        blueprint_identifier: str,
        user_agent_type: str = "exporter",
        rules: List[dict[Any, Any]] | None = None,
        parameters_to_include: List[str] | None = None,
        limit: int = 100,
    ) -> AsyncIterator[List[Entity]]:
        query = {
            "combinator": "and",
            "rules": [
                {
                    "property": "$datasource",
                    "operator": "contains",
                    "value": f"port-ocean/{self.auth.integration_type}/",
                },
                {
                    "property": "$datasource",
                    "operator": "contains",
                    "value": f"/{self.auth.integration_identifier}/{user_agent_type}",
                },
            ],
        }

        if rules:
            query["rules"] = query["rules"] + rules


        page_token = None
        while True:
            logger.info(f"Searching entities with query {query}")
            data = {
                    "query": query,
                    **({"from": page_token} if page_token is not None else {}),
                    "limit": limit,
                    "include": parameters_to_include or ["blueprint", "identifier"],
                }
            response = await self.client.post(
                f"https://api.port.io/v1/blueprints/{blueprint_identifier}/entities/search",
                json=data,
                headers=await self.auth.headers(user_agent_type),
            )
            handle_status_code(response)
            response_data = response.json()
            
            yield [Entity.parse_obj(entity_data) for entity_data in response_data["entities"]]
                
            if not (page_token := response_data.get("next")):
                break

    
    async def search_entities_updated_at(
            self, from_date: str, to_date: str, blueprint_identifiers: List[str], user_agent_type: str =  "exporter", 
    ) -> AsyncIterator[Entity]:
        tasks: List[AsyncIterator[list[Entity]]] = []
        for blueprint_identifier in blueprint_identifiers:
            search_rules = [
                {
                    "property": "updatedAt",
                    "operator": "notBetween",
                    "value": {
                        "from": from_date,
                        "to": to_date
                    }
                }
            ]
            tasks.append(self.search_paginated_entities(
                blueprint_identifier,
                user_agent_type,
                search_rules
            ))
        
        async for entity in stream_async_iterators_tasks(*tasks):
            yield entity
