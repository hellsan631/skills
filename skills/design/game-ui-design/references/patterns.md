<!-- Adapted from omer-metin/skills-for-antigravity; rewritten for hellsan631/skills on 2026-10-15. See ../NOTICE and ../LICENSE. -->

# Design priorities by game screen

Choose the relevant screen family, then adapt its composition to the actual mechanics, art direction, and pace of play. These are design decisions to resolve in rendered frames. Review the result with [rendered critique](critique.md).

## Visual information and compression

Use these patterns when explanations dominate the screen or the user asks for a more visual treatment. Start with the meaning the player needs, then choose how to draw it. Reducing word count alone can leave the same reading burden or remove the distinction that made a choice understandable.

### Match the representation to the meaning

| Meaning | Visual treatment | Keep clear |
| --- | --- | --- |
| Identity | Recognizable artwork, silhouette, or emblem | Preserve established motifs; retain a short name for unfamiliar subjects. |
| Sequence | Aligned objects with directional connections | Arrows must express the actual order; a sequence is different from branching prerequisites. |
| Assignment | An item seated in its socket or attached to its owner | Show the relationship directly instead of repeating it in an adjacent list. |
| Quantity or capacity | Length, fill, countable chunks, and a capacity marker | Define the unit and scale so the visual supports comparison. |
| Difference or tradeoff | Aligned comparisons with the changed capability and cost visible | Show what the player gains and sacrifices when the rules establish both. |
| Fit | Current values positioned against requirements | Mark the shortfall as well as its color; preserve uncertainty in estimates. |
| Action preview | A ghost of the resulting object in its destination | A dragged card can reveal its actual banner or socket before the player drops it. |

The [illustrated examples](visual-information.svg) turn a sequence into connected objects and a capacity explanation into segmented bars. Their geometry teaches the relationship; their short labels keep the meaning explicit. These are schematic examples, not a proposed art direction or evidence of player comprehension.

Use position and length for quantities the player must compare precisely. Use shape and artwork for identity. Color can reinforce status, but give a critical state another cue such as a marker, icon, or value. Keep learned meanings stable: a gem that identifies an assignment should not also change meaning to indicate selection.

### Combine information around the object

A build shield can carry its identity in the artwork, its chosen assignments in socketed gems, and its workload in edge markings. The combination earns its space when players can distinguish those meanings without a nearby paragraph explaining the arrangement. Preserve the accepted asset treatment when adding marks so they belong to the object.

Give peer objects consistent geometry and align comparable details. Selection can use an outline or focus cue while the shield keeps its size. Inspect the combined object beside its peers at actual display size. If the gems merge into the artwork or the markings obscure the silhouette, reduce their prominence or move a secondary detail into inspection.

Compare three treatments when compression is uncertain: a text-heavy object, a bare object with unclear symbols, and a composed object with enough labeling to identify its parts. Keep the same decision-relevant information in the comparison. The useful middle treatment preserves both recognition and meaning.

### Make inspection visual too

Give the overview the result the player is judging. Use inspection to show the contributing parts. For a combined technical demand, two aligned gauges labeled "APM" and "Attention" can expose the overloaded component. A paragraph describing those two readings adds reading without improving the comparison. Use a short explanation only for a relationship the graphic cannot express reliably.

Apply the same restraint to choosers. Show recognizable options with matching dimensions and a short name; add one sentence when their difference needs explanation. A compact chooser can hold a growing unit catalog beside its tree node while the tree retains the strategic relationships. Add search when locating an option becomes a real task. Keep the current configuration recognizable when the chooser closes.

### Give gauges a stable meaning

Specify the measured quantity, capacity, amount per segment, color bands, and overflow behavior before drawing a segmented meter. For fixed-value chunks, keep the amount per chunk constant as capacity changes. When the bar has a fixed overall width, more chunks occupy less width each. Show capacity separately from demand so overflow remains visible, and retain an uncapped value when the ratio can exceed 100%.

Choose a whole-chunk rounding rule and keep each filled chunk a solid color when using an RPG health-bar treatment. The exact label can preserve precision between chunk boundaries. Explain the scale on inspection when needed. Keep thresholds and formulas in the game's design reference; the illustration's values are examples.

For a combined gauge, use the game's aggregation rule and expose its components where the player inspects it. Check the case where one component is overloaded and another is comfortable. The summary must communicate the supported conclusion without suggesting that spare capacity in one component automatically solves the other.

## Action HUD

Let the playable scene own the composition. Identify where the player watches movement, anticipates threats, aims, or reads an opponent. Place persistent groups around that activity using a representative scene, including terrain and effects. Empty corners in a blank mockup provide little evidence about the eventual composition.

Make the game's moment-to-moment relationships visible. Group an ability with its readiness, cost, and input when those facts inform the same action. Distinguish quantities that support anticipation from signals that demand an immediate response. A regenerating shield and a scarce healing reserve may need different emphasis because losing them has different consequences.

Create a stable visual grammar for ready, active, depleted, and threatened states. Choose differences in silhouette, fill, contrast, and emphasis that remain recognizable during a glance. A pulse or flash needs a specific meaning; reserve strong changes for events that warrant redirecting attention. Show damage direction near the relevant spatial cue when direction changes the player's response.

Keep identity in the shapes, marks, textures, and motion that survive the intended viewing scale. A cockpit instrument panel can be dense and expressive; an exposed landscape may benefit from sparse markings. The game's activity determines which treatment fits.

Show a routine-play frame and a pressure frame. The difference should reveal what becomes urgent while the scene and learned HUD locations remain readable. Judge whether the player can anticipate the next meaningful action from the displayed relationships.

## Planning, loadout, and inventory

Compose around the current choice. Give the selected item, unit, or build enough visual presence to establish what the player is considering. Its name, appearance, capabilities, and role should reinforce each other. Artwork, silhouettes, diagrams, and typography can each supply that presence; choose what fits the game and available material.

Arrange comparisons around the tradeoff. Keep current and proposed values close, aligned, and expressed in matching units. Distinguish improvement from preference: more damage with slower recovery is a different decision from a strict upgrade. Explain consequences only when the game's rules support them. Group secondary statistics under the capability they describe so a wall of numbers does not carry the entire explanation.

Choose a list when names and comparable values drive selection. Use a grid when item recognition, spatial arrangement, or collection matters. Cards work when each candidate needs its own image and concise proposition. Vary emphasis between the selected subject, alternatives, and supporting controls so repeated components preserve the screen's hierarchy.

Connect equipment to build identity. Show which slots, item combinations, resources, or restrictions constrain the choice, using the relationships the game actually has. A unit portrait, weapon diagram, or compact role summary can make the resulting build easier to understand than isolated item statistics.

Design a selection frame and a proposed-change frame. The viewer should see what would change, what is gained or sacrificed, and which element owns the current choice. Preserve stable comparison positions as selection changes.

## Progression and talent trees

Choose the spatial model from the progression decision. A branching tree can reveal prerequisites and divergent commitments; a track can express a sequence; a board can support independent purchases. Decorative connecting lines imply dependencies, so every connection needs a mechanical meaning.

Establish the relationship between current investment, reachable upgrades, and later build options. Give the next reachable choices enough presence to invite inspection while keeping the wider build legible. Use scale or grouping to distinguish a build-defining unlock from incremental bonuses when the rules make that distinction.

Design acquired, available, selected for inspection, and blocked by prerequisites as distinct states. Show the cost and consequence at the point of consideration. A preview can trace the prerequisite path and proposed spending without visually claiming that the purchase has happened.

Preserve intended mystery. Undiscovered branches may need silhouettes or partial information; known dependencies still need enough explanation to support an informed commitment. The reveal itself can become a designed moment when discovery matters to the game.

Show the overall progression composition and a focused choice with its path. The viewer should be able to distinguish where they are, what they could pursue next, and why that direction changes their character or options.

## Maps and exploration

Decide whether the player is steering, planning a route, remembering a place, or discovering the world. A compass can prioritize bearing; a local map can explain nearby connections; a regional map can communicate geography and alternatives. Match the amount of geography to the decision.

Art-direct the map as a representation of this world. Its coastline, terrain, landmarks, lettering, and marks should share a visual language. A survey chart, hand-drawn travel journal, and tactical scan imply different knowledge and different player roles. Keep route information and location labels legible within that treatment.

Use landmark silhouettes, region shapes, and spatial relationships to help places become recognizable. Give the player, inspected destination, and chosen route distinct emphasis. Resolve dense marker clusters through grouping or level of detail so the map's geography still has visual presence.

Make discovery rules visible. Distinguish known paths, uncertain areas, visited places, and inferred destinations only where those categories exist. Show vertical separation and route constraints when a flat view would imply a connection the player cannot travel.

Render an exploration view and a route-consideration view. Judge whether each communicates location and possibility, whether the world remains recognizable, and whether the map reveals the intended amount of knowledge.

## Character, reward, and results

Choose the emotional subject: this character, this earned object, or this accomplishment. Give it visual ownership through scale, placement, light, framing, or typography. Supporting numbers should explain the subject's significance. A character screen may need equipment and identity in the same composition; a results screen may make the performance itself the spectacle.

Tie emphasis to meaning. Show what was earned, what caused the result when that information is available, and what becomes possible next. A rare object needs a treatment consistent with the game's rarity language. A personal best, failed objective, and routine completion should produce different focal arrangements when they represent different emotional moments.

Design a short reveal sequence when anticipation or celebration serves the game. Establish the subject, reveal its significance, then settle into a readable result with the next action available. Timing and intensity should fit the frequency of the event: a repeated match result and a major campaign milestone deserve different pacing.

Use a storyboard to show the reveal and the settled frame. Include a reduced-motion composition that preserves the result and hierarchy. Judge whether the screen makes the moment feel earned and whether its final frame remains useful after the spectacle ends.

## Title, main menu, and pause menu

Treat the title screen as a promise about the game's experience. Compose scene, emblem, character, typography, or abstract imagery around that promise. Identify the visual idea that will remain recognizable when the game's title is covered. Elaborate illustration is optional; a precise typographic or symbolic composition can carry the direction.

Place the menu within the composition with enough separation from its background to read. Choose whether the art frames the choices, shares their alignment, or occupies a separate visual mass. Preserve the subject's silhouette and the menu's reading order as selection changes.

Prioritize the player's reason for arriving. A first visit may foreground beginning the experience; returning play may foreground continuing. A pause screen should preserve orientation to the interrupted activity and make resuming easy to locate. Settings and secondary destinations should fit this hierarchy without competing for the same emphasis.

Render the landing frame and one selected state. Judge whether the game's tone is apparent, the intended entry point has appropriate prominence, and the selected state belongs to the screen's art direction.
