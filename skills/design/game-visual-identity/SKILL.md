---
name: game-visual-identity
description: "Develops a recognizable visual identity for video game characters, icons, items, and related art. Use to align global game design pillars with local asset-family pillars, explore art directions, interpret visual references, or extend an established asset family. Focuses on asset appearance and consistency; screen layout and character lore alone belong elsewhere."
---

# Game visual identity

Develop visible art that makes the game's subjects recognizable and gives them a shared visual language. Carry useful decisions from exploration into repeatable assets. A successful direction explains both what stays consistent across the game and how individual characters, abilities, or items remain distinct.

Match the deliverable to the request. Visual exploration needs rendered comparisons. An established style needs matching assets. A brief, critique, or prompt set can stand alone when the user requests it. Keep each game's art decisions in its project, so this skill remains reusable.

## Establish the visual problem

Inspect the supplied images, relevant project instructions, accepted art, and recent feedback. Distinguish current decisions from experiments and superseded versions. A file named `final` does not establish user acceptance.

Identify the subject's gameplay role, intended feeling, viewing angle, display size, surrounding art, and requested output. For early exploration, state reasonable assumptions where these are unknown. Ask only about missing information that would materially change the direction; a small asset request does not need a full art interview.

Summarize what to keep, what to explore, and what to avoid. Preserve content and game meanings during visual exploration. Changes to ornament, color, or framing must not accidentally imply new rarity, faction, ability, or state rules.

Choose the relevant guidance:

- For characters, creatures, portraits, and roster consistency, read [character identity](references/characters.md).
- For ability icons, items, emblems, and symbol families, read [icon identity](references/icons.md).
- For other assets, apply the shared workflow and the closest relevant guidance. Do not load every reference by default.

## Align global and local design pillars

Start with the game's accepted overall design pillars. These describe the intended player experience and the priorities that guide tradeoffs. Establish local pillars for the relevant product or asset family, such as character portraits, ability icons, or collectible items. Local pillars define how that family should look and how its appearance supports the global intent. Different families can express the same game pillar through different visual choices.

Give each pillar a concrete meaning, a reason, and a consequence for design decisions. Name what it prioritizes when choices compete, then describe a visible result that would support or violate it. Separate the pillar from its implementation. For example, a global priority of readable tactical decisions might lead an ability-icon family to prioritize distinct action silhouettes, expressed through one dominant motif and limited background detail.

Before settling a new direction, show the user a concise connection from global pillars to local pillars to proposed visual choices. Resolve material uncertainties with the user. Existing agreements and delegated decisions count as alignment; do not reopen them for routine assets. If pillars are missing, propose a small set from the supplied game context and label them as proposed. Rough visual studies can make these choices concrete while alignment is pending.

When a local direction conflicts with a global pillar, explain the tradeoff and recommend a resolution. Keep the accepted global intent in force unless the user chooses to revise it. Do not silently redefine it to accommodate an attractive reference. Conflicting global pillars also need an explicit priority for the decision at hand.

## Turn references into a direction

Inspect the images themselves before describing their visual qualities. For each useful reference, name the qualities to borrow and the qualities to leave behind. Illustration, silhouette, rendering, framing, background, and information placement can come from different sources. Record links or local paths so future work can inspect the same evidence.

Define the visible decisions that matter to this task: shape language, proportions, value grouping, color roles, materials, edge treatment, and detail density. Explain how major choices express the agreed pillars in this subject and gameplay use. Replace labels such as "stylized fantasy" with drawable instructions. For example, "broad shoulders, one tall vertical accessory, two large shadow masses, and sharp detail concentrated at the face."

Separate shared style rules from subject identity. A cast can share brushwork, proportions, and lighting while each character keeps a different silhouette and signature feature. Similar colors alone do not establish a coherent style.

Keep asset art and interface treatment distinct unless the request covers both. Borrowing a painted subject does not imply borrowing its card border or surrounding website palette.

## Explore and refine

When direction is unresolved, compare a small set of meaningfully different candidates. Keep representative subjects, viewing conditions, and level of finish comparable so the differences can be judged. Vary consequential choices such as proportions, silhouette, value structure, material treatment, or mark density. Palette swaps alone are usually color exploration.

Use a representative sample appropriate to the request. For a shared character-and-icon direction, include both before claiming that the style works across them. For a single character or icon, keep the exploration focused on that asset.

Create the requested visuals with the available tools. Use the installed `imagegen` skill and built-in image generation for raster concept art and image edits. Use native vector tools or source files when the requested deliverable is vector artwork or extends an existing vector family. Read current tool instructions instead of assuming model names or parameters. If rendering is unavailable, deliver the useful brief or prompts and identify the work as unrendered.

Label reference images by purpose in generation instructions: subject identity, rendering style, composition, or edit target. Keep the identity requirements explicit when changing pose, costume, lighting, or framing. For edits, state the intended change and the features that must stay fixed.

Inspect the actual outputs before judging them. Compare candidates at the intended display size and on a representative background. Explain the strongest visible differences and recommend a direction based on how it serves the agreed global and local pillars. Name any tradeoff. Follow an existing selection or delegated choice without asking again. Until the user selects a direction or delegates selection, keep recommendations provisional and continue useful exploration within the requested scope.

Refine the most consequential mismatch while preserving the successful features. For a request to simplify, examine mark density and contrast as well as object count. Removing props will not help if every remaining fold and strand still competes for attention. Keep iteration proportional to the request; report unresolved defects instead of continuing generation indefinitely.

## Preserve the identity for reuse

When a direction will be reused, save a compact record beside the relevant project art. Follow existing project organization and update the current record instead of creating a competing style guide. Keep global pillar definitions in their existing project source and link to them from family records. Keep local pillars beside the family they govern. Include only what later work needs:

- The direction's status, accepted or proposed, and any user selection that established it.
- Applicable global and local pillars, their sources, alignment status, and any resolved priorities or exceptions.
- Reference images and representative outputs with their intended uses.
- Shared visual rules and how consequential choices support the pillars.
- Features that define each subject, plus allowed variation and known failures to avoid.
- Prompts or editable sources needed to continue the work, and known display or export requirements.

Use an accepted image as a visual anchor when extending a family. A repeated text prompt alone is weak evidence of consistency. Check new assets against the anchor and against neighboring assets. Shared treatment must preserve differences between subjects.

## Verify and deliver

Review recognizable shape, focal hierarchy, subject differences, style consistency, and fit at actual use size. Check whether the rendered art expresses the agreed global and local pillars, using visible evidence for each relevant claim. Check value and silhouette where they carry identity. Meaningful distinctions need cues beyond color. State which checks were actually performed; an image prompt or written description is not proof of the resulting pixels.

For production deliverables, verify requested file type, dimensions, framing, padding, and transparency. Request real alpha for transparent artwork. A checkerboard painted into an image is not transparency. Keep comparison sheets separate from individual runtime assets. A concept image does not establish animation, rigging, vector editability, or import readiness.

Show the resulting visuals and link saved files. Briefly explain the visual decisions, changes made during refinement, and unresolved issues. Save project-bound deliverables in the project. Keep new experiments separate from accepted assets unless replacement was requested. Update consuming code only when integration is part of the task.
