"""
Configuration settings for the Port Cleaner
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PortConfig:
    """Configuration for Port API connection"""

    client_id: str
    client_secret: str
    integration_identifier: Optional[str] = None
    integration_type: Optional[str] = None
    api_url: str = "https://api.getport.io/v1"
