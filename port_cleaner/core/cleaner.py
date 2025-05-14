"""
Main cleaner class implementation
"""

import asyncio
import httpx
from datetime import datetime
from typing import List, Dict, Any
from loguru import logger
from port_cleaner.core.entities import EntityClientMixin
from port_cleaner.core.auth import PortAuthentication
from port_cleaner.config.settings import PortConfig
from port_cleaner.utils.models import SummaryStats


class PortBlueprintCleaner(EntityClientMixin, PortAuthentication):
    def __init__(self, config: PortConfig):
        client = httpx.AsyncClient()
        auth = PortAuthentication(
            client,
            config.client_id,
            config.client_secret,
            config.api_url,
            config.integration_identifier,
            config.integration_type,
        )
        EntityClientMixin.__init__(self, auth, httpx.AsyncClient())
        self.stats = SummaryStats()

    async def clean(
        self,
        from_date: str,
        to_date: str,
        blueprint_identifiers: list[str],
        dry_run: bool = True,
    ):

        mode = "dry run" if dry_run else "cleanup"
        logger.info(
            f"Starting {mode} for blueprints: {', '.join(blueprint_identifiers)}"
        )

        async for entities in self.search_entities_updated_at(
            from_date=from_date,
            to_date=to_date,
            blueprint_identifiers=blueprint_identifiers,
        ):
            self._update_stats(entities)

            if not dry_run:
                await self.batch_delete_entities(
                    entities=entities,
                    request_options={
                        "merge": False,
                        "create_missing_related_entities": False,
                        "delete_dependent_entities": True,
                        "validation_only": False,
                    },
                    user_agent_type="exporter",
                )

        self._log_summary(dry_run)

    def _update_stats(self, entities: List[Any]):
        """Update statistics about entities to be deleted."""
        self.stats.total_entities += len(entities)

        for entity in entities:
            blueprint = entity.blueprint
            self.stats.entities_by_blueprint[blueprint] = (
                self.stats.entities_by_blueprint.get(blueprint, 0) + 1
            )

            updated_at = entity.properties.get("updatedAt")
            if updated_at:
                updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                if (
                    not self.stats.oldest_entity
                    or updated_at < self.stats.oldest_entity
                ):
                    self.stats.oldest_entity = updated_at
                if (
                    not self.stats.newest_entity
                    or updated_at > self.stats.newest_entity
                ):
                    self.stats.newest_entity = updated_at

    def _log_summary(self, dry_run: bool):
        action = "Would delete" if dry_run else "Deleted"
        blueprint_summary = ", ".join(
            f"{bp}: {count}" for bp, count in self.stats.entities_by_blueprint.items()
        )

        logger.info(
            f"{action} {self.stats.total_entities} entities ({blueprint_summary})"
        )
