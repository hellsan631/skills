---
name: unslop
description: Use while writing any prose, in a chat reply or a file. Always applies.
---

<!-- humanize-lint: ignore-file list-density -->

# Unslop

Apply these rules while drafting any prose.

## Process

1. Scan for the patterns below.
2. Rewrite. Keep the meaning and try to match intended tone.
3. Add soul (see next section).
4. Self-audit: "What makes this obviously AI generated?" Fix remaining tells.

## Add soul

A scrubbed sentence can still say nothing, so read each one for what it gives the reader.

- Have opinions. React to facts instead of neutrally listing pros and cons.
- Vary rhythm. Short sentences. Then longer ones that take their time. Mix it up.
- Acknowledge complexity. "Impressive but also kind of unsettling" beats "impressive."
- Use "I" when it fits. First person isn't unprofessional.
- Let some mess in. Perfect structure looks machine-made.
- Be specific. Not "this is concerning" but "there's something unsettling about agents churning away at 3am."
- Never invent specifics. A made-up detail is worse than the puffery it replaced. Delete the empty sentence or ask for the fact.

## Patterns to detect and fix

### Content

1. **Puffery.** Examples: "pivotal moment", "testament to", "evolving landscape", "setting the stage for", "indelible mark", "deeply rooted", "plays a vital role". Cut puffery, state what happened (`significance-bloat`, `ecology-filler`).
2. **Name-dropping.** Listing media outlets without context. Pick one, say what was said (`notability-performance`).
3. **Superficial -ing phrases.** Examples: "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete or expand with real sources (`superficial-analysis`).
4. **Promotional language.** Examples: "nestled", "vibrant", "breathtaking", "groundbreaking", "renowned", "stunning", "must-visit". Use neutral descriptions (`puffery`).
5. **Vague attributions.** Examples: "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete (`vague-attribution`).
6. **Formulaic challenges.** Examples: "Despite challenges... continues to thrive." Replace with specific facts (`challenges-formula`).

### Language

7. **AI vocabulary.** Examples: "additionally", "crucial", "delve", "enduring", "enhance", "fostering", "garner", "interplay", "intricate", "landscape" (abstract), "pivotal", "showcase", "tapestry" (abstract), "testament", "underscore", "vibrant". Replace with plain words (`ai-vocabulary`).
8. **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Just say "is" or "has" (`copula-avoidance`).
9. **"Not just X, but Y."** Both claims are true. Write "X and Y" when both matter, or write Y alone when X only sets it up. Removing "just" changes X from true to false. The same rewrite applies to punctuation variants such as "doesn't just X; it Y". For bare "X, not Y", drop Y when it repeats a nearby rule. Keep Y when removing it changes the meaning or a requirement. Turn Y into "Do not Y" only when the source states a prohibition (`negative-parallelism`, `negative-parallelism-density`).
10. **Rule of three.** Forcing ideas into groups of three, or five, or ten. Use a natural number, the one that comes from what there is to say (`rule-of-three`).
11. **Synonym cycling.** Protagonist, main character, central figure, hero all in one paragraph. Pick one, repeat it.
12. **False ranges.** "from X to Y" where X and Y aren't on a meaningful scale. List topics directly (`false-range`).

### Style

13. **Em dash overuse.** Avoid em dashes entirely. Use periods or commas only. This means: no parentheses, no en dashes, no hyphen-as-dash substitutes. Em dashes are an AI tell, and reaching for parentheses instead just trades one tell for another. If a thought needs separation, end the sentence or use a comma (`em-dash-density`, `em-dash-present`).
14. **Colon overuse.** Colons are fine before a list or example. As mid-sentence connectors they add nothing: "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" adds nothing with the colon. Always rewrite these to let the point stand on its own without comparison framing. "Describing when the scheduler should fire works best as plain English." Same meaning, no crutch punctuation.
15. **Boldface overuse.** Don't bold every proper noun or acronym (`bold-density`).
16. **Inline-header lists.** The tell is a bold label and colon that restates the line: "**Performance:** Performance improved...". Convert those to prose. A bold lead-in that ends in a period, names the item, and is followed by genuinely new detail ("**Schema in TypeScript.** Tables live in one file.") is fine, not a tell (`inline-header-list`, `redundant-label`).
17. **Title case headings.** Use sentence case (`heading-case`).
18. **Decorative emojis.** Remove from headings and bullets (`emoji`).
19. **Curly quotes.** Replace with straight quotes (`quote-consistency`).

### Communication artifacts

20. **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!" Remove (`assistant-artifact`).
21. **Cutoff disclaimers.** "While specific details are limited..." Find sources or remove (`gap-filling`).
22. **Sycophantic tone.** "Great question! You're absolutely right!" Respond directly (`sycophancy`).
23. **Narrating the document.** "In this section we will explore...", "As mentioned above...", "By the end of this guide...". Delete the narration and say the thing (`meta-commentary`).
24. **Machinery leftovers.** Stray citation tokens from a chatbot's own browsing UI, unfilled placeholders ("[Insert Name]"), a subject line on something that isn't an email. Delete them (`citation-artifact`, `placeholder-text`, `subject-line`).

### Filler

25. **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". "It is important to note that" gets deleted (`filler-phrase`, `didactic-disclaimer`).
26. **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may" (`hedging`).
27. **Generic conclusions.** "The future looks bright." State specific plans or facts (`conclusion-formula`).

### Jargon

28. **Abstract metaphor nouns.** "substrate", "wedge", "vector", "locus", "vantage", "nexus", "primitive" (as noun), "harness" (as metaphor), "surface" (as in "API surface"), "bedrock", "scaffolding" (as metaphor), "modality", "paradigm", "gold-plating", "ratchet" (as metaphor), "evacuate" (for moving code), "endgame", "north star", "flywheel". These read as technical but usually have a plainer concrete word. "Substrate" becomes "base". "Wedge in" becomes "add". "Vector" becomes "way" or "method". "Gold-plating" becomes "more than the job needs". "Ratchet" becomes the mechanism's real name or "a limit that only tightens". "Evacuate" becomes "move out". "Endgame" becomes "the last phase". Pick the concrete word (`abstract-metaphor`).

### Plain speech

29. **Say what it does, not how it feels.** "the database stays close at hand", "SQL you can read", "types that follow your schema" all name a feeling. The fix names the mechanism or a number: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build". Ask what the sentence tells the reader to do or know, then write that. If you can't restate it as a concrete instruction, fact, or number, cut it. One more check: if the sentence could appear unchanged in another project's docs, it says nothing about this one. Cut it.
30. **Shorten or split dense sentences.** If the reader has to backtrack to parse a sentence, break it in two or drop clauses. One idea per sentence (`long-sentence`).
31. **Active voice.** Prefer it. Catch "is/are/was/were + past participle" and name the actor: "queries are validated" becomes "the compiler validates queries", "the file is parsed by the loader" becomes "the loader parses the file". Passive is fine only when the actor is unknown or genuinely doesn't matter (`passive-voice`).
32. **Cut adverbs, or use a stronger verb.** "runs quickly" becomes "is fast" or the number. "significantly improves" becomes the measured delta. An adverb propping up a weak verb means the verb is wrong (`weak-adverb`).
33. **Prefer the plain word.** "utilize" becomes "use", "leverage" becomes "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if". The fancier synonym is rarely clearer (`plain-word`).
