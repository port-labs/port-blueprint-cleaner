import asyncio
import argparse
from port_cleaner.core.cleaner import PortBlueprintCleaner
from port_cleaner.config.settings import PortConfig


def main():
    parser = argparse.ArgumentParser(description='Clean Port blueprints')
    parser.add_argument('--client-id', required=True, help='Port client ID')
    parser.add_argument('--client-secret', required=True, help='Port client secret')
    parser.add_argument('--api-url', default='https://api.getport.io/v1', help='Port API URL')
    parser.add_argument('--integration-identifier', required=True, help='Integration identifier')
    parser.add_argument('--integration-type', required=True, help='Integration type')
    parser.add_argument('--from-date', required=True, help='Start date in ISO format (e.g. 2025-05-13T00:00:00.000Z)')
    parser.add_argument('--to-date', required=True, help='End date in ISO format (e.g. 2025-05-13T23:59:59.999Z)')
    parser.add_argument('--blueprint-identifiers', required=True, nargs='+', help='Blueprint identifiers (space-separated list)')

    args = parser.parse_args()

    config = PortConfig(
        client_id=args.client_id,
        client_secret=args.client_secret,
        api_url=args.api_url,
        integration_identifier=args.integration_identifier,
        integration_type=args.integration_type,
    )

    cleaner = PortBlueprintCleaner(
        client_id=config.client_id,
        client_secret=config.client_secret,
        api_url=config.api_url,
        integration_identifier=config.integration_identifier,
        integration_type=config.integration_type,
    )
    
    asyncio.run(cleaner.clean(
        from_date=args.from_date,
        to_date=args.to_date,
        blueprint_identifiers=args.blueprint_identifiers
    ))


if __name__ == "__main__":
    main()
