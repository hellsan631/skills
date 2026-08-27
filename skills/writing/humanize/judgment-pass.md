Now Prompted workflow: run after humanize_lint.py reports zero errors. Twelve questions must be handled in order.

1. Is every sentence providing real information? You're looking at a question that humanize_lint.py only knows how to answer by listing filler. The answer could be "nothing" if you're looking at an empty content block, such as a single-line paragraph; so if the answer is "nothing," delete the sentence (or if it starts with something like [fn][1], delete the entire paragraph).

2. Are flagged words doing real work? When you see a flagged word, you have a choice to rename it as something more generic. You want to test whether the new generic term does its job. Delete the new word entirely and see if the sentence still survives on its own merits. Similarly with any other renamed terms.

3. Is the register held steady? Compare the first and last paragraphs of the draft, making sure they aim at the same level. Keep the overall grammar quality as constant as possible, matching the medium (web log entry, op-ed, etc.).

4. Is every significant claim being supported? If the evidence for a significant claim isn't in the surrounding text, consider removing the claim (don't invent a reason to justify it!). Every community carries some expectations about what kind of evidence is sufficient.

5. Is anything invented? Line by line, compare against your source material. In particular, this is the place to zero in on names, dates, and numbers that are concrete details, and on directly quoted material. The replacement of vague general praise with specific, concrete details, such as turns out to be the source of invention information.

6. Is any load-bearing content lost? Keep verifiable facts, the caveats and conditions on claims, clear statements of the scope boundaries around your information, and intentional hedges. They are all content that you should keep.

7. Does each heading, bullet list, and table earn its place? Every heading should denote a genuinely separate topic. Lists should usually be used when you want to group together genuinely parallel items. Tables are for genuinely tabular material. If you're working with them (as this varies per output format), you'll know when that material is truly tabular in nature.

8. Is vocabulary staying workable? Avoid evasion by naming or using a pronoun for one person. Don't force a change in person when it isn't necessary. Avoid the ornamental repetition that comes from using distinctive words or distinctive constructions too often.

9. Is each sentence describing a mechanism rather than suggesting a feeling? Since feeling-only phrasing is insufficient, cut any sentence that cannot be restated as a concrete instruction, or as a number, or as a measurable consequence.

10. Is there a person behind this text? Particularly where the medium allows the author to express opinion, you'll want to look for a position taken, a tradeoff admitted, or a preference stated with reason. Otherwise, you must rely on detail that is so well-tuned to this particular subject that it's only clear when you see it all together.

11. Does the ending land? It lands when it stops after the point with no recap or forward-looking speculation, and it lands when the final paragraph completes an idea without trailing off.

12. Does every contrast earn its clauses? Read the second clause of every pair alone. If deleting the first clause loses you nothing, keep the plain claim. Both negation pivots and *however* pivots are scaffolds that still carry the point, so is any X rather than Y that so looks, or any mirrored affirmative clauses that merely rename the first.

Delegating this pass You may delegate the pass to a subagent every time, regardless of draft length or audience. Provide the subagent with the draft, the path to this file, the medium, and the audience. Request findings only, formatted as `line: problem: suggested fix`. Do not return a rewritten draft. Apply fixes, then re-run the checker. Applied fixes can reintroduce mechanical tells.