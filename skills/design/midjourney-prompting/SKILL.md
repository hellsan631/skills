---
name: midjourney-prompting
description: Use when the user requests Midjourney prompts, reference and model setup, guided image generation, or revisions based on generated results. Adapts prompts to the selected model and prepares them for user submission, then critiques returned images.
---

# Midjourney Prompting

Turn a visual brief into a prompt the user can paste into Midjourney, with suitable references and generation settings. After the user generates images, inspect the results and provide a focused revision. Adapt to the selected model and interface; this skill has no fixed model version.

Use a user-submitted workflow. The agent prepares and reviews; the user handles navigation, login, settings, uploads, generation, and downloads in Midjourney. This follows the owner's chosen workflow and Midjourney's restriction on automated interactions. Give direct destination links and concrete setup instructions; inspect screenshots the user supplies to check their state. See the [Community Guidelines](https://docs.midjourney.com/hc/en-us/articles/32013696484109-Community-Guidelines).

## Choose the operation

Identify the intended subject, use size, composition, visual direction, and features that must survive iteration. Use supplied art and accepted project decisions. Ask about missing choices only when they would materially change the prompt.

Distinguish a new image from an edit to an established image. Ordinary generation describes the desired result. Editing instructions depend on the selected editing workflow. Choose reference roles by purpose: composition, style, or subject identity. Match the mechanism to the model instead of treating every reference as interchangeable.

Read the relevant support before preparing the result:

- [Model compatibility](references/model-compatibility.md) when choosing parameters, reference roles, or adapting a prompt to a different model.
- [Prompt construction](references/prompting.md) when writing a prompt or diagnosing a failed result.
- [Manual generation workflow](references/manual-workflow.md) when guiding navigation, checking model settings, submitting, iterating, or exporting on the website.

For game art, work from `game-visual-identity` when available to preserve global and local design pillars. Use `visual-identity-grilling` when the user wants decision rounds. Translate the agreed visual choices into Midjourney instructions without restarting an accepted art direction.

## Prepare a usable prompt

Use the model requested by the user or established by their current workflow or source job. When none is known, a prompt-only request can proceed with descriptive text and no version-dependent flags. If model choice affects a required capability, consult current official documentation and recommend a supported model, stating the assumption. Ask only when the choice would materially change the result.

When preparing a configured submission, identify the model and verify the parameters and reference workflow it supports. Use the documented selector when pinning a version. Preserve a requested older model or Niji model unless the user agrees to a change. Treat website, Alpha, and Discord availability separately.

Write the prompt around visible content and the few details that determine success. Keep website instructions outside the copyable prompt. Use actual supplied reference URLs or explain which images the user should attach in the web interface; never invent URLs, style codes, or account profile IDs.

Return one recommended prompt unless the request calls for alternatives. Provide the reference assignment and only the settings the user needs to check. State what each proposed variant tests. Avoid adding unrelated creative requirements to a specific brief.

Use a supported standard generation mode as a starting point for exploration unless the user needs another workflow. Keep job and output counts explicit when known. Resolution, quality, speed, and Draft behavior vary by model; verify them before adding controls. Repeats and permutations can create additional jobs, so use them only when they serve the requested scope.

## Guide generation and review

Guide the user to the correct destination and check the effective settings before submission, using the manual workflow reference. Return the prompt with its intended setup, including inherited settings that could change it. Report setup as recommended, user-confirmed, or visible in supplied evidence; a URL or sign-in alone does not verify controls.

A prompt-only request ends with the prompt and setup. For a generation session, wait for the user to submit and return the image or saved file. A report that submission succeeded is not evidence of image quality.

Inspect the returned pixels. Compare the result with the intended silhouette, composition, style, and required details at its target use size. For characters, check the defining features. For icons, check separation from the background and confusion with neighboring icons. Describe only defects visible in the supplied result.

Choose the next operation from the observed failure. A new prompt can change the concept; a variation can explore a promising result; a supported edit workflow can target a specific change. Preserve successful features and change the most consequential mismatch first. Provide the complete revised prompt or edit instruction, not just a vague suggestion to improve it.

## Keep a reproducible record

For work that will be reused, save the exact submitted prompt, reference assignments, effective model and settings, and the selected result. Record the job link or ID and seed only when the user supplies them. Include the resolved personalization or style code when it affects the result. A seed alone does not preserve a character or establish permanent reproducibility.

Save selected files in the user's requested project location once they are available locally. Check real file dimensions and format before reporting export readiness. Keep an original download when making delivery copies. A white or checkerboard background does not prove alpha transparency, and a generated illustration does not establish vector editability.

Finish with the prompt, the selected image if available, and the next unresolved decision or material limitation. Distinguish documented behavior, user-reported settings, and observed results. Do not report an image as generated, downloaded, or verified until that step has evidence.
