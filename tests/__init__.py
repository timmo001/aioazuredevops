"""Setup for tests."""

from typing import Final

ORGANIZATION: Final[str] = "testorg"
PROJECT: Final[str] = "testproject"
PAT: Final[str] = "testpat"


RESPONSE_JSON_BASIC: Final[dict] = {"test": "test"}

RESPONSE_JSON_DEVOPS_PROJECT: Final[dict] = {
    "id": "testid",
    "name": "testname",
    "description": "testdescription",
    "url": "testurl",
    "state": "teststate",
    "capabilities": {
        "processTemplate": {
            "templateName": "Agile",
            "templateTypeId": "abc123-abc1-abc1-abc1-abc123456789",
        },
        "versioncontrol": {
            "sourceControlType": "Git",
            "gitEnabled": "True",
            "tfvcEnabled": "False",
        },
    },
    "revision": 1,
    "visibility": "testvisibility",
    "lastUpdated": None,
    "defaultTeam": {
        "id": "testid",
        "name": "testname",
        "url": "testurl",
    },
    "_links": {
        "self": {"href": "testself"},
        "collection": {"href": "testcollection"},
        "web": {"href": "testweb"},
    },
}


RESPONSE_JSON_DEVOPS_BUILD_DEFINITION: Final[dict] = {
    "id": 1,
    "name": "testname",
    "url": "testurl",
    "path": "testpath",
    "type": "testtype",
    "queueStatus": "testqueuestatus",
    "revision": 1,
}

RESPONSE_JSON_DEVOPS_BUILD: Final[dict] = {
    "id": 1,
    "buildNumber": "testbuildnumber",
    "status": "teststatus",
    "result": "testresult",
    "sourceBranch": "testsourcebranch",
    "sourceVersion": "testsourceversion",
    "priority": "testpriority",
    "reason": "testreason",
    "queueTime": "testqueuetime",
    "startTime": "teststarttime",
    "finishTime": "testfinishtime",
    "definition": RESPONSE_JSON_DEVOPS_BUILD_DEFINITION,
    "project": RESPONSE_JSON_DEVOPS_PROJECT,
    "_links": {
        "self": {"href": "testself"},
        "web": {"href": "testweb"},
        "sourceVersionDisplayUri": {"href": "testsourceversiondisplayuri"},
        "timeline": {"href": "testtimeline"},
        "badge": {"href": "testbadge"},
    },
}


RESPONSE_JSON_DEVOPS_BUILDS: Final[dict] = {"value": [RESPONSE_JSON_DEVOPS_BUILD]}

RESPONSE_JSON_DEVOPS_WIQL_RESULT: Final[dict] = {
    "queryType": "testqueryType",
    "queryResultType": "testqueryResultType",
    "asOf": "testasOf",
    "columns": [
        {
            "referenceName": "testreferenceName",
            "name": "testname",
            "url": None,
        }
    ],
    "workItems": [
        {
            "id": 123,
            "url": "testurl",
        }
    ],
}

RESPONSE_JSON_DEVOPS_WORK_ITEM: Final[dict] = {
    "id": 123,
    "rev": 234,
    "fields": {
        "System.Id": 123,
        "System.Title": "testTitle",
        "System.AreaPath": "testAreaPath",
        "System.TeamProject": "testTeamProject",
        "System.IterationPath": "testIterationPath",
        "System.WorkItemType": "testWorkItemType",
        "System.State": "testState",
        "System.Reason": "testReason",
        "System.CreatedDate": "testCreatedDate",
        "System.ChangedDate": "testChangedDate",
        "System.CommentCount": 1,
        "Microsoft.VSTS.Common.Priority": 1,
    },
    "url": "testurl",
}

RESPONSE_JSON_DEVOPS_WORK_ITEMS: Final[dict] = {
    "count": 1,
    "value": [
        RESPONSE_JSON_DEVOPS_WORK_ITEM,
    ],
}
