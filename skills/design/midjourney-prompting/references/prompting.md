# Prompt construction

For ordinary generation, describe the image you want to see. Use concrete nouns, visible attributes, meaningful counts, and composition. Include details that determine success; avoid redundant adjectives and unrelated quality slogans. In an editing workflow that accepts instructions, write the requested change and the features that should remain. Other workflows may require a description of the final image; check the selected tool. See [Prompt Basics](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics) and [Edit Model](https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model).

## Build the prompt from the brief

Start with the subject and its action or pose. Add the rendering medium, framing, and visual traits that matter to the intended use. Specify background, lighting, and palette only where they shape the result. Use the user's selected references to reduce repeated style language.

Translate abstract art direction into visible instructions. "Readable at small size" can become a dominant silhouette, large value masses, few internal marks, and clear separation from the background. "The same character" requires a source image and identified features, not a seed promise.

For image text, place the exact short wording in double quotes and identify where it belongs. Inspect the letters in the generated result before accepting them. See [Text Generation](https://docs.midjourney.com/hc/en-us/articles/32502277092109-Text-Generation).

Keep prompt text and parameters together in one copyable block. Put reference attachment directions, the intended test, and manual website steps outside that block. If the required reference is absent, provide the useful draft and identify what remains missing before identity matching can be evaluated.

## Examples

These examples illustrate descriptive text without choosing a model. Their style is not a default for every project. For a configured submission, append only parameters verified for the selected model, such as the agreed aspect ratio, and return the complete copyable prompt.

A character exploration with a clear silhouette:

```text
Bust portrait of a woodland courier with a broad square jaw, tall triangular hair, small round spectacles, one oversized shoulder bag, and a tired warm grin. Loose gouache illustration, broad flat shadow masses, detail concentrated around the face, quiet cream background, fully visible hair silhouette
```

A compact ability icon:

```text
Single ability icon of a broken stone gate, two chunky wall sections separated by a wide opening, bold white shapes with one muted gold accent, dark charcoal background, generous outer padding, flat graphic illustration, few internal marks
```

An instruction for a supported edit workflow, with the accepted courier image attached as its source:

```text
Simplify the painting by reducing small folds and competing edge detail. Preserve the broad square jaw, triangular hair silhouette, small round spectacles, oversized shoulder bag, tired grin, and existing crop. Keep the loose gouache treatment and broad shadow masses
```

For a family extension, pair a complete new-subject description with the accepted image as a style reference where supported. For the same character in a new pose, use the selected model's subject-reference or editing workflow and describe the pose and defining features. Keep these reference roles distinct.

## Diagnose before rewriting

| Observed mismatch | Next useful change |
| --- | --- |
| Subject or action is wrong | Clarify the subject and its relationship to the other elements; remove competing instructions. |
| Important detail is ignored | Make it explicit; where supported, test lower Stylize or Raw while holding the subject fixed. |
| Character identity drifts | Check the supported subject-reference or editing workflow and defining features; a style reference or seed alone is insufficient. |
| Art is too busy | Reduce competing contrast, mark density, and ornament while preserving the preferred shape and personality. |
| Family style drifts | Check the reference slot, actual style code, personalization, and rendering words before changing the subject. |
| A promising image needs a small change | Choose an available edit or variation operation based on what must stay fixed. |

For a comparison, change one consequential variable while retaining the rest of the brief. Record the visible result and the next decision. When the user gives a clear refinement request, prepare that revision directly. Stop when the requested direction or asset is accepted; additional variants need a purpose.
