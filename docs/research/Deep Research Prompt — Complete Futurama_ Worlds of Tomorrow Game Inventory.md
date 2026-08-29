# Deep Research: Reconstruct the Complete Futurama: Worlds of Tomorrow Game

## Mission

Conduct an exhaustive digital-preservation investigation of **Futurama: Worlds of Tomorrow**, the discontinued mobile game developed by TinyCo/Jam City and based on the Futurama television universe.

The objective is to reconstruct, as completely as practical, the game's:

- characters  
- costumes/outfits  
- buildings  
- businesses  
- decorations  
- districts  
- maps  
- environments  
- planets  
- space locations  
- enemies  
- NPCs  
- vehicles  
- spacecraft  
- objects  
- inventory items  
- crafting materials  
- currencies  
- consumables  
- resources  
- quests  
- quest chains  
- character jobs/tasks  
- dialogue/story content  
- events  
- limited-time content  
- levels  
- unlock requirements  
- progression systems  
- combat systems  
- space missions  
- game mechanics  
- UI systems  
- asset identifiers  
- downloadable content  
- server-controlled configuration  
- historically released content  
- unreleased/cut content where evidence exists

This is **not a review, retrospective, walkthrough, or list of popular content**.

Treat the game as an archaeological dataset that needs to be reconstructed after its official servers were shut down.

The ultimate purpose is **software preservation and research toward restoring lawful personal/local gameplay using a replacement backend or otherwise reconstructing lost game behavior**.

Completeness matters substantially more than narrative prose.

---

# Primary Research Question

Answer:

> What exactly existed inside Futurama: Worlds of Tomorrow, how was it organized, how did its systems relate to one another, and how much of that information can still be recovered today?

The desired end state is a structured world/game model sufficiently detailed that another technical team could use it alongside preserved client software to understand what needs to be restored.

---

# Core Research Principle

Do not ask:

> “What were the main characters and buildings in Worlds of Tomorrow?”

Instead ask:

> “What distinct entities, content records, systems, interactions, unlocks, visual assets, quests, events, items and configuration values can still be identified from any surviving source?”

Obscure content matters.

A decoration available for one event matters.

A costume with one quest chain matters.

A currency used for three weeks matters.

A background structure matters.

An enemy encountered once matters.

A character task lasting 60 minutes matters.

A deprecated asset identifier matters.

A server response schema matters.

Do not optimize for readability by omitting long-tail content.

---

# Research Period

Research the entire operational history of Futurama: Worlds of Tomorrow from launch through shutdown.

Establish and verify:

- announcement date  
- beta/soft-launch history if applicable  
- worldwide release  
- major versions  
- major events  
- major gameplay additions  
- content removals  
- end-of-development period  
- delisting  
- server shutdown  
- post-shutdown preservation efforts

Create a timeline.

---

# CATEGORY 1 — ALL CHARACTERS

Build as close to a complete character roster as possible.

Include:

- playable characters  
- NPCs  
- temporary characters  
- event characters  
- villains  
- enemies  
- bosses  
- alternate versions  
- historical characters  
- robots  
- aliens  
- creatures  
- mutants  
- game-original characters  
- background entities when game-relevant  
- characters announced but potentially unreleased

For every character capture:

| Field | Description |
| :---- | :---- |
| character\_id | Stable research ID |
| game\_name | Displayed game name |
| canonical\_name | Futurama canonical identity |
| internal\_name | Internal/client identifier if recoverable |
| entity\_type | Human, alien, robot, creature, etc. |
| playable | Yes/No |
| rarity\_or\_class | If applicable |
| unlock\_method | How acquired |
| unlock\_level | Player level if applicable |
| event | Associated event |
| building\_requirement | Required structure |
| quest\_requirement | Required quest |
| costume\_requirements | Associated costumes |
| character\_jobs | Tasks/jobs available |
| combat\_role | If applicable |
| space\_role | If applicable |
| skills | Combat/gameplay abilities |
| visual\_description | Game-specific model/design |
| first\_available | Date/version/event |
| availability | Permanent/limited/etc. |
| status\_at\_shutdown | Available/unavailable/unknown |
| source | Evidence |
| confidence | Confirmed/Probable/Uncertain |

Do not assume television characters and game characters have identical representations.

---

# CATEGORY 2 — COSTUMES / OUTFITS / CHARACTER VARIANTS

Treat costumes as separate entities whenever the game did.

Catalog:

- alternate outfits  
- profession variants  
- event costumes  
- holiday costumes  
- historical variants  
- alternate universe versions  
- combat variants  
- special skins

Capture:

| Field |
| :---- |
| costume\_id |
| costume\_name |
| base\_character |
| internal\_identifier |
| unlock\_method |
| required\_items |
| quest\_chain |
| special\_jobs |
| combat\_effect |
| event |
| first\_available |
| visual\_description |
| source |
| confidence |

Determine whether each was:

- cosmetic only  
- mechanically distinct  
- quest-gated  
- combat-relevant  
- story-relevant

---

# CATEGORY 3 — BUILDINGS

Build a comprehensive database of every placeable or game-relevant building.

Include:

- character residences  
- businesses  
- landmarks  
- institutional buildings  
- production buildings  
- event buildings  
- quest buildings  
- premium buildings  
- temporary buildings  
- upgradeable structures  
- background/non-placeable buildings when identifiable

Capture:

| Field |
| :---- |
| building\_id |
| name |
| internal\_identifier |
| category |
| district |
| canonical\_location |
| footprint |
| purchase\_cost |
| currency |
| build\_time |
| unlock\_level |
| unlock\_quest |
| unlock\_character |
| associated\_characters |
| jobs |
| resource\_output |
| payout |
| XP |
| cooldown |
| event |
| premium |
| limited\_time |
| upgrade\_levels |
| visual\_states |
| first\_available |
| source |
| confidence |

Search specifically for structures no longer documented on current wiki pages.

---

# CATEGORY 4 — DECORATIONS AND PLACEABLE OBJECTS

Inventory every known:

- decoration  
- statue  
- tree  
- sign  
- prop  
- street object  
- event decoration  
- scenery object  
- animated decoration  
- premium decoration  
- landscape element  
- special structure

Capture cost, footprint, event association, availability and screenshots where possible.

Do not discard objects merely because they had no gameplay function.

---

# CATEGORY 5 — CITY / MAP STRUCTURE

Reconstruct the game's primary city-building world spatially and conceptually.

Identify:

- districts  
- map expansions  
- terrain  
- roads  
- water  
- blocked areas  
- unlockable zones  
- special zones  
- environmental objects  
- city boundaries  
- placement mechanics  
- district-specific structures

Attempt to reconstruct the map progression.

Determine:

> What did a completely new player's map contain?

Then:

> What could eventually be unlocked?

Where historical screenshots exist, organize them chronologically.

---

# CATEGORY 6 — PLANETS AND SPACE LOCATIONS

The space exploration system should receive its own research pass.

Inventory every known:

- planet  
- moon  
- asteroid  
- space station  
- destination  
- mission location  
- enemy encounter area  
- special event destination

Capture:

| Field |
| :---- |
| location\_id |
| name |
| canonical\_equivalent |
| unlock\_requirement |
| mission\_type |
| enemies |
| rewards |
| energy/fuel requirements |
| progression |
| associated\_story |
| visual\_description |
| source |
| confidence |

Reconstruct the space map where possible.

---

# CATEGORY 7 — SPACECRAFT AND VEHICLES

Inventory:

- Planet Express ship variants  
- enemy spacecraft  
- alien ships  
- mission vehicles  
- city vehicles  
- event vehicles

Determine whether they were:

- playable  
- decorative  
- combat entities  
- UI representations  
- animated map objects

Capture internal asset identifiers when recoverable.

---

# CATEGORY 8 — ENEMIES AND COMBAT

Reconstruct the combat system.

Identify all known:

- enemies  
- bosses  
- enemy classes  
- enemy factions  
- combat encounters  
- character combat classes  
- status effects  
- attacks  
- abilities  
- buffs  
- debuffs  
- damage types  
- combat items

Determine:

- team composition rules  
- turn order  
- damage calculations if documented  
- enemy scaling  
- rewards  
- failure conditions  
- energy/resource costs  
- encounter progression

Do not merely describe the system.

Inventory the actual content within it.

---

# CATEGORY 9 — CHARACTER JOBS / TASKS

This category is especially important.

Create as close to a complete database as possible of character activities.

Example fields:

| Field |
| :---- |
| job\_id |
| character |
| costume |
| displayed\_job\_name |
| internal\_identifier |
| duration |
| building |
| location |
| animation |
| reward\_currency |
| reward\_amount |
| XP |
| quest\_related |
| event\_related |
| prerequisite |
| source |
| confidence |

Search videos and old wiki pages for job lists that may have disappeared from current sources.

---

# CATEGORY 10 — QUESTS

Reconstruct the quest system in detail.

Identify:

- main story quests  
- side quests  
- character unlock quests  
- costume quests  
- building quests  
- tutorial quests  
- event quests  
- planet quests  
- combat quests  
- temporary quests

For each quest:

| Field |
| :---- |
| quest\_id |
| name |
| quest\_chain |
| sequence\_number |
| triggering\_condition |
| characters |
| required\_jobs |
| required\_buildings |
| required\_items |
| dialogue |
| rewards |
| next\_quest |
| event |
| first\_available |
| source |
| confidence |

---

# Quest Chains

Preserve the actual dependency graph.

For example:

Quest A  
→ unlocks Building B  
→ unlocks Character C  
→ begins Quest D  
→ unlocks Planet E

Relationships are more important than simply collecting quest names.

---

# CATEGORY 11 — EVENTS

Create a complete event history.

Identify every:

- major event  
- mini-event  
- holiday event  
- promotional event  
- crossover  
- rerun  
- content update

For each event reconstruct:

| Field |
| :---- |
| event\_id |
| name |
| start\_date |
| end\_date |
| theme |
| story |
| characters\_added |
| costumes\_added |
| buildings\_added |
| decorations\_added |
| currencies |
| crafting |
| enemies |
| quests |
| gameplay\_mechanics |
| premium\_content |
| rewards |
| source |
| confidence |

Create an event timeline.

Then calculate what percentage of the known game's content entered through temporary events.

---

# CATEGORY 12 — ITEMS AND INVENTORY

Inventory every identifiable game item.

Include:

- crafting materials  
- character unlock items  
- costume materials  
- quest objects  
- event items  
- upgrade items  
- consumables  
- resource drops  
- combat items

Capture:

| Field |
| :---- |
| item\_id |
| displayed\_name |
| internal\_identifier |
| item\_type |
| source/drop |
| used\_for |
| character |
| costume |
| building |
| event |
| rarity |
| visual\_description |
| source |
| confidence |

---

# CATEGORY 13 — CURRENCIES AND ECONOMY

Catalog every currency/resource system ever used.

Include permanent and temporary currencies.

Research:

- Pizza  
- Nixonbucks  
- event currencies  
- crafting currencies  
- premium currency  
- combat resources  
- space resources  
- energy systems

Do not assume this list is complete.

For each currency determine:

- earning methods  
- spending methods  
- purchase methods  
- sinks  
- event association  
- premium/free status  
- icon description  
- internal identifier if recoverable

---

# CATEGORY 14 — LEVELS AND PROGRESSION

Determine:

- player level cap over time  
- XP progression  
- building unlock levels  
- character unlock levels  
- district unlocks  
- planet unlocks  
- feature unlocks  
- tutorials  
- progression gates

Create a progression table.

Attempt to reconstruct what a new player would experience chronologically.

---

# CATEGORY 15 — DIALOGUE AND STORY CONTENT

Identify surviving sources of in-game dialogue.

Research:

- quest dialogue  
- character dialogue  
- tutorial text  
- event dialogue  
- combat text  
- flavor text  
- building descriptions  
- character descriptions  
- item descriptions

Do NOT reproduce huge quantities of copyrighted dialogue verbatim.

Instead:

- identify where it exists  
- summarize content  
- preserve identifiers  
- quote only short portions where necessary for identification

Determine whether dialogue remains inside the client or was server-delivered.

---

# CATEGORY 16 — UI / GAME SCREENS

Inventory major interfaces.

Examples:

- startup  
- login  
- city  
- build menu  
- character menu  
- inventory  
- quest log  
- space map  
- combat  
- store  
- event interface  
- character unlock interface  
- dialogue screens  
- settings

For each UI area document:

- purpose  
- visible controls  
- data displayed  
- likely client/server dependencies  
- visual evidence  
- screenshots/video references

---

# CATEGORY 17 — GAME SYSTEMS

Create a system-level inventory.

Potential systems include:

- authentication  
- account/player profile  
- cloud saves  
- city persistence  
- building placement  
- character state  
- jobs  
- quests  
- dialogue  
- inventory  
- currencies  
- crafting  
- events  
- timers  
- combat  
- space travel  
- purchases  
- ads if applicable  
- notifications  
- DLC/content downloads  
- analytics  
- configuration  
- localization

For each system determine:

### Client-side responsibilities

What appears to be implemented locally?

### Server-side responsibilities

What appears to require backend responses?

### Unknown

What needs additional investigation?

This distinction is extremely important for restoration.

---

# CATEGORY 18 — GAME ASSETS

Research what asset types existed and where they may survive.

Investigate:

- sprites  
- textures  
- character models  
- animations  
- audio  
- music  
- voice clips  
- icons  
- UI graphics  
- building graphics  
- backgrounds  
- fonts  
- localization files  
- configuration data  
- downloadable bundles  
- manifests

Where legal and technically possible, identify:

- filename  
- path  
- bundle  
- asset ID  
- hash  
- format  
- associated entity

Do not redistribute copyrighted assets.

The goal is identification and mapping.

---

# CATEGORY 19 — CLIENT ARCHAEOLOGY

Investigate surviving Android and iOS client software.

Research public technical documentation surrounding:

- APK structure  
- IPA structure  
- Unity or other engine components  
- native libraries  
- configuration files  
- strings  
- manifests  
- API URLs  
- content delivery URLs  
- authentication URLs  
- telemetry  
- serialization formats

Document findings from existing preservation work.

Do not assume the game was entirely server-driven.

Identify what is clearly embedded in the client.

---

# CATEGORY 20 — SERVER / PROTOCOL ARCHAEOLOGY

Research existing efforts to recreate the game's backend.

Give special attention to:

- WOTServer  
- forks  
- related repositories  
- issue trackers  
- commits  
- technical discussions  
- Reddit posts from preservation developers  
- Discord/forum discussions if publicly accessible  
- archived documentation

Determine:

### What has already been discovered?

### What currently works?

### What does not work?

### What endpoints have been identified?

### What request/response formats are known?

### What authentication flow is understood?

### What content-loading mechanism is understood?

### What dependencies remain unresolved?

Create a structured table:

| Endpoint/System | Known Request | Known Response | Status | Evidence |

Status:

- WORKING  
- PARTIAL  
- IDENTIFIED  
- HYPOTHESIZED  
- UNKNOWN

---

# Related TinyCo / Jam City Games

Investigate whether related games share infrastructure or protocol concepts.

Especially examine publicly documented technical relationships with:

- Family Guy: The Quest for Stuff  
- other TinyCo titles from the same period

Possible similarities may include:

- API architecture  
- endpoint names  
- serialization  
- player state  
- CDN layout  
- event configuration  
- inventory structures

Do not assume compatibility.

Clearly label:

- confirmed shared behavior  
- probable similarity  
- speculation

---

# CATEGORY 21 — DOWNLOADABLE CONTENT / CDN

Determine what content may have been downloaded after installation.

Research:

- DLC manifests  
- asset bundles  
- CDN hosts  
- patch files  
- cached files  
- event packages  
- localization packages

This may be critical because some content may not exist inside the base APK/IPA.

Determine whether archived copies survive.

Search public preservation sources and Internet Archive where appropriate.

Do not facilitate unauthorized distribution.

The purpose is preservation research and identification.

---

# CATEGORY 22 — CUT / UNUSED / UNRELEASED CONTENT

Specifically investigate evidence of content that existed in:

- client files  
- asset bundles  
- configuration  
- localization  
- promotional material

but was never released or fully enabled.

Mark these carefully:

`release_status`

Values:

- RELEASED  
- LIMITED\_RELEASE  
- UNUSED  
- CUT  
- PROTOTYPE  
- UNKNOWN

Never treat unused assets as released game content without evidence.

---

# CATEGORY 23 — SCREENSHOT ARCHAEOLOGY

Search aggressively for historical screenshots.

Useful sources may include:

- App Store pages  
- Google Play pages  
- gaming sites  
- review articles  
- Reddit  
- fan forums  
- YouTube thumbnails  
- archived wikis  
- social media  
- developer promotional material  
- press kits

For every useful image, identify visible:

- characters  
- buildings  
- decorations  
- UI  
- currencies  
- map configuration  
- quests  
- objects  
- planets  
- enemies

Screenshots may provide evidence for content missing from textual databases.

---

# CATEGORY 24 — VIDEO ARCHAEOLOGY

Search YouTube and other publicly accessible gameplay archives.

Particularly valuable:

- launch-day gameplay  
- new-player walkthroughs  
- event walkthroughs  
- character unlock videos  
- building showcases  
- combat gameplay  
- space missions  
- final-version gameplay  
- shutdown-era recordings

Build a video source index.

For particularly useful videos, note approximate timestamps associated with recoverable game information.

---

# CATEGORY 25 — COMMUNITY MEMORY

Research historical:

- Reddit discussions  
- fan forums  
- Discord discussions where publicly indexed  
- strategy guides  
- event guides  
- spreadsheets  
- player-maintained databases  
- screenshots  
- save-state discussions  
- modding/preservation conversations

Community knowledge should not automatically be treated as canonical fact.

Use confidence indicators.

However, do not dismiss community sources—they may contain the only surviving record of temporary content.

---

# SOURCE HIERARCHY

Use as many source categories as practical.

Prioritize:

1. surviving game client data  
2. developer/publisher material  
3. actual gameplay footage/screenshots  
4. archived official pages  
5. preservation repositories  
6. game databases/wikis  
7. contemporary walkthroughs  
8. Reddit/community posts  
9. retrospective recollections

Triangulate important claims.

---

# INTERNET ARCHIVE RESEARCH

Use the Internet Archive / Wayback Machine extensively where appropriate.

Investigate historical snapshots of:

- official game website  
- Jam City/TinyCo pages  
- Futurama game wiki pages  
- event guides  
- community documentation  
- promotional pages  
- support documentation

Current webpages may have lost significant information that older snapshots preserve.

---

# EXHAUSTIVENESS METHOD

Perform systematic passes.

## Pass 1 — Game history

Establish timeline and major versions.

## Pass 2 — Characters

Enumerate complete roster.

## Pass 3 — Costumes

Enumerate all variants.

## Pass 4 — Buildings

Enumerate all structures.

## Pass 5 — Decorations

Enumerate placeable objects.

## Pass 6 — Quests

Reconstruct quest graphs.

## Pass 7 — Character jobs

Recover task database.

## Pass 8 — Events

Reconstruct complete event history.

## Pass 9 — Items and currencies

Inventory economy.

## Pass 10 — Space system

Planets, enemies, rewards and progression.

## Pass 11 — Combat

Entities and mechanics.

## Pass 12 — Client archaeology

Investigate embedded data.

## Pass 13 — Backend archaeology

Investigate protocols/server behavior.

## Pass 14 — Screenshots/videos

Find visual-only entities.

## Pass 15 — Archived sources

Recover deleted documentation.

## Pass 16 — Long-tail audit

Search explicitly for entities missed by all previous passes.

Do NOT stop once prominent content has been identified.

---

# EVIDENCE MODEL

Every record should indicate evidence.

Use:

### CONFIRMED

Directly supported by reliable evidence.

### PROBABLE

Strong circumstantial evidence.

### UNCERTAIN

Some evidence but unresolved.

### SPECULATIVE

Hypothesis requiring validation.

Do not silently convert speculation into fact.

---

# VERY IMPORTANT — DISTINGUISH THREE THINGS

For every entity, distinguish:

### Canonical Futurama identity

What the entity is in the TV/comic universe.

### Worlds of Tomorrow implementation

How the game represented it.

### Technical implementation

How the client/server may internally represent it.

Example:

Planet Express Ship

        │

        ├── Futurama canonical entity

        │

        ├── game-visible spaceship

        │

        └── internal asset/configuration IDs

Do not collapse these into one record without relationships.

---

# STABLE IDS

Assign stable research IDs.

Examples:

`WOT_CHAR_FRY`

`WOT_COSTUME_FRYPHARAOH`

`WOT_BUILDING_PLANET_EXPRESS`

`WOT_ITEM_HYPNOWAVE`

`WOT_EVENT_ROBOT_HELL`

`WOT_PLANET_OMEGA3`

Actual names above are illustrative only.

Do not invent content based on examples.

---

# RELATIONSHIP GRAPH

Build relationships between records.

Examples:

`CHARACTER → HAS_COSTUME → COSTUME`

`CHARACTER → PERFORMS_JOB → JOB`

`JOB → OCCURS_AT → BUILDING`

`QUEST → REQUIRES → CHARACTER`

`QUEST → UNLOCKS → BUILDING`

`QUEST → REWARDS → ITEM`

`EVENT → ADDS → CHARACTER`

`EVENT → USES_CURRENCY → CURRENCY`

`PLANET → CONTAINS → ENEMY`

`ITEM → UNLOCKS → COSTUME`

`BUILDING → PRODUCES → RESOURCE`

`CLIENT_ASSET → REPRESENTS → CHARACTER`

`SERVER_ENDPOINT → RETURNS → PLAYER_STATE`

The graph is a major deliverable.

---

# MACHINE-READABLE MODEL

Recommend a JSON/relational schema capable of storing the reconstructed game.

Example:

{

  "id": "WOT\_CHAR\_EXAMPLE",

  "type": "character",

  "name": "",

  "internal\_ids": \[\],

  "canonical\_entity\_id": "",

  "unlock": {},

  "jobs": \[\],

  "quests": \[\],

  "costumes": \[\],

  "events": \[\],

  "assets": \[\],

  "relationships": \[\],

  "first\_available": "",

  "last\_known\_available": "",

  "evidence": \[\],

  "confidence": "confirmed"

}

Develop specialized sub-schemas for:

- characters  
- buildings  
- quests  
- jobs  
- events  
- items  
- currencies  
- planets  
- enemies  
- technical assets  
- network endpoints

---

# DELIVERABLE 1 — GAME CONTENT SUMMARY

Provide counts of recovered:

- characters  
- costumes  
- buildings  
- decorations  
- quests  
- jobs  
- events  
- currencies  
- items  
- planets  
- enemies  
- vehicles  
- other content

Avoid claiming completeness without evidence.

---

# DELIVERABLE 2 — COMPLETE MASTER INVENTORY

Create a master table:

| ID | Name | Category | Internal ID | Event | Availability | Source | Confidence |

Do not impose arbitrary row limits.

If thousands of records are identified, preserve them.

---

# DELIVERABLE 3 — CHARACTER / COSTUME DATABASE

Detailed table.

---

# DELIVERABLE 4 — BUILDING / DECORATION DATABASE

Detailed table.

---

# DELIVERABLE 5 — QUEST GRAPH

Provide both:

- structured quest table  
- dependency graph

---

# DELIVERABLE 6 — CHARACTER JOB DATABASE

Recover durations, locations and rewards where possible.

---

# DELIVERABLE 7 — COMPLETE EVENT TIMELINE

Map every known event and the content introduced by it.

---

# DELIVERABLE 8 — WORLD / MAP MODEL

Reconstruct:

- New New York  
- districts  
- expansion  
- special areas  
- planets  
- space navigation

---

# DELIVERABLE 9 — ECONOMY MODEL

Describe the game's economic relationships:

JOB

 ↓

RESOURCE

 ↓

ITEM

 ↓

CHARACTER/COSTUME/BUILDING

Map currencies and resource loops.

---

# DELIVERABLE 10 — TECHNICAL CLIENT INVENTORY

Document:

- packages  
- native libraries  
- configuration files  
- content manifests  
- URLs  
- asset bundles  
- identifiers  
- serialized data structures

Only include information supported by public evidence or legally obtained analysis.

---

# DELIVERABLE 11 — BACKEND RECONSTRUCTION MATRIX

Produce:

| System | Client Evidence | Server Evidence | Current Understanding | Restoration Difficulty |

Systems should include at minimum:

- startup  
- authentication  
- account creation  
- player state  
- town loading  
- building placement  
- character state  
- jobs  
- timers  
- inventory  
- currencies  
- quests  
- events  
- space  
- combat  
- DLC  
- saving  
- purchases

Restoration difficulty:

- EASY  
- MODERATE  
- HARD  
- UNKNOWN

Explain ratings.

---

# DELIVERABLE 12 — PRESERVATION STATUS

Explicitly determine:

## What survives?

## What is partially preserved?

## What appears lost?

## What may still exist inside clients?

## What may exist in cached files?

## What may survive in videos/screenshots only?

## What requires server reconstruction?

---

# DELIVERABLE 13 — EXISTING REVIVAL EFFORTS

Identify every credible known attempt to restore the game.

For each:

- project  
- developer/community  
- repository  
- implementation language  
- approach  
- current status  
- last meaningful activity  
- what works  
- known blockers  
- discoveries worth preserving

Pay special attention to WOTServer and any related or forked work.

---

# DELIVERABLE 14 — RESTORATION ROADMAP

Based strictly on evidence uncovered during research, propose the minimum technical path toward:

### Milestone 0

Client launches.

### Milestone 1

Client contacts replacement server.

### Milestone 2

Startup/bootstrap succeeds.

### Milestone 3

Local player account exists.

### Milestone 4

Town/world state loads.

### Milestone 5

A character appears.

### Milestone 6

A building can be placed.

### Milestone 7

State persists across restart.

### Milestone 8

Character jobs work.

### Milestone 9

Quest progression works.

### Milestone 10

Space/combat works.

### Milestone 11

Historical event content can be enabled.

Do not assume these milestones are technically correct if research reveals a different architecture.

Modify them based on evidence.

---

# DELIVERABLE 15 — “FIRST VISIBLE WIN”

Determine the **smallest achievable experiment that would visibly demonstrate that the dead game is being revived**.

Favor something achievable quickly, such as:

- successful replacement-server request  
- startup screen progressing farther  
- player state being returned  
- a city loading  
- Fry appearing  
- one persistent building

Explain:

1. what needs to happen  
2. what files/components are involved  
3. known unknowns  
4. evidence supporting the approach  
5. likely blockers

This deliverable is particularly important.

---

# DELIVERABLE 16 — RESEARCH BACKLOG

Produce a prioritized list of unresolved mysteries.

Use:

### P0 — Blocks restoration

### P1 — Important game behavior

### P2 — Missing content/data

### P3 — Historical curiosity

Examples:

- unknown startup response schema  
- missing DLC package  
- unexplained asset ID  
- event data unavailable  
- character unlock requirements uncertain

---

# DELIVERABLE 17 — CROSSWALK TO FUTURAMA UNIVERSE INVENTORY

Assume a separate comprehensive Futurama universe database is being constructed.

Prepare this dataset so the two inventories can later be joined.

For each game entity provide when possible:

`canonical_entity_name`

`canonical_entity_type`

`canonical_match_confidence`

`game_specific_variant`

And classify:

- DIRECT\_CANON\_MATCH  
- GAME\_VARIANT  
- GAME\_ORIGINAL  
- UNKNOWN

This should eventually allow:

**Futurama Universe → Worlds of Tomorrow → Surviving Game Asset**

to be traversed as one knowledge graph.

---

# FINAL COMPLETENESS AUDIT

Before concluding, perform a deliberate missing-content audit.

Ask:

> What content might this research have missed because it existed only during a temporary event?  
>   
> What might only exist in old screenshots or videos?  
>   
> What could exist inside the client but never appear on a wiki?  
>   
> What downloadable content may no longer be hosted?  
>   
> What assets might have been present but unused?  
>   
> Which quests/jobs/items appear referenced but are not yet accounted for?  
>   
> Which technical assumptions are based on inference rather than observed protocol behavior?

Report the results.

---

# Final Output Structure

Return:

1. Executive findings  
2. Historical timeline  
3. Master content inventory  
4. Character database  
5. Costume database  
6. Buildings/decorations  
7. Quest database  
8. Character jobs  
9. Events  
10. Items/currencies  
11. World/space model  
12. Combat/enemies  
13. Asset archaeology  
14. Client architecture  
15. Backend/protocol findings  
16. Existing preservation projects  
17. Survival/loss assessment  
18. Restoration roadmap  
19. First Visible Win  
20. Research backlog  
21. Machine-readable schema  
22. Sources and evidence  
23. Completeness audit

---

# Research Philosophy

Treat **Futurama: Worlds of Tomorrow as a lost software system being reconstructed from surviving evidence**.

Use all available forms of evidence:

**code \+ binaries \+ archives \+ screenshots \+ videos \+ wikis \+ community knowledge \+ surviving repositories \+ related software \+ human recollection.**

Do not confuse absence from a wiki with absence from the game.

Do not confuse an internal asset with released content.

Do not confuse AI inference with evidence.

Do not optimize for a short answer.

The desired result is the **closest practical reconstruction of the entire Futurama: Worlds of Tomorrow game world and content model**, detailed enough to become the foundation for subsequent client archaeology, server-emulator development, AI-assisted reverse engineering, QA, and long-term preservation.  
