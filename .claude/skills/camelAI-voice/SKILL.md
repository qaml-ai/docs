---
name: camelai-voice
description: How to channel the brand's voice for our docs page. Use when drafting copy.
---

# Writing in camel's Voice

## Core Principles

- Direct, simple sentences. Say the thing, not the thing around the thing.
- Never use em dashes.
- Adjectives are fine but use them sparingly.
- Don't show off technical knowledge. Use the simplest term that's accurate.
- Add practical value for the reader rather than just narrating your own story.

## Writing docs

**What to do:**
- Details matter here. Name the tools, services, and technical specifics. Blog readers came for the depth.
- Let the facts tell the story. If you tried three services and they all failed, that sequence is inherently dramatic. You don't need to add drama on top.
- Descriptive titles over clickbait. "We tried Modal, Cloudflare Containers, and Sprites before building our own persistent container service" not "We Tried Every Container Service. Then We Built Our Own in a Week."
- Use simple verbs. "went from" not "ballooned." "simple" not "almost comically simple."
- Mix personal blog tone with informational guide. It should feel like a smart friend explaining something, not a press release.
- End with a factual summary (TL;DR), not a moral. Let the reader draw their own conclusions.
- Leave room for links to tools and services mentioned.
- Merge sections that cover one continuous thought. Don't create separate sections for dramatic effect.

**What to avoid:**
- Dramatizing. No "And then we had The Conversation." No "this was the nail in the coffin." No sentence fragments for emphasis ("All of them. Immediately." should just be "immediately").
- Narrating other people's internal states. Don't write "he felt silly" or "worst debugging days of his career." Observable behavior is fine ("Miguel was frustrated") but don't put words in someone's head.
- Moralizing. No bolded lesson statements. No pithy closing lines ("Sometimes the simplest solution is the one you build yourself"). The story IS the lesson.
- Rhetorical buildup. Don't write "What happened next is something Miguel tried to do quietly." Just say what happened.
- Anaphora and repetition for effect. "We tried X. We tried Y. We tried Z." should be "We tried X, Y, and Z."
- Meta-commentary. Don't write "We get asked about this, so here's the honest answer." Just give the answer.
- Marketing speak, hype language, filler transitions ("In this blog post, we'll explore...").
- Vague "AI magic" statements. Don't write "It knew what to do," "It built one," "Now it just happens," or "Then it does something I couldn't do manually." These sound like hype. Say what the tool actually did. "It knew what to do" → "It set up the HTML structure, metadata fields, and scaffolding." "It built one" → "It built a dashboard that shows traffic sources, page performance, and signup attribution."
- Incomplete sentences used as lists. Don't drop a series of nouns as a standalone sentence ("Canonical tags, sitemaps, meta descriptions, structured data."). Either use a proper bulleted list with a complete introductory sentence, or fold them into a grammatically complete sentence.
- Dramatic repetition without added value. Don't restate a point just to make it sound more severe ("Google will stop indexing them. Your landing page just dies."). If you want to restate for emphasis, add the concrete impact on the reader's work ("Google will stop indexing them, which means all the work you put into that content stops contributing to your rankings."). If there's no real-world impact to add, don't restate.

## FAQ and troubleshooting sections in docs

Patterns from editing the Hermes subagent guidance (Aug 2026):

- Prefer an `<AccordionGroup>` of 3-4 simple questions over one heading with paragraphs of prose, and over one broad question with a bulky answer. Overlap between answers is fine; each reader expands only the question that matches theirs.
- Each question must stand alone. Don't write a question like "What's the fix?" that only makes sense after reading the previous one.
- Don't frame question titles as the product failing. "Why does Hermes hang and then fail under parallel work?" reads like a promise of failure. Use conditional framing: "What happens if a request queues for too long?"
- Answers must survive the reader's obvious follow-ups. If the answer says "kills the request after a timeout," give the actual numbers. If it references "the loop," walk the sequence step by step instead of naming it.
- When one fix is buying more of the product, never present it as the only fix. Open with a plain framing sentence ("There are a few options to get X to work well with Y."), recommend the purchase for the workloads that genuinely need it, and give the non-purchase path its own paragraph. Two short paragraphs, one per path, beat one dense paragraph joined by "Or".
- Recommendation voice is "we recommend you..." rather than a bare imperative like "Match your streams to your workload." Use numerals for purchase counts ("at least 1 additional Stream").
- Cut qualifiers that only matter to edge cases when the plain version is accurate enough. "Current builds give DeepSeek V4 models 10 minutes; older builds and some request types kill after as little as 90 seconds" became "stays silent past 10 minutes; older builds kill after as little as 90 seconds." Same for mechanism detail like "sends no bytes" — drop it if the sentence works without it.
- Don't promise absolute outcomes from a fix. "Prevents the kills entirely" became "should reduce the likelihood of a request getting killed." Hedge to what we can actually guarantee.

## Writing changelogs

Changelogs go in `changelog/platform.mdx` (current product) or `changelog/legacy.mdx` (old BI product). Each release is a `<Update label="DATE" description="TITLE">` block. New entries go at the top.

**What to include:**
- User-visible changes only. New features, new models, new integrations, new UI surfaces, billing/plan changes, and tools the agent can now use on the user's behalf.
- Lead with the items users will be most excited about. Custom domains, team plans, and new model support belong at the top. Settings polish and minor sandbox additions go below.
- Closing the loop on prior "Coming soon" items is a strong lead — but don't edit prior entries to mark them shipped. The new entry is the source of truth.

**What to cut:**
- Internal infra: admin endpoints, worker logs, lazy-loading, deploy scripts, schema migrations, SDK bumps, RPC migrations, anything a user can't see or click.
- Prototypes that were removed before shipping.
- Implementation details behind a user-visible feature. Surface the feature, not the plumbing.

**Bug fixes — be ruthless.**
The audit you receive will list every fix. Most don't belong in the changelog. The bar: would a real user have hit this in production and noticed it was broken? If the bug only affected a code path users rarely reached, or if the symptom was invisible (silent failures, edge-case routing, internal auth checks), cut it. A short list of fixes users actually felt is better than a long list that buries them. Three to five is usually right; nine is too many.

**Verify currency before claiming features.**
Beta-era behavior expires. Free-credit grants, halved spend limits, and other launch-period mechanics may not be true anymore. Before describing how a feature works for users today, confirm it with the user or check the current product code — don't carry forward language from the audit if the policy has changed.

**Pricing in changelogs.**
When billing changes, name the actual numbers ($10 Starter, $30 Pro, $10 per seat Team). Vague phrasing like "monthly credits included" reads like marketing filler; concrete numbers respect the reader's time.

**Voice in changelogs:**
- Section headers + short paragraph for each major item. Bullets only for the "Minor Features" and "Bug Fixes" sections at the bottom.
- One or two sentences per major item. Say what it is and what the user can now do. Skip the marketing wind-up.
- No "we're excited to announce." No "we've been hard at work." Just ship the news.

## How to Improve This Skill

After drafting content, show me what you wrote. I will copy your version and apply my edits. You should compare the two. The delta is the signal. Update this skill with new patterns as they emerge.
