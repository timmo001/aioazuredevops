"""Enable CLI."""
import asyncio
import json

import click

from aioazuredevops.client import DevOpsClient, DevOpsProject


@click.command()
@click.option("--organization", "-u", help="Organization")
@click.option("--project", "-p", help="Project")
@click.option("--pat", "-t", help="Personal Access Token")
def cli(organization: str, project: str, pat: str = None):
    """CLI for this package."""
    asyncio.run(handle(organization, project, pat))


async def handle(organization: str, project: str, pat: str = None) -> None:
    client = DevOpsClient()
    if pat is not None:
        if await client.authorize(pat, organization) is True:
            print("Authenticated.")
        else:
            return
    project: DevOpsProject = await client.get_project(organization, project)
    if project is not None:
        print(project.id)
        print(project.name)
        print(project.description)


cli()  # pylint: disable=E1120
