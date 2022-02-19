"""
Basic WIQL Query to get all work items in a project
https://docs.microsoft.com/en-gb/rest/api/azure/devops/wit/wiql/query-by-wiql?view=azure-devops-rest-6.0
"""
from datetime import datetime


class DevOpsWiqlColumn:
    reference_name: str
    name: str
    url: str

    def __init__(self, reference_name: str, name: str, url: str) -> None:
        self.reference_name = reference_name
        self.name = name
        self.url = url


class DevOpsWiqlWorkItem:
    id: int
    url: str

    def __init__(self, id: int, url: str) -> None:
        self.id = id
        self.url = url


class DevOpsWiqlResult:
    query_type: str
    query_result_type: str
    as_of: datetime
    columns: list[DevOpsWiqlColumn]
    work_items: list[DevOpsWiqlWorkItem]

    def __init__(
        self,
        query_type: str,
        query_result_type: str,
        as_of: datetime,
        columns: list[DevOpsWiqlColumn],
        work_items: list[DevOpsWiqlWorkItem],
    ) -> None:
        self.query_type = query_type
        self.query_result_type = query_result_type
        self.as_of = as_of
        self.columns = columns
        self.work_items = work_items
