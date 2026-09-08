# camelStream subsidy disclosure — copy plan (docs + sales site)

camelStream may start using API content to select and measure advertising, in
addition to the existing data-for-training posture. Today there are zero
advertisers and no training on anyone's data. This plan rewrites every
statement that would become false or misleading once either begins, so the
copy does not need another edit when the subsidy mix changes.

**Scope:** camelStream only. The coding agent's Privacy Policy
(`app/routes/privacy-policy.tsx`) and Terms (`app/routes/terms.tsx`) are out of
scope and must not be touched.

**Two repos:** the docs repo (`/Users/illiana/Projects/docs`) and the sales
site (`/Users/illiana/Projects/camelai-salessite`). Every edit below is an exact
old → new spec. Copy in fenced blocks is **verbatim** unless a heading says
"pattern". New copy uses no em dashes; sentences you are not told to touch keep
whatever punctuation they have.

---

## 1. The posture (context, not copy)

**Categories fixed, methods open.** The binding docs name exactly two
categories of subsidy use: training AI models, and selecting and measuring
advertising, sponsored content, or offers. Inside each category nothing is
stated about method, partner, surface, or timing, so the mix can change without
a copy edit. Adding a third category later is a one-line edit to the same list
in the Terms and Policy.

**One umbrella phrase.** Legal and docs copy calls the whole set "the
arrangements that keep the price flat." Marketing copy points at it as "the
data rights in our Terms." Neither phrase enumerates methods, so it never goes
stale.

**"May" everywhere.** The Terms already say: "We say 'may': we promise neither
that we do all of this today nor that we will not." That sentence now covers
both categories. Nowhere may the copy say "we don't currently show ads," "we
have no advertisers," or "we don't train today." Those go stale the day either
starts.

**The floor is specific, and it appears wherever the "may" does:**

1. We never sell your data to data brokers.
2. We never attach your account details (name, email, billing information,
   camelStream API key) to a request, never share them with inference
   providers, partners, or advertisers, and never use them for training or
   advertising. This is about the record we hold, not about what you type:
   the prompt itself goes to the provider as you sent it. A key pasted into a
   prompt, or one an agent reads off your machine and sends in tool output,
   is prompt content. camelStream does not scrub traffic in transit, and no
   copy may imply it does. Always write "camelStream API key," never a bare
   "API keys," when stating the floor.
3. We separate API content from your account identity before we use it
   ourselves for any subsidy purpose.

**Docs and FAQ only, never the Terms or Policy:** every agent trace we store
runs through the self-hosted OpenAI Privacy Filter. This is already true of the
legal docs today (neither mentions the filter); keep it that way.

---

## 2. Vocabulary rules (apply everywhere)

| Never write | Write instead |
| --- | --- |
| "we don't sell your data" (unqualified), "No." as a FAQ opener | "we never sell your data to data brokers" |
| "we don't sell to advertisers", "anyone outside the inference path" | drop; the floor is brokers plus account identity |
| "targeted advertising", "target ads", "match you with an advertiser", "pair" | docs: "select and measure ads and offers" · legal: "select and measure advertising, sponsored content, or offers" |
| any closed list: "Two parties see it", "That is the entire arrangement", "Two things make it possible" (unless the second thing is the umbrella) | the umbrella phrase, or a list that ends in the umbrella phrase |
| "we don't currently…", "today we…", "we have no advertisers" | "may" |
| "no-training terms" as the only custom option | "custom terms" / "no-training, no-advertising, or zero-retention terms" |
| any description of an ad surface, format, or measurement mechanism | nothing; the system does not exist |

---

## 3. Source-of-truth facts

| Fact | Value | Source |
| --- | --- | --- |
| Product name | camelStream ("Stream" on second reference) | docs `CLAUDE.md` |
| Subsidy categories | training; select and measure advertising, sponsored content, or offers | founder decision, 2026-09-08 |
| Floor 1 | never sell your data to data brokers | founder decision, 2026-09-08 |
| Floor 2 | account details (name, email, billing, camelStream API key) are never attached to a request, never shared with providers, partners, or advertisers, and never used for training or advertising; keys inside prompts or tool output are prompt content | existing Terms §4 and Policy §2, extended; proxy verified 2026-09-08 (rows below) |
| Floor 3 | API content separated from account identity before we use it ourselves | existing Policy §2 sentence, extended to all subsidy purposes |
| Privacy filter | OpenAI Privacy Filter, self-hosted, stored traces only, never the live request path; docs and FAQ only | docs `CLAUDE.md`, `stream/data-usage.mdx` |
| What the proxy attaches upstream | camelAI's own gateway token for auth (never the caller's key); forwarded request headers are only `anthropic-version`, `anthropic-beta`, `openai-beta`; no client IP; caller-supplied `user` and `safety_identifier` are deleted and replaced with an opaque `camel_account_<id>` for abuse isolation; `session_id` removed | `qaml-api-dashboard/src/server/camel-stream.server.ts` (`upstreamHeaders`, `configureAttempt`), verified 2026-09-08 |
| Redaction in the request path | none; the request body is forwarded as sent | same file; grep for redact, scrub, mask, or PII returns nothing |
| Where stored traces come from | Cloudflare AI Gateway logs with payload collection on (`cf-aig-collect-log-payload`) | same file, `upstreamHeaders` |
| Posture on both categories | "may"; never present-tense denials | docs `CLAUDE.md`, founder |
| Custom terms threshold | 1,000 streams | `stream/data-usage.mdx` |
| Umbrella phrase | "the arrangements that keep the price flat" (legal, docs); "the data rights in our Terms" (marketing) | this plan |
| Console (`qaml-api-dashboard`) | has no user-facing copy about selling, advertising, or training | verified 2026-09-08 |

---

## 4. Docs repo edits (`/Users/illiana/Projects/docs`)

### 4.1 `stream/data-usage.mdx` — replace the whole file (verbatim)

Keep the existing "What we scrub from the traces we store" section's intro
paragraphs and table exactly as they are today; only its closing paragraph
changes (shown in place below). Everything else is replaced. Set the
"Last updated" line to the implementation date.

```mdx
---
title: 'How We Handle Your Data'
sidebarTitle: 'Data usage'
description: 'Who can see your prompts, what we scrub from the traces we store, and how to get custom terms'
---

camelStream is cheap because prompts and responses may be retained and used to
train AI models, by us or by the providers we partner with, and may be used to
select and measure ads and offers. Those arrangements are what keep the price
flat. Here is who can see your prompts, how we scrub sensitive data, and what
is never shared. The [camelStream Terms](https://camelai.com/stream/terms) and
[Privacy Policy](https://camelai.com/stream/privacy) are the binding versions.

## Who can see your prompts

A prompt goes from your client to camelStream, then to the model provider
serving your stream, and the response comes back the same way.

- **The provider serving your request.** A model has to read the prompt to
  answer it. The request reaches the provider without your name, email,
  camelStream API key, or IP address attached. Providers may retain prompts
  and use them for training under their own policies.
- **Us.** We store agent traces on our own infrastructure so we can debug the
  service, understand what agents actually do, and, potentially, train or
  evaluate models or select and measure ads and offers. Every trace we store
  runs through the privacy filter described below, and we separate it from
  your account before using it for anything beyond running the service.
- **Partners in the arrangements that keep the price flat.** Model-development
  partners may receive API content for training. Advertising partners may
  receive content separated from your identity, signals derived from it, or
  aggregate results. None of them receive your account details.

We never sell your data to data brokers.

## What we scrub from the traces we store

[KEEP the current two intro paragraphs and the table exactly as they are. Replace
only the paragraph after the table with the one below.]

The filter runs on the copy we store, not on the request itself. We do not
scrub what you send on its way to the provider. The model has to read the
original prompt to answer it, so a key you paste into a prompt, or one an
agent reads off your machine and sends in tool output, reaches the provider
like everything else. That is the same exposure as calling the provider
yourself, minus your identity. No filter catches everything, which is why the
Terms still ask you not to send data you are not allowed to share.

## What is never shared

Your account details are separate from your API content. We never attach
your name, email, billing information, or camelStream API key to a request,
never share them with a provider, partner, or advertiser, and never use them
for training or to select ads. Card payments are handled by Stripe, and
camelStream API keys are stored hashed.

## If you need custom terms

There is no opt-out on a standard subscription. Starting at 1,000 streams we
can customize your terms so your data is never used for training or
advertising. Your traffic goes only to providers that do not train on or
retain data, and that can go into a contract if you want it in writing. Ask at
[camelai.com/stream/contact](https://camelai.com/stream/contact).

_Last updated: [implementation date, e.g. September 9, 2026]_

## What's next?

<CardGroup cols={2}>
  <Card title="The model fleet" icon="layer-group" href="/stream/fleet">
    The models serving streams, the intelligence floor, and the guarantees.
  </Card>
  <Card title="Custom terms" icon="envelope" href="https://camelai.com/stream/contact">
    Ask about no-training, no-advertising, or zero-retention terms for 1,000+ streams.
  </Card>
</CardGroup>
```

The heading "If you need no-training terms" becomes "If you need custom terms".
Its anchor changes; nothing links to the old one (verified in both repos).

### 4.2 `stream/fleet.mdx` — two edits

**Edit A.** In "How the flat price works", replace the paragraph that begins
`camelStream sources capacity across the fleet` (currently lines 70 to 80)
with:

```mdx
camelStream sources capacity across the fleet and partner providers, wherever
frontier-floor intelligence is most economical: bulk deals, new-model offers,
and data-for-training arrangements. That sourcing, plus the data rights in
our Terms, is what subsidizes unlimited tokens at a flat price. Requests and
responses may be retained and used to train AI models, by us or by our
inference providers, and may be used to select and measure ads and offers.
Your account details are never used for either, and every agent trace we
store is scrubbed of personal information.
[How we handle your data](/stream/data-usage) explains what that means in
practice. The [camelStream Terms](https://camelai.com/stream/terms) and
[Privacy Policy](https://camelai.com/stream/privacy) describe the data
rights in full.
```

**Edit B.** In "Common questions", the accordion titled
`Do you use my prompts for training?` (currently line 110) becomes:

```mdx
  <Accordion title="How do you use my prompts?">
    Requests and responses may be retained and used to train AI models, by
    us or by our inference providers, and may be used to
    select and measure ads and offers. Your account details never are.
    These arrangements are part of what keeps the price flat.
    We never sell your data to data brokers, and every agent trace we store
    runs through a self-hosted privacy filter that masks names, emails,
    phone numbers, addresses, account numbers, and secrets. See
    [how we handle your data](/stream/data-usage) for who sees what and what
    gets scrubbed. The
    [camelStream Terms](https://camelai.com/stream/terms) and
    [Privacy Policy](https://camelai.com/stream/privacy) are the full
    description.
  </Accordion>
```

Keep the line wrapping above: the verification greps count "select and measure ads and
offers" and "never sell your data to data brokers" per line, so each phrase must stay on
one line.

Do not add a "Will I see ads?" accordion. See decision 5.

### 4.3 `CLAUDE.md` (docs repo) — update the data-copy rules

Replace the paragraph that begins `` `stream/data-usage.mdx` is the plain-language data page `` with:

```md
`stream/data-usage.mdx` is the plain-language data page. The sales site links to it
(`DATA_DOCS_URL` in `app/lib/stream-guarantees.ts`) instead of restating details that can go
stale. Rules for that page and any camelStream data copy:

- Two categories of use, and only two: training AI models, and "select and measure ads and
  offers" (legal docs: "advertising, sponsored content, or offers"). Together they are "the
  arrangements that keep the price flat." Never name a method, partner, surface, or timing.
- The posture on both is always "may." Never state that we do not train, have no advertisers,
  or do not show ads, and never state that we do.
- The floor appears wherever the "may" does: we never sell your data to data brokers; account
  details are never attached to a request, never shared with providers, partners, or
  advertisers, and never used for training or advertising; API content is separated from
  account identity before we use it ourselves.
- camelStream is a pipe. Nothing is scrubbed in transit; the prompt reaches the provider as
  sent. Say "attach" or "share" about account details, never "sent" or "go to," which read as
  a scrubbing claim. Write "camelStream API key," never a bare "API keys," in the floor: keys
  inside prompts or tool output are prompt content and reach the provider.
- The self-hosted OpenAI Privacy Filter runs only on the agent traces we store, never in the
  live request path, so do not imply live redaction. It is described in the docs and FAQ only,
  never in the Terms or Privacy Policy.

State what we do plainly and keep caveats to one clause; readers should come away feeling
protected, not warned.
```

---

## 5. Sales site edits (`/Users/illiana/Projects/camelai-salessite`)

### 5.1 `app/data/legal/stream-terms.md`

**Edit A — line 8, "The deal" bullet 4.** Old:

```md
> - **What you send may train AI.** Prompts and outputs may be retained and used to train models — by our inference providers under their own policies, and potentially by us. There is no opt-out on standard plans. Assume anything you send can be kept and used for training (Section 4).
```

New:

```md
> - **What you send may subsidize the price.** Prompts and outputs may be retained and used to train AI models, by our inference providers under their own policies and potentially by us, and may be used to select and measure advertising, sponsored content, or offers. There is no opt-out on standard plans. Assume anything you send can be kept and used this way (Section 4).
```

**Edit B — line 9, "The deal" bullet 5.** Old:

```md
> - **Your account details are different.** We never give inference providers your name, email, billing details, or API keys, and we never use them to train models.
```

New:

```md
> - **Your account details are different.** We never give inference providers, partners, or advertisers your name, email, billing details, or camelStream API keys, and we never use them for training or advertising. We never sell your data to data brokers.
```

**Edit C — line 21, Section 2, end of the sentence about issuing keys to your
own users.** Replace the fragment
`that their content may be retained and used for AI training.` with
`that their content may be retained and used for AI training and the other purposes in Section 4.`

**Edit D — line 27, heading.** `## 4. Your content and AI training` becomes
`## 4. Your content and how it subsidizes the price`. The rendered anchor
changes from `your-content-and-ai-training` to
`your-content-and-how-it-subsidizes-the-price`; nothing links to the old
anchor in either repo (verified).

**Edit E — line 31, Section 4, second paragraph.** Replace the whole
paragraph (it begins `Input, output, and their request metadata`) with:

```md
Input, output, and their request metadata together are "API content." You grant us the license needed to process API content to run camelStream, and a separate **perpetual, irrevocable, worldwide, royalty-free license, sublicensable to our inference providers and partners, to retain API content and use it in the arrangements that keep the price flat: to train, evaluate, and improve AI models and services, including models unrelated to camelStream, with human review; and to select and measure advertising, sponsored content, or offers**. We say "may": we promise neither that we do all of this today nor that we will not, and the mix of arrangements changes as we learn what keeps the price flat. Before we use API content ourselves for any of these purposes, we separate it from your account identity. Inference providers may also retain API content under their own policies, may train on it, and may be anywhere in the world; we cannot retrieve or delete what they hold, and this license survives the closing of your account. **Assume anything you send through the API can be retained and used for training and the other purposes above. API content is not confidential.** This is part of why the price is low, and there is no opt-out on a standard plan; for no-training, no-advertising, or zero-retention terms, ask about a custom agreement at [/stream/contact](/stream/contact).
```

**Edit F — line 33, Section 4, the "Your account data" paragraph (the one
right after Edit E).** Replace the tail
`we never share it with inference providers and never use it to train models.`
with
`we never share it with inference providers, partners, or advertisers, and never use it for training or advertising.`
In the em-dashed opening of that same sentence, replace `API keys, support messages`
with `camelStream API keys, support messages`. Nothing else in the opening changes.

**Edit G — date.** `STREAM_TERMS_LAST_UPDATED` in
`app/routes/stream.terms.tsx` (line 8) becomes the implementation date.

### 5.2 `app/data/legal/stream-privacy.md`

**Edit A — line 3, the bold "short version" paragraph.** Replace the whole
paragraph with:

```md
**The short version: what you send through the API may be kept and used in the arrangements that keep camelStream cheap: to train AI models, by our inference providers under their own policies and potentially by us, and to select and measure advertising, sponsored content, or offers. Your account details (name, email, billing information, camelStream API keys) are never shared with inference providers, partners, or advertisers, and never used for training or advertising. We never sell your data to data brokers.**
```

**Edit B — line 9, "Usage data" bullet.** Delete the final sentence
`No advertising cookies.` and the space before it. Nothing else in the bullet
changes. See decision 3.

**Edit B2 — line 14, Section 2, the "We use account information" paragraph.**
Replace the bold sentence
`**We never use account information to train AI models and never share it with inference providers.**`
with
`**We never use account information for training or advertising, and never share it with inference providers, partners, or advertisers.**`
The first sentence of the paragraph stays.

**Edit C — line 16, Section 2, the "We use API content" paragraph.** Replace
everything before the sentence that begins `Do not send sensitive data` with:

```md
We use API content to generate responses (by sending it to inference providers), to operate, debug, and protect the service, and potentially, in the arrangements that keep the price flat: by us, our providers, and our model-development partners, **to train, evaluate, and improve AI models and services, including with human review**, and by us and our advertising partners, **to select and measure advertising, sponsored content, or offers**. We separate API content from your account identity before using it ourselves for any of these purposes. **Assume anything sent through the API can be retained and used for training and the other purposes above. There is no opt-out on standard plans**; no-training, no-advertising, or zero-retention terms require a custom agreement ([/stream/contact](/stream/contact)).
```

The existing `Do not send sensitive data — …` sentence stays unchanged at the
end of the paragraph.

**Edit D — line 20, "Inference providers" bullet.** Delete the final sentence
`Because providers give us better pricing in exchange, some US state laws may treat this as a "sale" of personal information; the only ways to opt out are a custom agreement or not using camelStream.`
It moves below the list (Edit F).

**Edit E — insert a new bullet after line 22 ("Model-development partners")
and before "Legal and business":**

```md
- **Advertising partners.** Never your account information. Depending on the arrangement, they may receive API content separated from your identity, signals derived from it, or aggregate results, to select and measure advertising, sponsored content, or offers.
```

**Edit F — insert a standalone paragraph after the bullet list, before the
"We do not sell account information" line:**

```md
Because providers and partners give us better pricing or pay us in exchange, some US state laws may treat these arrangements as a "sale" of personal information; the only ways to opt out are a custom agreement or not using camelStream.
```

**Edit G — line 25.** Old:

```md
We do not sell account information, and we do not share your data for targeted advertising.
```

New:

```md
We do not sell account information, and we never sell your data to data brokers.
```

**Edit H — Section 4, Retention.** Replace
`API content used for model development may be kept for years`
with
`API content used for model development or advertising may be kept for years`.

**Edit I — date.** `STREAM_PRIVACY_EFFECTIVE` in
`app/routes/stream.privacy.tsx` becomes the implementation date.

### 5.3 `app/routes/stream.tsx` — two FAQ entries

Both entries have a plain-string `answer` and a JSX `richAnswer`. Edit both so
they say the same thing; only the link markup differs.

**Edit A — the FAQ whose question begins `How is $` (line 94).** In `answer`
(line 96) and `richAnswer` (lines 97 to 108), replace the sentence

`Requests and responses may be retained and used to train AI models — by us or by our inference providers — though your account details never are.`

with

`Requests and responses may be retained and used to train AI models, by us or by our inference providers, and may be used to select and measure ads and offers. Your account details are never used for either.`

The surrounding sentences and the two `<Link>`s stay.

**Edit B — the FAQ `Do you sell my data?` (line 111).** Keep the question.
Replace `answer` (line 113) with this string, verbatim:

```
We never sell your data to data brokers. A request reaches the model provider serving it without your name, email, camelStream API key, or IP address attached. Providers may retain prompts and use them for training under their own policies, and we may too. We may also use what you send, separated from who you are, to select and measure ads and offers. Advertisers never get your account details. Every agent trace we store runs through a self-hosted copy of OpenAI's open-source Privacy Filter, which masks names, emails, phone numbers, addresses, account numbers, and secrets like API keys. See how we handle your data in our docs.
```

In `richAnswer` (lines 114 to 141, the JSX block): replace the opening
`No. We never sell prompts to data brokers or advertisers.` with
`We never sell your data to data brokers.`; after `and we may too.` insert
` We may also use what you send, separated from who you are, to select and measure ads and offers. Advertisers never get your account details.`;
in the sentence `A request reaches the model provider serving it without your name, email, API key, or IP address attached.` change `API key` to `camelStream API key`; leave the two existing `<a>` links and everything after them unchanged.

### 5.4 `app/components/stream/agent-guide.tsx` — line 51

Old:

```
"No token metering, no overage charges, cancel anytime. Sourcing efficiently across the fleet is what keeps the price flat."
```

New:

```
"No token metering, no overage charges, cancel anytime. Sourcing efficiently across the fleet, plus the data rights in our Terms, is what keeps the price flat."
```

---

## 6. What does not change, and why

- **Coding agent Privacy Policy and Terms** (`privacy-policy.tsx`, `terms.tsx`): out of scope.
- **The privacy filter stays out of the Terms and Privacy Policy.** It is not there today. It stays in `data-usage.mdx`, `fleet.mdx`, and the `stream.tsx` FAQ.
- **`app/lib/stream-guarantees.ts`:** no change. `DATA_DOCS_URL` and `PRIVACY_FILTER_URL` still point where they should.
- **Console (`qaml-api-dashboard`):** no user-facing copy about selling, advertising, or training exists there. Nothing to edit.
- **Other `stream/` docs pages** (`openclaw`, `hermes`, `agents`, `pi`, guides): no data-handling copy. Nothing to edit.
- **No new "Will I see ads?" FAQ** on any surface. See decision 5.

---

## 7. Verification checklist

Run from each repo root after the edits. Every grep lists its expected result.

**Docs repo**

```bash
grep -rn "data brokers or advertisers\|outside the inference path\|Two parties see it\|no-training terms\|Do you use my prompts for training\|the training posture is always\|never sent to a provider" stream/ CLAUDE.md
```
Expect no output.

```bash
grep -rn "never sell your data to data brokers" stream/
```
Expect exactly 2 lines: `stream/data-usage.mdx` and `stream/fleet.mdx`.

```bash
grep -rn "select and measure ads and offers" stream/
```
Expect exactly 4 lines: 2 in `data-usage.mdx` (intro, "Us" bullet), 2 in `fleet.mdx` (paragraph, accordion).

```bash
grep -c "—" stream/data-usage.mdx stream/fleet.mdx
```
Expect `0` for both (the baseline is 0 for both today).

```bash
npm run build
```
Expect a clean build.

**Sales site**

```bash
grep -rn "data brokers, advertisers\|That is the entire arrangement\|targeted advertising\|No advertising cookies\|Your content and AI training\|What you send may train AI\|never use them to train models\|never use it to train models\|account information to train AI models\|used for AI training\.\|sublicensable to our inference providers and model-development\|billing details, or API keys\|billing details, API keys\|billing information, API keys\|email, API key," app/data/legal/ app/routes/stream.tsx app/components/stream/
```
Expect no output. (Today this grep returns 12 lines across the two legal files and
`stream.tsx`; every one of them is touched by an edit above.)

```bash
grep -rn "never sell your data to data brokers" app/
```
Expect exactly 5 lines: 1 in `stream-terms.md`, 2 in `stream-privacy.md`, 2 in `stream.tsx`.

```bash
grep -rn "select and measure advertising, sponsored content, or offers" app/data/legal/
```
Expect exactly 5 lines: 2 in `stream-terms.md`, 3 in `stream-privacy.md`.

```bash
grep -rn "select and measure ads and offers" app/routes/stream.tsx
```
Expect exactly 4 lines (two FAQs, `answer` and `richAnswer` each).

```bash
grep -rn "your-content-and-ai-training\|if-you-need-no-training-terms" app/ /Users/illiana/Projects/docs/stream /Users/illiana/Projects/docs/docs.json
```
Expect no output (confirms no inbound links to the renamed anchors).

```bash
grep -n "STREAM_TERMS_LAST_UPDATED =\|STREAM_PRIVACY_EFFECTIVE =" app/routes/stream.terms.tsx app/routes/stream.privacy.tsx
```
Expect both to show the implementation date.

```bash
npm run typecheck && npm run build
```
Expect clean.

Manual: open `/stream/terms` and `/stream/privacy` in the dev server and confirm
the new bullet and paragraph render inside the list and blockquote correctly,
and the Section 4 heading shows the new title.

---

## 8. Decisions I made, veto if wrong

1. **Categories fixed, methods open.** The Terms license names training and advertising as the two categories and does not add "and similar arrangements." A third category later is a one-line edit to the same list plus the notice the Policy already promises. The open-ended alternative reads as a blank check and buys nothing you have described wanting.
2. **Advertising partners may receive pseudonymized API content.** Policy §3 says they "may receive API content separated from your identity, signals derived from it, or aggregate results." That is the maximum-flexibility position. If you would rather commit that advertisers only ever see aggregate results, delete "API content separated from your identity, signals derived from it, or" from that bullet and from the partners bullet in `data-usage.mdx`. It is a real trust win, and it closes a door.
3. **"No advertising cookies" is deleted, not softened.** It promises a measurement design that does not exist, and it is already fragile: conversion tracking for your own ad campaigns would break it. If you want to keep a cookie promise, "No third-party advertising cookies." is the narrower form.
4. **The "Do you sell my data?" FAQ no longer opens with "No."** The Privacy Policy itself says some state laws may treat the provider arrangement as a "sale." Opening with "No" and then describing a possible sale is the contradiction that reads as a lie later. This was a pre-existing problem; the new answer leads with the specific true promise instead.
5. **No "Will I see ads?" FAQ anywhere.** It would describe a surface that does not exist. The existing FAQs now disclose the category. Add a surface-specific question when there is a surface.
6. **The privacy filter stays out of the legal docs.** It is not there today, and this plan keeps it in docs and FAQ only.
7. **Two headings renamed, two anchors change.** Terms §4 and the data-usage custom-terms section. No inbound links exist in either repo.
8. **The "sale" caveat moved** from the provider bullet to a standalone sentence covering providers and partners. I did not add the CPRA word "sharing." That is counsel's call (see §9).
9. **Custom terms are described as "no-training, no-advertising, or zero-retention"** everywhere the custom-terms offer appears (Terms §4, Policy §2, data-usage page and card).
10. **The Terms sublicense reads "inference providers and partners."** The old text said "model-development partners." The generic word lets the same license cover advertising partners; Policy §3 still names both partner types separately.
11. **"We promise neither that we do all of this today nor that we will not" is unchanged.** It already covers the zero-advertisers, no-training-today reality. I did not change "all" to "any."
12. **Umbrella phrases.** "the arrangements that keep the price flat" in legal and docs copy; "the data rights in our Terms" in marketing copy, because the `/stream` FAQ already uses it.
13. **Account-detail wording says "attach" and "share," never "sent" or "go to."** An earlier draft read as a claim that we scrub names and keys out of traffic. We do not, and the docs page now says so in one sentence. The claim is only that the account record is never attached to a request or shared.
14. **The opaque account ID sent upstream is not disclosed in copy.** The proxy sends OpenRouter a `user` value of `camel_account_<id>` for abuse isolation and per-account usage reporting. It is not a name, email, key, or IP, so "without your name, email, camelStream API key, or IP address attached" stays literally true. If you would rather disclose it, add to the provider bullet in `data-usage.mdx`: "It carries an opaque account number so the transport can isolate abuse, and nothing else about you."
15. **"API key" is always "camelStream API key" in the floor.** A bare "API keys" reads as every key, including ones pasted into prompts or read off the user's machine by an agent. Those are prompt content and reach the provider. The docs page now says so in the scrub section; the legal docs only qualify the noun.

---

## 9. For counsel (not blocking the copy)

- Once a paying advertiser receives pseudonymized API content, whether that content is "personal information" under CCPA/CPRA and whether it triggers a "Do Not Sell or Share" opt-out. The Policy currently says the only opt-out is a custom agreement or not using camelStream; that theory now carries more weight.
- Whether to add "sharing" alongside "sale" in the moved caveat (Policy §3).
- Policy §9 promises email or console notice of material changes. This is one.
