---
name: game-ui-design
description: Use when designing or redesigning game HUDs, menus, inventories, character screens, maps, progression screens, or results screens; when making text-heavy game UI more visual; when creating composition, art direction, visual hierarchy, and interaction storyboards.
disable-model-invocation: true
license: Apache-2.0
---

<!-- Adapted from omer-metin/skills-for-antigravity; rewritten for hellsan631/skills on 2026-10-15. See NOTICE and LICENSE. -->

# Game UI design

Design game screens whose composition, imagery, typography, and feedback express the game's activity and player fantasy. Deliver the rendered design and the consequential states needed to understand it. Use a short rationale to explain choices visible in the work.

This skill is for design work: concepts, screen layouts, visual direction, mockups, and interaction prototypes. A prose specification is the deliverable only when the user asks for one. Use the available design tools to make the screen visible. If rendering is unavailable, identify the result as an unrendered proposal.

## What good game UI focuses on

### The game activity determines the composition

Identify what the player is doing: reacting, navigating, comparing, planning, expressing a character, or celebrating a result. Let that activity determine the layout. A combat HUD preserves the scene and supports short glances. A planning screen can hold related choices together for deliberate comparison. A reward screen can make an earned item or achievement the dominant subject.

Name what the player should notice first, what they inspect next, and what they can do from there. Use this order to decide which elements receive space, contrast, detail, and motion. Avoid importing the same panel arrangement into every screen family.

### The layout expresses the mechanics

Use position, grouping, connections, and sequence to show how the game works. Place a cost beside the choice it enables, a candidate item beside what it replaces, and a prerequisite on the path to its unlock. Distinguish ownership, selection, availability, and investment when they mean different things.

Choose a spatial structure that matches the relationship. Slots express equipment assignment; a tree expresses development or dependency; a list supports repeated comparison; a map expresses location. A decorative connector must not imply a mechanical dependency that does not exist. Make the important relationship understandable before the player opens a tooltip.

### The player fantasy guides art direction

Describe the role and moment precisely enough to choose visual devices. A field commander allocating scarce resources, a collector admiring a rare creature, and a performer receiving a score need different emphasis even within one world.

Translate that direction into imagery, shape, material, type, color roles, and motion. A cartographer's map may use route markings and marginal notes; a tournament broadcast may use bold standings, team insignia, and a score reveal. Choose devices that reinforce the activity. Genre labels and a dark palette alone leave the design undecided.

### Compose a screen with a focal subject

Decide what owns the frame: the playable scene, a character, an item, a map, a build, or an accomplishment. Establish a dominant visual mass, supporting groups, and quiet space. The subject may be a mechanical arrangement such as a build tree; large character art is useful when it serves this screen.

Vary scale, value, silhouette, alignment, and density to create the reading order. Reserve the strongest accents for the current choice or event. Keep supporting frames and textures subordinate to the content they organize. At thumbnail size, the main subject and hierarchy should still be recognizable.

### Visuals carry information

Identify what each explanation tells the player: identity, sequence, quantity, capacity, configuration, or consequence. Choose a visual relationship that communicates that meaning. An arrow can show the next step; a socket can show an assignment; aligned gauges can reveal which demand exceeds capacity. Moving the explanation into a tooltip still leaves the player reading it.

Use the [visual information patterns](references/patterns.md#visual-information-and-compression) when a screen depends on prose or repeats information. Keep short names and exact rules where pictures would be ambiguous. A collection of unfamiliar symbols can demand more interpretation than a sentence.

### Information density serves the decision

Combine related information into a recognizable object when its parts remain distinguishable. Artwork can identify a build, socketed emblems can show its configuration, and a marking can show its state. Give each part a stable position and meaning. Keep the object recognizable at its actual display size; separate details when the combination becomes crowded or ambiguous.

Keep related values visible together when the player must compare them. Show the overall result in the overview and its contributing parts on inspection. Retain enough information to choose without opening every object. Remove repeated explanations, and judge tooltips by the same visual standard as the main screen.

Treat deliberate uncertainty as part of the design. A player may need to recognize a strategic role while discovering its exact interactions through play. Expose what makes a choice intentional without inventing certainty the game does not provide. Judge empty space and density by the work the player needs to do.

### Text uses the player's concepts

Name choices by the action, role, or outcome the player recognizes in this game. Keep established terminology consistent across the object, chooser, and inspection. Check examples against the game's actual mechanics; a reference game's technology or units do not establish what exists here.

When a choice needs explanation, use one sentence that states what it does and the consequence that matters for choosing it. For example, "Attack before the enemy builds up, at the cost of a smaller economy." Keep necessary uncertainty labels short. Put calculation methods in design notes unless the player needs them to decide.

### Feedback gives an action weight

Design how attention lands on a choice, what a preview reveals, and how the screen changes after commitment. Equipping can update the visible character and comparison; investing can illuminate a path and change the remaining budget; a reward reveal can resolve into a stable summary.

Use changes of scale, value, position, and motion to explain the event and its importance. Differentiate a routine selection from a major unlock. Show key before-and-after frames or a short interaction sequence. Keep the result understandable when motion is reduced, and let repeated actions reach their useful state promptly.

## Design the screen

### Establish the moment and constraints

Inspect the existing game, supplied brief, accepted screens, and available assets. Identify the screen's place in the game loop, the player's role, intended feeling, meaningful choice, input method, and target dimensions. Carry forward the project's accepted visual language unless redesign is requested.

State the intended experience in one concrete sentence, then list only assumptions that affect the design. Ask about missing facts that change the direction; make ordinary visual decisions yourself. Scale the exercise to the request: a component change does not require a new art direction.

### Study and choose a direction

Inspect relevant reference images when available. Name the particular composition, typographic relationship, asset treatment, or interaction worth borrowing and why it fits this game. Use the case studies in [design sources](references/sources.md) when choosing references. A game title is not a visual brief.

Define a small set of visible choices: the focal subject, layout structure, type roles, shape language, palette roles, and asset treatment. Identify the character render, item art, map, icons, or background that the composition depends on. Use existing assets where suitable; create or source missing art when tools allow it. Mark provisional art so it can be judged at the right level of finish.

When the composition is unresolved, explore distinct rough arrangements before polishing one. Vary the focal subject or relationship between regions, not merely the colors. Choose the arrangement that best expresses the activity and intended feeling, then develop it.

### Render and develop the design

Work from the relevant [screen patterns](references/patterns.md). Build the composition with representative content and the art it needs. Establish large shapes and visual emphasis before refining typography, icons, materials, and fine spacing. For a HUD, compose over gameplay imagery or a clearly identified scene mockup.

Make the important choice and its consequence visible. Design the states that change the composition or the meaning of a control, such as selection, preview, equipped, locked, and earned. Show them as frames, overlays, or a prototype. Match the depth of interaction design to the request.

Design for the intended input and viewing conditions. Keep labels, focus, and meaningful state distinctions readable; fit long names and enlarged text without losing the central choice. Treat these as constraints on the composition while preserving its character.

### Critique the rendered work and revise

Inspect the actual result at thumbnail size and intended viewing size. Apply [design critique](references/critique.md) to its focal hierarchy, mechanical relationships, fantasy, visual coherence, density, and feedback. Identify the strongest mismatch between the intended experience and the visible screen, make a concrete design change, and inspect it again.

Finish with the rendered artifact, a brief explanation of the consequential design choices, and any unresolved asset or interaction limitations. A written rationale cannot establish visual quality. When improving this skill itself, compare its generated screens using [visual evaluation](references/evaluation.md).
