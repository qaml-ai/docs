# camelAI Sales Site - Agent Documentation

> **Note to agents:** Keep this file up to date. When you add new features, routes, components, or make significant architectural changes, update the relevant sections of this document.

## Overview

This is the **docs page** for camelAI — not the product itself.

**What is camelAI?** An AI coding assistant built on Cloudflare's edge infrastructure. Users chat with an agent powered by their selected model, with a persistent workspace where files survive across sessions. Users create applications by having the agent write code, then publish them to live `*.camelai.app` URLs. The product repo is at `/Users/illiana/Projects/camelai` (internal codename: chiridion). Please feel free to access and explore the repo at anytime to research, plan, or audit how we do things in that codebase.

For additional context on camelAI, our sales site is available in this machine at `/Users/illiana/Projects/camelai-salessite`.

If you need in depth Company context (for building content, writing copy, etc.), please read - docs/camelAI-company-context.md

You have complete access to the codebase that these docs cover at /Users/illiana/Projects/camelai. Chiridion is the internal name for camelAI. (live site link is camelai.dev)

We also have 2 legacy offerings covered in these docs that are no longer actively maintained. 
/Users/illiana/Projects/camel-app - our old product offering was a data analytics chat where users could connect a database and “chat with their data” (live site link is app.camelai.com)
/Users/illiana/Projects/camel-api - our API product offering that creates an embedded data chat so users can embed our data chat into their own product (live site link is console.camelai.com)

## Tech Stack

This is a Mintlify docs page.

## Partner guides

Per-tool integration guides live in the **Partners** group under the Getting Started tab
(one `getting-started/partners/<tool>.mdx` page per guide). The first guide is Resend;
OpenRouter is planned next.

Every partner page follows the same structure so the next one is quick to add and the
section stays consistent: **Intro + disambiguation → What you can build (agent prompts) →
Connect (Steps, both Settings and agent paths) → Use it (no-code prompt first, code second)
→ How it works → FAQ → Stop using or remove.** When you add a guide, register it in the
Partners group in `docs.json` and link it from the relevant tab in
`getting-started/connections.mdx`. Verify connection details (UI labels, the
`CONNECTIONS.find()` signature, code examples) against the product repo before publishing.

## camelStream documentation

The Stream tab documents **camelStream**, camelAI's flat-rate inference API. Its product
repository is `/Users/illiana/Projects/qaml-api-dashboard`. Position it as unlimited
frontier intelligence above a published floor, never as a fixed-model promise.

`stream/fleet.mdx` is the canonical fleet list for every camelAI property. The sales site
links to it and, since September 2026, also names the current models in `CURRENT_MODELS` in
`app/lib/stream-guarantees.ts` (camelai-salessite), so a fleet change lands in both. When the
fleet or a model version changes, update the table and the "Last updated" line.

A weekly GitHub Action (`.github/workflows/fleet-floor-check.yml`, running
`scripts/fleet_floor_check.py`, Mondays 13:00 UTC) parses the fleet page's floor sentence
(thresholds and the `(vX.Y)` index version), the `_Floor verified against ..._` line, and the
table's `artificialanalysis.ai/models/<slug>` links, then compares each model's live score and
the sales site against the docs. Findings open or update a GitHub issue labeled `fleet-check`.
If you change the structure of the floor section or the table, update the script in the same
change, and test with `python3 scripts/fleet_floor_check.py --dry-run`.

`stream/reasoning.mdx` documents the reasoning controls (`reasoning_effort`, `reasoning.effort`,
`thinking.budget_tokens`, `output_config.effort`). Effort levels are passed through as the caller
sends them; do not document any effort remapping. The old remap of `medium` to `high` existed only
because DeepSeek V4 Flash rejected `medium`, and a product PR removes it as of September 2026.
Do not document the gateway's thinking-budget cap from `normalizeReasoningLimit` either; it is a
relic and reads as too much detail (CTO decision, September 2026). Describe the parameters and
their pass-through, not internal limits. Budgets are optional on every endpoint: present effort as
the primary control and budgets as an optional ceiling, never as something the caller must send.
Live-tested against staging in September 2026: every effort level and both Messages `thinking`
forms are accepted and return reasoning, while `reasoning_effort: "none"` and
`thinking: {"type": "disabled"}` are rejected with a 400 by fleet models that require reasoning.
Re-test with a staging key from Illiana before changing those claims.

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

Keep these vocabulary invariants:

- The product name is "camelStream."
- The only benchmarks are Terminal-Bench 2.1 at 70% and the Artificial Analysis
  Intelligence Index at 35 on index v4.3. Name the index version wherever the number
  appears. Artificial Analysis recalibrates the index between versions: the v4.3
  recalibration dropped every fleet model below the old floor of 50, and Illiana
  re-baselined to 35 on September 15, 2026. `stream/fleet.mdx` is the definition and
  carries the "floor verified" date; the sales site's `INTELLIGENCE_FLOOR` in
  `app/lib/stream-guarantees.ts` mirrors the number. When a new index version ships,
  re-check every fleet model, settle the new number with Illiana, and update the docs
  page, this line, and the sales-site constant together.
- Speeds are targets, never guarantees: p10 at or above 40 tok/s, p5 at or above 20 tok/s,
  and p95 first token under 5 seconds. Keep the throughput floors and first-token ceiling
  clear.
- Context is "260K guaranteed, more when the model serving you supports it."
- Vision is guaranteed: every fleet model accepts image inputs, so requests with
  images work on `auto` no matter which model serves them.
- The model ID is `auto`. Document the legacy `deepseek-v4-flash` ID only in the fleet-page
  migration FAQ. After September 1, 2026, it is treated the same as `auto`.
- Do not add serving-precision tags.
