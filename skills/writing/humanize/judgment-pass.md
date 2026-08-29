<!-- humanize-lint: ignore-file list-density -->

Run this workflow after `humanize_lint.py` reports zero errors. Handle all twelve questions in order.

1. What does each sentence tell the reader? Delete words that do not change the answer. If the answer is nothing, delete the sentence unless it is the only statement of a requirement. Ask what must happen before rewriting an unclear requirement. Split the sentence only when the replacement leaves two complete statements.

2. Are flagged words doing real work? Remove the flagged word and read the claim again. Leave it out when the sentence still says the same thing. Otherwise, find what the word refers to in the source and say that directly. Ask the author when the source never explains it and the claim depends on it. Keep a domain term when the source uses it precisely.

3. Is the register held steady? Compare the first and last paragraphs of the draft. Confirm they aim at the same level. Keep the overall grammar quality as constant as possible and match the medium (web log entry, op-ed, etc.).

4. Is every significant claim and judgment supported? Evidence can come from supplied sources or from the original text itself. Ground an editorial judgment in a fact the reader can identify. Put the reason beside the judgment when that connection is unclear. Remove a claim when no source supports it.

5. Is anything invented? Compare the draft line by line with all source material. Check names, dates, numbers, and quoted text first. Then account for every added actor, action, motive, mechanism, and consequence. Specificity does not license filling a gap.

6. Did the rewrite lose anything the document depends on? Keep verifiable facts, caveats and conditions, scope boundaries, and intentional hedges.

7. Does each heading, bullet list, and table earn its place? Every heading should denote a separate topic. Use lists for parallel items. Use tables when rows share a stable set of columns.

8. Is each technical label defined or doing more than repeating nearby prose? Keep it when the document defines it, the code uses it as a name, or the author says the intended readers already know it. Test every other label by removing it and rereading the passage. Leave it out when the meaning stays the same, and change only the grammar affected by its deletion. Repeating a label does not explain it. Keep the same name for a person or thing throughout the passage.

9. Does the draft give software a human trait such as honest, smart, or thoughtful? Replace the trait with the action or result it refers to in the source. Delete it when nearby text already says the same thing. If the trait is the only statement of a requirement, ask what the software must do.

10. Does an opinion have support? Only add one when the source supports it, and put the supporting fact beside it. In neutral reference writing, use details specific to the subject.

11. Does the draft stop after its final point? Remove a recap or generic prediction. End after the last claim the source supports.

12. What does each contrast assert? `Not just X, but Y` says that both claims are true. Write `X and Y` when both matter, or Y alone when X adds nothing. Removing only `just` reverses the first claim. For bare `X, not Y`, keep Y when removing it changes the document's meaning or a requirement and no nearby sentence already states it. A separate `Do not Y` sentence still needs the same test. Use that command only when the source states a prohibition; otherwise keep a descriptive exclusion descriptive. State `X rather than Y` and *however* pivots directly when the comparison adds no fact from the source.

## Delegating this pass

You may delegate the pass to a subagent, regardless of draft length or audience. Provide the draft, the path to this file, the medium, and the audience. Request findings only, formatted as `line: problem: suggested fix`. Apply the fixes, then re-run the checker because a fix can reintroduce a mechanical tell.