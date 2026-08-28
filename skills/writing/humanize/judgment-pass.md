<!-- humanize-lint: ignore-file list-density -->

Run this workflow after `humanize_lint.py` reports zero errors. Handle all twelve questions in order.

1. What does every claim add? Mark wording that sounds deliberate or insightful but names no fact, instruction, position, or relationship. Choose the smallest repair that carries the meaning: delete empty words, substitute a precise word or clause, or explain a mechanism found in the source. No repair has a minimum length.

2. Are flagged words doing real work? Remove the flagged word and read the claim again. Delete it when the meaning survives. Name the specific action or relationship when the word hides one. Keep a domain term when the source uses it precisely.

3. Is the register held steady? Compare the first and last paragraphs of the draft. Confirm they aim at the same level. Keep the overall grammar quality as constant as possible and match the medium (web log entry, op-ed, etc.).

4. Is every significant claim and judgment supported? Evidence can come from supplied sources or from the original text itself. Ground an editorial judgment in a fact the reader can identify. Put the reason beside the judgment when that connection is unclear. Remove a claim when no source supports it.

5. Is anything invented? Compare the draft line by line with all source material. Check names, dates, numbers, and quoted text first. Then account for every added actor, action, motive, mechanism, and consequence. Specificity does not license filling a gap.

6. Is any load-bearing content lost? Keep verifiable facts, the caveats and conditions on claims, clear statements of the scope boundaries around your information, and intentional hedges. They are all content that you should keep.

7. Does each heading, bullet list, and table earn its place? Every heading should denote a separate topic. Use lists for parallel items. Use tables when rows share a stable set of columns.

8. Does every technical label have a stable meaning? A compound such as `capability-oriented` is a real term only when the document defines it, the code names it, or the audience already shares its meaning. When nearby prose states the behavior, use that behavior and remove the label. Repetition alone does not establish a term. Keep person and pronoun choices steady, and avoid ornamental synonym cycling.

9. Is a phrase performing clarity instead of saying what it means? Human virtues applied to software often hide a technical claim. For "keeps the process honest," use any operation or consequence stated in the source. Delete the phrase when nearby text already carries its meaning or when it adds no unique content. Flag it for clarification when it is the only statement of a required property. A word or clause may be the complete repair.

10. Is there a person behind this text? Where the medium allows opinion, check that each position, admitted tradeoff, or preference has a reason. Opinion is optional. In neutral reference writing, use details specific enough that the prose could belong only to this subject.

11. Does the ending land? It lands when it stops after the point with no recap or forward-looking speculation, and it lands when the final paragraph completes an idea without trailing off.

12. Does every contrast carry required content? Explanatory prose should lead with the affirmative mechanism. Keep a negative clause when it states a source-backed exclusion, constraint, safety rule, or correction. For rhetorical `X, not Y`, `X rather than Y`, and *however* pivots, write the useful claim directly and explain its mechanism with only the text it needs.

## Delegating this pass

You may delegate the pass to a subagent, regardless of draft length or audience. Provide the draft, the path to this file, the medium, and the audience. Request findings only, formatted as `line: problem: suggested fix`. Apply the fixes, then re-run the checker because a fix can reintroduce a mechanical tell.