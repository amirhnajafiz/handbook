# Grafana

## Snapshots

Assuming that your Grafana address is `http://localhost:3000`. First take a snapshot of your dashboard. Then go to the snapshot lists and get your snapshot key.

E.g., if your snapshot key is `kOW0me2oLBg0288rdJtaCtU52Zm7qyIQ`, then:

```sh
curl -X GET http://localhost:3000/api/snapshots/kOW0me2oLBg0288rdJtaCtU52Zm7qyIQ \
  -o snap.json
```

Now to upload a snapshot, you must make sure to have a service acount token with admin or editor level.

E.g., if your service token is `glsa_Zjr48XbIojlBJdhSbMD886pSrePaxcrU_9cdc8de2`, then:

```
curl -X POST http://localhost:3000/api/snapshots \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer glsa_Zjr48XbIojlBJdhSbMD886pSrePaxcrU_9cdc8de2" \
  -d @snap.json
```
