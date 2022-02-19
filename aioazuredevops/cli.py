"""Enable CLI"""
import asyncio

import click

from aioazuredevops.builds import DevOpsBuild
from aioazuredevops.client import DevOpsClient
from aioazuredevops.core import DevOpsProject
from aioazuredevops.wiql import DevOpsWiqlResult
from aioazuredevops.work_item import DevOpsWorkItem


@click.command()
@click.option("--organization", "-u", help="Organization")
@click.option("--project", "-p", help="Project")
@click.option("--pat", "-t", help="Personal Access Token")
def cli(organization: str, project: str, pat: str = None):
    """CLI for this package."""
    asyncio.get_event_loop().run_until_complete(handle(organization, project, pat))


async def handle(organization: str, project: str, pat: str = None) -> None:
    """Handle CLI command"""
    client = DevOpsClient()
    if pat is not None:
        await client.authorize(pat, organization)
        print(client.authorized)
        if client.authorized:
            print("Authorized.")
        else:
            print("Not authorized.")
            return
    print("Project:")
    doProject: DevOpsProject = await client.get_project(organization, project)
    if doProject is not None:
        print(doProject.id)
        print(doProject.name)
        print(doProject.description)
    print("Builds:")
    builds: list[DevOpsBuild] = await client.get_builds(
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

    wiql_result: DevOpsWiqlResult = await client.get_work_items_ids_all(
        organization,
        project,
    )
    if wiql_result:
        ids: list[int] = [item.id for item in wiql_result.work_items]
        print("Work item ids:")
        print(ids)

        work_items: DevOpsWorkItem = await client.get_work_items(
            organization,
            project,
            ids,
        )
        if work_items:
            print("Work items:")
            for item in work_items.value:
                print("---------------------------------")
                print(item.id)
                print(item.fields.title)
                print(item.fields.created_by.display_name)
                print(item.fields.work_item_type)


cli()
