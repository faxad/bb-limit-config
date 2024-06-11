Utility to generate and configure user limits in bulk for prototyping

```console
Usage:  ./run [COMMAND]

Optional Command:
  build         Build docker image and execute config. utility
```

- Define the following (in limit.xlsx):
  -  limits
  -  business functions (FUN),
  -  job roles / function groups (FAG),
  -  service agreement (SA)
- Executing the limit config. utility:
  - generates combination of user limits for business functions and job roles
  - generates request payload for limit confirmation (for a user as separate json file)
  - posts the payloads to OOTB limit configuration API
  - persists the response payload for success / failure scenarios

### Structure

```
|-- ...
|-- limits.xlsx
|-- payload
|   |-- request
|   |   |-- 392135c3-728d-4651-9dbc-b6dccd354818.json
|   |   `-- 62b6660e-dd2e-4a08-b1e4-764c8c29b385.json
|   `-- response
|       |-- failure
|       |   `-- 392135c3-728d-4651-9dbc-b6dccd354818.json
|       `-- success
|           `-- 62b6660e-dd2e-4a08-b1e4-764c8c29b385.json
`-- run.sh
```

### Output

```javascript
[
  {
    "user-BBID": "4246cb35-f6b5-4a80-bc11-fd5cbfbbca01",
    "entities": [
      {
        "etype": "FUN",
        "eref": "1000"
      },
      {
        "etype": "FAG",
        "eref": "a338bcb2-1e34-4e83-bff9-7b365bfee426"
      },
      {
        "etype": "SA",
        "eref": "fa961529-aaa3-484c-bbc5-3cd10e1c8685"
      },
      {
        "etype": "PRV",
        "eref": "approve"
      }
    ],
    "shadow": false,
    "currency": "SAR",
    "periodic-limits-bounds": {
      "daily": "100000",
      "customPeriods": []
    }
  },
   ...
]
```

### Configuration

#### Limits

| FAG       | INTL      | LOCAL       | A2A     |
|-----------|-----------|-------------|---------|
| CLASSIC   | 50,000    | 100,000     | 30,000  |
| PREMIER   | 250,000   | 5,000,000   | 70,000  |

> Base implementation supports setting DAILY limits. However, it should be fairly straight forward to extend the implementation to support WEEKLY, MONTHLY etc. limoits.

#### Business Functions

| Name  | Code |
|-------|------|
| INTL  | 1000 |
| A2A   | 2000 |

#### Functions Groups

| Name      | FAG_ID                               |
|-----------|--------------------------------------|
| CLASSIC   | a338bcb2-1e34-4e83-bff9-7b365bfee426 |
| PREMIER   | 7bb08938-388f-47cf-a75d-f4ba97eee45f |


#### Service Agreement to User Mapping

| SA_ID                                | USER_ID                              |
|--------------------------------------|--------------------------------------|
| fa961529-aaa3-484c-bbc5-3cd10e1c8685 | 4246cb35-f6b5-4a80-bc11-fd5cbfbbca01 |
| f8690a12-ed2a-4d2a-b27a-a73efae611af | 82c4df16-cb65-4310-a520-00128042c938 |


> Limits configuration using the identifiers `*_ID` is required for the limits to appear on the Employee App
