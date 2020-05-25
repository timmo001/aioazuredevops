"""Enable CLI."""
import asyncio
import json
from typing import List

import click

from aioazuredevops.client import DevOpsClient
from aioazuredevops.core import DevOpsProject
from aioazuredevops.builds import DevOpsBuild


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
    print("Project:")
    doProject: DevOpsProject = await client.get_project(organization, project)
    if doProject is not None:
        print(doProject.id)
        print(doProject.name)
        print(doProject.description)
    print("Builds:")
    builds: List[DevOpsBuild] = await client.get_builds(
        organization,
        project,
        "?queryOrder=queueTimeDescending&maxBuildsPerDefinition=1",
    )
    if builds is not None and len(builds) > 0:
        build: DevOpsBuild = builds[0]
        if build is not None:
            print(build.id)
            print(build.build_number)
            print(build.status)
            print(build.result)
            print(build.source_branch)
            print(build.source_version)
            print(build.definition.id)
            print(build.definition.name)
            print(build.project.id)
            print(build.project.name)


cli()  # pylint: disable=E1120
