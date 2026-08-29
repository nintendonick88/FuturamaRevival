# Experiment Log

This file records runtime experiments in chronological order. It distinguishes observations from interpretations and preserves exact artifacts outside the repository where they may contain copyrighted client material or device identifiers.

## 2026-08-27 — Android 1.6.6 client under local control

### Source preservation

- Original APK: `C:\Users\nick\Documents\apk\Futurama_+Worlds+of+Tomorrow_1.6.6_APKPure.apk`
- Original APK SHA-256: `5FF63E3F46622114C5A14D86038E1D5085A676B8A3F919E02ADD6BC1F5991D0F`
- Original `libclient.so` SHA-256: `9DDA40327156C38277808898C608943BE398668B10D7034F8B6B0278B267A279`
- The source artifact was not overwritten.

### Lab environment

- Android 11 / API 30 Google APIs x86_64 emulator with ARM translation
- AVD: `D:\Android\avd\Futurama_API30.avd`
- Host-visible emulator gateway: `10.0.2.2`
- Probe port: TCP 8302
- The legacy external directory `/storage/emulated/0/Android/data/com.tinyco.futurama` had to be created before the client progressed to its loading screen.

### Derived preservation build

Apktool 3.0.3 decoded and rebuilt a separate client. The decoded tree and output APK are lab artifacts outside Git.

Changes:

1. In `lib/armeabi-v7a/libclient.so`, replace the one native C string `https://futurama.prod.tinyco.com/tapservice/` with `http://10.0.2.2:8302/tapservice/`, then NUL-pad the remaining bytes so the library length and all later offsets remain unchanged.
2. In `com/tinyco/griffin/licensing/LicenseCheckerPolicy.smali`, make `allowAccess()` return true. This bypasses only the obsolete Play Store license decision that otherwise rejects any preservation re-signing.

The build was zip-aligned and signed with a local test key.

- Output: `D:\Android\patched\Futurama-1.6.6-local-signed.apk`
- Output SHA-256: `1A89DEC7084A3354082A17CA71A551636B5C57765268DA912E1B23DC646A4D57`
- Signature verification: Android APK Signature Scheme v1, v2, and v3 verified
- Runtime licensing log: `BPC: User license validated.`

### Experiment A — controlled transport failure

Response: HTTP 503 from `experiments/client_probe/probe_server.py`.

Observed:

- The client made `POST /tapservice/api/` to the host probe.
- The client displayed its own **Connect Error** screen after the controlled response.
- Request evidence: `D:\Android\evidence\client-requests-local-build-20260827.jsonl`
- Screenshot: `D:\Android\evidence\futurama-local.png`

Conclusion: **CONFIRMED** — original Futurama game code is executing network behavior and changing visible UI state in response to software controlled by this project.

### Experiment B — WOTServer sample JSON

Response: HTTP 200, `application/json`, body copied from WOTServer's `saltResponse.json`.

Observed:

- The HTTP response completed.
- The client immediately reported `ENGINE_CONNECT_ERROR` and displayed **Connect Error**.
- Evidence: `D:\Android\evidence\client-requests-wot-response-20260827.jsonl`
- Screenshot: `D:\Android\evidence\futurama-wot-response.png`

Conclusion: **CONFIRMED** — WOTServer's sample JSON is not accepted as a valid bootstrap response by this client under these transport conditions.

### Experiment C — WOTServer sample with its transport clues

Response: HTTP 200, gzip-compressed JSON, plus `X-TC-Digest: 4f2564d324730e58cdedcb55a06a240d`.

Observed:

- The HTTP response completed.
- The client again reported `ENGINE_CONNECT_ERROR` and displayed **Connect Error**.
- Evidence: `D:\Android\evidence\client-requests-wot-full-response-20260827.jsonl`
- Screenshot: `D:\Android\evidence\futurama-wot-full.png`
- MD5 of the uncompressed sample response is `2C1492E5FDDA9B088734FDFA1B74E686`, not WOTServer's hardcoded header value.

Conclusion: **CONFIRMED** — gzip and the hardcoded response header are not sufficient to make the sample valid. Whether the header is necessary for a genuinely valid response remains unknown.

### First captured request contract

- Method: `POST`
- URL: `http://10.0.2.2:8302/tapservice/api/`
- Content type: `application/x-www-form-urlencoded; charset=utf-8`
- User agent: `futurama/1.6.6 android/30`
- `RPC` header: `getSalt,getOrCreatePlayerId`
- Accepted response encoding: gzip
- Form fields: `request` and `chksum`
- `chksum`: 32 lowercase hexadecimal characters; it changed between requests
- Request JSON `appid`: `com.tinycorp.futurama.android`
- Request JSON `software_version`: `1.6.6`
- Batched calls: `["getSalt"]` and `["getOrCreatePlayerId", {"type":"device","id":"<device id>"}]`
- Initial `player_id` and `human_id`: empty

The device identifier is intentionally omitted from this repository document. The raw evidence file preserves the exact request.

### Experiments D-F — response-envelope probes

Three additional HTTP 200, gzip-compressed responses were tested while keeping the client build and destination constant:

| Response hypothesis | Evidence file | Observed result |
|---|---|---|
| Direct two-element JSON array | `D:\Android\evidence\client-requests-bootstrap-direct-array-20260827.jsonl` | `ENGINE_CONNECT_ERROR`; no later game request |
| Object containing `response: [...]` with locally generated string values | `D:\Android\evidence\client-requests-bootstrap-object-20260827.jsonl` | `ENGINE_CONNECT_ERROR`; no later game request |
| Direct array with WOTServer-shaped IDs and timestamped `signed_salt` | `D:\Android\evidence\client-requests-bootstrap-shaped-20260827.jsonl` | `ENGINE_CONNECT_ERROR`; no later game request |

Conclusion: **CONFIRMED** — neither a bare result array nor WOTServer's array-valued `response` is sufficient. Changing identifier appearance and the superficial `signed_salt` shape did not satisfy the gate.

### Experiment G — WOT-shaped values with string `human_id`

Response: object containing the same two-element `response` array, with production-shaped placeholder IDs and a string rather than JSON `null` for `human_id`.

- Evidence: `D:\Android\evidence\client-requests-bootstrap-shaped-strings-20260827.jsonl`
- Observed: HTTP 200 followed by `ENGINE_CONNECT_ERROR`; no later game request.

Conclusion: **CONFIRMED** — WOTServer's `human_id: null` is not the only reason its fixture fails.

### Experiment H — one combined response object

Response: one object under `response` containing salt and player fields together.

- Evidence: `D:\Android\evidence\client-requests-bootstrap-combined-object-20260827.jsonl`
- Screenshot: `D:\Android\evidence\futurama-bootstrap-combined.png`
- Observed: HTTP 200 followed by `ENGINE_CONNECT_ERROR`; no later game request.

Conclusion: **CONFIRMED** — the client does not accept all bootstrap fields merged into one result object.

### Native response-container trace

Static ARM analysis was performed against the exact original `libclient.so`; the disassembly artifacts are preserved at:

- `D:\Android\evidence\native-target-functions.txt`
- `D:\Android\evidence\native-target-string-xrefs.txt`
- `D:\Android\evidence\native-response-flow.txt`
- `D:\Android\evidence\native-json-functions.txt`

Evidence-backed findings:

- The JSON member helper at `0x6933f8`, used to read top-level `response`, returns a value only when its internal JSON type is `4`.
- String members (`salt`, `signed_salt`, `player_id`, `human_id`, and `community_id`) are read by the helper at `0x692c88`, which requires internal JSON type `1`.
- Boolean `success` is read by `0x68be90`, which requires internal JSON type `3`; JSON `true` is therefore the correct value class.
- The bootstrap callback obtains two child results: one through the first-child helper at `0x13e075c` and one through indexed child access at `0x690ef0` with index `1`.
- The salt callback copies `salt` and `signed_salt` into the client singleton. No cryptographic validation of `signed_salt` is visible in this callback.
- `server_md5` is referenced by a separate configuration/file-loading path, not this initial salt callback.
- The literal `X-TC-Digest` does not occur in the APK's DEX, native library, or decoded resources.

Interpretation after follow-up: the internal type map is consistent with string `1`, boolean `3`, array `4`, and object `5`. The dedicated `response` accessor therefore appears to require an array, and its two child helpers require object-valued elements. This supports the broad `{"response":[{...},{...}]}` shape, but does not validate WOTServer's field values.

### Experiment I — object-valued `response`

Response: `response` was changed from an array to an object keyed by the two captured RPC names.

- Evidence: `D:\Android\evidence\client-requests-bootstrap-named-object-20260827.jsonl`
- Screenshot after returning from the client's privacy-policy browser launch: `D:\Android\evidence\futurama-bootstrap-named-object-after-back.png`
- Observed: HTTP 200 followed by `ENGINE_CONNECT_ERROR`; no later game request.

Conclusion: **CONFIRMED** — the named-object alternative is rejected. Combined with the native type checks, the array-valued `response` is now the leading and code-supported container model. This test falsifies the earlier object-container inference.

### Immediate next experiment

Keep the array-valued two-object envelope and vary only trace-supported field values. If that remains ambiguous, make a diagnostic-only disposable native build that distinguishes the bootstrap parser's failure branches without forcing success.
