# Futurama: Worlds of Tomorrow Preservation Project Context

## Purpose

This project is a software-preservation effort for the discontinued mobile game *Futurama: Worlds of Tomorrow* (WoT). The immediate goal is to understand the surviving Android client and restore the smallest evidence-backed server behavior needed to make it advance toward a playable local town.

The project began with archaeology. On 2026-08-27 the maintainers explicitly authorized changes to a disposable copy of the APK and implementation work. The original APK remains fingerprinted and untouched. No large replacement-server architecture has yet been selected; the current implementation is still a deliberately small protocol probe.

## Direction and constraints

The project is directed by its maintainers. Before any large architectural decision, client rewrite, APK modification, or WOTServer rewrite, discuss the choice with the maintainers.

For the current phase:

- preserve the original APK unchanged and make client changes only in derived builds;
- preserve the WOTServer checkout unchanged;
- prefer reversible inspection and small experiments;
- record direct evidence separately from inference;
- do not invent protocol fields or treat plausible endpoint names as observed traffic;
- do not redistribute copyrighted game assets;
- record every client patch, output hash, request, response, and visible result;
- optimize first for an initial town-loading path, while keeping protocol claims evidence-backed.

## Artifacts presently available

### Research documents

- `docs/research/Deep Research Prompt — Complete Futurama_ Worlds of Tomorrow Game Inventory.md` defines the long-term preservation inventory, evidence model, and milestone concept.
- `docs/research/Futurama Game Preservation Research.md` compiles historical and gameplay research. Its technical endpoint matrix is explicitly labelled “Hypothesized.”
- `docs/research/Futurama_ Worlds of Tomorrow was a free-to-play.md` is primarily a business, licensing, and full-revival strategy document. Its technical estimates are not protocol evidence.

### Android APK

- Source artifact: `C:\Users\nick\Documents\apk\Futurama_+Worlds+of+Tomorrow_1.6.6_APKPure.apk`
- Size: 95,728,636 bytes
- SHA-256: `5FF63E3F46622114C5A14D86038E1D5085A676B8A3F919E02ADD6BC1F5991D0F`
- Package: `com.tinyco.futurama`
- Manifest version: `1.6.6` (`versionCode` 1665)
- Android SDK range: minimum 14, target 26
- Archive inventory: 4,326 entries, including 2,546 entries under `assets/`, three DEX files, compiled resources, and one ARMv7 native library.

This fingerprint identifies the exact artifact discussed in the current documentation. Findings should not automatically be generalized to other releases.

### WOTServer

- Local checkout: `C:\Users\nick\Documents\GitHub\WOTServer`
- Upstream: `https://github.com/BirkinSornberger/WOTServer.git`
- Inspected commit: `22e533d3bebcc54821ee08c725b459a1b52d2477`
- Last commit in the local history: 2025-04-20
- Files: `README.md`, `main.py`, and `saltResponse.json`
- The README explicitly says the project is not functional and cannot currently make the game playable.

The repository is a very small capture-and-response prototype, not a replacement backend. Its value is that it preserves a few observed or suspected connection details and one proposed bootstrap response shape.

### Related replacement-server references

The specific successful *The Simpsons: Tapped Out* reference is [Team TSTO / Project Springfield](https://teamtsto.org/). Its public site describes a live community private server with patched Android and iOS clients, account login, persistent towns, imported original town saves, restored events, and web-based town tools.

The site names BodNJenie as its server developer. A public repository under the matching GitHub name, [Tsto---Simpsons-Tapped-Out---Private-Server](https://github.com/bodnjenie14/Tsto---Simpsons-Tapped-Out---Private-Server), contains a C++ server, APK patcher, payloads, tools, and web panel. This is strong comparative evidence. However, the Team TSTO site does not link that repository, so it is not yet proven that the repository is the exact source deployed by Project Springfield.

A local copy of Team TSTO's Android client is also available for read-only comparative analysis:

- Source artifact: `D:\Downloads\Springfield-V08.apk`
- Size: 76,514,319 bytes
- SHA-256: `B3776198CEAED350FA0233CFA26C12BDB9F9D9DF5C100170F1F0B979FD1FAF40`
- Package/version: `com.ea.game.simpsons4_row.Springfield`, version `4.70.5` (`versionCode` 695)

This APK was inspected but not installed, executed, or modified.

The matching public server repository is also available locally:

- Checkout: `C:\Users\nick\Documents\GitHub\Tsto---Simpsons-Tapped-Out---Private-Server\Tsto---Simpsons-Tapped-Out---Private-Server`
- Upstream: `https://github.com/bodnjenie14/Tsto---Simpsons-Tapped-Out---Private-Server.git`
- Inspected Git commit: `1a4afa14dd6a02c405db5c8f74565526bf176819`
- Commit date/subject: 2025-07-03, `Update README.md`

The checkout arrived in an unusual dirty state: Git reports almost every tracked file staged as deleted while a replacement tree is untracked. No reset, checkout, build, or repair was performed. To avoid confusing uncommitted replacement files with published evidence, the comparative source findings in this pass were taken from the committed `HEAD` objects with read-only `git show`/archive operations.

The committed repository includes a C++ server, protobuf schemas, a Python APK patcher, web dashboard, original-client HTTP Toolkit HAR captures, and a committed original TSTO APK. These artifacts make it a strong methodology and protocol reference. They do **not** prove that Futurama uses any TSTO endpoint or schema.

### Attached iPad

Windows presently enumerates an attached Apple iPad over USB. iMazing 3.6.2 and current Apple Mobile Device support are installed, but read-only iMazing CLI discovery did not return a paired/available device session. No pairing, backup, app-data extraction, IPA extraction, or device setting change was attempted.

On a normal non-jailbroken iPad, a device backup can preserve allowed app data but does not provide a reusable decrypted copy of an installed App Store executable. The installed iMazing CLI exposes app-data extraction but no command to export an installed app as an IPA. The next safe step requires the iPad to be unlocked and to trust this computer; even then, preserving Team TSTO's publicly distributed `Springfield-V08.ipa` is likely more direct than attempting to reconstruct it from the installed app.

## Verified technical baseline

The exact APK is **not a Unity/IL2CPP game client**. It contains:

- `lib/armeabi-v7a/libclient.so`, not `libil2cpp.so`;
- `assets/app.icf` with Marmalade-style `[S3E]` and `IW_GL` settings;
- native C++ symbols and compiler paths referring to `cocos2d`, TinyCo's shared `griffin` library, and game-specific C++ sources;
- no `assets/bin/Data` Unity content tree.

The manifest does contain a Unity Ads activity, but that identifies an advertising SDK, not the game engine. The Unity claims in the research documents are therefore contradicted for this APK.

The client includes a built-in Android preference screen with server choices and an `Other Service URL` field. The preference activity is declared with an intent filter and no explicit `android:exported="false"`; for this target-SDK-era manifest that strongly suggests it can be launched through ADB. This has not yet been tested on a device.

The production game base URL and several non-production URLs are embedded in both `resources.arsc` and `libclient.so`. The native client also contains `tapservice/api`, JSON/form content-type strings, salt/player identity field names, a message-queue PHP path format, JSON implementation symbols, and compiled protobuf model names.

## Current runtime milestone (2026-08-27)

A derived, locally signed preservation build now reaches software controlled by this project. Two narrowly scoped client changes were required:

1. Replace the native production service base with `http://10.0.2.2:8302/tapservice/`, preserving the native library length with NUL padding.
2. Make the legacy Google Play licensing policy return `true`. Without this second change, the re-signed build stops before network bootstrap because its signature no longer matches the retired store license.

The preservation build sent a real bootstrap request to the probe and displayed the game's own **Connect Error** after a controlled HTTP 503. This is the first visible proof that the surviving client is responding to software under project control.

The same client rejected WOTServer's sample `saltResponse.json` both as plain JSON and as gzip JSON with WOTServer's hardcoded `X-TC-Digest`. WOTServer therefore remains useful protocol evidence, but its response is not a working bootstrap fixture for this APK.

The next blocker is the exact accepted field values and any later validation of the initial salt/player response. Native tracing and a rejected named-object experiment support an array-valued `response` containing two object results. The client reads `salt` and `signed_salt` as strings and stores them, but no cryptographic verification is visible in that callback. `server_md5` belongs to a separate configuration/file-loading path.

## Current working model

The strongest current hypothesis is:

1. The Android wrapper initializes shared preferences and native TinyCo/Griffin code.
2. Although the Java preference UI stores alternate service choices, this production native build continued to use its compiled production URL in runtime testing. A native URL patch was required.
3. The main client performs an HTTP form POST to `/tapservice/api/` and identifies batched actions in the `RPC` header.
4. The first observed batch requests `getSalt` and `getOrCreatePlayerId`.
5. Native code expects an array-valued `response` with two object results and string fields for salt/player identity; the exact accepted identifier/signature values are not yet runtime-confirmed.
6. Later work probably depends on a server message queue, player state/configuration, and CDN-hosted content.

Steps 1–4 are runtime-confirmed for the Android 1.6.6 preservation build. Step 5 combines confirmed native field/type reads with an inferred container model. Step 6 remains a working hypothesis. No response has yet advanced the client beyond bootstrap.

## Evidence policy

Use these labels in future work:

- **CONFIRMED** — directly present in the exact APK, repository source, or a captured runtime trace.
- **PROBABLE** — strongly supported by multiple direct clues but not observed end to end.
- **UNCERTAIN** — plausible, with incomplete or ambiguous evidence.
- **HYPOTHESIZED** — proposed for testing; not evidence of original behavior.
- **CONTRADICTED** — inconsistent with the inspected artifact.

The detailed evidence, endpoint inventory, and confidence calls are in `docs/DISCOVERIES.md`. Blocking questions and the proposed first experiments are in `docs/QUESTIONS.md`.
