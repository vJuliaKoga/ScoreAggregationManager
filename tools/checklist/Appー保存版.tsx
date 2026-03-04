{
  "exportVersion": "1.0",
  "templateId": "QG-PLAN-001",
  "templateVersion": "0.1.0",
  "phaseId": "planning",
  "exportedAtLocal": "2026-03-04T13:32:12.672Z",
  "actor": {
    "displayName": "Sam",
    "actorId": null
  },
  "nodes": {
    "P-001": {
      "status": "Pending",
      "pendingReason": "無理、わかんない☺",
      "actorName": "Sam",
      "riskLevel": "A",
      "updatedAtLocal": "2026-03-04T13:31:13.968Z",
      "checkedItems": {
        "P-001-C1": true,
        "P-001-C2": false
      }
    },
    "P-002": {
      "status": "Done",
      "pendingReason": null,
      "actorName": "Sam",
      "riskLevel": "S",
      "updatedAtLocal": "2026-03-04T13:31:18.306Z",
      "checkedItems": {
        "P-002-C1": true
      }
    },
    "P-003": {
      "status": "Done",
      "pendingReason": null,
      "actorName": "Sam",
      "riskLevel": "A",
      "updatedAtLocal": "2026-03-04T13:31:21.619Z",
      "checkedItems": {
        "P-003-C1": false
      }
    },
    "P-004": {
      "status": "Done",
      "pendingReason": null,
      "actorName": "Sam",
      "riskLevel": "B",
      "updatedAtLocal": "2026-03-04T13:31:25.291Z",
      "checkedItems": {}
    },
    "CUSTOM-1772631095730": {
      "status": "Done",
      "pendingReason": null,
      "actorName": "Sam",
      "riskLevel": "C",
      "updatedAtLocal": "2026-03-04T13:31:58.997Z",
      "checkedItems": {
        "CUSTOM-1772631095730-C1": true,
        "CUSTOM-1772631095730-C2": true,
        "CUSTOM-1772631095730-C3": false,
        "CUSTOM-1772631095730-C4": false,
        "CUSTOM-1772631095730-C5": false
      }
    },
    "CUSTOM-1772631126571": {
      "status": "Done",
      "pendingReason": null,
      "actorName": "Sam",
      "riskLevel": "C",
      "updatedAtLocal": "2026-03-04T13:32:11.462Z",
      "checkedItems": {
        "CUSTOM-1772631126571-C1": false,
        "CUSTOM-1772631126571-C2": false,
        "CUSTOM-1772631126571-C3": false,
        "CUSTOM-1772631126571-C4": false,
        "CUSTOM-1772631126571-C5": false
      }
    }
  },
  "customNodeDefinitions": [
    {
      "nodeId": "CUSTOM-1772631095730",
      "title": "頼む",
      "description": "",
      "detailedChecks": [
        {
          "checkId": "CUSTOM-1772631095730-C1",
          "text": "行けたやんけ！",
          "checked": false
        },
        {
          "checkId": "CUSTOM-1772631095730-C2",
          "text": "最高！",
          "checked": false
        },
        {
          "checkId": "CUSTOM-1772631095730-C3",
          "text": "大変だった...",
          "checked": false
        },
        {
          "checkId": "CUSTOM-1772631095730-C4",
          "text": "",
          "checked": false
        },
        {
          "checkId": "CUSTOM-1772631095730-C5",
          "text": "",
          "checked": false
        }
      ],
      "unlocks": [
        "CUSTOM-1772631126571"
      ],
      "ui": {
        "initialVisible": false
      },
      "isCustom": true
    },
    {
      "nodeId": "CUSTOM-1772631126571",
      "title": "これもいけるか",
      "description": "",
      "detailedChecks": [
        {
          "checkId": "CUSTOM-1772631126571-C1",
          "text": "",
          "checked": false
        },
        {
          "checkId": "CUSTOM-1772631126571-C2",
          "text": "",
          "checked": false
        },
        {
          "checkId": "CUSTOM-1772631126571-C3",
          "text": "",
          "checked": false
        },
        {
          "checkId": "CUSTOM-1772631126571-C4",
          "text": "",
          "checked": false
        },
        {
          "checkId": "CUSTOM-1772631126571-C5",
          "text": "",
          "checked": false
        }
      ],
      "unlocks": [],
      "ui": {
        "initialVisible": false
      },
      "isCustom": true
    }
  ],
  "logEvents": [
    {
      "eventId": "evt-1772631073968-538",
      "nodeId": "P-001",
      "fromStatus": "ToDo",
      "toStatus": "Pending",
      "actorName": "Sam",
      "reason": "無理、わかんない☺",
      "occurredAtLocal": "2026-03-04T13:31:13.968Z"
    },
    {
      "eventId": "evt-1772631078306-199",
      "nodeId": "P-002",
      "fromStatus": "ToDo",
      "toStatus": "Done",
      "actorName": "Sam",
      "reason": null,
      "occurredAtLocal": "2026-03-04T13:31:18.306Z"
    },
    {
      "eventId": "evt-1772631081619-261",
      "nodeId": "P-003",
      "fromStatus": "ToDo",
      "toStatus": "Done",
      "actorName": "Sam",
      "reason": null,
      "occurredAtLocal": "2026-03-04T13:31:21.619Z"
    },
    {
      "eventId": "evt-1772631085291-618",
      "nodeId": "P-004",
      "fromStatus": "ToDo",
      "toStatus": "Done",
      "actorName": "Sam",
      "reason": null,
      "occurredAtLocal": "2026-03-04T13:31:25.291Z"
    },
    {
      "eventId": "evt-1772631118997-303",
      "nodeId": "CUSTOM-1772631095730",
      "fromStatus": "ToDo",
      "toStatus": "Done",
      "actorName": "Sam",
      "reason": null,
      "occurredAtLocal": "2026-03-04T13:31:58.997Z"
    },
    {
      "eventId": "evt-1772631131462-593",
      "nodeId": "CUSTOM-1772631126571",
      "fromStatus": "ToDo",
      "toStatus": "Done",
      "actorName": "Sam",
      "reason": null,
      "occurredAtLocal": "2026-03-04T13:32:11.462Z"
    }
  ]
}