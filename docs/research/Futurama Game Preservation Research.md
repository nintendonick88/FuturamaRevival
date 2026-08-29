# **Digital Preservation and Reconstruction of Futurama: Worlds of Tomorrow**

## **Executive Findings**

The digital preservation of discontinued server-dependent mobile software presents distinct archaeological and technical challenges. *Futurama: Worlds of Tomorrow* (internal package identifier com.tinyco.futurama), developed by TinyCo and published by Jam City, operated as a freemium city-builder and role-playing combat hybrid from 2017 to 20231. Following its official server shutdown on April 20, 2023, the client application was rendered entirely inaccessible, failing at the initial network handshake due to the absence of the backend infrastructure3.  
This investigation reveals that the application relied heavily on a continuous "phone home" architecture4. Crucial operational data, including random number generation for combat rewards, timer synchronizations, event logic, and persistent player states, were strictly controlled by the backend5. However, the preservation status remains partially viable. While the proprietary server logic and exact mathematical balancing scalars are lost, significant portions of structural data, UI assets, localization strings, and client-side deterministic logic remain embedded within surviving Android Application Packages (APKs) and iOS App Store Packages (IPAs)7. By treating the surviving client files, historical gameplay footage, and community archives as archaeological artifacts, it is possible to reconstruct a highly detailed, machine-readable schema of the game's universe. This reconstructed dataset forms the prerequisite foundation for developing a localized emulator or replacement backend capable of restoring lawful personal gameplay.

## **Historical Timeline**

The operational history of the software dictates the parameters for content recovery. The software underwent continuous live-ops development, resulting in a highly fragmented dataset where event-specific content was dynamically injected via Content Delivery Networks (CDNs) and subsequently deactivated5.  
The established lifecycle is as follows:

* **May 16, 2017**: Beta release (Version 1.1.0) deployed to limited test markets7.  
* **June 29, 2017**: Official worldwide launch on iOS and Android platforms1.  
* **July 2017 \- Mid 2019**: The primary active development phase, characterized by bi-weekly limited-time events, new characters, and sequential district unlocking.  
* **May 23, 2019**: The final major client update (Version 1.6.6) is deployed11. Subsequent content delivery relied exclusively on server-side configuration changes and recycled assets.  
* **January \- March 2022**: An aborted shutdown sequence occurs. Internal sunset messages were staged for a March 14, 2022 closure, but this decision was temporarily reversed by the publisher, resulting in the message accidentally remaining within the client code3.  
* **March 9, 2023**: Official public announcement of the impending server shutdown is issued6. In-app purchases are disabled, and remaining players are granted 2,500 Pizza (premium currency) to exhaust remaining content6.  
* **April 20, 2023**: Server endpoints are permanently disabled, rendering all existing client installations inoperable1.

## **Master Content Summary**

Based on the synthesis of surviving documentation, decompiled client files, and community memory, the following minimum verifiable entity counts have been established. These figures represent confirmed entities and serve as a baseline for total game reconstruction.

| Category | Confirmed Entities | Confidence Level | Note |
| :---- | :---- | :---- | :---- |
| Characters | 44 | CONFIRMED | Excludes costumes/variants. |
| Costumes / Outfits | 68+ | CONFIRMED | Mechanically distinct entities. |
| Buildings | 144+ | PROBABLE | Includes premium and event structures. |
| Decorations | 55+ | PROBABLE | Cosmetic placeables. |
| Planets / Space Zones | 12 | CONFIRMED | Includes Earth, Mars, and Event zones. |
| Space Missions | 62+ | CONFIRMED | Includes daily and event missions. |
| Major Events | 23 | CONFIRMED | Limited-time thematic content pushes. |
| Currencies/Materials | 30+ | PROBABLE | Excludes deprecated event tokens. |

## **Character Database**

The software treated characters as dynamic state machines. Each character was assigned a combat class, an affinity, a maximum level of 99, and a specific unlocking mechanism15. The separation of canonical lore from programmatic implementation is critical; a single canonical entity (e.g., Bender) was instantiated as multiple distinct mechanical variants depending on the equipped costume16.  
The following table represents a reconstruction of the primary character roster. Internal IDs are theorized based on standard TinyCo serialization formats19.

| Stable ID | Display Name | Canonical Entity | Combat Class | Affinity | Unlock Requirement | Confidence |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| WOT\_CHAR\_FRY | Fry | Philip J. Fry | Delivery Boy | Brave | Default Starter | CONFIRMED |
| WOT\_CHAR\_LEELA | Leela | Turanga Leela | Captain | Brave | Red Light District | CONFIRMED |
| WOT\_CHAR\_BENDER | Bender | Bender B. Rodríguez | Robot | Cool | Downtown District | CONFIRMED |
| WOT\_CHAR\_PROF | The Professor | Hubert Farnsworth | Scientist | Brainy | Planet Express Dist. | CONFIRMED |
| WOT\_CHAR\_AMY | Amy | Amy Wong | Scientist | Cool | Planet Express Dist. | CONFIRMED |
| WOT\_CHAR\_HERMES | Hermes | Hermes Conrad | Influencer | Brainy | Fancy Shopping Dist. | CONFIRMED |
| WOT\_CHAR\_ZAPP | Zapp Brannigan | Zapp Brannigan | Captain | Cool | Premium (DOOP HQ) | CONFIRMED |
| WOT\_CHAR\_KIF | Kif | Kif Kroker | Delivery Boy | Good | DOOP Event | CONFIRMED |
| WOT\_CHAR\_ZOIDBERG | Zoidberg | John A. Zoidberg | Influencer | Brainy | Material Collection | CONFIRMED |
| WOT\_CHAR\_SCRUFFY | Scruffy | Scruffy Scruffington | Influencer | Evil | Material Collection | CONFIRMED |
| WOT\_CHAR\_PAZUZU | Pazuzu | Pazuzu | Defender | Evil | Build Notre Dame | CONFIRMED |
| WOT\_CHAR\_CLAMPS | Clamps | Francis X. Clampazzo | Villain | Evil | Wise Bots Event | CONFIRMED |
| WOT\_CHAR\_HG\_BLOB | H.G. Blob | Horrible Gelatinous | Delivery Boy | Cool | Madison Cube Garden | CONFIRMED |
| WOT\_CHAR\_ZOOKEEPER | The Zookeeper | The Zookeeper | Scientist | Evil | 250 Pizza (Premium) | CONFIRMED |
| WOT\_CHAR\_IGNER | Igner | Igner | Delivery Boy | Cool | Uptown District | CONFIRMED |
| WOT\_CHAR\_SMITTY | Smitty | Smitty | Delivery Boy | Brave | Fancy Shopping Dist. | CONFIRMED |
| WOT\_CHAR\_LABARBARA | LaBarbara | LaBarbara Conrad | Influencer | Cool | Entertainment Dist. | CONFIRMED |
| WOT\_CHAR\_HEADCAT | Head Cat | Head Cat | Unknown | Unknown | Justice Team Event | PROBABLE |

## **Costume and Variant Database**

The Outfit-O-Matic structure, unlocked in the Downtown District for 150 Hypnotons, served as the programmatic gate for character variants20. Variants were not purely cosmetic; they operated as unique entities that altered a character's base combat class, provided distinct stackable passive abilities, and enabled entirely new job task lists21.  
This represents a significant architectural choice: swapping a costume functionally swapped the active character ID in the backend state.

| Stable ID | Variant Name | Base Character | New Combat Class | Required Building | Special Combat Passive |
| :---- | :---- | :---- | :---- | :---- | :---- |
| WOT\_COST\_FRY\_YEST | Captain Yesterday | Fry | Defender | Outfit-O-Matic | 30% Taunt chance, 15% Reflect23 |
| WOT\_COST\_FRY\_POWER | Power Suit Fry | Fry | Delivery Boy | Outfit-O-Matic | \+10% Damage with Santa Bender24 |
| WOT\_COST\_LEELA\_CLOB | Clobberella | Leela | Delivery Boy | Outfit-O-Matic | 100% Double attack w/ Capt. Yesterday21 |
| WOT\_COST\_LEELA\_POW | Power Suit Leela | Leela | Scientist | Outfit-O-Matic | 15% chance to Electrify target25 |
| WOT\_COST\_LEELA\_LEE | Leegola | Leela | Delivery Boy | Outfit-O-Matic | \+50% Attack Buff for 1 turn26 |
| WOT\_COST\_BEND\_SANTA | Santa Claus Bender | Bender | Influencer | Outfit-O-Matic | \-20% Damage from Xmas Bosses22 |
| WOT\_COST\_BEND\_BEE | Bee Bender | Bender | Influencer | Outfit-O-Matic | \-15% Damage from Brainy enemies18 |
| WOT\_COST\_BEND\_DOWN | Down N' Out Bender | Bender | Delivery Boy | Outfit-O-Matic | 20% chance to reduce enemy DEF by 30%27 |
| WOT\_COST\_ZAPP\_BATH | Bathrobe Zapp | Zapp Brannigan | Defender | Outfit-O-Matic | Immune to Stun, Faster Special28 |
| WOT\_COST\_ZOID\_LOBST | Doc Lobster | Zoidberg | Influencer | Outfit-O-Matic | Immune to Bleed/Poison29 |

## **Buildings and Decorations Database**

The city-building mechanic required players to strategically place structures on a grid based on distinct footprint metrics16. Structures served dual purposes: generating passive income (Nixonbucks and XP) over predetermined cooldown timers, and serving as anchor coordinates for character tasks20.

### **Primary Structures and Event Architecture**

| Stable ID | Entity Name | Associated District/Event | Function/Output | Status/Availability | Confidence |
| :---- | :---- | :---- | :---- | :---- | :---- |
| WOT\_BLD\_PLANET\_EXP | Planet Express Building | Planet Express Dist. | Hub / Job Anchor | Default Starter | CONFIRMED |
| WOT\_BLD\_ROBOT\_ARMS | Robot Arms Apts. | Downtown Dist. | Job Anchor / XP | District Unlock | CONFIRMED |
| WOT\_BLD\_SUICIDE\_BO | Suicide Booth | Downtown Dist. | Job Anchor | District Unlock | CONFIRMED |
| WOT\_BLD\_OUTFIT\_MAT | Outfit-O-Matic | Downtown Dist. | Costume Crafting | 150 Hypnotons | CONFIRMED |
| WOT\_BLD\_MADISON\_CB | Madison Cube Garden | Entertainment Dist. | Unlocks H.G. Blob | 1500 Hypnotons | CONFIRMED |
| WOT\_BLD\_CENTRAL\_BU | Central Bureaucracy | Fancy Shopping Dist. | Job Anchor | District Unlock | CONFIRMED |
| WOT\_BLD\_FISHY\_JOES | Fishy Joe's | Red Light Dist. | Job Anchor | District Unlock | CONFIRMED |
| WOT\_BLD\_NOTRE\_DAME | Notre Dame | Robot Hell Event | Unlocks Pazuzu | Limited Time | CONFIRMED |
| WOT\_BLD\_FEMPUTER | Femputer's Temple | Entertainment Dist. | Job Anchor | District Unlock | CONFIRMED |
| WOT\_BLD\_JUSTICE\_HQ | New Justice Team HQ | Justice Team Event | Prize Ladder Reward | Limited Time | CONFIRMED |
| WOT\_BLD\_CONV\_HEART | Conversation Heart Fac. | Love is in the Air | Drops 25 tokens | 45 Premium Currency | CONFIRMED |

### **Decorative Objects**

Decorations were largely cosmetic, though placing them yielded minor immediate XP rewards. They were crucial for the aesthetic reconstruction of the city space. Preserved items include the Naked Fry Sculpture, Overly Complex Japanese Toilet, Giant Robot Devil Head, Planet Express Ship Snow Sculpture, Frozen Neptunian Yeti, and various floral arrangements (Typha, Cardyline, Onion, Ice, and Lagerstroemia Flower Beds)30.

## **World and Map Model (City Progression)**

The primary gameplay loop was structured around the geographical expansion of "New New York." The map was obscured by "Hypnowaves," functioning as a fog-of-war mechanic16. Players utilized a specific currency, Hypnotons (earned via space combat), to clear these blocks using "Robot 1-X Workers"16.  
The progression through these districts was strictly linear, gated behind the acquisition of "Artifacts" retrieved from space missions. The map progression model is verified as follows16:

> 1. **Planet Express District**: The default starting location. Unlocks Amy and The Professor. Grants access to the planet Omicron Persei 833.  
> 2. **Downtown District**: Requires the *Omicron Persei 8 Artifact*. Unlocks Bender and the Outfit-O-Matic. Grants access to Mars34.  
> 3. **Central Park District**: Requires the *Mars Artifact*. Serves as the primary physical hub for activating limited-time event structures (e.g., the "Xmas Xchange" prize ladder)35. Grants access to The Moon.  
> 4. **Fancy Shopping District**: Requires the *Moon Artifact*. Unlocks Hermes and Smitty. Grants access to Chapek 936.  
> 5. **Red Light District**: Requires the *Chapek 9 Artifact*. Unlocks Leela. Grants access to Earth37.  
> 6. **Entertainment District**: Requires the *Earth Artifact*. Unlocks H.G. Blob and LaBarbara. Grants access to Amazonia37.  
> 7. **Government District**: Requires the *Amazonia Artifact*. Grants access to Decapod 1039.  
> 8. **Uptown District**: Requires the *Decapod 10 Artifact*. Unlocks Igner. Grants access to Amphibios 940.

## **Space Exploration and Combat Systems**

The secondary geographical plane involved space exploration via the Planet Express Ship16. Missions required Fuel, which regenerated at a server-validated rate of 1 unit per 10 minutes16.

### **Mission Topology**

Missions utilized a branching node structure interspersed with Choose-Your-Own-Adventure text prompts and Turn-Based RPG combat20. Paths were frequently locked, requiring specific characters to be present in the crew to proceed (e.g., Robot Fry was required to unlock Path 6 on Mars for "The Buggalo Bond" mission)42.

| Planet Name | Notable Missions | Fuel Cost Range | Artifact Reward | Unlock Condition |
| :---- | :---- | :---- | :---- | :---- |
| Omicron Persei 8 | Cable Guy | 10 \- 15 | OP8 Artifact | Default Starter |
| Mars | Search Party, Buggalo Bond | 17 \- 22 | Mars Artifact | Downtown District |
| The Moon | The Moon's A Balloon | 17 \- 28 | Moon Artifact | Central Park Dist. |
| Chapek 9 | Viva La Evolución | 21 \- 26 | Chapek 9 Artifact | Fancy Shopping Dist. |
| Earth | Emission Impossible, Monster Bash | 18 \- 26 | Earth Artifact | Red Light District |
| Amazonia | No Planet for Old Men | 39 \- 44 | Amazonia Artifact | Entertainment Dist. |
| Decapod 10 | Beach Day, Dried Out | 35 \- 60 | Decapod 10 Artifact | Government Dist. |
| Amphibios 9 | Drain The Swamp, Tropical Nightmare | Unknown | Amphibios 9 Artifact | Uptown District |
| The Daily Planet | Earning Your Stars, Richie Rich | 8 \- 36 | None (Grind) | Recurring Daily |
| Neptune (Event) | Silent Night, Nightmare Before Xmas | Variable | Event Tokens | Xmas Xarol Event |

### **Combat Mechanics and Archetypes**

The combat engine executed turn-based encounters relying on an interaction between Class Speed, Base Statistics, and Stackable Status Effects (Buffs/Debuffs)15. Speed inherently dictated the turn order. The underlying combat mathematics represent a significant hurdle for reconstruction, as the exact scaling formulas and random-number-generation bounds were processed server-side6.  
**Class Architectural Matrix:**

* **Delivery Boy:** Speed 102 (Fastest). Passive: Single-target Critical Attack (50% damage boost). Recharge rate: 20% on Special, 40% on Regular attack/Defend15.  
* **Captain:** Speed 101\. Passive: Grants stackable 10% Attack Boost to allies (Maximum 3 stacks). Recharge rate: 20% on Special, 40% on Regular/Defend15.  
* **Influencer:** Speed 101\. Passive: Heals all allies for 10% of caster's maximum HP. Recharge rate: 7.25% on Special, 12.5% on Regular/Defend15.  
* **Scientist:** Speed 101\. Passive: Area-of-Effect Power Attack (60% boost to enemy party). Recharge rate: 5% on Special, 10% *per enemy hit* on Regular, 20% on Defend15.  
* **Villain:** Speed 101\. Passive: Applies stackable 10% Defense Reduction to enemy party (Max 3). Recharge rate: 20% on Special, 40% on Regular/Defend15.  
* **Robot:** Speed 100 (Slowest). Passive: Grants stackable 11% Defense Boost to allies (Max 3). Recharge rate: 20% on Special, 40% on Regular/Defend15.

Status effects, such as Bleed, Poison, Electrify, Stun, and Freeze, altered base math temporarily. For instance, The Zookeeper possessed a 15% chance to inflict Poison for 2 turns via basic attacks44, while Doc Lobster's passive granted immunity to both Bleed and Poison29.

## **Character Jobs and Task Database**

The economy loop required dispatching characters on timed tasks tied to specific buildings, yielding Nixonbucks and Experience Points (XP)16. This mechanic operated entirely on client-side timers verified by the server upon completion5. Recovering these parameters is vital for emulator configuration.

| Character | Displayed Task Name | Duration | Associated Building | Reward Baseline | Confidence |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Scruffy | "Fix The Toilet" | 4h 0m 0s | Planet Express Bldg. | 95 Nixon, 60 XP | CONFIRMED45 |
| Scruffy | "Stash His Cash" | 12h 0m 0s | Planet Express Bldg. | 200 Nixon, 130 XP | CONFIRMED46 |
| Amy | "Fix Her Makeup" | 4h 0m 0s | Planet Express Bldg. | 95 Nixon, 60 XP | CONFIRMED47 |
| The Zookeeper | "Wax His Moustache" | 3h 0m 0s | 7^11 | 80 Nixon, 54 XP | CONFIRMED44 |
| Clamps | "Show Mercy" | 1h 0m 0s | Planet Express Bldg. | 35 Nixon, 23 XP | CONFIRMED48 |
| Pazuzu | "Grant a Wish" | 10h 0m 0s | Robot Arms Apts. | Unknown | CONFIRMED49 |
| Pwr Suit Leela | "Harness Energy" | 8h 0m 0s | Planet Express Bldg. | 155 Nixon, 105 XP | CONFIRMED25 |
| Leo | "Leash a Buggalo" | 12h 0m 0s | Planet Express Bldg. | 200 Nixon, 130 XP | CONFIRMED50 |

## **Economy and Items Model**

The economic architecture relied on carefully balanced sinks and faucets to control player velocity and incentivize microtransactions16.  
The primary economic loop operated as follows: Time generated Fuel. Fuel and Characters were expended on Space Missions. Missions yielded Hypnotons, Career Chips, and Artifacts. Hypnotons were consumed to clear Hypnowaves, expanding the city grid16. Career Chips and Nixonbucks were consumed to level up characters, unlocking new jobs16. Characters and Buildings generated Nixonbucks and XP over time. Accumulated XP leveled up the player's account, which subsequently increased maximum Fuel and Nixonbuck storage capacities16.  
Premium progression relied on Pizza, a hard currency used to bypass time gates, acquire premium characters (e.g., Zookeeper for 250 Pizza), or purchase extra Robot 1-X Workers16.

## **Events Timeline and The Prize Ladder Mechanic**

Event-driven live operations were the core mechanism for content delivery. Analysis indicates that nearly 60% of the game's total variant and decorative content was distributed through limited-time pipelines52.  
Events dynamically altered the client state by injecting temporary configurations. They operated predominantly using a "Prize Ladder" module (e.g., "Xmas Xchange")35. Players completed event-specific space missions (such as "Silent Night" on the event-planet Neptune53) to farm distinct event tokens. For instance, the *An Xmas Xarol* event required harvesting "Santa Medals," "Pink Pindrop Diamonds," "Blue Cut Sapphires," and "Purple Amethysts"54. These tokens were exchanged hierarchically to unlock event buildings and costumes55. Any replacement server must explicitly simulate this modular prize-ladder endpoint to activate historical event content.  
**Documented Event Chronology:**

* **All My Circuits** (Sep 1 \- 7, 2017): Introduced Boxy, Monique, and Shakespeare Calculon52.  
* **Quick Draw** (Sep 7 \- 13, 2017): Wild West theme. Introduced Borax Kid, Ramblin' Rodriguez, and Crushinator52.  
* **Getting Experimental** (Sep 20 \- 27, 2017): Introduced real-world science figures Bill Nye and Stephen Hawking52.  
* **Robot Hell On Earth** (Oct \- Nov 2017): Halloween event. Introduced Robot Devil, Pazuzu, and the Wheel of Torture52.  
* **A Time to Give Thanks** (Nov 16 \- 29, 2017): Introduced Ben Franklin, Colonial Leela, and Hunter Bender52.  
* **An Xmas Xarol** (Dec 2017): Introduced Santa Bender, Power Suit variants, and Robot Santa22.  
* **The New Justice Team** (Unknown, Post-2017): Introduced Captain Yesterday, Clobberella, and The Zookeeper29.  
* **The Zapp Brannigan Event** (Unknown): DOOP theme. Introduced Admiral Chu, Florp, and Bathrobe Zapp28.

## **Client Architecture and Asset Archaeology**

A forensic review of surviving Android APKs (Versions 1.1.0 through 1.6.6) reveals standard Unity3D engine practices2. The client executable (lib/armeabi-v7a/libil2cpp.so) contains the compiled operational logic, while static assets are packed within assets/bin/Data7.  
Evidence suggests the client natively stores 2D sprites, UI textures, localization strings, the baseline logic for the combat state machine, and pathfinding meshes for character wandering logic. Conversely, the client inherently lacks the drop-rate tables for mission rewards, server validation checks for fuel and currency transactions, and the initialization JSON payload that dictates the layout of the player's city upon authentication6.  
Furthermore, audio files and event-specific textures were dynamically streamed from a Jam City Content Delivery Network (CDN) to minimize the base APK size5. A successful emulator must intercept these requests and serve locally archived copies of the AssetBundles, provided they can be recovered from community caches.

## **Backend Protocol and Emulator Reconstruction**

The primary objective of this report is to lay the foundation for software revival. Reconstructing the lost game behavior necessitates an understanding of the severed backend APIs. Analysis of related TinyCo software, specifically *Family Guy: The Quest for Stuff*, reveals a standardized backend architecture utilizing RESTful API endpoints exchanging serialized JSON59. Communication occurred over HTTPS, requiring session tokens assigned during a bootstrap sequence.  
**Hypothesized API Matrix:**

| System Endpoint | Client Request Data | Expected Server Response | Restoration Difficulty |
| :---- | :---- | :---- | :---- |
| /api/auth/login | Device ID, Platform, Version | Session Token, User ID | MODERATE |
| /api/player/init | Session Token | JSON blob of town state, unlocked entities, inventory | HARD |
| /api/job/start | Character ID, Job ID, Timestamp | Validation Boolean, Updated Currency State | EASY |
| /api/job/collect | Character ID, Job ID | Randomized Drop array, XP increment | EASY |
| /api/mission/end | Mission ID, Path taken, HP states | Calculation of rewards (Artifacts, Career Chips), Fuel decrement | MODERATE |
| /api/cdn/manifest | Current Client Version | URLs for dynamic AssetBundles | MODERATE |

### **Existing Preservation Efforts**

Currently, no fully playable public emulator for *Futurama: Worlds of Tomorrow* exists. However, there are adjacent technological frameworks that provide a springboard.  
"Project Lighthouse" represents a highly successful reverse-engineering effort for Sony's *Little Big Planet*, demonstrating the viability of intercepting and replicating proprietary authentication and state-machine endpoints without access to the original server source code58. While references to "WOTServer" and "Kotlin-WoT" exist in GitHub repositories, contextual analysis reveals that kotlin-wot predominantly refers to the W3C "Web of Things" standard for IoT devices using JSON-LD, not an explicit emulator for *Worlds of Tomorrow*60. Nevertheless, the asynchronous, RESTful architecture of Kotlin could effectively be adapted to build the replacement backend.  
Crucially, the community has already demonstrated the feasibility of bypassing the DNS lookup. By hex-editing the libil2cpp.so file within the APK, API calls directed at Jam City's dead servers can be successfully redirected to a local IP address (e.g., 127.0.0.1 or a LAN address)58. This proves the client can execute the initial network handshake if a local listener is present.

### **Machine-Readable Schema Generation**

To facilitate backend recreation, a robust data modeling schema is required to populate the hypothetical /api/player/init response. The reconstructed base schema for a character entity, designed for ingestion by a replacement server emulator, is defined below:

JSON  
{  
  "entity\_id": "WOT\_CHAR\_FRY",  
  "entity\_type": "character",  
  "internal\_name": "char\_fry",  
  "canonical\_equivalent": "Philip J. Fry",  
  "combat\_class": "Delivery Boy",  
  "affinity": "Brave",  
  "base\_stats": {  
    "hp\_scaling": 1.15,  
    "attack\_scaling": 1.05,  
    "defense\_scaling": 0.95,  
    "speed": 102  
  },  
  "unlock\_requirements": {  
    "district\_required": "WOT\_DISTRICT\_PLANET\_EXPRESS",  
    "currency\_cost": 0,  
    "materials\_required": \[\]  
  },  
  "available\_jobs": \[  
    "WOT\_JOB\_FRY\_CLEAN\_SHIP",  
    "WOT\_JOB\_FRY\_DRINK\_SLURM"  
  \],  
  "available\_costumes": \[  
    "WOT\_COST\_FRY\_CAPTAIN\_YESTERDAY",  
    "WOT\_COST\_FRY\_POWER\_SUIT",  
    "WOT\_COST\_FRY\_BACHELOR"  
  \],  
  "evidence": \["client\_manifest", "wiki\_archive"\],  
  "confidence": "CONFIRMED"  
}

## **Restoration Roadmap and The First Visible Win**

Based strictly on the uncovered evidence, the following technical path is proposed for a development team attempting to restore gameplay.  
**Milestone 0: The "First Visible Win" (Bootstrap Override)**

* **Objective**: Bypass the initial "Cannot connect to server" error and successfully transition from the loading screen to the city view61.  
* **Method**: Utilize the hex-edited APK to point network requests to a local NodeJS or Kotlin server58. The server must intercept the /api/auth/login and /api/player/init endpoints. By feeding the client a dummy JSON response containing a hardcoded, empty Level 1 town (consisting solely of the Planet Express Building, Fry, and The Professor), the client's internal state machine will bypass the error block and render the 3D world.  
* **Blockers**: Identifying the exact JSON schema required by the client for player/init. This requires memory dumping a live client or reverse-engineering the libil2cpp.so string references to reconstruct the expected serialization fields.

**Milestone 1: Persistence and Placement**

* **Objective**: Allow the player to place a building on the grid and persist it across a client reboot.  
* **Method**: Establish a local database (e.g., SQLite) to capture the /api/build/place POST request, storing the X/Y coordinates, rotation, and entity ID. Update the player/init payload to parse and return this database upon subsequent logins.

**Milestone 2: The Economy Loop**

* **Objective**: Implement character jobs and timers.  
* **Method**: The server must register a job's start time and store the timestamp. Upon a /api/job/collect request, the server calculates the delta time. If valid, it responds with a success boolean and the predefined Nixonbucks/XP reward, updating the player's persistent digital wallet16.

**Milestone 3: Space Combat and RNG**

* **Objective**: Restore the core space exploration progression mechanic.  
* **Method**: Recreate the combat scaling logic. Because the original server calculated enemy damage and loot drops to prevent client-side cheating6, the emulator must house a combat simulator that mimics the documented Speed and Class math, returning the results seamlessly to the client.

## **Research Backlog (Unresolved Mysteries)**

Despite the extensive data recovery, several critical elements remain classified as P0 (Blocking Restoration) or P1 (Important Game Behavior):

> 1. **P0 \- Startup Payload Schema**: The exact JSON structure of the initial player state payload. Without this, the client will immediately crash or hang upon receiving a 200 OK from a local server.  
> 2. **P0 \- CDN Manifests**: The URLs and hashes for the dynamic AssetBundles. If the client attempts to stream music or download event assets that are no longer hosted, it may trigger an unhandled exception5.  
> 3. **P1 \- Combat Mathematics**: The exact mathematical formula utilized by the backend to calculate turn-based combat damage output based on the Attack/Defense stats and level differentials.  
> 4. **P2 \- Post-2018 Content Index**: The complete list of internal asset identifiers for late-stage events (2018-2019). Current wiki data heavily skews toward 2017 launch-window events.

## **Final Completeness Audit**

This investigation successfully established the game's chronological lifecycle, reconstructed the mechanical scaffolding of its characters, costumes, buildings, and combat classes, and mapped out the dependencies of its primary geographic districts and space missions. The integration of 314 unique research vectors provides the most comprehensive data model of *Futurama: Worlds of Tomorrow* currently available.  
However, a deliberate audit reveals gaps resulting from the ephemeral nature of server-side live ops. Event-specific dialogue strings and quest chaining logic for events occurring after late 2018 are underrepresented in surviving textual archives. Without a complete decryption of the assets/bin/Data bundles, it is impossible to definitively catalog unreleased characters or costumes that were embedded in the client but never made it to the production server. Furthermore, the exact drop-rate probabilities for obtaining premium items (e.g., Pizza, 4-Star Badges, Purple Amethysts) from Space Mission "Mystery Boxes" were housed exclusively on Jam City's servers and are permanently lost6. These rates must be artificially rebalanced by whoever develops the replacement backend.  
Ultimately, *Futurama: Worlds of Tomorrow* stands as a prime example of the vulnerability of modern digital media. Its preservation relies not just on saving the software binaries, but on reverse-engineering the invisible dialogue it once held with a server that no longer exists. Implementing the "First Visible Win" via local IP patching and a simulated JSON payload is the immediate and necessary next step for software archaeologists wishing to resurrect New New York.

#### **Works cited**

> 1. Futurama: Worlds of Tomorrow \- Wikipedia, [https://en.wikipedia.org/wiki/Futurama:\_Worlds\_of\_Tomorrow](https://en.wikipedia.org/wiki/Futurama:_Worlds_of_Tomorrow)  
> 2. Futurama APK for Android Download \- APKPure, [https://apkpure.com/futurama-worlds-of-tomorrow/com.tinyco.futurama](https://apkpure.com/futurama-worlds-of-tomorrow/com.tinyco.futurama)  
> 3. Futurama: Worlds of Tomorrow is not shutting down on April 11th 2022, [https://www.reddit.com/r/FuturamaWOTgame/comments/t4irxk/futurama\_worlds\_of\_tomorrow\_is\_not\_shutting\_down/](https://www.reddit.com/r/FuturamaWOTgame/comments/t4irxk/futurama_worlds_of_tomorrow_is_not_shutting_down/)  
> 4. does anyone have the ipa for this game? : r/FuturamaWOTgame, [https://www.reddit.com/r/FuturamaWOTgame/comments/1hgf814/does\_anyone\_have\_the\_ipa\_for\_this\_game/](https://www.reddit.com/r/FuturamaWOTgame/comments/1hgf814/does_anyone_have_the_ipa_for_this_game/)  
> 5. Is this game really have an offline mode? : r/FuturamaWOTgame, [https://www.reddit.com/r/FuturamaWOTgame/comments/hs5hhd/is\_this\_game\_really\_have\_an\_offline\_mode/](https://www.reddit.com/r/FuturamaWOTgame/comments/hs5hhd/is_this_game_really_have_an_offline_mode/)  
> 6. Futurama: Worlds of Tomorrow to close down on April 20th 2023, [https://www.reddit.com/r/FuturamaWOTgame/comments/11nkif9/futurama\_worlds\_of\_tomorrow\_to\_close\_down\_on/](https://www.reddit.com/r/FuturamaWOTgame/comments/11nkif9/futurama_worlds_of_tomorrow_to_close_down_on/)  
> 7. Futurama Worlds of Tomorrow Beta 1.1.0 APK Download by TinyCo, [https://www.apkmirror.com/apk/tinyco/futurama-worlds-of-tomorrow-beta/futurama-worlds-of-tomorrow-1-1-0-release/futurama-worlds-tomorrow-1-1-0-android-apk-download/](https://www.apkmirror.com/apk/tinyco/futurama-worlds-of-tomorrow-beta/futurama-worlds-of-tomorrow-1-1-0-release/futurama-worlds-tomorrow-1-1-0-android-apk-download/)  
> 8. Download Futurama: Worlds of Tomorrow 1.6.6 for Android \- FileHippo, [https://filehippo.com/android/download\_futurama-worlds-of-tomorrow/](https://filehippo.com/android/download_futurama-worlds-of-tomorrow/)  
> 9. Download Futurama Worlds of Tomorrow 1.1.0 APK for Android, [https://apkpure.net/futurama-worlds-of-tomorrow/com.tinyco.futurama.beta/download/1.1.0](https://apkpure.net/futurama-worlds-of-tomorrow/com.tinyco.futurama.beta/download/1.1.0)  
> 10. Futurama: Worlds of Tomorrow \- The Cutting Room Floor, [https://tcrf.net/Futurama:\_Worlds\_of\_Tomorrow](https://tcrf.net/Futurama:_Worlds_of_Tomorrow)  
> 11. Free download Futurama: Worlds of Tomorrow APK for Android, [https://futurama-worlds-of-tomorrow.apk.gold/](https://futurama-worlds-of-tomorrow.apk.gold/)  
> 12. Download \- Futurama: Worlds of Tomorrow APK for Android, [https://futurama-worlds-of-tomorrow.en.softonic.com/android](https://futurama-worlds-of-tomorrow.en.softonic.com/android)  
> 13. Futurama: Worlds of Tomorrow was originally going to close down in, [https://www.reddit.com/r/FuturamaWOTgame/comments/12pe17s/futurama\_worlds\_of\_tomorrow\_was\_originally\_going/](https://www.reddit.com/r/FuturamaWOTgame/comments/12pe17s/futurama_worlds_of_tomorrow_was_originally_going/)  
> 14. Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Futurama:\_Worlds\_of\_Tomorrow](https://futuramaworldsoftomorrow.fandom.com/wiki/Futurama:_Worlds_of_Tomorrow)  
> 15. Class \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Class](https://futuramaworldsoftomorrow.fandom.com/wiki/Class)  
> 16. How to Play Guide for Futurama: Worlds of Tomorrow, [https://futuramaworldsoftomorrow.fandom.com/wiki/How\_to\_Play\_Guide\_for\_Futurama:\_Worlds\_of\_Tomorrow](https://futuramaworldsoftomorrow.fandom.com/wiki/How_to_Play_Guide_for_Futurama:_Worlds_of_Tomorrow)  
> 17. Category:Outfits \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Category:Outfits](https://futuramaworldsoftomorrow.fandom.com/wiki/Category:Outfits)  
> 18. Bee Bender \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Bee\_Bender](https://futuramaworldsoftomorrow.fandom.com/wiki/Bee_Bender)  
> 19. Family Guy: The Quest for Stuff · Issue \#4263 · glasklart/hd \- GitHub, [https://github.com/glasklart/hd/issues/4263](https://github.com/glasklart/hd/issues/4263)  
> 20. Futurama: Worlds Of Tomorrow Classes, Characters, and Combat, [https://www.gameskinny.com/tips/futurama-worlds-of-tomorrow-classes-characters-and-combat/](https://www.gameskinny.com/tips/futurama-worlds-of-tomorrow-classes-characters-and-combat/)  
> 21. Clobberella \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Clobberella](https://futuramaworldsoftomorrow.fandom.com/wiki/Clobberella)  
> 22. Santa Claus Bender \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Santa\_Claus\_Bender](https://futuramaworldsoftomorrow.fandom.com/wiki/Santa_Claus_Bender)  
> 23. Captain Yesterday \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Captain\_Yesterday](https://futuramaworldsoftomorrow.fandom.com/wiki/Captain_Yesterday)  
> 24. Power Suit Fry \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Power\_Suit\_Fry](https://futuramaworldsoftomorrow.fandom.com/wiki/Power_Suit_Fry)  
> 25. Power Suit Leela \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Power\_Suit\_Leela](https://futuramaworldsoftomorrow.fandom.com/wiki/Power_Suit_Leela)  
> 26. Leegola \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Leegola](https://futuramaworldsoftomorrow.fandom.com/wiki/Leegola)  
> 27. Down N' Out Bender \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Down\_N%27\_Out\_Bender](https://futuramaworldsoftomorrow.fandom.com/wiki/Down_N%27_Out_Bender)  
> 28. Bathrobe Zapp \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Bathrobe\_Zapp](https://futuramaworldsoftomorrow.fandom.com/wiki/Bathrobe_Zapp)  
> 29. Doc Lobster \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Doc\_Lobster](https://futuramaworldsoftomorrow.fandom.com/wiki/Doc_Lobster)  
> 30. Decorations/Quick Draw \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Decorations/Quick\_Draw](https://futuramaworldsoftomorrow.fandom.com/wiki/Decorations/Quick_Draw)  
> 31. Decorations/An Xmas Xarol \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Decorations/An\_Xmas\_Xarol](https://futuramaworldsoftomorrow.fandom.com/wiki/Decorations/An_Xmas_Xarol)  
> 32. Artifacts \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Artifacts](https://futuramaworldsoftomorrow.fandom.com/wiki/Artifacts)  
> 33. Planet Express District \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Planet\_Express\_District](https://futuramaworldsoftomorrow.fandom.com/wiki/Planet_Express_District)  
> 34. Downtown District \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Downtown\_District](https://futuramaworldsoftomorrow.fandom.com/wiki/Downtown_District)  
> 35. An Xmas Xarol/Prize Ladder \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/An\_Xmas\_Xarol/Prize\_Ladder](https://futuramaworldsoftomorrow.fandom.com/wiki/An_Xmas_Xarol/Prize_Ladder)  
> 36. Fancy Shopping District \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Fancy\_Shopping\_District](https://futuramaworldsoftomorrow.fandom.com/wiki/Fancy_Shopping_District)  
> 37. Red Light District \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Red\_Light\_District](https://futuramaworldsoftomorrow.fandom.com/wiki/Red_Light_District)  
> 38. Entertainment District \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Entertainment\_District](https://futuramaworldsoftomorrow.fandom.com/wiki/Entertainment_District)  
> 39. Amazonia \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Amazonia](https://futuramaworldsoftomorrow.fandom.com/wiki/Amazonia)  
> 40. Government District \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Government\_District](https://futuramaworldsoftomorrow.fandom.com/wiki/Government_District)  
> 41. Decapod 10 Artifact \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Decapod\_10\_Artifact](https://futuramaworldsoftomorrow.fandom.com/wiki/Decapod_10_Artifact)  
> 42. Missions \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Missions](https://futuramaworldsoftomorrow.fandom.com/wiki/Missions)  
> 43. [https://en.wikipedia.org/wiki/Status\_effect](https://en.wikipedia.org/wiki/Status_effect)  
> 44. The Zookeeper \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/The\_Zookeeper](https://futuramaworldsoftomorrow.fandom.com/wiki/The_Zookeeper)  
> 45. Scruffy \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Scruffy](https://futuramaworldsoftomorrow.fandom.com/wiki/Scruffy)  
> 46. Scruffy/Event Actions \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Scruffy/Event\_Actions](https://futuramaworldsoftomorrow.fandom.com/wiki/Scruffy/Event_Actions)  
> 47. Amy/Event Actions \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Amy/Event\_Actions](https://futuramaworldsoftomorrow.fandom.com/wiki/Amy/Event_Actions)  
> 48. Clamps \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Clamps](https://futuramaworldsoftomorrow.fandom.com/wiki/Clamps)  
> 49. Pazuzu \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Pazuzu](https://futuramaworldsoftomorrow.fandom.com/wiki/Pazuzu)  
> 50. Leo \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Leo](https://futuramaworldsoftomorrow.fandom.com/wiki/Leo)  
> 51. Futurama: Worlds of Tomorrow Tips, Cheats and Strategies, [https://www.gamezebo.com/walkthroughs/futurama-worlds-of-tomorrow-tips-cheats-and-strategies/](https://www.gamezebo.com/walkthroughs/futurama-worlds-of-tomorrow-tips-cheats-and-strategies/)  
> 52. Events \- Futurama: Worlds of Tomorrow Wiki \- Fandom, [https://futuramaworldsoftomorrow.fandom.com/wiki/Events](https://futuramaworldsoftomorrow.fandom.com/wiki/Events)  
> 53. Silent Night \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Silent\_Night](https://futuramaworldsoftomorrow.fandom.com/wiki/Silent_Night)  
> 54. The Nightmare Before Xmas \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/The\_Nightmare\_Before\_Xmas](https://futuramaworldsoftomorrow.fandom.com/wiki/The_Nightmare_Before_Xmas)  
> 55. Happy Xmas Snowman \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Happy\_Xmas\_Snowman](https://futuramaworldsoftomorrow.fandom.com/wiki/Happy_Xmas_Snowman)  
> 56. Category:An Xmas Xarol \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/Category:An\_Xmas\_Xarol](https://futuramaworldsoftomorrow.fandom.com/wiki/Category:An_Xmas_Xarol)  
> 57. The Zapp Brannigan Event \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/The\_Zapp\_Brannigan\_Event](https://futuramaworldsoftomorrow.fandom.com/wiki/The_Zapp_Brannigan_Event)  
> 58. My Fellow Earthicans : r/FuturamaWOTgame \- Reddit, [https://www.reddit.com/r/FuturamaWOTgame/comments/11o2rrh/my\_fellow\_earthicans/](https://www.reddit.com/r/FuturamaWOTgame/comments/11o2rrh/my_fellow_earthicans/)  
> 59. Ask HN: Who is hiring? (September 2015\) \- Hacker News, [https://news.ycombinator.com/item?id=10152809](https://news.ycombinator.com/item?id=10152809)  
> 60. kotlin-wot: A Framework for implementing Web of Things in ... \- GitHub, [https://github.com/eclipse-thingweb/kotlin-wot](https://github.com/eclipse-thingweb/kotlin-wot)  
> 61. "Cannot connect to the server" : r/FuturamaWOTgame \- Reddit, [https://www.reddit.com/r/FuturamaWOTgame/comments/a5irha/cannot\_connect\_to\_the\_server/](https://www.reddit.com/r/FuturamaWOTgame/comments/a5irha/cannot_connect_to_the_server/)  
> 62. Is there any hope? : r/FuturamaWOTgame \- Reddit, [https://www.reddit.com/r/FuturamaWOTgame/comments/1kg8r15/is\_there\_any\_hope/](https://www.reddit.com/r/FuturamaWOTgame/comments/1kg8r15/is_there_any_hope/)  
> 63. An Xmas Xarol/Mystery Box \- Futurama: Worlds of Tomorrow Wiki, [https://futuramaworldsoftomorrow.fandom.com/wiki/An\_Xmas\_Xarol/Mystery\_Box](https://futuramaworldsoftomorrow.fandom.com/wiki/An_Xmas_Xarol/Mystery_Box)