---
name: visual-identity-grilling
description: Use when the user wants to quickly iterate on game visual identity through challenging questions and rendered comparisons, or asks to combine grilling with character, icon, or asset-family design.
---

# Visual identity grilling

Reach a shared visual direction through short rounds of questions, art, and feedback. Each round should settle a consequential choice or produce a visible revision that tests it. Keep accepted decisions stable as the work becomes more specific.

This skill adapts the decision tree and recommendations from `grilling` to visual exploration. Work from `game-visual-identity` when available for detailed pillar alignment, asset guidance, and production checks. Use the round boundaries here for interviewing and iteration. The workflow below also works when those skills are unavailable.

## Frame the next decision

Inspect the brief, accepted art, and recent feedback. Establish the asset family and the current goal: choose an overall direction, distinguish family members, or refine an existing candidate. Find environmental facts yourself; delegate independent research when it helps. Ask the user for decisions that require their judgment.

Map only decisions that affect the requested outcome. Global game pillars describe the player experience and priorities. Local family pillars describe how appearance expresses those priorities. Visual rules and individual asset choices depend on them. Mark consequential decisions as agreed, proposed, or open, and retain rejected directions when they explain a constraint.

Reuse existing agreements. When pillars are missing, propose a small set grounded in the game context and make their visual consequences concrete. State reversible assumptions so rough studies can begin before every detail is settled. If an unresolved fact or decision would invalidate the next study, resolve that prerequisite first.

The next round is ready when it has a named decision, a representative subject, and enough context to create useful evidence.

## Make the choice visible

Use inspected references or existing variants when they already expose the decision. Otherwise, render the smallest useful study. A brief with sufficient context can start with images; a missing foundational choice may need one short question round first.

For a broad direction, two or three contrasting candidates often make the tradeoff clear. Keep the subject, viewing conditions, and finish comparable. For refinement, a focused before-and-after comparison is usually enough. Use labels the user can refer to. Include every asset class needed to support the current claim, such as a portrait and an icon when evaluating a shared direction for both.

Generate or edit raster studies with image generation tools, using `imagegen` for tool-specific guidance when available. Use native vector tools for vector artwork. If rendering is unavailable, state that limitation and keep written proposals explicitly unrendered. A prompt alone does not establish visual quality.

Inspect the actual result at the intended display size and on a representative background. Identify the visible evidence for the recommendation and its cost. Connect the comparison to the relevant global and local pillars. When a user decision remains, advance to the question once the alternatives make its consequences visible.

## Grill the consequential choice

Default to one decision per round; group up to three independent choices when that reduces back-and-forth. Ask only questions whose prerequisites are settled. Keep questions dependent on pending research or another answer for a later round.

For an unresolved user decision, show the comparison, then give a numbered question, the options, and a recommended answer with its reason. Use the available question UI or a compact numbered prompt. Prefer questions about visible consequences: which silhouette expresses the role, where detail should concentrate, or which quality must survive simplification.

Challenge contradictions directly and constructively. For example, explain when preferred ornament competes with an agreed readability goal and show how reducing it changes the image. Offer a resolution and accept an informed tradeoff. Keep accepted global intent in force unless the user chooses to revise it.

When a choice needs the user's answer, deliver the current comparison and wait before doing dependent work. Continue independent fact-finding while waiting. Silence and preselected options do not settle a decision. Existing delegated choices remain delegated, so the agent can make those decisions and explain them without another approval round.

## Turn feedback into the next image

Extract what to keep, what to change, and what remains uncertain. Translate feedback such as "too busy" into a visible cause: competing contrast, dense marks, repeated ornaments, or unclear hierarchy. Preserve what the user liked.

Apply a clear refinement request directly. Ask a follow-up when plausible interpretations would produce materially different art. A mixed preference can become a deliberate combination, and rejecting every option calls for a new direction. Do not force the user to choose a failed candidate.

Revise the most consequential mismatch, inspect the result, and show the change. Every additional render must answer a named open decision or implement requested feedback. Recompute the remaining decisions from the latest answer instead of restarting the interview.

For example, "B has the right personality; simplify it but keep the crooked hat" calls for preserving B's identity and hat while reducing competing detail. The next useful result is that revision.

## Keep the outcome and stop

When the direction will be reused, create or update its family record beside the project art as decisions settle. Keep the selected images, the reason for consequential choices, the agreed visual rules, and the next unresolved decision. Distinguish user decisions from proposed interpretations. Link to global pillar definitions and keep local rules beside the family art.

Stop when the requested decision or artifact is satisfied and the user has selected the direction or delegated that choice. Deliver the selected visual, a compact account of its reusable rules, and any material limitation. If the comparison still needs an answer, end the round with that decision pending. Production work proceeds when requested; exploration does not require visiting every possible design branch.
