# Judgment pass

Eleven questions the checker cannot answer, each with a test you can apply. Run them
after `humanize_lint.py` reports zero errors.

Work through them in order against the draft. The pass is done when every question has an
answer, not when the draft starts to feel finished.

## 1. Does every sentence carry information?

The checker catches known filler phrases. It cannot catch novel filler. Read each sentence
and ask what the reader knows after it that they did not know before. Delete any sentence
whose answer is nothing.

This is the most common miss. A draft can be clean of banned phrases and still be 40
percent air.

## 2. Is a flagged word doing real work, or did it just get renamed?

Check the words you kept and the words you replaced. "Crucial" cut to "important" is not a
fix. "Serves as the primary interface" changed to "acts as the primary interface" is not a
fix. The test is whether the sentence would survive deleting the word entirely. If it
would, delete it.

## 3. Does the register match the medium and hold steady?

Read the first paragraph and the last paragraph back to back. If one is looser than the
other, the piece drifts, and drift is a stronger AI tell than any single phrase. Grammar
quality should also be constant: do not open with clipped notes and close with textbook
prose.

Match the medium. A forum reply that reads like a memo is as wrong as a memo that reads
like a forum reply.

## 4. Is every claim of significance backed by a fact in the text?

Find each sentence asserting that something matters, is influential, or is widely used.
Confirm the surrounding text supplies the evidence. If it does not, either the evidence is
missing or the claim is. Remove the claim rather than inventing support.

## 5. Did the rewrite invent anything?

Compare against the source line by line for names, dates, numbers, quotations, causal
claims, and source attributions. Fabricated specificity is the worst possible outcome of a
humanize pass, because the prose now reads more credible while being less true.

Check especially where you replaced vague praise with concrete detail. That is the exact
place where invention happens.

## 6. Did the rewrite lose anything?

The reverse check. Facts, caveats, conditions, scope boundaries, and hedges that were
load-bearing sometimes vanish when a sentence gets tightened. A hedge the author put there
on purpose is content, not filler.

## 7. Is the structure earned?

Ask whether each heading, bullet list, and table is doing work that prose could not. Lists
are for genuinely parallel items, tables for genuinely tabular data. Prose that was chopped
into bullets reads like a slide deck and is a formatting tell the checker only partly sees.

## 8. Is the vocabulary varied but not evasive?

Two failures pull in opposite directions. Elegant variation cycles through "the artist,"
"the visionary," "the celebrated creator" for one person: use the name or a pronoun and
repeat it. The opposite failure is a distinctive word or construction reused three times in
a short piece, which reads as generated. Repetition of plain words is fine. Repetition of
ornamental ones is not.

## 9. Does the sentence name a mechanism or only a feeling?

"The database stays close at hand", "SQL you can read", and "types that follow your
schema" all name a feeling. The fix names a mechanism or a measurable consequence:
".toSQL() returns the exact string sent to the database", "a column rename fails the
build".

Ask what the sentence tells the reader to do or know, then write that. If you cannot
restate it as a concrete instruction or a number, cut it.

## 10. Is there a person behind it?

This is the check that catches over-correction. A draft can pass every rule above and
still read as machine-written because nothing in it commits to anything.

Where the medium allows an author, look for a position taken, a tradeoff admitted, a
preference stated with a reason. Neutral surveys of considerations are the safest thing
to write and the most obviously generated. Where the medium is reference writing and
opinion is out of bounds, look instead for detail specific enough that no other subject
could carry the same sentence.

## 11. Does the ending land?

The piece should stop when the point is made, with no recap and no forward-looking
speculation. It should also not stop mid-thought. Read the final paragraph alone and ask
whether it completes an idea or trails off.

## Delegating this pass

For a long draft or public writing, hand this to a subagent. It works better than doing it
yourself because the reader has no memory of writing the sentences and no investment in
keeping them.

Give the subagent the draft, the path to this file, the medium, and the audience. Ask for
findings only, formatted as `line: problem: suggested fix`, and tell it not to return a
rewritten draft. You apply the fixes, then re-run the checker, because applied fixes can
reintroduce mechanical tells.
