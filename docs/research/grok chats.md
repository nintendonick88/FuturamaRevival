

Skip to main content
Ctrl+K
Ctrl+J



codex raw chat build.md

Futurama Game Preservation Research.md

Futurama_ Worlds of Tomorrow was a free-to-play.md
Refer to the following content:


Worked for 25s
Status update from the interrupted session

The previous pass made real progress on the native response authenticity gate and then hit a usage limit mid-analysis. Here is the clean, evidence-backed state of knowledge right now, followed by the three smallest experiments that should be run next.

Confirmed technical findings (high confidence)
Client is not Unity/IL2CPP

APK 1.6.6 contains lib/armeabi-v7a/libclient.so, Marmalade/S3E-style strings (s3e, Iw_GL, etc.), and assets/app.icf. The research document’s Unity claim is incorrect for this binary.

Built-in server selector exists

An exported preference activity exposes Beta / Dev / Localhost / Prod / Review / Staging / Other Service URL.

Localhost hard-codes http://127.0.0.1:8302/tapservice/.

This is the cleanest redirection path (adb reverse + unchanged or lightly patched APK).

Primary endpoint path

Client POSTs to /tapservice/api/ (and related paths under the same base).

/process_queue.php also appears in supporting evidence.

The research document’s /api/auth/login, /api/player/init, job, mission, and CDN endpoints remain unverified hypotheses.

X-TC-Digest header grammar (the latest breakthrough)

The native verifier in libclient.so does not accept a bare 32-character MD5.

It requires both delimiters and parses the header as:

prefix?key1=value1,key2=value2#digest
Everything before the first ? is the prefix.
The section between ? and # is treated as comma-separated key=value pairs.
Everything after # is the digest that is checked against a client-side computation that incorporates request/response context.
Observed failure strings: "missing checksum", "missing/bad data".

A minimal syntactically acceptable placeholder that reaches the comparison stage is of the form:

X-TC-Digest: local?a=b#00000000000000000000000000000000
(The actual accepted keys and the exact hash input are still unknown; the comparison itself can be patched out cleanly.)

WOTServer

It is a three-path debugging scaffold, not a functional replacement backend. It does not yet emit a correctly structured digest or a bootstrap JSON the native parser accepts.

Patches already exercised

Localhost routing (or adb reverse).
Forced acceptance of the digest comparison (single-instruction change at the final return point).
Trap/diagnostic builds that surface more logcat information.
The client can be made to receive an HTTP 200 with a shaped body and a syntactically valid digest header. It still does not advance past the loading / connection-error state in a stable way, which indicates that either (a) the JSON body shape is still wrong, (b) a subsequent native check fails, or (c) required follow-on requests are missing.

What remains inferred or unknown
Exact set of accepted keys inside the ?…# section.
Exact bytes that are hashed to produce the digest (request body + salt + response body + prefix?).
Minimal JSON schema that lets the client leave the loading screen and instantiate the city view.
Whether any of the research document’s hypothesized REST endpoints are actually used by this APK.
CDN / AssetBundle URLs and whether the client hard-fails when they 404.
Recommended next experiments (ranked)
All three are deliberately small, reversible, and produce visible evidence (logcat + probe server logs + client UI change).

1. Highest likelihood / highest teaching value / lowest difficulty

Keep the existing checksum-accept patch.

Serve a response with the corrected three-part digest header and the current best-shaped bootstrap JSON.

Capture full logcat for any new native strings after the digest is accepted (especially anything containing “parse”, “JSON”, “RPC”, “player”, “salt”, “getOrCreate”, “LoadingViewController”).

Payoff: confirms whether the digest gate is now fully open and surfaces the next concrete failure.

2. Visible client-controlled behavior

With the same patched APK + adb reverse, change only the HTTP status or a single top-level JSON field that the probe server logs.

Observe whether the loading screen text, spinner, or error dialog changes in a way that is clearly caused by the software you control.

Payoff: the “first visible win” the project originally asked for—proof that the original client is reacting to a server under your control.

3. Slightly deeper but still contained

Static search for the string constants that appear immediately after a successful digest check (or the functions that call the digest verifier).

Identify the next validation or JSON-deserialization routine and decide whether a second one-instruction patch or a richer fixture is the cheaper next step.

Payoff: maps the exact call chain so future patches stay minimal.

I will not rewrite WOTServer or the APK beyond the already-discussed single-instruction digest acceptance, and I will not invent protocol details that are not visible in the binary or runtime logs.

Would you like me to:

draft the exact probe-server command line + fixture for experiment 1,
produce an updated DISCOVERIES.md / QUESTIONS.md reflecting the digest grammar, or
walk through the next native disassembly targets once you have the latest logcat from a digest-accepted run?
Just say which one to do first.

Analyze Tapped Out Reborn architecture


Worked for 57s
Tapped Out Reborn architecture analysis

(Focused on the open-source TappedOutReborn/GameServer-Reborn project and its supporting tools. This is the most directly relevant working private-server effort for The Simpsons: Tapped Out.)

High-level overview
Tapped Out Reborn is a multi-user Node.js replacement server that lets the original (patched) mobile client continue playing after the official EA/Jam City shutdown. It does not reimplement the full game client. Instead it:

Redirects the original client via APK binary patching.
Speaks enough of the original protocol (mostly HTTP + Protocol Buffers) to authenticate, load/save town state, serve DLC assets, and drive events.
Stores per-player game state as protobuf files + a small SQLite metadata database.
Provides simple web dashboards for users and admins.
It is a practical, working example of the exact pattern needed for Futurama: Worlds of Tomorrow.

Core repositories
Repo	Role
GameServer-Reborn	Main Node.js/Express server (auth, land load/save, currency, events, DLC serving, dashboards)
Patch-Apk	Scripts (bash + Python + radare2) that rewrite server/DLC URLs inside the original APK’s native libraries and resources
DLC-Downloader	Tool to fetch the large asset packs (characters, buildings, quests, etc.) the client expects
GameplayConfig-Downloader (archived)	Extracts gameplay configuration as JSON via the protobuf definitions
TSTO-Toolbox	Smaller Rust tooling (less central)
Related community efforts (e.g. Project Springfield / teamtsto.org) exist and appear to share the same general approach, but the public source of truth for architecture is the TappedOutReborn GitHub org.

Technology stack
Runtime: Node.js (ES modules)
HTTP framework: Express 4
Serialization: protobufjs + a large TappedOut.proto (LandMessage, CurrencyData, auth messages, telemetry, error types, etc.)
Persistence:
SQLite (users.db) for accounts, tokens, and path metadata
Filesystem for the actual town state (.pb protobuf files)
Other: compression, cookie-parser, JWT, nodemailer, Pug templates for dashboards, uuid, chalk for logging
Config: config.json (listen IP/port, data directory, DLC folder, admin key, etc.)
Request routing structure
The server mounts several route groups under src/routes/:

authRoutes – account creation, login, token issuance/refresh, Nucleus-/Mayhem-style identity mapping
mhRoutes (“Mayhem”) – core game-state endpoints (land load/save, currency, WholeLandToken)
directorRoutes – game director / configuration / event control
dashboardRoutes – admin + user web UIs
userRoutes – profile/email/username management, town import/export
proxyRoutes / trackingRoutes – telemetry, client metrics, miscellaneous original endpoints
Static /dlc mount when local DLC serving is enabled
The root index.js sets up Express, compression, SQLite schema initialization, optional local DLC static serving, and basic logging.

Data model & persistence
SQLite UserData table (key columns):

MayhemId (unique player identifier used by the game)
UserId, UserName, UserEmail
Token fields: UserAccessToken, UserAccessCode, UserRefreshToken, SessionId, SessionKey
WholeLandToken (optimistic-concurrency token)
LandSavePath, CurrencySavePath (filesystem locations of the protobuf blobs)
Game state (per player):

land.pb → LandMessage protobuf
Contains the entire town: buildings, characters, jobs, quests, inventory, terrain (roads/rivers), notifications, friend data, variables, time gates, etc.
currency.pb → CurrencyData / related currency messages
Donuts, cash, special currencies, purchase history, etc.
The WholeLandToken acts as an optimistic lock: the client must present a valid token when saving, preventing concurrent overwrite races.

Client redirection (Patch-Apk)
The original client hard-codes official server and DLC hostnames. Patch-Apk:

Takes an original APK + new game-server URL + new DLC-server URL.
Uses string replacement and native binary patching (radare2-assisted) to rewrite those URLs.
Produces a re-signed APK that talks only to the private server.
This is the functional equivalent of the localhost / adb reverse / binary-patch experiments already being performed on the Futurama APK.

Typical client–server flow
Patched client boots and contacts the private server (auth / bootstrap / director endpoints).
Server creates or looks up a MayhemId and issues access/session tokens.
Client requests a WholeLandToken.
Client loads LandMessage + currency data (or creates a new empty town).
Gameplay proceeds; periodic or action-triggered saves write updated protobufs back to disk (token-checked).
DLC/asset requests are satisfied from the local dlc/ folder (or a configured remote).
Admin dashboard can set the current event, manage users/towns, and tweak server-side configuration.
User dashboard allows account management and town import/export.
Strengths of this architecture (for a Futurama project)
Minimal surface area: only the endpoints the client actually calls need to be implemented.
Protobuf-first: matches the original serialization; once the .proto definitions and a few key messages are understood, load/save becomes straightforward.
Filesystem + SQLite split: simple, inspectable, easy to back up or migrate.
Optimistic locking via WholeLandToken: clean concurrency model without heavy locking.
DLC separation: assets are treated as a separate downloadable concern, exactly as the original live-ops model worked.
Dashboard-driven events: server can force historical or custom events without client changes.
Working multi-user design: already supports accounts, multiple towns, and concurrent players.
Limitations / differences relevant to Futurama
TSTO’s protocol and protobuf schemas are different from Worlds of Tomorrow (different engine, different studio lineage inside TinyCo/Jam City). The concrete message names and endpoint paths will not transfer 1:1.
The Reborn server still relies on a patched original client; it does not reimplement rendering or client-side logic.
Some advanced features (full friend systems, certain live-ops edge cases, perfect event parity) are still evolving or marked as planned.
teamtsto.org / Project Springfield is a parallel community effort that may use additional closed-source or differently structured components; the public architectural reference remains GameServer-Reborn.
Direct lessons for the Futurama: Worlds of Tomorrow effort
Redirect first, implement second – get the client talking to a controlled listener (via built-in localhost selector, adb reverse, or a minimal binary patch) before trying to perfect response bodies.
Identify the authoritative state blob – TSTO uses LandMessage + currency; Futurama almost certainly has an analogous bootstrap / player-init payload (possibly JSON or a different protobuf). Capturing and round-tripping that blob is the real “first visible win.”
Separate asset serving – treat any CDN / AssetBundle / DLC requests as a static-file problem once the URLs are known.
Token / checksum / authenticity gates – TSTO has WholeLandToken; Futurama has the X-TC-Digest header you are already reverse-engineering. Both are server-controlled authenticity mechanisms that can be satisfied or bypassed with small, targeted changes.
Keep the server thin – start with auth + load/save + a minimal valid town, then expand. Do not try to reimplement combat math or economy logic until the client is past the loading screen and can place a building.
In short, Tapped Out Reborn demonstrates a proven, low-complexity path: patch the client’s server URLs → speak the original wire protocol with protobuf (or the Futurama equivalent) → persist the big state blob → serve assets locally → control events from the server. That is the architecture that should inform the next stages of the Worlds of Tomorrow preservation work.




60 sources
Explore Tapped Out Reborn protobuf definitions


Worked for 20s
Tapped Out Reborn protobuf definitions

Source: the single consolidated file TappedOut.proto (~55 KB) in the GameServer-Reborn repo. It is a merged set of original TinyCo/EA protocol definitions under package Data; using syntax = "proto3";. Many fields are marked optional (proto3 style with explicit presence).

The file is organized by original source filenames (comments such as // source filename: LandData.proto). Below is a structured exploration of the important message groups.

1. Auth & identity (AuthData.proto)
Message	Purpose
UserIndirectData	userId, telemetryId
AnonymousUserData	Simple anonymous flag
TokenData	sessionKey + expirationDate
UsersResponseMessage	Returns user + token on bootstrap
LinkData / LinkUserResponseMessage	Links TNT_ID ↔ NUCLEUS_TOKEN identities
DeleteUserResponseMessage	Account deletion
These support the Nucleus / Mayhem identity model the original client expects.

2. Error handling (Error.proto)
ErrorMessage is the common error envelope used almost everywhere:

Code enum (HTTP-style: 400, 401, 404, 409, 500, 501, 503…)
Type enum (AUTHENTICATION_ERROR, NO_SUCH_RESOURCE, MISSING_VALUE, LOCK_REQUEST_FAILED_DUE_TO_TIMEOUT, PROTOCOL_MISMATCH, DATABASE_ERROR, SHARD_UNDER_MAINTENANCE, etc.)
Severity (DEBUG → FATAL)
Optional field and free-text message
Most response wrappers contain an optional ErrorMessage error field.

3. Core game-state response wrappers (CustomerServiceData.proto)
Message	Contains
LandResponseMessage	LandMessage land + PlayerSession + error
CurrencyResponseMessage	CurrencyData + error
WholeLandTokenResponseMessage	Token response + error
LandBackupResponseMessage	List of dated LandMessage backups
UserResponseMessage	Game ID + reverse identity mappings
These are the primary HTTP response bodies the server returns for land/currency operations.

4. The heart of the protocol: LandMessage (LandData.proto)
This is the single most important message. A full town is one LandMessage serialized to a .pb file.

Top-level fields (selected):

message LandMessage {
  optional string id = 1;                          // usually the MayhemId
  optional FriendData friendData = 2;
  optional UserData userData = 3;
  optional InnerLandData innerLandData = 4;
  optional TerrainData roadsData = 5;
  optional TerrainData riversData = 6;
  repeated BuildingData buildingData = 7;
  repeated CharacterData characterData = 8;
  repeated ConsumableData consumableData = 9;
  repeated JobData jobData = 10;
  repeated QuestData questData = 11;
  repeated NotificationData notificationData = 12;
  repeated InventoryItemData inventoryItemData = 13;
  // ... many more (memorabilia, premium unlocks, events,
  //    action limits, skins, delayed actions, spendables,
  //    special events, sub-lands, minigames, friend lists,
  //    timers, DNA, group storage, etc.)
}
Key nested messages:

UserData – level, experience, money, tutorial flags, prestige, power-ups, subscriptions, stickers, preferences.
InnerLandData – land block dimensions/position, next instance IDs, entity counts, play-time statistics, creation time, version list.
TerrainData – encoded map data + TerrainType enum (PAVEMENT, ROADS, RIVERS, OCEAN, DIRT, COBBLESTONE, SAND, special event roads, etc.).
BuildingData – building ID, position (x/y), flip state, build state, hurry flag, vandalism info, skin, sub-land ID, timestamps, flags.
CharacterData – character ID, position, skin, path cache, sub-land, flags.
JobData – job ID, character/building references, state, hurry, grid position, sub-land.
QuestData – quest ID/state, objectives (with custom data for buildings, resources, item counts, friend visits, etc.).
FriendData – level, name, rating, spendables, sub-land info, last played time (used both for the owner and for friends).
Supporting types include VariableSet, SharedVariableSet, TimeGateSet, AdvancedVariableSet, ObjectVariables, SpendableElement, OwnerList, CurrencySaveData, timed-attack data, etc.

5. Currency & purchases (PurchaseData.proto)
CurrencyData – the main currency blob (donuts/premium, cash, special currencies, purchase history).
CurrencySaveData – simpler money/premium/special counters.
PurchasedItemData, PurchaseRequestMessage, PurchaseResponseMessage, OrderData, SubscriptionData, PurchaseErrorData.
Currency is often stored separately from the land (as currency.pb) even though some money fields also appear inside UserData.

6. Concurrency control (WholeLandTokenData.proto)
message WholeLandTokenRequest { ... }
message WholeLandTokenResponse { ... }
message DeleteTokenRequest / DeleteTokenResponse
The WholeLandToken is an optimistic-locking token. The client must present a valid token when saving the land; the server issues a new one on successful updates. This prevents two clients (or a race) from overwriting each other.

7. Configuration & live-ops
GameplayConfigResponse – simple list of NameValue pairs (server-driven gameplay knobs).
ClientConfigResponse – client configuration items.
EventMessage / EventsMessage – event state.
Various special-event, daily-task, and minigame structures inside LandMessage.
8. Telemetry, friends, friends, matchmaking
Rich client telemetry (ClientTelemetryMessage) including FPS, memory, DLC download stats, session GUIDs.
Friend data request/response.
Offers, matchmaking, and gamble response messages.
How the server uses these definitions
In GameServer-Reborn (and similar servers such as the Rust tsto_server):

On land load → deserialize land.pb → LandMessage.
On land save → validate WholeLandToken → write updated LandMessage.
Currency is loaded/saved independently as CurrencyData.
Auth endpoints return the smaller auth/token messages.
Most other endpoints are thin wrappers that return one of the *ResponseMessage types containing either the payload or an ErrorMessage.
Relevance to Futurama: Worlds of Tomorrow
TSTO’s design is server-authoritative state in a single large protobuf blob (LandMessage) plus a separate currency blob and a concurrency token.
Futurama almost certainly follows the same high-level pattern (one or a few large bootstrap/state payloads, authenticity headers such as the X-TC-Digest you are already reverse-engineering, and downloadable content packs).
The concrete field names, IDs, and nesting will be different, but the archaeology method transfers directly:
Recover or reconstruct the .proto (or equivalent JSON schema).
Capture a real (or minimal valid) state blob.
Round-trip it through a controlled server.
Satisfy any token/checksum/authenticity gate.
The TappedOut.proto file is therefore an excellent reference for “what a complete TinyCo-era city-builder state message looks like,” even though the exact schema cannot be reused for Futurama.

Would you like a deeper dive into any specific nested message (e.g. full QuestData / BuildingData / currency fields), or a comparison of how these messages are actually loaded and saved in the Node.js server code?




10 sources
Explore QuestData structure


Worked for 13s
QuestData structure (from Tapped Out Reborn TappedOut.proto)

QuestData is a nested message inside LandMessage. Every active or completed quest the player has touched is stored as one entry in the repeated field:

repeated .Data.LandMessage.QuestData questData = 11;
Full definition
message QuestData {
  optional .Data.LandMessage.EntityHeader header = 1;  // just { optional uint32 id = 1; }
  optional uint32 questID = 2;
  optional int32  questState = 3;
  optional int32  questScriptState = 4;
  optional int32  numObjectives = 5;
  repeated .Data.LandMessage.QuestData.ObjectiveData objectiveData = 6;
  optional int32  timesCompleted = 7;

  message ObjectiveData {
    optional int32  objectiveID = 1;
    optional int32  objectiveState = 2;
    optional int32  objectiveType = 3;
    optional int32  version = 4;
    optional bool   questLastRetVal = 5;
    optional bool   questLocal = 6;
    optional bool   rushed = 7;
    optional bool   keepDone = 8;
    optional bool   blockDoneScript = 9;

    // Type-specific payload (only one is typically populated)
    optional BuildingCustomData   buildingCustomData   = 10;
    optional ResourcesCustomData  resourcesCustomData  = 11;
    optional ItemCountCustomData  itemCountCustomData  = 12;
    optional VisitFriendCustomData visitFriendCustomData = 13;
    optional DynamicData          dynamicData          = 14;

    message BuildingCustomData {
      optional int32 qty = 1;          // e.g. “own 3 of building X”
    }
    message ResourcesCustomData {
      optional uint32 money = 1;
      optional uint32 premium = 2;     // cash / donuts required or collected
    }
    message ItemCountCustomData {
      optional int32 count = 1;        // generic counter
    }
    message VisitFriendCustomData {
      optional int32  num = 1;
      optional bool   fakeIncluded = 2;
      repeated string friend = 3;      // friend IDs that have been visited
    }
    message DynamicData {
      optional int32 value = 1;        // catch-all integer
    }
  }
}
Field-by-field meaning
Field	Type	Role
header	EntityHeader	Internal instance ID used by the land’s entity system
questID	uint32	Canonical quest identifier (matches game data tables)
questState	int32	High-level progress (not started / active / completed / failed / etc. – exact enum is client-side)
questScriptState	int32	Finer-grained script / dialogue step inside the quest
numObjectives	int32	How many objectives belong to this quest
objectiveData	repeated	The actual checklist of objectives
timesCompleted	int32	For repeatable / daily quests
ObjectiveData
Each objective is a small state machine:

Identity: objectiveID, objectiveType, version
Progress flags:
objectiveState – current status of this objective
questLastRetVal – last return value from the quest script
questLocal – whether the objective is considered local
rushed – player spent premium currency to skip
keepDone – keep the “done” flag even after reset
blockDoneScript – prevent the completion script from running again
Type-specific payload (only the relevant one is filled):
Building ownership / construction count
Resource (money / donuts) targets
Generic item counters
Friend-visit tracking (including a list of friend IDs and a “fake friend” flag)
Simple dynamic integer
This design lets the same ObjectiveData structure represent very different quest requirements without a huge union of every possible objective type.

Related: QuestGroupData
Quests can also be grouped (story arcs, daily sets, event chains):

message QuestGroupData {
  optional EntityHeader header = 1;
  optional uint32 questGroupID = 2;
  optional int32  questGroupState = 3;
  optional int32  currentChild = 4;
  optional int32  lastChild = 5;
  optional int32  numChildren = 6;
  optional int32  childIDListLen = 7;
  optional int32  weightListLen = 8;
  optional string childIDList = 9;     // serialized list of child quest IDs
  optional string weightList = 10;    // weights for random selection
  optional uint32 numCompleteDaily = 11;
  optional int64  dailyCompletionTime = 12;
}
LandMessage stores these as:

repeated .Data.LandMessage.QuestGroupData questGroupData = 29;
Daily tasks also reference questID inside DailyTaskMessage.DailyTaskData.

How the private server treats it
The entire LandMessage (including every QuestData and QuestGroupData) is loaded from / saved to a single land.pb file.
The server does not interpret quest logic; it just persists whatever the client sends.
When a player progresses a quest, the client updates the relevant QuestData / ObjectiveData fields and pushes the whole land (protected by the WholeLandToken).
Creating a new town usually starts with an empty or template questData list; the client populates it as the player advances.
Relevance to Futurama preservation
Futurama: Worlds of Tomorrow almost certainly stores quest / mission / job progress in an analogous structure (either inside a large bootstrap JSON/protobuf or as separate timed-job records). The TSTO QuestData pattern shows the classic TinyCo approach:

One record per quest instance.
Nested objectives with type-specific payloads.
Simple integer state machines rather than complex server-side scripting.
Everything embedded in the big player-state blob that is round-tripped on load/save.
When you eventually capture a Futurama player-init or job-related payload, looking for repeated structures that contain an ID + state + a list of sub-objectives will be a strong signal that you have found the equivalent of QuestData.

Analyze QuestGroupData structure


Worked for 2s
QuestGroupData structure (from Tapped Out Reborn TappedOut.proto)

QuestGroupData is a nested message inside LandMessage. It groups related quests into arcs, daily sets, or weighted pools and is stored as:

repeated .Data.LandMessage.QuestGroupData questGroupData = 29;
(InnerLandData also tracks numQuestGroups so the client knows how many groups exist.)

Full definition
message QuestGroupData {
  optional .Data.LandMessage.EntityHeader header = 1;  // { optional uint32 id = 1; }
  optional uint32 questGroupID = 2;
  optional int32  questGroupState = 3;
  optional int32  currentChild = 4;
  optional int32  lastChild = 5;
  optional int32  numChildren = 6;
  optional int32  childIDListLen = 7;
  optional int32  weightListLen = 8;
  optional string childIDList = 9;      // serialized list of child quest IDs
  optional string weightList = 10;     // parallel weights for selection
  optional uint32 numCompleteDaily = 11;
  optional int64  dailyCompletionTime = 12;
}
Field-by-field meaning
Field	Type	Role
header	EntityHeader	Internal instance ID used by the land’s entity system
questGroupID	uint32	Canonical ID of this quest group (matches game data tables)
questGroupState	int32	High-level state of the whole group (inactive / active / completed / locked / etc.)
currentChild	int32	Index or ID of the quest the player is currently on inside the group
lastChild	int32	Index or ID of the most recently completed / visited child
numChildren	int32	How many child quests belong to this group
childIDListLen	int32	Length metadata for the serialized child list
weightListLen	int32	Length metadata for the serialized weight list
childIDList	string	Serialized list of child questIDs (exact encoding is client-side; often a packed or delimited string)
weightList	string	Parallel list of weights used for random or weighted selection of the next child
numCompleteDaily	uint32	How many times this group (or its daily subset) has been completed today
dailyCompletionTime	int64	Timestamp of the last daily completion (used for daily reset logic)
How it relates to QuestData
Individual quests live in the repeated questData field (QuestData messages).
Groups live in the separate repeated questGroupData field.
A group does not embed full QuestData objects. It only stores:
references (via childIDList) to the questIDs of its members, and
lightweight progression state (currentChild, lastChild, daily counters).
The actual per-quest progress (objectives, questState, timesCompleted, etc.) remains in the corresponding QuestData entries.
This keeps the group record small while still allowing the client to know which quests belong together and which one is active.

Typical usage patterns
Linear story arcs
childIDList holds an ordered sequence. currentChild / lastChild track position in the chain.
Weighted / random pools
weightList supplies selection weights so the client (or server-driven config) can pick the next quest non-uniformly.
Daily / repeatable sets
numCompleteDaily + dailyCompletionTime implement the classic “reset at midnight / after 24 h” logic without needing a separate daily-quest table.
Event quest lines
Temporary event groups can be added or removed from the questGroupData list when an event starts or ends; the underlying QuestData records can stay or be cleaned up independently.
Interaction with other land structures
InnerLandData.numQuestGroups – quick count of how many groups exist.
DailyTaskMessage – separate daily-task system that also references questIDs; some daily content may be represented either as a QuestGroupData or as entries inside DailyTaskMessage.
Event and special-event data elsewhere in LandMessage can enable or disable entire groups by ID.
Server-side treatment (GameServer-Reborn style)
Exactly like QuestData:

The private server treats QuestGroupData as opaque state.
On land load it deserializes whatever is in the land.pb.
On land save it writes the client-supplied list back (protected by the WholeLandToken).
No quest-group logic is evaluated server-side; progression is entirely client-driven and then persisted.
Relevance to Futurama: Worlds of Tomorrow
Futurama’s event and story structure (district unlocks, limited-time events, prize ladders, character job chains) very likely used a similar grouping concept—even if the on-the-wire format is JSON or a different protobuf. When examining Futurama bootstrap or save payloads, look for:

A list of group/arc IDs,
Current/last child indices,
Serialized child lists or parallel weight lists,
Daily completion counters + timestamps,
as strong signals that you have found the equivalent of QuestGroupData.

look at how we tranlate the simpsons work to the futurama project we ant to revive it


Worked for 3s
Translating Tapped Out Reborn → Futurama: Worlds of Tomorrow

The goal is the same: keep a discontinued TinyCo/Jam City freemium city-builder playable by pointing the original client at software we control. The architecture pattern transfers cleanly; the concrete protocol details do not. Below is a practical mapping of what we learned from TSTO Reborn onto the Futurama project, ranked by how directly it applies.

1. Core pattern that transfers 1:1
TSTO Reborn practice	Futurama equivalent	Why it matters
Patch client URLs (or use built-in selector) so traffic hits our server	Use the APK’s built-in Server Configuration (Localhost → http://127.0.0.1:8302/tapservice/) + adb reverse, or a minimal binary patch	First visible win: client does something because of code we control
Persist one big authoritative state blob (LandMessage in land.pb)	Identify and round-trip the bootstrap / player-init payload (whatever the native client expects after the digest check)	Once this loads and saves, the city can appear and progress can stick
Separate currency blob + optimistic concurrency token (WholeLandToken)	Expect a parallel currency/wallet structure + the X-TC-Digest authenticity header you are already reverse-engineering	Don’t mix concerns; satisfy the gate before inventing game logic
Serve DLC/assets locally	Intercept any CDN / AssetBundle / static requests and host recovered packs	Prevents secondary crashes after the main handshake succeeds
Thin server that mostly stores what the client sends	Same philosophy for WOTServer: start with auth + load/save + minimal valid town, add logic later	Avoids rewriting combat/economy math until the client is past the loading screen
Admin/user dashboards for events and town import/export	Later convenience layer; not required for the first playable state	Nice-to-have once the core loop works
2. What does not transfer directly
Protobuf schemas – TSTO’s LandMessage, QuestData, QuestGroupData, CurrencyData, etc. are specific to Tapped Out. Futurama uses a different engine (Marmalade/S3E/C++ native, not the same Unity/IL2CPP stack the old research assumed) and almost certainly different message layouts (possibly JSON for some paths, or its own binary/protobuf-like format).
Endpoint paths – TSTO uses /mh/..., Mayhem IDs, Nucleus tokens. Futurama evidence points at /tapservice/api/, process_queue.php, and the localhost base already discovered. The research document’s /api/auth/login etc. remain unverified hypotheses.
Quest/event model details – The nested QuestData + QuestGroupData pattern (ID + state + typed objectives + daily counters) is a design idea, not a drop-in schema. Futurama’s jobs, space missions, and prize-ladder events will have their own fields.
Auth flavor – TSTO is Nucleus/Mayhem-heavy. Futurama’s token/digest scheme is the X-TC-Digest: prefix?key=value#digest grammar you are currently mapping.
3. Concrete translation of the TSTO success path into Futurama experiments
Phase 0 – Redirection (already in progress)

TSTO: Patch-Apk rewrites server + DLC hosts.
Futurama: Prefer the built-in Localhost / Other Service URL menu + adb reverse tcp:8302. Fall back to a one-instruction or string patch only if needed.
Success criterion: probe server sees a real POST from the original client.
Phase 1 – Authenticity gate

TSTO: Issue and check WholeLandToken.
Futurama: Satisfy or surgically bypass the native X-TC-Digest verifier (correct delimiter order prefix?data#digest, then the comparison).
Success criterion: client accepts an HTTP 200 and advances past the pure “missing checksum / bad data” failures.
Phase 2 – Bootstrap / state blob

TSTO: Return a valid (even empty/template) LandMessage.
Futurama: Capture or synthesize the minimal payload that lets the client leave the loading screen and instantiate the Planet Express district (Fry + Professor + starting building is the classic “first visible win”).
Do not invent fields. Log everything the client sends and every native error string after the digest is accepted.
Phase 3 – Persistence

TSTO: Write land.pb + currency.pb on save, re-issue token.
Futurama: Store whatever the client posts back; return it on next load. Add the smallest possible concurrency or version field only if the client demands it.
Phase 4 – Assets & live-ops

TSTO: Local dlc/ folder + dashboard-driven events.
Futurama: Host any recovered AssetBundles / textures / audio; later drive historical events by server-side config the same way TSTO forces old events.
4. Recommended near-term experiments (mapped from TSTO lessons)
Highest leverage (already planned)
Keep the checksum-accept patch. Serve a response with a syntactically valid three-part X-TC-Digest and the best-shaped bootstrap body you have. Capture full logcat for the next failure after the digest gate.
→ Direct analogue of “return a minimal LandMessage and see what the client does.”
Visible proof of control
Change only one field or HTTP status in the probe server and show that the loading UI, error dialog, or spinner text changes.
→ Same psychological and technical milestone TSTO achieved when the patched client first rendered Springfield from a private server.
State-blob archaeology
Once past the digest, dump every request/response body. Look for large structured payloads that contain repeated entity-like records (IDs + positions + states). Those are the Futurama equivalents of BuildingData / CharacterData / QuestData.
→ Exactly how the TSTO community recovered the meaning of LandMessage.
5. Documentation / process habits to copy
Keep evidence and inference strictly separated (as in the existing DISCOVERIES.md / QUESTIONS.md).
Prefer one-instruction or single-string patches over large rewrites.
Treat the original client as the source of truth; the server’s job is to be a faithful enough mirror that the client proceeds.
Recover assets independently of logic.
Only after the city renders and a building can be placed should you invest in economy, combat, or event re-implementation.
Bottom line
Tapped Out Reborn proves the revival strategy works for this class of game:

Redirect original client → satisfy authenticity/token gate → round-trip the big state blob → serve assets → add persistence and events later.

Apply that exact sequence to Futurama. Re-use the process and the architecture style; do not re-use the TSTO protobuf field names or endpoint paths. The next decisive step remains the same one the TSTO projects took early: get a controlled response that the real client accepts, then let the client tell you what the state schema actually looks like.

If you want, I can turn this mapping into an updated section for PROJECT_CONTEXT.md or a short “TSTO → WOT translation” page in docs/.

what about the game that is on an ipad can we pull it, it it of use we have tyhe apk


Worked for 12s
Yes, the iPad/iOS version can be useful — but it is secondary to the Android APK you already have.

Can you pull the iOS version?
Yes, in principle:

If the game is still installed on an iPad/iPhone that previously downloaded it, you can often extract the IPA with tools such as Apple Configurator, ideviceinstaller, Frida-based extractors, or older methods (iTunes backup + decryption on older iOS, or ipatool-style flows when the Apple ID still owns the app).
Community IPA archives and old forum posts (4PDA, iOSGods, etc.) circulated versions around 1.2.x–1.6.6 historically. Availability of a clean, complete 1.6.6 IPA today is hit-or-miss; many links are dead or incomplete.
The App Store listing is long gone, so you cannot simply re-download it from Apple unless it remains linked to an old purchase on that Apple ID.
Practical reality: pulling a usable IPA is more friction than working with the Android APK you already possess, and success depends on whether you still have a device/Apple ID that owns the app.

Is the iOS version useful when you already have the Android APK?
Useful for some things, not a replacement.

Aspect	Android APK (you have 1.6.6)	iOS IPA	Value for the project
Native code / networking	libclient.so (ARM), Marmalade/S3E-style, the digest logic you are already reversing	Different binary (ARM64/ARMv7 Mach-O), different packing	Medium – can confirm whether the same URL strings, digest header format, and endpoint paths exist
Assets (textures, audio, localization, UI)	Present but packed for Android	Often cleaner or differently compressed; sometimes higher-res iPad assets	High – good for recovering missing or higher-quality assets
Protocol / server URLs	Already partially mapped (/tapservice/, localhost:8302, X-TC-Digest)	Should talk to the same backend	Medium – cross-check that the server API is shared
Easy patching & local testing	Excellent (apktool, adb, Frida, re-sign)	Harder (codesigning, sideloading, fewer mature reverse-engineering workflows on Windows)	Android wins for active experimentation
Runtime experiments	What you are doing now	Possible but slower	Android is the right primary target
Bottom line

The Android 1.6.6 APK is the correct primary artifact for protocol reverse-engineering, digest bypass, and the first visible win. That work does not need the IPA.
An IPA is still worth obtaining if you can get it reasonably easily, mainly for:
Asset recovery (sprites, audio, localization, any iPad-specific content)
Confirming that the network endpoints and digest scheme are the same
Having a second binary in case the Android native library has been heavily stripped or obfuscated in places the iOS one is clearer
Recommendation for the Futurama project
Keep pushing on the Android client + probe server + digest gate. That is the highest-leverage path (exactly the TSTO Reborn pattern).
If you still have an iPad/iPhone with the game installed, or an Apple ID that previously owned it, try to extract the IPA and archive it. Treat it as a secondary research asset, not the main development target.
Do not switch the main effort to iOS unless the Android binary turns out to be unusually hostile and the IPA is dramatically easier to read.
So: yes, pull it if the opportunity is low-cost. It is of use for assets and cross-checks. It is not required to revive the game, and it should not displace the Android archaeology you already have in motion.




20 sources
yes please werite up thi whole findings fromt he convo


Worked for 1m 28s
Full findings from this conversation are written up in:

/home/workdir/artifacts/docs/

File	What it covers
FINDINGS_SUMMARY.md	Executive overview + index
PROJECT_CONTEXT.md	Goals, principles, strategy, ownership rules
DISCOVERIES.md	Evidence-backed findings (client type, localhost selector, endpoints, X-TC-Digest grammar, WOTServer status, experiment outcomes, TSTO comparison, research corrections)
QUESTIONS.md	Ranked open questions (P0–P2)
TSTO_TRANSLATION.md	How Tapped Out Reborn maps onto the Futurama revival plan
IOS_NOTES.md	Whether/how the iPad IPA helps when you already have the APK
Short recap of the core findings
Client — Native Marmalade/S3E (libclient.so), not Unity/IL2CPP.
Redirection — Built-in Server Configuration → Localhost http://127.0.0.1:8302/tapservice/ (plus adb reverse).
Gate — X-TC-Digest: prefix?key=value#digest (order and structure matter).
WOTServer — Scaffold only; probe server used for controlled responses.
Strategy — Same as TSTO Reborn: redirect → satisfy gate → round-trip state blob → assets → persistence/events. Reuse process, not TSTO schemas.
iOS — Useful for assets/cross-checks; Android stays primary.
Next recommended experiments remain: valid three-part digest + best body, then prove visible client reaction under your control, then hunt the real state blob in the captures.

search fro more applicale work out there were to get the dlcs or seasonal or to add new charactors and buikldings


Worked for 22s
Search results: applicable work for DLCs, seasonal content, characters, and buildings

There is very little dedicated Futurama: Worlds of Tomorrow private-server or content-modding work. Almost everything useful is either (a) the one WIP server you already know, (b) community documentation/asset rips, or (c) transferable patterns from Tapped Out Reborn and related TinyCo games.

1. Futurama-specific work (thin)
Source	What it offers	Use for DLC / characters / buildings
WOTServer (BirkinSornberger)	Only public WIP emulator. Author states it is not playable. Patch libclient.so, HTTP instead of HTTPS, basic request handling.	No DLC pipeline, no content injection, no character/building add tools. Useful only as protocol starting point.
Author’s Reddit server blog	Progress notes, patching notes, call for help	Same limitation — early networking, not content.
Futurama Worlds of Tomorrow Wiki	Full catalogs of buildings, characters, costumes, events, missions, prize ladders, mystery boxes	Best design reference for what content exists (IDs, costs, event grouping). Not wire formats or downloadable packs.
The Spriters Resource – WoT	Some ripped building sprites (Planet Express, Robot Arms Apts., etc.)	Partial visual assets only; not complete DLC sets.
TCRF – Worlds of Tomorrow	Unused graphics, debug leftovers, notes that iOS/Android assets and Family Guy: The Quest for Stuff leftovers share filenames (fg_*, placeholders)	Confirms shared TinyCo pipeline; suggests FGQFS CDN/asset patterns may partially apply.
Old Discord / r/FuturamaWOTgame	Community memory, shutdown notes, occasional “assets in files” mentions (e.g. cancelled PvP event leftovers)	Anecdotal; no organized DLC archive found.
No public project currently provides: a Futurama DLC downloader, event pack server, or tools to inject new characters/buildings into a private backend.

2. Closest applicable work: Tapped Out Reborn (use as template)
This is the strongest model for “get DLCs + seasonal content + characters/buildings”:

Repo / piece	What it does	How it maps to Futurama
DLC-Downloader	Python script; pulls full DLC set (characters, buildings, quests, tiers, languages). Needs ~30 GB.	Build the same kind of tool once you discover Futurama’s CDN / asset URLs from the client or old captures.
GameplayConfig-Downloader (archived)	Pulls gameplay config as JSON via protobuf definitions	Equivalent of server-driven event/character unlock tables.
GameServer-Reborn admin dashboard	Set current event, manage towns, serve local dlc/	Same design: host recovered packs statically; drive “which event is live” from config, not client patches.
Patch-Apk	Rewrites game-server + DLC server URLs	You already have localhost / patch paths; ensure DLC base URL is redirected too when you find it.
TSTO’s approach to adding content:

Client already contains or downloads asset packs.
Server decides which content is unlocked (config + land/quest state).
New characters/buildings are mostly data + assets, not new client code.
Events are switched by server config (prize ladders, timers, currency).
That is the realistic path for Futurama once bootstrap works — not a full custom client mod.

3. Related TinyCo / sibling-game signals
Family Guy: The Quest for Stuff shares engine leftovers and filename patterns with WoT (TCRF). Historical CDN scraping and sprite rips exist in the FGQFS community (Spriters Resource, old forum dumps). Worth mining for methodology (how they found CDN hosts, pack structure), not for Futurama assets themselves.
No mature public FGQFS private server with a polished “add character” pipeline was found in this search either; the pattern still tracks back to TSTO-style work.
4. What “adding new characters and buildings” actually requires (realistic order)
Bootstrap + state blob working (city loads, buildings persist) — current priority.
Discover asset/CDN URLs the client requests (logcat / mitm / binary strings). Redirect them to a local static host (TSTO dlc/ pattern).
Recover packs — from APK assets, any surviving CDN caches, community rips (Spriters, wiki images), IPA if obtained.
Content tables — IDs, costs, unlock rules, event membership (wiki is the best public list today; wire format still unknown).
Server-side unlock / event flags — so the client treats a character or building as available without official servers.
Only then: optional tools to inject new custom IDs (harder; needs schema understanding and often client-side data the APK already embeds).
There is no shortcut project that skips steps 1–3 for Futurama.

5. Practical recommendations for this project
Priority	Action
High	Keep focusing on digest gate + bootstrap body. Content tools are useless until the client stays in the city.
High	When capturing traffic, log every URL that looks like CDN / asset / “dlc” / “pack” / “bundle”. That list is the seed for a Futurama DLC-Downloader.
Medium	Systematically archive wiki + Spriters + any APK-extracted assets into a local content tree (even if incomplete).
Medium	Study TSTO DLC-Downloader + GameServer dlc/ serving as the implementation template.
Low (for now)	Custom “add new character” tooling — after vanilla content can be served and unlocked.
Optional	Scrape/compare FGQFS CDN history and TCRF notes for shared TinyCo pack layout clues.
Bottom line
No ready-made Futurama DLC or “add characters/buildings” project exists beyond WOTServer’s early networking work and community documentation/rips.
The applicable work is Tapped Out Reborn’s DLC + config + local asset serving pipeline, plus the WoT wiki/Spriters/TCRF as content inventories.
Next concrete step that advances DLC/seasonal/character goals: once past the digest gate, treat every asset URL the client hits as a preservation target and stand up a local static mirror the same way TSTO serves dlc/.
I can add a short “Content & DLC sources” section to docs/DISCOVERIES.md or QUESTIONS.md if you want that captured in the project docs.




60 sources
Study Tapped Out Reborn DLC downloader


Worked for 34s
Study: Tapped Out Reborn DLC-Downloader

Repo: TappedOutReborn/DLC-Downloader

Main script: downloadDlcs.py (~183 lines)

Deps: requests, colorama

Purpose
Download the full set of Tapped Out DLC asset packs (characters, buildings, quests, audio, resolution tiers, languages) from EA’s still-reachable CDN so a private server can host them under a local dlc/ directory. GameServer-Reborn serves that folder statically; the patched client loads assets from the private host instead of EA.

How the CDN is structured
Everything hangs off one base:

http://oct2018-4-35-0-uam5h44a.tstodlc.eamobile.com/netstorage/gameasset/direct/simpsons/
Flow:

Master index (zipped XML)
…/dlc/DLCIndex.zip
→ unzip → XML listing secondary index files.
Secondary indexes (also zipped XML)
Paths taken from <IndexFile index="…"> (colons rewritten to /).
Each index describes many Package entries.
Individual packages
Each package has metadata and a download path. The script queues and fetches those files.
Path style uses colon-separated logical names that are turned into directory + filename on disk (e.g. something:file.ext → folder something, file file.ext).

Configuration (top of script)
OUT_DIR = "./dlc"

LANGUAGE = ["all", "en"]   # en, fr, it, de, es, ko, zh, cn, pt, ru, tc, da, sv, no, nl, tr, th
TIER = ["all", "25", "50", "100", "retina", "iphone", "ipad", "ipad3", "mp3", "caf", "wav"]

ALL_LANGUAGES = True
ALL_TIERS = True
LANGUAGE – localization of text/audio packs.
TIER – resolution / device / audio format variants (25/50/100 quality, retina, iPhone/iPad, mp3/caf/wav).
Flags force “download everything” when true (~30 GB).
Code structure
Piece	Role
log()	Colorama info / warn / error
downloadFile(url, filename)	GET → write under OUT_DIR; skip non-200; return bytes
getDLCIndexXml(url, filename)	Download zip, open first entry in memory, return XML bytes
getDLCIndexes()	Fetch master DLCIndex.zip, parse <IndexFile index="…">, return list of secondary index paths
DLCIndexParser	Streaming XMLParser target: on each Package, collect tier/language/filename/etc., filter by config, append to DOWNLOAD_QUEUE as [url, filename, folder]
Main	Get indexes → parse each secondary index into queue → download unique URLs into OUT_DIR/<folder>/<filename>
Key design choices:

Index-driven, not hardcoded file lists — new packs appear when EA’s index is updated (as long as the CDN host stays up).
Streaming XML parse — avoids loading huge indexes as full DOM trees beyond the small master list.
Dedup via DOWNLOADED list so the same URL is not fetched twice across indexes.
No auth / no digest — public HTTP CDN; simple GET is enough.
No integrity checks after download — CRC/signature fields exist in the XML (IndexFileCRC, IndexFileSig) but the script does not verify them.
Package metadata captured from XML
Per <Package> the parser records (when present):

tier
LocalDir / FileName
FileSize / UncompressedFileSize
IndexFileCRC / IndexFileSig
Version
Language
Only tier + language are used for filtering; the rest is available if you want to extend the tool (size reporting, verification, versioning).

Output layout
./dlc/
  dlc/                    # master + secondary index zips (kept for reference)
  <LocalDir or path segment>/
    <package files>
  ...
GameServer-Reborn expects a dlc folder next to the server and serves it so the patched client’s DLC base URL resolves locally.

Operational notes
Runtime: long (many small/medium files; full set ~30 GB).
Failure mode: non-200 → log and skip (no retries).
No parallelism — sequential requests.get.
Hard dependency on the specific CDN host string remaining online; if EA retires that hostname, the tool breaks until a mirror or archived index+blobs exist.
Lessons for Futurama: Worlds of Tomorrow
TSTO DLC-Downloader idea	Futurama application
Single public CDN base + master index zip/XML	Find Futurama’s asset host(s) and any manifest/index (from libclient.so strings, logcat, or old captures)
Secondary indexes → package list	Same pattern if WoT uses multi-level manifests; otherwise a flat URL list from client requests
Language + tier filters	Map to WoT’s resolution / locale / platform variants if they exist
Local tree under dlc/ served by private server	Static file server (or WOTServer extension) that answers the same paths the client requests
No client change beyond URL redirect	Patch or override only the DLC/CDN base; keep pack formats the client already understands
Index-driven updates	Prefer discovering official indexes over hardcoding every character/building file
What you still need for a Futurama equivalent

CDN / asset base URL(s) the 1.6.6 client actually hits.
Whether there is a master index (zip, XML, JSON, custom) or only direct URLs.
Pack naming and directory conventions.
Optional: language/tier dimensions.
Until those are known, the TSTO script is a template, not a drop-in. Practical next step on the Futurama side remains: after the digest/bootstrap gate, log every non-API asset URL and treat that list as the seed for a download_wot_assets.py styled after this tool.

Minimal mental model (copyable)
1. GET master index (zipped XML)
2. For each secondary index:
     GET index zip → parse Package entries → queue URL + local path
3. For each unique URL:
     GET → write under OUT_DIR mirroring CDN path
4. Point private server DLC root at OUT_DIR
5. Client DLC base URL → private server
That five-step pipeline is what made Tapped Out Reborn’s asset story workable; the same shape is the right target for Worlds of Tomorrow once the CDN surface is mapped.

Explore GameServer-Reborn Architecture


Worked for 43s
GameServer-Reborn architecture

Private multi-user server for The Simpsons: Tapped Out. Node.js + Express, SQLite for accounts, filesystem for town/currency blobs, protobuf for most game payloads, static local DLC serving.

High-level shape
Patched client
    │  (game server + DLC URLs rewritten)
    ▼
Express (src/index.js)
    ├── Auth          /connect, /probe
    ├── Mayhem (mh)   /mh/games, /mh/users, /mh/gameplayconfig, …
    ├── Director      /director/api
    ├── User API      /user/api
    ├── Proxy         /proxy/identity (and //proxy/…)
    ├── Tracking      /tracking/api
    ├── Dashboards    /dashboard, /userdash
    └── Static DLC    /dlc  →  ./dlc
              │
              ▼
     SQLite users.db  +  data/<user>/land.pb, currency.pb
     configs/*.json   +  TappedOut.proto
Philosophy: thin server. Persist what the client sends; do not reimplement Springfield simulation. Unlock/events come from config + tokens, not heavy game logic.

Stack
Piece	Choice
Runtime	Node.js, ES modules ("type": "module")
HTTP	Express 4
Compression	compression (always on, level 6)
DB	sqlite3 → data/users.db
Wire format	protobufjs + root TappedOut.proto
Auth helpers	jsonwebtoken, custom token generator
UI	Pug views for admin/user dashboards
Other	uuid, cookie-parser, express-fileupload, optional SMTP (nodemailer)
Entry: npm start → node src/index.js.

Boot sequence (src/index.js)
Load config.json (+ env overrides for port/IP).
Open/create SQLite DB; ensure UserData table exists.
Auto-generate adminKey if missing; write back to config.json.
Reset latest.log.
Express: disable x-powered-by / etag, set Pug views.
Request logging middleware (skips pure 404 unless verbose).
Global compression.
Mount route tree from src/routes/routes.js.
If serveDlcsLocally: app.use("/dlc", express.static(localDlcFolder)).
Root Hello, World!, 404/500 handlers.
Listen; set global.running = true, global.lobbyTime = 0.
Configuration (config.json)
Key	Role
ip / listenPort	Bind address (client must use a reachable IP/host, not 127.0.0.1 in the patched APK for real devices)
dataDirectory	Root for users.db and per-user save paths
startingDonuts / startingUID / startingMID	Defaults for new accounts
adminKey	Dashboard auth (auto-filled)
serveDlcsLocally / localDlcFolder	Static DLC (./dlc)
SMTP / TSTO_API flags	Optional email and external helpers
Route map (src/routes/routes.js)
Mount	Controllers	Purpose
/mh	games, gameplayconfig, users, userstats, link, clienttelemetry	Core Mayhem game API
/director/api	platform	Director / platform bootstrap
/user/api	platform	User platform calls
/ (auth)	probe, connect	Nucleus-style auth
/proxy, //proxy	identity	Geo/age/identity proxy quirks
/tracking/api	api	Telemetry sink
/dashboard	admin UI	Events, users, towns, server status
/userdash	user UI	Register/login, town import/export
serverStatusMiddleware: if global.running is false, everything except /dashboard returns 503 (admin can bring the server back).

Data model
SQLite UserData (one row per account):

Identity: MayhemId, UserId, UserName, UserEmail
Auth: UserCred, UserAccessToken, UserAccessCode, UserRefreshToken, SessionId, SessionKey
Concurrency: WholeLandToken
Saves: LandSavePath, CurrencySavePath (filesystem paths)
Filesystem blobs (under data/):

land.pb — full LandMessage (buildings, characters, quests, …)
currency.pb — CurrencyData
Server mostly stores and returns these; it does not interpret quest graphs or combat.

Critical flows
1. Auth (authRoutes/connect)

Anonymous: authenticator_login_type=mobile_anonymous → new UID/MID, access token/code.
Email: create with ?email=… or login via signed sig (optional SMTP cred check).
Tokens minted with a small custom generator; some paths use JWT.
Responses shaped for EA/Nucleus-style code / lnglv_token query modes.
2. WholeLandToken (optimistic lock)

POST …/protoWholeLandToken/:mayhemId — issue new UUID token (optional force).
GET …/checkToken/… — validate current token.
Land load/save requires matching token; prevents two devices clobbering the same town.
3. Land / currency (games controller)

Protobuf request/response (application/x-protobuf).
Load: read land.pb / currency.pb for user → encode LandMessage / currency messages.
Save: decode body → write files → refresh token as needed.
Lobby time: simple XML epoch (/lobby/time), overridable via global.lobbyTime for event timing.
4. Gameplay / client config

GameplayConfig and ClientConfig loaded from configs/*.json, encoded with types from TappedOut.proto, returned as protobuf.
Admin dashboard can change “current event” and related knobs without code deploys.
5. DLC

Not generated by the server.
Operator runs DLC-Downloader → drops packs into ./dlc.
Express serves /dlc statically.
Patched client’s DLC base URL points at this host.
Protobuf role
Single schema file: TappedOut.proto (package Data).
Controllers protobuf.load → lookupType → create / encode / decode.
Important types: LandMessage, CurrencyData, WholeLandTokenResponse, GameplayConfigResponse, ClientConfigResponse, ErrorMessage, quest/building/character nested messages.
JSON under configs/ is a convenient edit surface; the wire format stays protobuf.

Dashboards
Path	Audience	Capabilities
/dashboard	Admin (adminKey)	Server on/off, current event, user/town management
/userdash	Players	Account, town import/export; friends planned
Implemented with Pug templates under src/views.

Design principles (why it works)
Client is authoritative for simulation — server is storage + auth + config + assets.
One big state blob — LandMessage round-trip is the core loop.
Token for concurrency — WholeLandToken instead of complex locking.
Config-driven live-ops — events and gameplay knobs in JSON/protobuf configs.
Assets out of band — DLC tree separate from Node process; only URL redirect + static files.
Multi-user from day one — SQLite accounts + per-user paths, not single-save hacks.
Mapping to Futurama (WOTServer direction)
GameServer-Reborn	Futurama analogue
Express route groups (/mh, auth, director)	/tapservice/ (and whatever real first paths logcat shows)
WholeLandToken + land/currency files	Satisfy X-TC-Digest, then persist bootstrap/save blob(s)
TappedOut.proto + configs/*.json	Unknown schema; capture bodies first, define types later
SQLite UserData	Lightweight account table once multi-user matters
/dlc static	Local mirror of WoT CDN/asset URLs once discovered
Admin event switch	Server-side event flags after city loads
Patch-Apk URL rewrite	Localhost selector and/or minimal native string/URL patch
Keep the same layering: auth gate → state load/save → static assets → config/events → dashboards. Do not port TSTO path names or protobuf field IDs; port the architecture.

Practical takeaway
GameServer-Reborn is a reference architecture, not a template to copy-paste:

Thin Node server
Account DB + filesystem state
Protobuf (or whatever WoT uses) for the big blob
Optimistic token
Local DLC
Small admin surface for events
For Worlds of Tomorrow, implement the same layers against the real /tapservice/ and digest behavior you are already reversing.

Add to chat



Native Digest Header Verification - Grok