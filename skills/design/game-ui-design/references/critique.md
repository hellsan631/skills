<!-- Adapted from omer-metin/skills-for-antigravity; rewritten for hellsan631/skills on 2026-10-15. See ../NOTICE and ../LICENSE. -->

# Critique rendered game UI

Critique the designed artifact against its game moment, player fantasy, and intended decision. The relevant [screen pattern](patterns.md) supplies priorities. A clear specification can explain intent; visible frames establish whether the composition expresses it.

## Establish the evidence

Inspect the actual screen, its target size, and the gameplay or menu context around it. For a HUD, use representative game imagery. For a sequence, inspect the designed frames or animation. Record which art, content, and state are final or provisional so a placeholder does not silently determine the verdict.

When only a written description exists, assess the proposed direction and identify the rendered frame needed to judge it. Keep observations separate from predictions about players. A screenshot can show relative scale, grouping, contrast, and imagery; it cannot establish how quickly players learn a system or how a reveal feels in motion.

## Read the composition

First view the screen at reduced size. Identify its dominant subject, strongest contrast, and major visual groups. Compare those observations with the intended focal point. If a secondary control or irrelevant decoration draws attention first, change the composition before polishing components.

Then inspect the intended display size. Follow the eye from subject to decision to consequence. Examine how imagery, typography, spacing, edges, and alignment guide that route. Identify which details reward inspection and which demand attention without helping the current moment.

Read the mechanics expressed by the design. Trace costs to actions, comparisons to candidates, progress to opportunities, and states to their meanings. Look for visual claims the rules do not support: connecting lines that suggest a nonexistent prerequisite, a positive color on a genuine tradeoff, or a selected object that appears already equipped.

Ask which explanations the player could understand from the picture, arrangement, or change in state. Identify what each visual communicates before reading its accompanying prose. Could a connection show sequence, aligned gauges show a difference, or a preview show where an item will land? Moving the same explanation into a tooltip reduces its persistent footprint but leaves the meaning in text.

Inspect objects that combine several meanings. Can the player distinguish identity, configuration, and current state at the intended size? Check whether an added gem, border, or meter has a consistent role and leaves the subject recognizable. Retain short labels where an unfamiliar symbol would require decoding. Read the remaining copy as a player choosing an action; names and descriptions should explain the choice in the game's established vocabulary.

Inspect the identity choices. Name the specific shape, material, mark, image treatment, typographic relationship, or motion that connects the screen to the player fantasy. A genre label alone cannot explain the direction. Check whether those choices repeat coherently across the screen and still leave room for different information roles.

Finally compare the consequential frames: routine and urgent, candidate and committed, anticipation and settled result. The changed emphasis should communicate what happened. Each frame should retain a clear subject and reading order.

## Turn findings into design changes

Use visible evidence and name the visual operation needed. Replace "make it more game-like" with a change to composition, imagery, typography, information grouping, or feedback. These examples illustrate reasoning; they are not universal style rules.

| Visible failure | Why it weakens this screen | Concrete design correction |
| --- | --- | --- |
| The selected card is indistinguishable from its peers. | The current choice has no visible cue. | Preserve accepted peer sizes and positions; distinguish selection through framing, contrast, or a marker. Reserve enlargement for a separate inspection view when it serves that view. |
| Item identity, play style, and comparison are all explained through paragraphs. | Text carries distinctions that could be apparent before detailed reading. | Give the item a recognizable image, silhouette, or typographic identity; group statistics by capability; visualize the relevant difference and retain text for precise meaning. |
| A workload tooltip uses several sentences to explain which component exceeds capacity. | The player must reconstruct the comparison from prose. | Align labeled component gauges with clear capacity marks and visible overflow. Keep the whole-plan summary compact and show the cause on inspection. |
| A composite gauge mixes component colors without showing their separate scales. | A green component can make another component's overload ambiguous. | Give each component a readable scale in the breakdown. Preserve the aggregate's stated meaning and identify the limiting component without relying on color alone. |
| A shield's artwork disappears beneath tiny symbols, meters, and decorative marks. | The combined object loses both recognition and readable detail. | Keep the identity image dominant, give configuration markers stable positions, and move lower-priority detail into inspection. Label unfamiliar symbols until their meaning is established. |
| A choice uses an implementation category as its name and a paragraph to explain its purpose. | The player has to translate the system into an intended action. | Name the choice in the game's vocabulary. Use one sentence for its distinguishing benefit and cost, retaining only details the visuals cannot express clearly. |
| Ornate frames surround every group, but none reflects the game's setting or activity. | Decoration consumes emphasis without establishing a specific identity. | Choose a motif with a role in the world or player fantasy, apply it at a few meaningful structural points, and simplify competing borders. |
| A character screen has a small portrait surrounded by equally prominent controls and statistics. | The character cannot anchor the composition or communicate identity. | Increase the character's visual presence, arrange equipment in relation to the figure where useful, and group supporting values by the decisions they inform. |
| Tree lines imply dependencies that the rules do not have, or every statistic increase is green. | The visual language teaches an incorrect mechanical relationship. | Draw only meaningful connections; show tradeoffs together; use labels or symbols that distinguish improvement from a change whose value depends on the build. |
| A reward appears as another list row and the sequence has no change in emphasis. | The design gives little visual weight to an event the game treats as significant. | Create a reveal frame around the earned subject, show why it matters, then settle into a readable result. Scale the treatment to the event's importance and frequency. |
| A combat objective banner is the strongest shape and covers the area where enemies telegraph attacks. | Secondary reading competes with immediate anticipation. | Move or compact the objective group, lower its persistent emphasis, and reserve stronger treatment for a change that demands action. |

## Revise and show the result

Prioritize the change that most affects the focal subject, comprehension of the mechanics, or intended feeling. Make it in the artifact before refining smaller details. Revisit the same frame after the change so the claimed improvement can be compared directly.

Report the artifact first, then the consequential design changes with visible evidence: what drew attention before, what draws it now, and why that serves this game moment. Name any unresolved constraint, such as unavailable character art or a storyboard whose timing has not been animated. Stop at the evidence available; claim visual progress only for the frames inspected.
