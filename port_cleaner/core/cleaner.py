import httpx
from port_cleaner.core.entities import EntityClientMixin
from port_cleaner.core.auth import PortAuthentication


class PortBlueprintCleaner(EntityClientMixin, PortAuthentication):
    def __init__(self, 
                    client_id: str,
                    client_secret: str,
                    api_url: str,
                    integration_identifier: str,
                    integration_type: str,
        ):
        client = httpx.AsyncClient()
        auth = PortAuthentication(client, client_id, client_secret, api_url, integration_identifier, integration_type)
        EntityClientMixin.__init__(self, auth, httpx.AsyncClient())

    async def clean(self, from_date: str, to_date: str, blueprint_identifiers: list[str]):
        async for entities in self.search_entities_updated_at(
            from_date=from_date,
            to_date=to_date,
            blueprint_identifiers=blueprint_identifiers
        ):
            await self.batch_delete_entities(
                entities=entities,
                request_options={
                    "merge": False,
                    "create_missing_related_entities": False,
                    "delete_dependent_entities": True,
                    "validation_only": False
                },
                user_agent_type="exporter"
            ) 
