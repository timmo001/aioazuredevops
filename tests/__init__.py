"""Setup for tests."""

from __future__ import annotations

from typing import Final

ORGANIZATION: Final[str] = "testorg"
PROJECT: Final[str] = "testproject"
PAT: Final[str] = "testpat"


RESPONSE_JSON_BASIC = {"test": "test"}

RESPONSE_JSON_DEVOPS_PROJECT = {
    "id": "testid",
    "name": "testname",
    "description": "testdescription",
    "url": "testurl",
    "state": "teststate",
    "revision": 1,
    "visibility": "testvisibility",
    "last_updated": None,
    "default_team": None,
    "links": None,
}


DEVOPS_BUILD_DEFINITION = {
    "id": 1,
    "name": "testname",
    "url": "testurl",
    "path": "testpath",
    "type": "testtype",
    "queueStatus": "testqueuestatus",
    "revision": 1,
}

DEVOPS_BUILD = {
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
    "definition": DEVOPS_BUILD_DEFINITION,
    "project": RESPONSE_JSON_DEVOPS_PROJECT,
    "_links": {
        "self": {"href": "testself"},
        "web": {"href": "testweb"},
        "sourceVersionDisplayUri": {"href": "testsourceversiondisplayuri"},
        "timeline": {"href": "testtimeline"},
        "badge": {"href": "testbadge"},
    },
}


RESPONSE_JSON_DEVOPS_BUILDS = {"value": [DEVOPS_BUILD]}

RESPONSE_JSON_DEVOPS_BUILD = DEVOPS_BUILD

RESPONSE_JSON_DEVOPS_WIQL_RESULT = {
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
