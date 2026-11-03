# Grafana

## Quick Description (QD)

Grafana is a dashboarding and visualization platform. This page covers moving dashboard snapshots between Grafana instances.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Snapshots

Assume that your Grafana address is `http://localhost:3000`. First, take a snapshot of your dashboard. Then go to the snapshot list and get your snapshot key.

To upload a snapshot, you need a service account token with a role that is allowed to create snapshots (e.g., Editor or Admin). Keep tokens out of your notes and shell history.

## Examples (e.g.,)

### Downloading a Snapshot

If your snapshot key is `<snapshot-key>`, then:

```sh
curl -X GET http://localhost:3000/api/snapshots/<snapshot-key> \
  -o snap.json
```

The response is a JSON object with the `dashboard` model and a `meta` part.

### Uploading a Snapshot

If your service account token is `<service-account-token>`, then (use the address of the target Grafana):

```sh
curl -X POST http://localhost:3000/api/snapshots \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <service-account-token>" \
  -d @snap.json
```

The API requires the `dashboard` field in the request body, which `snap.json` already has. The response contains the key and the URL of the new snapshot.

## References

- [Grafana snapshot HTTP API](https://grafana.com/docs/grafana/latest/developers/http_api/snapshot/)
- [Grafana service accounts](https://grafana.com/docs/grafana/latest/administration/service-accounts/)
