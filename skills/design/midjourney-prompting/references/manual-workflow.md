# Manual generation workflow

Guide the user through the website while keeping navigation, settings, and submission under their control. The documented workflow below was checked on 2026-10-20; the user's account controls and generated output have not been tested by this skill's author.

Midjourney's [Terms](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service) prohibit automated tools from accessing, interacting with, or generating assets through the service. The owner chose prompt preparation and user-submitted generation. Prepare complete instructions rather than requesting an automation exception on each use.

## Reach the correct workspace

For new images, give the user the [Create page](https://www.midjourney.com/imagine). The destination should show an Imagine bar and their creation feed. A URL under `/personalize/`, including a profile's `/teach` page, belongs to profile training; completing that training is only relevant when the chosen workflow needs personalization. If login interrupts navigation, the user signs in and returns to Create. See [Getting Started](https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide) and [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization).

For edits, identify the intended source image and a compatible edit tool before directing the user to controls such as Quick Edit or Open Editor. Keep main-site and Alpha instructions separate. Use current labels from a user-supplied screenshot when they differ from documentation; request the relevant view rather than inventing a control or claiming navigation succeeded.

## Check the effective setup

Have the user open the settings icon in the Imagine bar. Look for Model, Aesthetics, and speed controls. Their options depend on the selected model and website release. These controls set defaults. Prefer supported parameters for a single job and change lasting defaults only when the user wants that. See [Creating on Web](https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web).

Resolve these checks against the prompt before asking the user to submit:

| Check | Intended state |
| --- | --- |
| Operation | Still image; verify again after attaching references. |
| Model | Requested or established model, with a verified selector when pinning it. |
| Resolution and ratio | Agreed dimensions or ratio, using controls supported by that model. |
| Raw | Where supported, match the intended direction; omission from a prompt does not reset an inherited toggle. |
| Aesthetics | Check supported Stylization, Variety, and Weirdness values so prior defaults do not alter a comparison. |
| Speed | Existing preference if supported by the model, operation, and plan. |
| Personalization | Off unless an agreed profile or moodboard is part of the brief; otherwise verify its identity. |
| References | Only the intended images, assigned to the intended roles; check locked references left from earlier prompts. |
| Prompt handling | Draft off for ordinary generation; Conversational off for exact prepared prompts, if shown. |

Use the [model compatibility reference](model-compatibility.md) to resolve available controls and ranges. No single aesthetics preset fits every project or model. For a literal comparison, consider less automatic styling and lower variation where supported; provide actual verified values in the setup. Preserve previously agreed settings for continuing work.

The Personalization button beside the Imagine bar applies selected defaults when enabled. Omitting `--p` alone does not disable them. Have the user turn it off for a comparison without personalization, or verify the intended profile/code when enabled. See [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization).

Draft availability, output count, and resolution vary by model. Conversational writes prompts for the user. Check these modes separately from resolution so a prepared prompt goes through the intended process. See [Draft & Conversational Modes](https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes).

For attachments, name the destination supported by the chosen model: an Image Prompt, Style Reference, subject reference, or edit source. Have the user check each role after upload and remove unintended attachments from the current prompt. Check current upload limits if a file fails. See [Creating on Web](https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web) and [Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts).

Summarize the actual intended setup beside the copyable prompt. To verify setup, use the user's confirmation of values or supplied screenshots showing the controls and attachments. State which checks remain unverified. Keep screenshot requests limited to relevant controls; do not request account credentials.

## Submit one job

State whether the submission is one ordinary job, a Draft job, or a requested batch. Give the expected image count when verified for that model and mode; do not assume every submission produces four images. See [Getting Started](https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide).

If the work is confidential, establish the intended visibility before the user uploads or generates it. Midjourney content is public by default; a private browser tab does not make a job private. Stealth depends on account entitlement and where the image is created. See [Terms, content rights](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service).

The user pastes the prompt and presses Enter to submit. Have them compare the completed job's displayed prompt and settings with the intended setup; this can reveal inherited parameters or a model mismatch. Ask for the resulting images or saved file. A screenshot supports visual critique; the downloaded file is needed to verify original dimensions and export properties.

## Continue from a result

Use the selected image as the basis for the next action. Where available, Vary Subtle stays closer to it and Vary Strong explores larger changes. For targeted changes, select an edit workflow compatible with the source and intended result. Flag any required model change before proposing it. Use current visible control names supplied by the user if their interface differs. See [Variations](https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations) and [Edit Model](https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model).

Upscalers depend on the model and source resolution. Verify the available options; creative upscaling can change detail, so inspect identity and small marks afterward. Check the downloaded dimensions before claiming an export meets its target. See [Upscalers](https://docs.midjourney.com/hc/en-us/articles/32804058614669-Upscalers).

If a submission fails, ask for the exact error and submitted prompt. Correct the specific incompatible parameter or reference setup before another submission. If the user is unsure whether a job was sent, have them inspect the queue or recent creations before resubmitting, which could spend resources twice.

## Download and retain the selected result

Have the user open the selected image and use its download control, or use Organize for a requested bulk download. Ask for the final generated image when delivery needs the artwork; Editor exports can also contain the current edit canvas or mask. See [Organizing Your Creations](https://docs.midjourney.com/hc/en-us/articles/33329462451469-Organizing-Your-Creations) and [Editor](https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor).

When useful for reuse, have the user copy the job ID or link, exact prompt, seed, and reference or personalization codes from the completed job. Pair those details with the downloaded asset. Record missing information as unknown and distinguish a preview from an export that has been inspected.
