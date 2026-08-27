# Skill mechanics

This section (`SKILL-INVOCATION.MD`) is the skill-specific branch of [`writing-for-agents`](SKILL.md). That is, what changes when the document is a skill (frontmatter, invocation choice, router skills), versus everything else which is universal reference in `SKILL.md`.

## Invocation

Every skill must choose one of two invocation options: **model-invoked** or **user-invoked**.

**Mechanics.** For a model-invoked skill, omit `disable-model-invocation` from frontmatter, write the model-facing description `use when:` followed by a list of triggers that tell the agent which branch to fire, and continue in the usual way. For a user-invoked skill, add `disable-model-invocation: true` to the frontmatter, write the skill's description as a list of triggers, and proceed as usual. (Counters like language are user-invoked in practice, almost always.)

**Note well.** Pick model-invocation only if the agent must reach the skill on its own, or if another skill must reach it.

## Descriptions As Triggers

When the agent looks at the skill, the description naming the subject is just telling it what the skill is about, not when it applies. Building it is more like building the help for any executable (download the manpage, weed out the banners that say the command takes control of the keyboard, and so on), except that each skill is one trigger word.

For a skill with many usages, the `use when:` list will dwarf the name. Start with `use when:` and build on that.

Write triggers for both invocation modes; for the model-invoked skill, the agent will use the list of triggers for choosing branches, while for the user-invoked skill, the list becomes a free-form reverse index for human readers.

**Tip.** Where you can, write parallel `when` clauses and omit bare participles. For example, write:

```text
use when:
- the melody starts in A minor and ends in B major
- the melody is diatonically complete
- the melody moves stepwise in perfect 5ths
- the melody is 2 phrases long with a half cadence at the end of the first phrase
```

rather than:

```text
use when:
- in A minor (i) to B major (i6)
- diatonically complete, stepwise, in perfect 5ths
- 2 phrases, half cadence at the end of the first
```

Stripping down a trigger to its essential meaning can simplify this. Usually you want a distinct list, but one optimization is to strip a trigger only if it turns up later listing a different branch and renames it. (A thorough job would include listing your replaced branch by both names, but that's probably just pedantic.)

Only user-invoked skills can share a reference. If you get two user-skills within the same paragraph, push them to a plain file outside the skill system.

## Splitting by invocation

Whenever a new skill must reach on its own, split it into a model-invoked skill and a router skill. Also, when a distinct trigger word would add significant utility compared to the context load, split off a new model-invoked skill.

## Router skills

As the number of user-invoked skills in your list increases, your agent has to keep track of several more trigger words. That increases what's in its head and hence impacts its ability to parse conversational contexts.

When two or three user-invoked skills are active, to simplify the agent's head try summarizing them all into one skill. Humans have better head memory than agents, so you can just leave the many trigger words in a plain file.

The one user-invoked skill that names the others serves only to remind humans what skills are available. It cannot give the agent new advice and hence can only contain hints.
