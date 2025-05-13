
from pydantic import BaseModel, Field, PrivateAttr
from port_cleaner.utils.helpers import get_time
from typing import Any, TypedDict

RequestOptions = TypedDict(
    "RequestOptions",
    {
        "merge": bool,
        "create_missing_related_entities": bool,
        "delete_dependent_entities": bool,
        "validation_only": bool,
    },
)



class TokenResponse(BaseModel):
    access_token: str = Field(alias="accessToken")
    expires_in: int = Field(alias="expiresIn")
    token_type: str = Field(alias="tokenType")
    _retrieved_time: int = PrivateAttr(default_factory=lambda: int(get_time()))

    @property
    def expired(self) -> bool:
        return self._retrieved_time + self.expires_in <= get_time()

    @property
    def full_token(self) -> str:
        return f"{self.token_type} {self.access_token}"



class Entity(BaseModel):
    identifier: Any
    blueprint: Any
    title: Any
    team: str | None | list[Any] | dict[str, Any] = []
    properties: dict[str, Any] = {}
    relations: dict[str, Any] = {}

    @property
    def is_using_search_identifier(self) -> bool:
        return isinstance(self.identifier, dict)

    @property
    def is_using_search_relation(self) -> bool:
        return any(
            isinstance(relation, dict) for relation in self.relations.values()
        ) or (
            self.team is not None and any(isinstance(team, dict) for team in self.team)
        )
