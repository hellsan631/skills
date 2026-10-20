# Model and control compatibility

Resolve the model, interface, and operation before choosing parameters. Midjourney changes defaults and introduces features on different schedules; a valid parameter in one workflow may be unsupported or mean something different in another.

## Establish the intended workflow

- Preserve an explicitly requested model or version, including Niji or an older Midjourney version. Use the current default only when the user has no version preference, and identify the model you prepared for.
- Distinguish the main website, Alpha, and Discord. A dated Alpha announcement does not establish availability elsewhere.
- Identify ordinary generation, variation, reference-based generation, or editing. Check the compatibility of that operation as well as the base model.
- Consult the official [Version comparison](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version) and the relevant feature page. For recent rollouts, check [Midjourney Updates](https://updates.midjourney.com/).
- If sources disagree, explain the narrow uncertainty and use a documented supported path. User-supplied UI evidence can establish available controls; it does not establish untested output behavior.

## Choose references by purpose

| Intended influence | Workflow to investigate |
| --- | --- |
| Content, composition, or color | [Image Prompt](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts). Describe the complete desired result. |
| Medium, palette, texture, lighting, or overall appearance | [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference). It is not an identity lock. |
| A recognizable character or object | The chosen model's supported identity/reference workflow: Character Reference, Omni Reference, or Edit Model. |
| Changing an existing image or combining particular sources | [Edit Model](https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model) where supported; use the [Editor](https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor) for targeted areas. |

Ordinary prompts describe the image to create. Instruction-based editing can describe what to change and what to preserve. A reference upload alone does not determine its role; name the required attachment destination in the setup instructions.

Character Reference (`--cref`, `--cw`), Omni Reference (`--oref`, `--ow`), and Edit Model references are different systems. Use [Legacy Features](https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features), [Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference), and the Edit Model documentation to resolve support. Do not carry their weights between systems, invent equivalent values, or silently switch models.

Reference limits, text requirements, accepted files, weight ranges, and combinations vary. Check the specific reference documentation when they matter. In particular, an Edit Model may inherit the first source's aspect ratio instead of the account default.

## Select only supported controls

The [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List) describes syntax across multiple models; it is not a compatibility guarantee. Put supported parameters after the prompt text, separated by spaces. Preserve syntax required by individual parameters.

| Control | Syntax to verify for the chosen workflow |
| --- | --- |
| Model | `--v <version>`; Niji uses `--niji <version>` as a model-family choice. |
| Shape | `--ar <width>:<height>`; check accepted ratios and resolution restrictions. |
| Interpretation | `--raw`, `--s <value>` for Stylize, `--c <value>` for Chaos/Variety, `--w <value>` for Weirdness. |
| Exclusions | `--no <items>`; describe desired content positively where a negative phrase would be ambiguous. |
| Controlled comparison | `--seed <integer>`; keep the model and other settings fixed. Seeds do not preserve identity or guarantee permanent reproduction. |
| Image/style influence | `--iw <value>`, `--sref <URL or code>`, `--sw <value>`, and, where supported, `--sv <version>`. |
| Personalization | `--p` or `--p <profile or code>`; check model/profile compatibility and inherited UI settings. |
| Editing | Where documented, Discord accepts `--edit <image URLs>`; use the appropriate reference attachment on web. |

Do not assign universal ranges or defaults to these controls. Check the selected model's current documentation before proposing an adjustment. Likewise, verify text multi-prompt weights (`::`), Quality (`--q`), Tile (`--tile`), and experimental controls before including them.

Omitting a parameter does not necessarily remove an account default or pinned reference. Explicit prompt values can override supported defaults; disabling a boolean feature or inherited personalization may require the user's UI control. Do not invent an “off” parameter.

## Resolve resource and output choices

- Check [GPU speed](https://docs.midjourney.com/hc/en-us/articles/32016412137741-GPU-Speed-Fast-Relax-Turbo) against both model and plan before choosing Fast, Relax, or Turbo. A supported speed on one model may be unavailable on another.
- Check native resolution, HD/SD support, and [Upscalers](https://docs.midjourney.com/hc/en-us/articles/32804058614669-Upscalers) for the model and operation. Aspect ratio changes pixel dimensions; editing and upscaling can also change the result.
- Verify [Repeat](https://docs.midjourney.com/hc/en-us/articles/32757107922061-Repeat), [Permutations](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations), and any Draft behavior before proposing a batch. State the expanded job count and expected output count separately when known.
- Do not infer plan availability, remaining GPU time, or successful generation from documentation. Use information the user supplies and label unknowns.

## Preserve provenance

For reusable work, record the intended and effective model, interface, operation, complete submitted prompt, reference roles, relevant settings, resolved style/personalization codes, and selected asset. Retain job ID/link and seed when supplied.

When compatibility affects a decision, retain the official feature URL and date checked. Distinguish documented support, user-reported setup, and results verified from returned images. Recheck on model changes, interface changes, conflicting evidence, or a rejected parameter.
