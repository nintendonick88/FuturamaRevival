# Evidence-Backed Technical Discoveries

## Scope and method

The initial pass read the three research documents, inspected every tracked WOTServer file and its six-commit local history, listed and fingerprinted the APK, decoded its binary manifest and preference XML, extracted printable strings from its native library/DEX/resources, disassembled the primary DEX to temporary storage, and inspected the embedded DER certificate.

On 2026-08-27, after explicit maintainer authorization, runtime experiments were performed with a separately rebuilt and locally signed preservation APK. The original APK and WOTServer checkout remain unchanged. Runtime evidence below is labelled separately from static evidence; exact commands, hashes, and artifact paths are in `docs/EXPERIMENT_LOG.md`.

## Runtime-confirmed bootstrap contract (2026-08-27)

The derived Android 1.6.6 client made this request to the project probe:

| Property | Observed value |
|---|---|
| Method and path | `POST /tapservice/api/` |
| Content type | `application/x-www-form-urlencoded; charset=utf-8` |
| User agent | `futurama/1.6.6 android/30` |
| Action header | `RPC: getSalt,getOrCreatePlayerId` |
| Content coding accepted | `gzip` |
| Form fields | `request`, `chksum` |
| `chksum` appearance | 32 lowercase hexadecimal characters; changes between requests |
| JSON application ID | `com.tinycorp.futurama.android` |
| JSON software version | `1.6.6` |
| First action | `["getSalt"]` |
| Second action | `["getOrCreatePlayerId", {"type":"device","id":"<device id>"}]` |
| Initial identities | empty `player_id` and `human_id` |

This resolves the path, slash form, method, outer encoding, initial action names, and basic batch order for this installation. The exact `chksum` algorithm and full JSON metadata semantics remain unknown.

### Client redirection and licensing

Runtime testing contradicted the earlier expectation that selecting `Localhost` in the Java preference screen would redirect this production build: native code continued to select the compiled production URL. The successful preservation build therefore used a one-occurrence, fixed-length native C-string replacement to `http://10.0.2.2:8302/tapservice/`.

Re-signing caused the legacy Google Play licensing policy to reject the client before bootstrap. A second derived-build change made `LicenseCheckerPolicy.allowAccess()` return true. The client then logged `BPC: User license validated.` and reached the probe. This is a preservation compatibility patch, not replacement-server behavior.

### Controlled response results

| Response controlled by this project | Client result | Finding |
|---|---|---|
| HTTP 503 JSON probe response | Visible **Connect Error** | **CONFIRMED:** client UI is responding to project-controlled software |
| HTTP 200 with WOTServer `saltResponse.json` | `ENGINE_CONNECT_ERROR`; visible **Connect Error** | **CONFIRMED:** sample body is not accepted |
| Same body, gzip, with WOTServer `X-TC-Digest` | Same rejection | **CONFIRMED:** those transport clues are insufficient |
| Bare two-result array | Same rejection | **CONFIRMED:** top-level array is not sufficient |
| `response` array with shaped IDs and string `human_id` | Same rejection | **CONFIRMED:** WOTServer's null `human_id` is not the sole fault |
| One combined object under `response` | Same rejection | **CONFIRMED:** salt and player results cannot simply be merged |
| `response` object keyed by RPC names | Same rejection | **CONFIRMED:** named-object alternative is not accepted |

The WOTServer sample body's MD5 is `2C1492E5FDDA9B088734FDFA1B74E686`, while its hardcoded `X-TC-Digest` is `4f2564d324730e58cdedcb55a06a240d`. The header is therefore not simply the MD5 of that uncompressed placeholder file. More importantly, the literal `X-TC-Digest` does not occur in this APK's DEX, native library, or decoded resources. The header's origin and relevance are **UNKNOWN** and it must not be treated as a client requirement.

### Native response-parsing clues

The same area of `libclient.so` contains the strings `getOrCreatePlayerIdAndSalt`, `empty response recieved from server`, `getOrCreatePlayerIdEmptyResponse`, `salt`, `signed_salt`, `server_md5`, `Missing data from server`, `unknown response type`, and `ENGINE_CONNECT_ERROR`. Java's `GriffinHttpClient.ServerApi` transports the response but does not parse it.

The traced bootstrap callback at approximately `0x00e46d9c` reads top-level `response`, obtains two child values, requires boolean `success`, then reads string `salt` and `signed_salt`. It stores those two strings in the client singleton at offsets `+0x256c` and `+0x2570`. No signature verification is visible in this callback. A later request-building path reads the stored values, so `signed_salt` may simply be forwarded to the server on subsequent calls.

The player-result parser at approximately `0x00e2853c` reads string `player_id`, string `human_id`, `env`, and string `community_id`. It contains an explicit diagnostic for a null/empty `player_id`.

The JSON helper at `0x006933f8` returns top-level `response` only for internal type `4`, while the string and boolean helpers require types `1` and `3`. The bootstrap callback selects a first child and an indexed child at position `1`; both child helpers require internal type `5`. The type map is consistent with string `1`, boolean `3`, array `4`, and object `5`. A runtime test of an object keyed by RPC names was rejected. **PROBABLE interpretation:** the broad WOTServer container shape—an array-valued `response` holding two objects—is correct, although its synthetic values are not proven valid.

`server_md5` is referenced in a separate configuration/file-loading path around `0x00e52d74`; it is not evidence of initial salt-signature validation.

Binary offsets below refer to files extracted from the APK identified by the SHA-256 in `PROJECT_CONTEXT.md`.

## What the WOTServer author appears to have discovered

In plain English, the author appears to have learned how to make the client call a computer under the researcher's control, then built the smallest possible HTTP listener to see and answer those calls.

The README says the author used an Android device/emulators, PCAP Droid, HTTP Toolkit, Wireshark, ADB/signing tools, an unmodified WoT APK, and an unmodified *Family Guy: The Quest for Stuff* client. It says connection values are in `lib\armeabi-v7a\libclient.so`; other connection data appears after Apktool decoding at `res\values\strings.xml`; and the proposed workflow was to replace the host with a local address, convert HTTPS strings to HTTP, rebuild, sign, install, then monitor requests.

The implementation shows that the author had identified or suspected:

- a central `POST /tapservice/api/` request;
- a salt/player bootstrap response represented as a JSON `response` array;
- a server-message path named `/process_queue.php`;
- a possible `/get_server.php` path;
- gzip-compressed JSON and an `X-TC-Digest` response header;
- nginx-like production response headers.

What the author implemented is only a debug scaffold:

- Python's `SimpleHTTPRequestHandler`, speaking HTTP/1.1;
- a raw UTF-8 request logger for POST bodies and query strings;
- a hardcoded response router for three paths;
- a gzipped JSON response for the exact trailing-slash path `/tapservice/api/`;
- placeholder text for the other two paths;
- one listener on TCP port 80, bound to all interfaces.

The repository itself explicitly disclaims functionality. There is no account database, authentication validation, player/town state, persistence, configuration service, content service, quest/economy logic, or TLS server.

## WOTServer endpoint inventory

| Path | Request implemented | Request data known | Response implemented | Confidence/status |
|---|---|---|---|---|
| `/tapservice/api/` | `POST` only; query parsed; body read as UTF-8 and logged | No fields are parsed or validated | `200 OK`; gzip body; `application/json; charset=utf-8`; body loaded from `saltResponse.json` | **PARTIAL** implementation; original schema is **UNCERTAIN** |
| `/tapservice/api` | `POST` only | Same raw handling | Because the special-case test requires the trailing slash, this receives `202 Accepted` and the same JSON uncompressed through the generic branch | **CONFIRMED implementation discrepancy** |
| `/process_queue.php` | `POST` only | APK also contains the format `process_queue.php?application_cd=%s&user_dttm=%lld&user_cd=%s`; body format remains uncertain | `202 Accepted`; plain-text placeholder saying processing is incomplete | Path **IDENTIFIED**; behavior **PLACEHOLDER** |
| `/get_server.php` | `POST` only | Unknown | `202 Accepted`; plain text `Server info response`; source comment says `Remove this` | Repository-only **HYPOTHESIS**; not found in the APK string scan |
| any other POST path | `POST` | Raw query/body logging | `202 Accepted`; JSON `{"error": "Unknown endpoint"}` | Debug fallback |
| arbitrary GET/HEAD path | Inherited from `SimpleHTTPRequestHandler` | Normal static-file semantics | Can expose files below the WOTServer working directory | Incidental behavior, not a discovered game endpoint |

### Exact `/tapservice/api/` response envelope in WOTServer

`saltResponse.json` contains two objects under `response`:

1. `signed_salt`, `salt`, and `success`;
2. `player_id`, `human_id`, `env`, `community_id`, and `success`.

The values look deliberately synthetic (`abc123...`, `1234567`, patterned IDs). They are evidence of the author's proposed field names and ordering, not evidence of real production values or a valid signature algorithm.

The response headers set by the server are:

- `Cache-Control: no-cache, no-store, must-revalidate, proxy-revalidate, max-age=0`
- `Connection: keep-alive`
- `Content-Encoding: gzip`
- `Content-Length`
- `Content-Type: application/json; charset=utf-8`
- `Cross-Origin-Opener-Policy: same-origin`
- `Date`
- `Referrer-Policy: same-origin`
- `Server: nginx/1.24.0 (Ubuntu)`
- `Strict-Transport-Security: max-age=3600`
- `Vary: Origin, Accept-Encoding`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-TC-Digest: 4f2564d324730e58cdedcb55a06a240d`

The code says some spoofed headers may be unnecessary. Their presence does not prove the client validates them. HSTS has no protective effect when delivered over the server's plain HTTP connection.

### Listener behavior

- `PORT_HTTP = 80` is active.
- `PORT_HTTP_ALT = 443` is declared as **plain HTTP**, but its thread is commented out.
- No TLS context or certificate is configured.
- `TCPServer(("", port), ...)` binds all local interfaces.
- A non-UTF-8 body can cause the debug logger's unconditional UTF-8 decode to fail.

## APK identity and architecture

### Confirmed package facts

| Item | Value |
|---|---|
| Package | `com.tinyco.futurama` |
| Version | `1.6.6` |
| Version code | `1665` |
| Minimum / target SDK | 14 / 26 |
| Native ABI/library | ARMv7, `lib/armeabi-v7a/libclient.so` |
| Manifest network permissions | `INTERNET`, `ACCESS_NETWORK_STATE`, `ACCESS_WIFI_STATE` |
| Graphics | OpenGL ES 2.0 required; ASTC texture declarations |
| Archive entries | 4,326 |

### Engine correction

The inspected APK is a native C++ client using Marmalade/S3E-era infrastructure and Cocos2d-style code, with TinyCo's shared `griffin` layer.

Direct clues include:

- `assets/app.icf`: `[S3E]`, `MemSize=[s3e]SCREENSIZE + 50331648`, `IW_GL=1`;
- native symbols referring to `cocos2d`;
- source-path strings under `jni/../../lib/griffin/...` and `jni/futurama/...`;
- only `libclient.so`, with no `libil2cpp.so`;
- no Unity `assets/bin/Data` tree.

`com.unity3d.ads.android.view.UnityAdsFullscreenActivity` is present in the manifest, but that is an ad SDK component. It does not make the client a Unity game.

Therefore the Unity/IL2CPP assertions in `Futurama Game Preservation Research.md` lines 191–193 and the “Unity (likely)” language in the strategy document are **CONTRADICTED for this APK**.

### Confirmed TinyCo/Family Guy code lineage

This is stronger than a generic similarity:

- Android classes use the package `com.tinyco.griffin`.
- Native compiler paths refer to `lib/griffin`.
- The base assets include many `fg_*.json` UI files.
- `GameLocalData.json` retains multiple localized *Family Guy* messages.
- Native paths/models include shared protobuf sources.

This supports using *Family Guy: The Quest for Stuff* as comparative protocol evidence, while not assuming its payloads are interchangeable.

## Built-in server configuration: an important new clue

`res/xml/preferences.xml` defines:

- a `ListPreference` with key `serviceURL`;
- an `EditTextPreference` with key `otherServiceURL`;
- `useInternalStaticURL`, `nukeFileCache`, log/performance controls, a cheat-button control, HUD control, tutorial control, sleep control, and debug-log level.

The corresponding resource strings enumerate:

- `Beta`
- `Dev`
- `Localhost`
- `Prod`
- `Review`
- `Staging`
- `Other Service URL`

`classes.dex` contains `FUPreferenceActivity`, which loads `res/xml/preferences.xml`. `FUBaseGameActivity` contains two paths that start this activity. The manifest declares `FUPreferenceActivity` with an `android.intent.action.MAIN` intent filter and does not set `android:exported="false"`. Given target SDK 26 behavior, it is **PROBABLE** that ADB can launch this internal screen without modifying the APK. Runtime confirmation is still required.

This finding may make the README's mandatory binary patch unnecessary for a first connection experiment.

## Core game/service URLs and paths

### Service bases embedded in both resources and native code

| Environment | Literal base URL | Evidence |
|---|---|---|
| Production | `https://futurama.prod.tinyco.com/tapservice/` | `resources.arsc` offset 162872; `libclient.so` offset 23237632 |
| Beta | `http://beta.futurama.tinyco.com/tapservice/` | `resources.arsc` offset 162745 |
| Development | `http://dev.futurama.tinyco.com/tapservice/` | `resources.arsc` offset 162791 |
| Local | `http://127.0.0.1:8302/tapservice/` | `resources.arsc` offset 162836 |
| Staging | `http://stage.futurama.tinyco.com/tapservice/` | `resources.arsc` offset 163070 |
| Review | `http://review.futurama.tinyco.com/tapservice/` | `resources.arsc` offset 163157 |

The native literal `tapservice/api` occurs at `libclient.so` offset 23375216. WOTServer's exact `/tapservice/api/` handler strongly suggests the effective production request was the production base plus `api`, but only a runtime trace can settle slash construction and the complete URL.

### First-party content/support URLs

- `https://config-fut-tc.akamaized.net/`
- `https://static-fut-tc.akamaized.net/`
- `https://static-fut-tc.akamaized.net/intro_movie_low.mp4`
- `http://static.futurama.tinyco.com/help/crashfaq.html`
- `http://www.tinyco.com/privacypolicy.html`
- `https://tc-futurama-android.firebaseio.com`
- resource host string `tc-futurama-android.appspot.com`

The two Akamai roots are confirmed; the exact configuration/asset manifest object paths are not yet known.

### TinyCo/SGN shared-service URL literals

- `https://gs.mindjolt.com`
- `https://tc-bic.appspot.com/t/api/1/`
- `http://invenio.sgn.com/`
- `http://edms.sgn.com/events/local/send`
- `http://mtx.sgnapps.com/invenio_tracking/record_transaction.php`
- `https://mtx.sgn.com/android_microtransactions/record_transaction.php`
- `http://push.android.sgnapps.com/trackpush.php`
- `http://push.android.sgnapps.com/trackopenpush.php`
- `http://sendpush.sgn.com/trackpush.php`
- `http://sendpush.sgn.com/trackpushedms.php`

These names suggest analytics, transaction, and push-notification roles. A literal URL establishes presence, not that version 1.6.6 actually calls it during bootstrap.

### Message-queue clue

The native client contains this exact format string:

`%sprocess_queue.php?application_cd=%s&user_dttm=%lld&user_cd=%s`

Nearby/protocol strings include:

- `%s=%s&json_val=%s`
- `application/x-www-form-urlencoded`
- `payload_json`
- `application/json`

This is evidence for a form-encoded JSON/message operation with query identifiers, but it does not establish the full request body, host, HTTP method, signature, or response schema. WOTServer's POST handler is supporting repository evidence for POST, not a packet capture preserved in the repository.

## Hostname and IP inventory

The following is the complete set of hostnames successfully parsed from static HTTP(S) URL literals in the APK. Many originate in bundled SDKs, documentation strings, test strings, OAuth scopes, or store links. Presence is not proof of a network call.

### Core/TinyCo/SGN/content hosts

`127.0.0.1`, `beta.futurama.tinyco.com`, `config-fut-tc.akamaized.net`, `dev.futurama.tinyco.com`, `edms.sgn.com`, `futurama.prod.tinyco.com`, `gs.mindjolt.com`, `invenio.sgn.com`, `mtx.sgn.com`, `mtx.sgnapps.com`, `push.android.sgnapps.com`, `review.futurama.tinyco.com`, `sendpush.sgn.com`, `stage.futurama.tinyco.com`, `static.futurama.tinyco.com`, `static-fut-tc.akamaized.net`, `tc-bic.appspot.com`, `tc-futurama-android.firebaseio.com`, `www.tinyco.com`.

### Third-party/service hosts

`accounts.google.com`, `ads.api.vungle.com`, `ad-x.co.uk`, `ags-ext.amazon.com`, `amazon-adsystem.amazon.com`, `api.nanigans.com`, `api.sponsorpay.com`, `api.vungle.com`, `app.adjust.com`, `applab-sdk.amazon.com`, `app-measurement.com`, `cortana-gateway.amazon.com`, `csi.gstatic.com`, `facebook.com`, `gdpr.adjust.com`, `googleads.g.doubleclick.net`, `graph.facebook.com`, `iframe.sponsorpay.com`, `imasdk.googleapis.com`, `ingest.vungle.com`, `init.supersonicads.com`, `login.live.com`, `login.yahoo.com`, `mobilecrashreporting.googleapis.com`, `mobilelogs.supersonic.com`, `outcome.supersonicads.com`, `pagead2.googlesyndication.com`, `play.google.com`, `plus.google.com`, `px.moatads.com`, `service.sponsorpay.com`, `ssl.google-analytics.com`, `staging.iframe.sponsorpay.com`, `staging.sws.sponsorpay.com`, `staging-iframe.sponsorpay.com`, `support.google.com`, `t.singular.net`, `track.atom-data.io`, `twitter.com`, `www.amazon.co.jp`, `www.amazon.com`, `www.facebook.com`, `www.google.com`, `www.google-analytics.com`, `www.googleapis.com`, `www.googletagmanager.com`, `www.linkedin.com`, `www.paypal.com`, `www.supersonicads.com`, `www.vungle.com`, `z.moatads.com`, `z-ecx.images-amazon.com`.

### Documentation/schema/example literals, not presently classified as runtime servers

`code.google.com`, `console.firebase.google.com`, `developer.android.com`, `developers.facebook.com`, `docs.sentry.io`, `firebase.google.com`, `gcc.gnu.org`, `github.com`, `goo.gl`, `google.com`, `hostname`, `localhost`, `lol.vungle.com`, `metadata`, `schema.org`, `schemas.android.com`, `www.example.com`, `www.firebase.com`, `www.slf4j.org`, `www.w3.org`.

Parameterized Facebook host strings (`graph.%s`, `graph-video.%s`, `www.%s.facebook.com`) and a malformed literal `https://.facebook.com` also occur.

### IP addresses

- `127.0.0.1` is the only confirmed literal server IP address.
- `2.0.76.4` and `2.1.26.0` match IPv4 syntax in the binary scan but occur as version-shaped strings; they are **not classified as server IPs** without context.
- No production TinyCo server IP is embedded as a confirmed literal. DNS would have supplied production addresses.

## Runtime-looking third-party endpoint literals

These are preserved because they may affect noisy startup traces. HTTP method and response type are unknown unless the URL itself makes a role obvious.

```text
http://ad-x.co.uk/API/androidevent.php?oursecret=
http://ad-x.co.uk/atrk/andrdapp?
http://amazon-adsystem.amazon.com/
http://api.nanigans.com/disallowed.php?
http://api.nanigans.com/mobile.php?
http://lol.vungle.com/
http://z-ecx.images-amazon.com/images/G/01/mobile/advertising/amazonMobileSDKv2._TTH_.json
https://accounts.google.com/o/oauth2/auth
https://accounts.google.com/o/oauth2/token
https://ads.api.vungle.com/config
https://ags-ext.amazon.com/service/gamedata/WhisperData
https://api.nanigans.com
https://api.sponsorpay.com/vcs/v1/
https://api.vungle.com/api/v4/unfilled
https://app.adjust.com
https://applab-sdk.amazon.com/1.0
https://app-measurement.com/a
https://cortana-gateway.amazon.com/cortana/gateway/getSignedDownloadUrl
https://gdpr.adjust.com
https://googleads.g.doubleclick.net/mads/static/mad/sdk/native/mraid/v2/mraid_app_banner.js
https://googleads.g.doubleclick.net/mads/static/mad/sdk/native/mraid/v2/mraid_app_expanded_banner.js
https://googleads.g.doubleclick.net/mads/static/mad/sdk/native/mraid/v2/mraid_app_interstitial.js
https://googleads.g.doubleclick.net/mads/static/mad/sdk/native/native_ads.html
https://googleads.g.doubleclick.net/mads/static/mad/sdk/native/production/native_ads.js
https://googleads.g.doubleclick.net/mads/static/mad/sdk/native/production/sdk-core-v40-impl.js
https://googleads.g.doubleclick.net/mads/static/mad/sdk/native/sdk-core-v40.html
https://graph.facebook.com/
https://graph.facebook.com/network_ads_common
https://iframe.sponsorpay.com/mobile
https://iframe.sponsorpay.com/unlock?
https://imasdk.googleapis.com/admob/sdkloader/native_video.html
https://ingest.vungle.com/
https://ingest.vungle.com/api/v1/sdkErrors
https://init.supersonicads.com/sdk/v
https://mobilecrashreporting.googleapis.com/v1/crashes:batchCreate?key=
https://mobilelogs.supersonic.com
https://outcome.supersonicads.com/mediation/
https://pagead2.googlesyndication.com/pagead/gen_204
https://pagead2.googlesyndication.com/pagead/gen_204?id=gmob-apps
https://px.moatads.com/pixel.gif?e=0&i=MOATSDK1&ac=1
https://service.sponsorpay.com/actions/v2
https://service.sponsorpay.com/installs/v2
https://ssl.google-analytics.com
https://staging.iframe.sponsorpay.com/vcs/v1/
https://staging.sws.sponsorpay.com/actions/v2
https://staging.sws.sponsorpay.com/installs/v2
https://staging-iframe.sponsorpay.com/mobile
https://staging-iframe.sponsorpay.com/unlock?
https://staging-iframe.sponsorpay.com/vcs/v1/
https://t.singular.net/v2/events
https://t.singular.net/v2/logs
https://track.atom-data.io
https://www.facebook.com/adnw_logging/
https://www.facebook.com/audience_network/server_side_reward
https://www.google-analytics.com
https://www.googletagmanager.com
https://www.supersonicads.com/mobile/sdk5/log?method=
https://z.moatads.com/
```

Store, privacy, help, documentation, schema, and OAuth-scope URL literals were classified separately rather than pretending they are game-backend endpoints.

## Request, response, and serialization clues

### Confirmed

- WOTServer handles `POST`; it does not implement a game-specific GET handler.
- Main server data is represented as JSON in WOTServer.
- The native client contains `application/json`, `application/x-www-form-urlencoded`, `json_val`, and `payload_json`.
- The native client uses `nlohmann::basic_json`; Android wrapper code also contains `org.json`.
- gzip, zlib, and deflate support exists in the client; WOTServer gzip-compresses `/tapservice/api/`.
- Client field strings include `salt`, `signed_salt`, `player_id`, `human_id`, and `community_id`.
- Shared Griffin header-name strings include `X-GS-ClientId`, `X-GS-DeviceId`, `X-GS-Last-ClientId`, `X-GS-Password`, and `X-GS-User`.
- Native symbols include `gs::ServerBootstrap`, `Bpc::ServerApi`, `Bpc::FUServerApi`, `ServerMessageQueueHandler`, `OOBServerEvents`, `RemoteStore`, `AsyncOpManager`, and server-time handling.

### Protobuf model clues

Compiler paths show generated protobuf sources for:

- `Achievements.pb.cc`
- `Common.pb.cc`
- `Entity.pb.cc`
- `FeaturedModal.pb.cc`
- `FloorPlan.pb.cc`
- `FU.pb.cc`
- `GameCenter.pb.cc`
- `GoalProgress.pb.cc`
- `History.pb.cc`
- `Player.pb.cc`
- `RandomGenerator.pb.cc`
- `TimedPromo.pb.cc`
- `Wallet.pb.cc`

The APK also contains `protobuf.meta`. This strongly supports protobuf-backed internal models or persistence. It does **not** prove the main HTTP body is protobuf; JSON and form evidence is also direct.

### TLS/certificate clue

`assets/cert-1.der` is a self-signed wildcard `CN=*.tinyco.com` certificate:

- SHA-256: `E9AFB8F5D0C8B12657D7377D1723F07189F10A8DEB87BCD8095C9C4961897D6F`
- RSA 1024-bit, `sha1RSA`
- validity: 2012-08-27 through 2013-08-27

Its role is unknown. Because it expired years before client 1.6.6, it may be an old bundled trust artifact or unused SDK data. It is not yet evidence of active certificate pinning.

## Relevant file-path inventory

### WOTServer files

- `README.md`
- `main.py`
- `saltResponse.json`

### APK paths directly relevant to archaeology

- `AndroidManifest.xml`
- `resources.arsc`
- `classes.dex`
- `classes2.dex`
- `classes3.dex`
- `lib/armeabi-v7a/libclient.so`
- `res/xml/preferences.xml`
- `assets/app.config.txt`
- `assets/app.icf`
- `assets/buildInfo.json` (`BuildRevision` `103d7d7+`)
- `assets/version.txt` (`1.5.0.17`, distinct from manifest version 1.6.6)
- `assets/EngineLocalData.json`
- `assets/GameLocalData.json`
- `assets/cert-1.der`
- `assets/containers/GTM-W44PZCC.json`
- `protobuf.meta`

The README's `res\values\strings.xml` is an Apktool-decoded path. The original APK stores those values in compiled `resources.arsc`; there is no literal ZIP entry at `res/values/strings.xml`.

### Embedded original source-path clues

These are strings inside `libclient.so`, not recovered source files:

- `jni/futurama/../../../shared/AccountSnsLogin.cpp`
- `jni/futurama/../../../shared/BattleSettingConfig.cpp`
- `jni/futurama/../../../shared/FUAccountLoginHelper.cpp`
- `jni/futurama/../../../shared/FUPlayer.cpp`
- `jni/futurama/../../../shared/HeadConfigManager.cpp`
- `jni/futurama/../../../shared/SpaceMapConfig.cpp`
- `jni/futurama/../../../shared/TownConfig.cpp`
- `jni/futurama/../../../shared/protobuf/FU.pb.cc`
- shared `lib/griffin` JSON and protobuf source paths

These names establish useful subsystem boundaries but reveal neither implementation details nor protocol schemas by themselves.

## What is known versus inferred

| Claim | Classification | Reason |
|---|---|---|
| Version 1.6.6 has a TinyCo production `tapservice` base and five non-production choices | **CONFIRMED** | Literal resources/native strings |
| The unmodified APK has an internal server-setting UI | **CONFIRMED** | Manifest, preference XML, and DEX code |
| ADB can launch that activity on the test device | **PROBABLE, untested** | Intent filter/default export behavior; no device run yet |
| The main endpoint is `/tapservice/api/` and uses POST | **PROBABLE** | Native suffix plus WOTServer implementation/README tooling; no preserved packet trace |
| The first successful response is exactly WOTServer's two-object JSON | **UNCERTAIN** | Field names align with client strings, values are synthetic, no successful run |
| `X-TC-Digest` is required or correctly calculated | **UNKNOWN** | Only a static spoofed value in WOTServer |
| `/process_queue.php` is real | **CONFIRMED path clue** | Exact native format string |
| `/get_server.php` is a real client endpoint | **HYPOTHESIZED** | WOTServer only; absent from APK string scan; source says remove it |
| `/api/auth/login`, `/api/player/init`, `/api/job/start`, `/api/job/collect`, `/api/mission/end`, `/api/cdn/manifest`, and `/api/build/place` are WoT endpoints | **HYPOTHESIZED, not observed** | They appear only in the research document's explicitly hypothesized matrix/roadmap; not in WOTServer or the APK scan |
| Main API payloads are JSON | **PROBABLE** | Direct JSON/content-type evidence and WOTServer; exact envelope remains unknown |
| Main API payloads are protobuf | **UNKNOWN** | Protobuf models exist, but transport use is not established |
| Dynamic content used the Akamai hosts | **PROBABLE** | Dedicated config/static roots and downloader symbols; exact manifest missing |
| The client is Unity/IL2CPP | **CONTRADICTED** | Exact archive architecture is native Marmalade/S3E/Cocos2d-style |
| The client shares a substantial framework lineage with TinyCo's Family Guy game | **CONFIRMED** | Package names, assets, source paths, and retained localization |
| WOTServer currently restores gameplay | **CONTRADICTED by its README and code** | It is a stateless three-path scaffold |

## Reliability notes on the research documents

The research documents are valuable as historical/content leads and as a preservation backlog. They are not equivalent to a packet trace or decompilation report.

In particular:

- the endpoint matrix at lines 198–207 is explicitly “Hypothesized” and must remain so;
- the proposed `/api/player/init` schema and later `/api/*` roadmap are design suggestions, not discoveries;
- claims that exact combat RNG/drop rates, timers, or specific logic were server-side require stronger technical evidence than the cited community sources presently provide;
- the Unity/IL2CPP client description is wrong for the inspected APK;
- the reported entity counts and “60%” event-content estimate may be useful baselines, but they are not established by the present archaeology pass.

## Bottom line

WOTServer preserved a valuable first foothold: likely routing, a probable batched bootstrap endpoint, candidate response fields, and some production-like headers. The APK adds a more important opportunity: it already contains a selectable localhost server configuration. The next evidence milestone should be a reproducible runtime trace from the unchanged APK, not a backend rewrite.

## Comparative case study: Team TSTO / Project Springfield

The maintainers identified [Team TSTO](https://teamtsto.org/) as the successful *The Simpsons: Tapped Out* revival they had in mind. The project's public name is **Project Springfield**.

### Directly confirmed from the Team TSTO site

- The site calls Project Springfield a community-driven private server and reports the server online at inspection time.
- It distributes separate patched clients named `Springfield-V08.apk` and `Springfield-V08.ipa` from `cdn.projectspringfield.com`.
- Players log in in the original game UI with an email and emailed verification code; anonymous play is documented as non-persistent.
- Players can start new towns or import preserved town files through a separate Town Manager.
- Imported saves use `.pb` files extracted from downloaded `.7z` archives.
- The linked Town Finder says its preservation effort saved more than 3 million town saves and exposes a 243 GB collection of 3,003,685 saves through the Internet Archive.
- The live project has separate Town Finder and Town Manager web applications.
- The site says events use limited-time quests and themed content, while explicitly warning that not all classic events are playable.
- It names distinct server, API, tooling, content-modding, and community roles. BodNJenie is named as server developer.

These statements demonstrate a mature operating model, but public-site claims are not substitutes for packet captures or source inspection.

### Public repository under the matching developer name

The public [BodNJenie TSTO private-server repository](https://github.com/bodnjenie14/Tsto---Simpsons-Tapped-Out---Private-Server) is a much larger and more complete reference than WOTServer. Its README and file tree directly show or describe:

- a C++ replacement server and a web dashboard;
- a Python GUI APK patcher that replaces separate server and DLC base URLs;
- configurable HTTP server and DLC URLs, with examples such as `http://192.168.1.1:80` and `http://192.168.1.2:80/static/`;
- roughly 30 GB of downloadable content required by that game;
- town persistence in protobuf-looking `.pb` files;
- dashboard town operations, save editing, game-configuration editing, event selection, force-save, currency editing, and IP/port configuration;
- Android and iOS client support;
- independent handling of server APIs, downloadable content, player saves, events, and operator tooling.

### Direct evidence from the local Project Springfield APK

Artifact: `D:\Downloads\Springfield-V08.apk`

| Item | Directly observed value |
|---|---|
| Size | 76,514,319 bytes |
| SHA-256 | `B3776198CEAED350FA0233CFA26C12BDB9F9D9DF5C100170F1F0B979FD1FAF40` |
| ZIP entries | 716 |
| Package | `com.ea.game.simpsons4_row.Springfield` |
| Client version | `4.70.5` (`versionCode` 695) |
| Minimum / target SDK | 21 / 34 |
| DEX files | `classes.dex`, `classes2.dex` |
| Native ABIs | ARMv7 and ARM64 |
| Main native libraries | `libscorpio.so`, `libscorpio-neon.so`, `libNimble.so`, `libopenal.so`, `libc++_shared.so` |

The binary Android manifest contains these exact routing/configuration values:

| Manifest key | Value | What it directly establishes |
|---|---|---|
| `MHClientVersion` | `Android.4.70.5` | Underlying TSTO client build |
| `ServerEnvironment` | `live` | Live configuration selected |
| `MayhemServerURL` | `https://game.pjtsto.com` | Replacement game-service base |
| `ServerAPIVersion` | `4.0.0` | Client-declared API version |
| `DLCSource` | `custom` | Non-default DLC source selected |
| `DLCLocation` | `https://cdn.projectspringfield.com/static/` | Replacement content base |
| `DLCSecretKey` | empty | No manifest-level DLC secret is supplied |
| `TntGameId` | `Simpsons-Tapped-Out` | Game identity retained |
| `Region` | `row` | Rest-of-world regional configuration retained |

The Project Springfield DLC hostname is also present in all four `libscorpio` variants as a fixed-width-looking string ending in `/static/`, with a long zero-padded representation of port 443. This is consistent with an in-place binary patcher preserving the original string allocation, but the reason for the padding has not been proven.

The APK is signed by a self-signed certificate whose subject is `CN=Android Debug, OU=Android, O=US, L=US, ST=US, C=US`, with SHA-256 fingerprint `1E:08:A9:03:AE:F9:C3:A7:21:51:0B:64:EC:76:4D:01:D3:D0:94:EB:95:41:61:B6:25:44:EA:8F:18:7B:59:53`. This directly confirms use of an Android Debug-style signing identity and strongly indicates community re-signing. Proving the signing-key change requires comparison with a hash-verified original 4.70.5 APK. The finding is consistent with Team TSTO's instruction to uninstall a previous version, because Android normally rejects an update signed by a different key. A basic JAR-signature verification completed, but Java also reported self-signing, no timestamp, and JAR/JAR-stream consistency warnings; a future pass should use Android's `apksigner` for authoritative APK Signature Scheme verification.

#### Server path clues retained in the TSTO native client

The ARM64 `libscorpio.so` contains the following game-service path strings. They are comparative evidence only; the static strings do not establish the HTTP method, complete host concatenation, request body, or whether every path is exercised by Project Springfield:

```text
/games/bg_gameserver_plugin/checkToken/
/games/bg_gameserver_plugin/currencyInventory/
/games/bg_gameserver_plugin/deleteToken/
/games/bg_gameserver_plugin/event/
/games/bg_gameserver_plugin/extraLandUpdate/
/games/bg_gameserver_plugin/friendData
/games/bg_gameserver_plugin/friendData/facebook
/games/bg_gameserver_plugin/friendData/origin
/games/bg_gameserver_plugin/land/
/games/bg_gameserver_plugin/migrateLand
/games/bg_gameserver_plugin/offers/
/games/bg_gameserver_plugin/protoClientConfig
/games/bg_gameserver_plugin/protoClientConfig/custom
/games/bg_gameserver_plugin/protocurrency/
/games/bg_gameserver_plugin/protoland/
/games/bg_gameserver_plugin/protoWholeLandToken/
/games/bg_gameserver_plugin/purchase/
/games/bg_gameserver_plugin/telemetrylog/
/games/bg_gameserver_plugin/trackinglog/
/games/bg_gameserver_plugin/trackingmetrics/
/games/bg_gameserver_plugin/upgradeland/
/games/lobby/time
/gameplayconfig
/gameplayconfig/custom
/playersearch/api/search
/user/api/android/getLatestUid
/director/api/android/getDirectionByPackage
/dlc/index
/save
```

The same native library contains protobuf type names for land, user, currency, event, friend, quest, timer, and whole-land-token data. This independently supports the Team TSTO documentation's use of `.pb` town saves, while not proving the exact on-disk town schema.

### Known versus inferred

| Claim | Classification | Reason |
|---|---|---|
| Project Springfield is a functioning hosted TSTO private server with patched mobile clients | **CONFIRMED public-project claim** | Team TSTO home page, install instructions, downloads, and public tools |
| The current Project Springfield service uses the public BodNJenie repository unchanged | **UNPROVEN** | Matching developer name and matching features, but no repository link or deployment attestation on Team TSTO |
| The TSTO protocol or patch offsets can be reused for Futurama | **CONTRADICTED as a direct assumption** | Different game/client binaries; only the investigation pattern transfers |
| Separating core API, DLC hosting, persistence, event controls, and operator tools is a useful future reference | **SUPPORTED comparative lesson** | Each concern is visible in the TSTO project, but adopting that architecture for WoT still requires maintainer approval |
| WoT will require a modified APK because TSTO did | **NOT SUPPORTED** | The WoT APK has an internal service-URL preference and localhost target that may avoid modification for early experiments |
| Team TSTO redirects game API and DLC traffic separately | **CONFIRMED for the inspected APK** | `MayhemServerURL`, `DLCSource`, and `DLCLocation` in its binary manifest |

### What transfers to Futurama archaeology

The valuable lesson is methodological: preserve saves and DLC separately, patch or redirect only the minimum client endpoints, reproduce the smallest startup contract first, and add operator tooling only after the protocol is understood. The TSTO implementation is not proof of any Futurama endpoint, payload, signature, or data model.

## Local TSTO repository archaeology

### Scope and provenance

The committed state of the local BodNJenie checkout was inspected at commit `1a4afa14dd6a02c405db5c8f74565526bf176819`. The repository was not built, run, repaired, reset, or modified. This distinction matters because its visible working tree is not clean: nearly all tracked files appear staged as deleted and a replacement tree appears untracked.

The committed evidence set contains:

- C++ replacement-server source under `source/server/`;
- 16 `.proto` schemas covering auth, client/game configuration, telemetry, friends, purchases, land, and whole-land tokens;
- HTTP Toolkit captures named `reg_login.har`, `boot after login.har`, `tutorial_reload.har`, and `tutorial_reload2.har`;
- `windows_gui_patcher.py`;
- a web dashboard and town tools;
- `config.json` with gameplay/event configuration overrides;
- an original TSTO APK named `tsto_original.apk`.

Two capture files are not usable as complete evidence: `dlc server.har` is exactly 8,388,608 bytes and terminates in the middle of a JSON string, and `tutorials.har` is empty. The valid HAR files contain identifiers, authorization material, and device/emulator telemetry, so this report inventories routes and types without reproducing credentials or personal identifiers.

### Plain-English reconstruction of what the author discovered and built

The author appears to have captured the original TSTO client's registration, login, bootstrap, town-load, town-save, and telemetry traffic shortly before or around the official shutdown. From those captures and the client binaries, they learned that startup is not one API call. It is a chain across EA service-discovery, account, identity, device, game, analytics, and DLC hosts.

Their central implementation idea is a facade: patch the client so both the EA director host and main Mayhem game host point at one local HTTP server. The replacement `/director/api/.../getDirection...` response then redirects a long list of service keys back to the same configured server base. That lets one dispatcher impersonate multiple original EA services without recreating the original DNS layout.

The implementation goes substantially beyond canned responses. It includes:

- Android and iOS direction/bootstrap responses;
- device/anonymous-ID, auth-code, token, token-info, persona, and registration flows;
- SQLite user records and generated replacement tokens/codes;
- protobuf client config, gameplay config, currency, friends, event, land, and whole-land-token responses;
- protobuf town loading and saving, including gzip-compressed land uploads;
- DLC ZIP/static-file hosting under `/static`;
- event-time controls and gameplay configuration overrides;
- a dashboard that can import, inspect, alter, and save town files.

This is convincing evidence that the author reconstructed enough of the client contract for a self-hosted TSTO town to operate. It is not evidence that the public repository is the exact hosted Project Springfield backend. In particular, this code has one process-wide `Session` singleton and one process-wide `LandMessage`, even though it stores some users separately. The README itself describes town switching as not being true multiuser support. That design is not consistent with an unchanged deployment serving the public site's claimed user population concurrently.

### Server architecture and persistence

- Language/runtime: C++ using evpp/libevent HTTP handling, RapidJSON, protobuf, SQLite, and filesystem storage.
- Listener: one game HTTP server, default TCP port 80, two worker threads. No TLS context or certificate setup is visible in startup code.
- Address: the server auto-detects a local IPv4 address, falls back to `127.0.0.1`, and can read `ServerIP`/`GamePort` configuration.
- DLC: a formerly separate DLC listener is commented out; the active dispatcher serves `/static` on the game server's port.
- Users: `tsto_users.db`, table `users(email, user_id, access_token, mayhem_id, access_code)` plus indices.
- Towns: `towns/<email>.pb` and legacy `towns/mytown.pb` paths, parsed as `Data::LandMessage`.
- Currency: several legacy/current paths appear, including `towns/currency.txt`, `towns/currency_<email>.txt`, and some `<email>.txt` branches. The inconsistency is direct code evidence and should not be normalized away without testing.
- Gameplay overrides: root-level `config.json`.
- DLC files: configured `DLCDirectory`, default `dlc`; requested through `/static/...`.
- Dashboard assets: `webpanel/...`.

The public server is best described as a feature-rich single-instance research/private server, not as a production-grade multi-tenant architecture. The dashboard routes are dispatched on the same listener as game traffic; most do not show an authentication gate. The DLC filename sanitizer permits dots and slashes, so this code should not be exposed to an untrusted network without a separate security review. These are observations about safe handling of the reference, not proposed Futurama architecture.

### Complete committed dispatcher route inventory

The following paths are direct source evidence. A brace denotes a variable segment reconstructed by the handler. Except where stated, the dispatcher does not restrict the HTTP method, so a path's presence must not be read as proof that every method is valid.

#### Root, discovery, device, identity, and authentication

| Route | Method evidence | Implemented response family |
|---|---|---|
| `/` | unrestricted in dispatcher | JSON status |
| `/probe` | unrestricted | empty body |
| `/director/api/{platform}/getDirectionByPackage` | original HAR: GET (Android) | JSON direction/service map |
| `/director/api/{platform}/getDirectionByBundle` | source route (iOS) | JSON direction/service map |
| `/mh/games/lobby/time` | HAR: GET | XML epoch time |
| `/proxy/identity/geoagerequirements` | source route | JSON |
| `/proxy/identity/progreg/code` | HAR: POST | JSON registration code/user ID |
| `/games/{numeric-game-id}/devices` | HAR equivalent: POST `/rest/v1/games/48302/devices`; source regex omits `/rest/v1` | JSON device registration |
| `/user/api/android/getAnonUid` | source route | JSON |
| `/user/api/iphone/getAnonUid` | source route | JSON |
| `/user/api/android/getDeviceID` | source route | JSON |
| `/user/api/iphone/getDeviceID` | source route | JSON |
| `/user/api/android/validateDeviceID` | HAR: GET | JSON |
| `/user/api/iphone/validateDeviceID` | source route | JSON |
| `/connect/auth` | HAR: GET | JSON/auth redirect-style payloads |
| `/connect/token` | HAR: POST | JSON token payload |
| `/connect/tokeninfo` | HAR: GET | JSON token/persona payload |
| `/proxy/identity/pids/me/personas/{id}` | HAR: GET | JSON |
| `/proxy/identity/pids/{id}/personas` | HAR: GET | JSON |
| `/mh/users` | HAR: GET and PUT | implementation returns protobuf |
| `/mh/userstats` | HAR: POST, original response 409 octet-stream | implementation returns an empty response |

The `/games/{id}/devices` mismatch is important: the captures show `/rest/v1/games/48302/devices`, while the committed regex is `^/games/\\d+/devices$`. Unless URI preprocessing not seen here removes `/rest/v1`, the captured original path would miss this handler. Treat it as an implementation discrepancy.

#### Game, telemetry, land, friends, and currency

| Route/template | Captured method where known | Implemented response/body clue |
|---|---|---|
| `/pinEvents` | POST | JSON `status: ok` |
| `/tracking/api/core/logEvent` | POST | JSON status |
| `/mh/games/bg_gameserver_plugin/trackinglog/` | source route | parses `ClientLog` protobuf; XML acknowledgement |
| `/mh/games/bg_gameserver_plugin/trackingmetrics/` | POST | parses `ClientMetrics` protobuf; XML acknowledgement |
| `/mh/clienttelemetry/` | POST | parses `ClientTelemetry` protobuf; XML acknowledgement |
| `/mh/games/bg_gameserver_plugin/checkToken/{land-id}/...` | GET | protobuf whole-land-token data |
| `/mh/games/bg_gameserver_plugin/protoClientConfig/` | GET | protobuf client configuration |
| `/mh/gameplayconfig` | GET in game capture; GET/POST also used by dashboard handler | protobuf for game client; JSON configuration for dashboard content negotiation/path handling |
| `/mh/games/bg_gameserver_plugin/event/{land-id}/protoland/` | GET | protobuf event/land response |
| `/mh/games/bg_gameserver_plugin/event/...` | source prefix | protobuf event response |
| `/mh/games/bg_gameserver_plugin/protoland/{land-id}/` | GET and POST captured; source explicitly handles GET, PUT, POST | protobuf download/update; POST accepts optional gzip and returns XML acknowledgement |
| `/mh/games/bg_gameserver_plugin/extraLandUpdate/{land-id}/protoland/` | POST | parses/returns protobuf land update |
| `/mh/games/bg_gameserver_plugin/protoWholeLandToken/{land-id}/` | POST | protobuf; captures sometimes label the original response XML |
| `/mh/games/bg_gameserver_plugin/deleteToken/{land-id}/protoWholeLandToken/` | POST | protobuf success or XML errors |
| `/mh/games/bg_gameserver_plugin/townOperations/` | source route | JSON operator operation |
| `/mh/games/bg_gameserver_plugin/friendData` | POST; `/origin` GET | protobuf friend data |
| `/mh/games/bg_gameserver_plugin/protocurrency/{land-id}/` | GET | protobuf `CurrencyData` |
| `/static/...` | GET implied by DLC client/captures | bytes from local DLC directory; MIME selected by extension |

The captures show that response type can vary by operation on the same path. For example, `protoland` GET returns `application/x-protobuf`, while a save POST can return XML. Therefore endpoint alone is insufficient to infer a schema.

#### Dashboard and operator routes

`/dashboard`, `/dashboard.html`, `/dashboard/*`, `/images/*`, `/town_operations.html`, `/town_operations`, `/town_operations.js`, `/tsto-styles.css`, `/css/tsto-styles.css`, `/game_config.html`, `/game_config`, `/proto/client_config.js`, `/proto/gameplay_config.js`, `/api/get-user-save`, `/api/save-user-save`, `/list_users`, `/api/dashboard/data`, `/edit_user_currency`, `/api/browseDirectory`, `/api/config/game`, `/api/server/restart`, `/api/server/stop`, `/api/forceSaveProtoland`, `/update_initial_donuts`, `/api/updateDlcDirectory`, `/api/updateServerIp`, `/api/updateServerPort`, `/api/events/set`, `/api/events/adjust_time`, `/api/events/reset_time`, `/api/events/get_time`, and `/upload_town_file`.

`/api/config/game` explicitly accepts GET or POST and returns 405 otherwise. The upload path expects `multipart/form-data`. Other dashboard handlers consume query parameters or JSON bodies according to the handler, but most lack an explicit dispatcher-level method constraint.

Unknown routes return HTTP 404 with JSON `{"status":"error","message":"Unknown endpoint"}`; dispatcher exceptions return HTTP 500 JSON. Response helpers set `application/json`, `application/x-protobuf`, or `application/xml`.

### What the valid original-client captures directly show

The four usable HARs collectively preserve HTTPS/HTTP 1.1 requests to these hosts:

`accounts.ea.com`, `api-new.bignox.com`, `bae.appmeasurements.com`, `deviceintegritytokens-pa.googleapis.com`, `eaavatarservice.akamaized.net`, `friends.gs.ea.com`, `gateway.ea.com`, `graph.facebook.com`, `in.appcenter.ms`, `m.avatar.dm.origin.com`, `oct2018-4-35-0-uam5h44a.tstodlc.eamobile.com`, `ping1.tnt-ea.com`, `pin-river.data.ea.com`, `pn.tnt-ea.com`, `prod.simpsons-ea.com`, `reign.appmeasurements.com`, `river-mobile.data.ea.com`, `stup9.appmeasurements.com`, `syn-dir.sn.eamobile.com`, `user.sn.eamobile.com`, and `www.googleapis.com`.

The emulator/analytics/Google/Facebook/App Center hosts are captured traffic, but they are not necessarily required for game bootstrap. The game-relevant captured sequence includes:

- `GET https://syn-dir.sn.eamobile.com/director/api/android/getDirectionByPackage` -> JSON;
- `GET https://user.sn.eamobile.com/user/api/android/validateDeviceID` -> JSON;
- `GET https://accounts.ea.com/probe`, `/connect/auth`, and `/connect/tokeninfo`; `POST /connect/token` -> JSON or auth data;
- `POST https://gateway.ea.com/proxy/identity/progreg/code` and persona/links GETs -> JSON;
- `POST https://pn.tnt-ea.com/rest/v1/games/48302/devices` -> JSON;
- `GET/PUT/POST https://prod.simpsons-ea.com/mh/...` for users, time, configuration, friend data, tokens, currency, event land, whole land, land save, and telemetry -> XML/protobuf/octet-stream depending on operation;
- `POST https://pin-river.data.ea.com/pinEvents` and `POST https://river-mobile.data.ea.com/tracking/api/core/logEvent` -> JSON;
- `GET` requests to the original DLC host for `DLCIndex.zip`, a versioned index, and a versioned patch ZIP -> ZIP or 404 HTML.

No public IP address is hardcoded as the replacement-server destination in the committed source. Example private addresses `192.168.1.1` and `192.168.1.2`, `127.0.0.1`, and user-configured/detected addresses are present. IP addresses that happen to appear inside captures as client telemetry or observer data have deliberately not been copied here; they are not server protocol requirements.

### Direction-response and protocol clues

The replacement direction response is a particularly useful blueprint. It returns JSON fields for product/game identity and a `serverData` array. Android and iOS get platform-specific package/bundle identifiers. Most service keys—including Nexus/account proxy, Mayhem, friends, identity, tracking, director, push, avatars, and recommendations—are pointed to the configured replacement base. `antelope.rtm.host` points to port 9000; no matching port-9000 server implementation is visible. Loader URLs point to `/loader/mobile/android/` or `/loader/mobile/ios/`, but those routes are not present in the dispatcher.

The response also inserts an original CDN URL for `akamai.url`, then includes `akamai.url` again among keys redirected to the replacement base. Which duplicate the client honors is **uncertain**. This is another sign that the public code contains experimental or compatibility-driven behavior rather than a clean specification.

### Exact behavior of the committed APK patcher

`windows_gui_patcher.py` uses Apktool 2.10.0 to decompile/rebuild and changes two text URLs:

- `https://prod.simpsons-ea.com` -> operator-supplied game server URL;
- `https://syn-dir.sn.eamobile.com` -> the same game server URL.

It also patches all four `libscorpio.so`/`libscorpio-neon.so` ABI variants, replacing this fixed native DLC string:

`http://oct2018-4-35-0-uam5h44a.tstodlc.eamobile.com/netstorage/gameasset/direct/simpsons/`

The new DLC base is forced to end in `/static/`. A shorter value is padded with repeated `./` text (and a final `/` for odd remaining length); a longer value is silently truncated. The rebuilt APK must therefore be re-signed.

This patcher revision is not the exact tool or settings that produced the inspected `Springfield-V08.apk`. That APK's native replacement is instead:

`https://cdn.projectspringfield.com:0000000000000000000000000000000000000000000443/static/`

The zero-padded port preserves the original native string length, but it does not match the public patcher's `./` padding algorithm. This is direct evidence of a different patcher revision, a manual patch, or a separate production build process.

### Original-versus-Project-Springfield APK comparison

The committed original APK was read from Git's object database without altering the dirty checkout:

| Artifact | Size | SHA-256 | Entries |
|---|---:|---|---:|
| Committed `tsto_original.apk` | 80,918,993 | `337D4B65924042F423F754AD08722F8B830AC4C5A0F413417E62F373282C946D` | 738 |
| `Springfield-V08.apk` | 76,514,319 | `B3776198CEAED350FA0233CFA26C12BDB9F9D9DF5C100170F1F0B979FD1FAF40` | 716 |

Manifest differences directly observed:

| Key | Committed original | Project Springfield |
|---|---|---|
| Package | `com.ea.game.simpsons4_row` | `com.ea.game.simpsons4_row.Springfield` |
| `versionName` / `MHClientVersion` | `4.69.5` / `Android.4.69.5` | `4.70.5` / `Android.4.70.5` |
| `versionCode` | 695 | 695 |
| `MayhemServerURL` | `https://prod.simpsons-ea.com` | `https://game.pjtsto.com` |
| `DLCLocation` | original `oct2018...eamobile.com/.../simpsons/` base | `https://cdn.projectspringfield.com/static/` |
| SDK, environment, API version, game ID, region | 21/34, live, 4.0.0, Simpsons-Tapped-Out, row | unchanged |

The original is **4.69.5, not a hash-verified original 4.70.5**, despite sharing versionCode 695 with the patched build. Consequently this pair cannot prove every intentional Project Springfield change.

At ZIP-entry level, only 68 entries are byte-identical; 51 same-name entries differ; 597 names occur only in the patched archive and 619 only in the original. Most of that enormous path churn is consistent with Apktool resource decoding/rebuilding and archive repacking, not 1,267 deliberate game changes. It would be misleading to call the raw archive diff an exact patch list.

The four native Scorpio libraries are the strongest normalized comparison because each retains exactly the same uncompressed length. Each differs in only 82 or 84 byte positions across five or six contiguous runs. The dominant run is the fixed-width DLC URL replacement; the remaining one-to-three-byte runs have not been explained and may be ancillary binary metadata/checksum changes. This shows that Project Springfield left these large native libraries essentially intact apart from a surgical endpoint patch.

The signature files also changed: the original `META-INF/EAMKEYST.DSA/.SF` entries are gone and `META-INF/ANDROIDD.RSA/.SF` entries appear. This corroborates community rebuilding/re-signing. The manifest, both DEX files, resources table, and numerous resource paths changed, so a normalized Apktool/smali comparison is still required before claiming an exhaustive logical patch set.

### Comparative known versus inferred

| Finding | Classification |
|---|---|
| The author captured original TSTO registration/login/bootstrap/land traffic | **CONFIRMED** by valid HARs |
| The source implements the listed facade routes and protobuf/JSON/XML responses | **CONFIRMED** by committed code |
| Original traffic used HTTPS and the public server listens in cleartext HTTP by default | **CONFIRMED** |
| The client can be redirected by changing director, game, and DLC bases | **CONFIRMED for the patcher/APKs** |
| The public server can load/save a protobuf `LandMessage` town | **CONFIRMED implementation**; not runtime-tested here |
| Every committed handler exactly matches the original server | **CONTRADICTED** by at least the device-route mismatch and missing loader/RTM routes |
| The inspected public commit is Project Springfield's production server | **UNPROVEN and unlikely unchanged**, based on singleton state and patcher mismatch |
| TSTO protocol details can be copied into Futurama | **CONTRADICTED**; only the archaeological workflow transfers |
