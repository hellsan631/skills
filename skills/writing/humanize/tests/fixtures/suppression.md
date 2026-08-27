# Suppression and masking regression

Everything below is slop that must not be reported, except one deliberate violation
at the end of this file.

Fenced code keeps its words:

```python
# This delves into the vibrant tapestry and serves as a testament.
pivotal = "showcases the enduring legacy"
```

Inline code such as `serves as a testament` is also exempt.

Quoted material is cited, not written:

> Nestled in the heart of a vibrant valley, the town boasts a rich heritage and
> serves as a testament to its enduring legacy.

The style guide bans "serves as a testament" and "a vibrant tapestry" by name, which
is why naming them here must not trip the checker. It also bans the word "boasts",
along with a dozen other stock phrases that a checker can match without any help from
a person reading along. That is the whole point of keeping the list in one file.
Short rule. Long enough, though.

One em dash per bullet is normal rhythm, not a density problem:

- The archive opened in 1801 — the year the parish registers begin.
- The reading room closed in 2009 — it reopened four years later.
- Digitization began in 2014 — about a third is done.

<!-- humanize-lint: ignore -->
This line delves into the vibrant tapestry and is exempt by directive.

<!-- humanize-lint: off -->
This whole region showcases a rich tapestry and serves as a testament.
It boasts a vibrant heritage, nestled in the heart of the valley.
<!-- humanize-lint: on -->

The deliberate violation: the museum boasts four rooms.
