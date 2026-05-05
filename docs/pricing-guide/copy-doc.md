# Pricing Guide — Copy Doc

## How to read this doc

This doc has two parts:

1. **Handoff instructions (this section)** — nav placement, files to create, cross-links to update, Mintlify component suggestions, source citations. Apply these mechanically.
2. **Page copy** — everything below the `=== PAGE 1 ===` and `=== PAGE 2 ===` markers is the final publishable prose. Format it into MDX without changing wording, headings, or section order.

The frontmatter for each page is provided at the top of its section. Anything inside `[FORMATTER NOTE: ...]` brackets is a directive to you (the formatting agent) and should be removed before publishing.

---

## Files to create

- `plans/overview.mdx` — published as **Plans & Pricing**
- `plans/model-providers.mdx` — published as **Model Providers**

Create the `plans/` folder at the repo root, alongside `getting-started/` and `features/`.

---

## `docs.json` change

Add a new `"Plans & Billing"` group inside the `"Getting Started"` tab, between `"Core Concepts"` and `"Features"`:

```json
{
  "tab": "Getting Started",
  "groups": [
    { "group": "Start Here",     "pages": ["getting-started/overview", "getting-started/quickstart"] },
    { "group": "Core Concepts",  "pages": ["getting-started/workspace", "getting-started/publishing", "getting-started/connections"] },
    {
      "group": "Plans & Billing",
      "pages": [
        "plans/overview",
        "plans/model-providers"
      ]
    },
    { "group": "Features",       "pages": ["features/cron-jobs", "features/email-and-slack"] }
  ]
}
```

No other `docs.json` changes are needed.

---

## Cross-link updates to existing pages

After the two new pages are published, also edit:

1. **`getting-started/overview.mdx`** — add a "Plans & pricing" `<Card>` to the bottom CardGroup linking to `/plans/overview`.
2. **`getting-started/quickstart.mdx`** — find the line that says `No credit card required — the beta is free.` and replace it with: `Free tier available with your own API key. See [plans and pricing](/plans/overview).`
3. **`getting-started/connections.mdx`** — in the "AI Services" tab where OpenAI, Anthropic, and OpenRouter are listed, add a `<Note>` clarifying these are *connections* (used inside apps the agent builds) not the model provider that powers the agent itself, and link to `/plans/model-providers`.
4. **`getting-started/publishing.mdx`** — find any language saying custom domains are "coming soon" and update it to reflect that custom domains are live. Link to `/plans/overview` for per-plan limits.

---

## Suggested Mintlify components per section

**Page 1 (`plans/overview.mdx`):**
- "Plans" tier list → `<CardGroup cols={3}>` for Free / Starter / Pro, then a separate `<CardGroup cols={2}>` for Team / Enterprise. Pro should have a "Most popular" badge to mirror the in-app paywall.
- "How model usage works" → `<Tabs>` with two tabs: "camelAI credits" and "Bring your own API key", to make the choice visually clear.
- "Topping up credits" steps → `<Steps>`.
- "Why prepaid" and "Free trial" / "Changing plans" → plain prose, no callouts.

**Page 2 (`plans/model-providers.mdx`):**
- The "Heads up" callout about not mixing providers → `<Warning>`.
- "When to bring your own key" / "When camelAI credits are simpler" → two short prose blocks, optionally inside a `<Tabs>` if it reads better visually.
- "Supported providers" → `<AccordionGroup>` with one `<Accordion>` per provider (Anthropic, OpenAI, OpenRouter, AWS Bedrock). Better than `<Tabs>` because users only care about the one they pick.
- "Adding a key" steps → `<Steps>`.
- "Using camelAI on the cheap" → `<Tip>` callout for the lead paragraph; the playbook itself as `<Steps>`.
- FAQ → `<AccordionGroup>` of `<Accordion>` items.

---

## Source citations (for verification only — do not publish)

All facts in the page copy below were reconciled against shipped code at `/Users/illiana/Projects/chiridion-app`:

- Plan tiers, prices, limits: `src/lib/billing-plans.ts:33-119`
- Custom domains (live): `src/routes/_app.settings.organization.domains.tsx`, `src/routes/api/orgs.$id.custom-domain.ts`, per-plan caps in `billing-plans.ts:44, 61, 78, 95, 112`
- Stripe wiring (all paid plans): `src/lib/billing.server.ts` (`createSubscriptionCheckoutSession` ~line 1360); welcome paywall at `src/routes/_onboarding.welcome.tsx`
- BYOK providers and what each unlocks: `src/lib/byok-providers.ts:18-57`, `src/lib/llm-provider-config.ts:65-79`
- Model picker options: `src/lib/llm-provider-config.ts:15-32` (treating Grok and Kimi as launched per Illiana's direction)
- Settings → AI Provider UI and per-provider "Get a key" links: `src/components/byok/byok-key-form.tsx`, `src/routes/_app.settings.organization.ai-provider.tsx`
- Top-up flow: `src/components/billing/top-up-dialog.tsx` (pack labels render from live Stripe price objects, so do not hardcode dollar amounts in the copy)
- Free tier is BYOK-only: `billing-plans.ts:34-50` (`byokOnly: true`)
- OpenRouter BYOK fee (5% / first 1M requests free): https://openrouter.ai/docs/use-cases/byok — verify the URL is live at publish time

---

# === PAGE 1 — `plans/overview.mdx` ===

**Frontmatter:**

```yaml
title: 'Plans & Pricing'
description: "What's included on each plan, how credits work, and how to top up."
```

**Body (publish exactly as written below):**

camelAI bills two things separately: a monthly subscription for the platform (workspaces, deployed apps, cron jobs, storage, custom domains), and model usage for what the AI actually costs to run. You can cover model usage two ways: prepaid camelAI credits, or by bringing your own API key.

## Plans

[FORMATTER NOTE: render the five tiers below as `<CardGroup cols={3}>` for Free / Starter / Pro, followed by a `<CardGroup cols={2}>` for Team / Enterprise. Pro gets a "Most popular" badge.]

### Free

For trying camelAI out.

- $0 / month
- Bring your own API key (required)
- 1 workspace, 5 GB of storage
- 3 deployed apps
- 2 cron jobs, daily frequency

You'll need an API key from one of [our supported providers](/plans/model-providers) before you can chat with the agent.

### Starter — $40 / month

For solo builders.

- $10 of model credits / month (don't carry over)
- Bring your own API key (optional)
- 1 workspace, 50 GB of storage
- 30 deployed apps
- 10 custom domains
- 10 cron jobs, hourly frequency
- 7-day free trial

### Pro — $150 / month

For power users.

- $30 of model credits / month (don't carry over)
- Bring your own API key (optional)
- 1 workspace, 100 GB of storage
- Unlimited deployed apps
- Unlimited custom domains
- 50 cron jobs, 5-minute frequency
- Email inbox (your workspace gets its own address)
- 7-day free trial

### Team — $50 / seat / month, 3 seat minimum

For teams.

- $10 of model credits / seat / month (don't carry over)
- Everything in Pro, per seat
- 2 workspaces, 100 GB each
- Unlimited deployed apps
- Unlimited custom domains
- 50 cron jobs per user, 5-minute frequency
- Workspace-level roles (admin / member)
- Email inbox
- 7-day free trial

### Enterprise — custom

For larger teams or anything custom.

- SSO / SAML
- Bring your own cloud (deploy apps inside your own Cloudflare account)
- Multiple workspaces
- HIPAA / SOC 2
- Dedicated support

[Contact sales](https://book-demo--camelai-team-d9e.camelai.app/) to talk through your requirements.

## How model usage works

Every chat with the agent uses an LLM, and someone has to pay for it. camelAI offers two ways to cover that cost.

### Option 1: camelAI credits

Top up a balance with camelAI and we route your requests to the model you pick at the provider's cost, no markup. Paid plans include a monthly credit allowance, and you can top up more anytime.

### Option 2: Bring your own API key

Add an API key from a provider you already use (Anthropic, OpenAI, OpenRouter, or AWS Bedrock). Your provider bills you directly for usage. This is the only option on the Free tier.

You pick one or the other. When a key is set, all of your model usage goes through that provider. We don't currently support a setup where you bring a key for one provider and use camelAI credits for everything else.

For details on which provider to pick and how to add a key, see [Model Providers](/plans/model-providers).

## Why prepaid

If you use camelAI credits, you pay for them up front. This is how OpenAI, Anthropic, and OpenRouter all sell credits, too. Prepaid billing keeps fraud and runaway bills off the table for both sides: you only spend what you put in, and we only run requests against funded accounts.

Subscription fees (the monthly platform fee) are billed normally on a recurring basis through Stripe.

## Topping up credits

To add credits to your account:

1. Open **Settings → Billing** in your workspace.
2. Click **Top up credits.**
3. Pick a credit pack and check out through Stripe.

Available pack sizes are shown in the dialog. Top-up credits don't expire, and they stack on top of your monthly plan credits. Monthly plan credits don't roll over month to month, but anything you top up does.

## Free trial

Starter, Pro, and Team plans include a 7-day free trial. You'll need a payment method to start the trial. Cancel anytime from **Settings → Billing.**

## Changing plans

Upgrade, downgrade, or cancel anytime from **Settings → Billing.** Plan changes go through the Stripe billing portal.

---

# === PAGE 2 — `plans/model-providers.mdx` ===

**Frontmatter:**

```yaml
title: 'Model Providers'
description: 'How to use your own API key with camelAI, and what each provider unlocks.'
```

**Body (publish exactly as written below):**

camelAI is model-agnostic. By default, paid plans use camelAI's hosted credits to call whichever model you've picked for the thread. If you'd rather use your own API key, you can bring one from any of four providers. This page explains what each option gives you and how to set it up.

The agent can run on Claude (Sonnet, Haiku, or Opus), GPT (GPT-5.4 or GPT-5.4 Mini), Grok, or Kimi. You can switch models any time from the model picker in the chat. Whichever provider you've connected determines which of these models are available to you.

[FORMATTER NOTE: render the next paragraph as a `<Warning>` callout.]

> Bringing your own key replaces camelAI's hosted credits entirely. You can't mix and match (for example, your own OpenAI key plus camelAI credits for Claude). All requests go through your one chosen provider. If you need access to multiple model families on a single key, use **OpenRouter.**

## When to bring your own key

- You're on the Free tier. A key is required.
- You already have provider credits. If you're an existing OpenAI or Anthropic customer, using your key avoids paying us for what you're already paying them for.
- Your company requires it. Some teams need usage to flow through a corporate AWS or Azure account for compliance or billing reasons.
- You want a provider we don't support natively (Microsoft Azure, Google Vertex, etc.). See [Using a provider we don't support directly](#using-a-provider-we-dont-support-directly-azure-vertex-etc) below.

## When camelAI credits are simpler

- You don't already have a provider account.
- You want one bill, not multiple.
- You want the agent to use any of our supported models without managing separate keys.

## Supported providers

camelAI supports four providers for BYOK. Each unlocks a specific set of models.

[FORMATTER NOTE: render the four providers below as `<AccordionGroup>` with one `<Accordion>` per provider.]

### Anthropic

**Unlocks:** Claude (Sonnet, Haiku, Opus).

**Get a key:** [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

You'll need to add a payment method and prepay for credits in the Anthropic console before your key will run requests. A new key with no credits behind it returns a billing error.

### OpenAI

**Unlocks:** GPT-5.4 and GPT-5.4 Mini.

**Get a key:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

Like Anthropic, OpenAI requires you to prepay credits in your OpenAI account before the key will run requests.

### OpenRouter

**Unlocks:** Claude (Sonnet, Haiku, Opus), GPT (GPT-5.4, GPT-5.4 Mini), Grok, and Kimi — all on a single key.

**Get a key:** [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)

OpenRouter is the most flexible BYOK option. Two reasons to pick it:

1. You want every model camelAI supports on one key. Anthropic, OpenAI, and Bedrock keys lock you into a subset of our models. OpenRouter gives you all of them.
2. You already have an account with a provider we don't connect to natively. OpenRouter supports plugging in your own keys for Microsoft Azure, AWS Bedrock, Google Vertex, and others, then routing requests through your account. So if your company runs AI on Azure OpenAI, you can connect your Azure key to OpenRouter, and then connect OpenRouter to camelAI. Usage runs against your Azure bill.

OpenRouter charges a 5% fee on requests routed through your own provider keys, but the first 1 million BYOK requests per month are free. See [OpenRouter's BYOK guide](https://openrouter.ai/docs/use-cases/byok) for details.

### AWS Bedrock

**Unlocks:** Claude (Sonnet, Haiku, Opus), served from your own AWS account.

**Get a key:** [console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock)

You'll need:

- An AWS access key with Bedrock permissions
- The region you want to run in (for example, `us-east-1`)

Bedrock is a good fit if your team needs Claude usage on an AWS bill, or has compliance requirements that route AI through your own AWS account.

## Using a provider we don't support directly (Azure, Vertex, etc.)

camelAI doesn't connect natively to Microsoft Azure OpenAI or Google Vertex AI. Each cloud provider has its own auth model, billing structure, and quirks, and supporting them all directly would slow down our work on the rest of the platform. The good news: if your company is on one of those providers, you can still run camelAI through your existing account by routing through **OpenRouter**.

### How it works

OpenRouter supports plugging in your own keys for a long list of cloud providers, including:

- **Microsoft Azure OpenAI**
- **Google Vertex AI**
- **AWS Bedrock** (alternative to our direct Bedrock integration)
- Others — see [OpenRouter's BYOK guide](https://openrouter.ai/docs/use-cases/byok) for the current list.

When you connect those keys to OpenRouter, OpenRouter forwards your requests to that provider. Usage runs against your Azure (or Vertex, or Bedrock) bill, and OpenRouter charges a 5% fee on top — waived for the first 1 million BYOK requests per month.

### Setup with Azure as the example

1. **Set up Azure OpenAI** in your Azure portal: deploy a model, note the endpoint URL, deployment name, and API key.
2. **Sign up for OpenRouter** at [openrouter.ai](https://openrouter.ai) and go to **Integrations → Bring Your Own Key.**
3. **Add Azure as a provider** in OpenRouter, pasting the endpoint URL, model ID, and API key per OpenRouter's [Azure setup instructions](https://openrouter.ai/docs/use-cases/byok).
4. **Generate an OpenRouter API key** at [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys).
5. **Add the OpenRouter key to camelAI** under **Settings → AI Provider → OpenRouter.**

The same flow works for Google Vertex (Google Cloud service account JSON) or AWS Bedrock through OpenRouter (AWS access key + region).

[FORMATTER NOTE: render the next paragraph as a `<Note>` callout.]

> Native Azure or Vertex support in camelAI isn't on the near-term roadmap. The OpenRouter pass-through is the recommended path for the foreseeable future, and it's how most of our customers in this situation are running today.

## Adding a key

1. Open **Settings → AI Provider** in your workspace.
2. Pick a provider.
3. Paste your API key (and select a region, if you're using Bedrock).
4. Save.

The form has a "Get a key" link next to each provider that takes you to the right page on the provider's site.

You can switch providers any time from the same screen, or remove your key and switch to camelAI hosted credits (paid plans only).

## Using camelAI on the cheap

[FORMATTER NOTE: render this lead paragraph as a `<Tip>` callout.]

> Model costs vary widely. The cheapest models on camelAI are 10–50× less expensive per request than the flagship models, and they handle most everyday work just as well. Pairing a cheaper model with a small OpenRouter top-up is the lowest-cost way to use the platform.

The playbook:

1. **Sign up for OpenRouter** and add **$5 to $10** in credits at [openrouter.ai/credits](https://openrouter.ai/credits). A small top-up goes a long way with cheap models.
2. **Generate an OpenRouter API key** at [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys).
3. **Add the key to camelAI** under **Settings → AI Provider → OpenRouter.**
4. **Pick a cheap model in the chat.** The most cost-efficient options are:
   - **Claude Haiku** — fast, cheap, strong for everyday code and copy work.
   - **GPT-5.4 Mini** — comparable price to Haiku, slightly different strengths.
   - **Kimi** — competitive on price with Haiku and Mini, particularly strong on long-context tasks.
   - **Grok** — flexible across general work, often cheaper than the flagship Claude or GPT models.
5. **Reserve flagship models for hard problems.** Switch to Sonnet, Opus, or GPT-5.4 only when a task is genuinely hard (complex reasoning, multi-step debugging, careful design work). Most chat turns don't need them.

OpenRouter shows the live per-token cost for every model on its [models page](https://openrouter.ai/models). Sort by price to compare.

## FAQ

[FORMATTER NOTE: render the FAQ items below as `<AccordionGroup>` of `<Accordion>` items.]

### Can I use my own API key for one model and camelAI credits for another?

No. When a BYOK key is set, all of your model usage runs through that one provider. If you want broad model coverage on a single key, use OpenRouter.

### Do my plan credits roll over month to month?

No. Monthly plan credits reset each billing cycle. Credits you've topped up on top of your plan credits do roll over and don't expire.

### Why does my new API key say "billing error" or "insufficient credits"?

Anthropic, OpenAI, and OpenRouter all let you create an API key without adding any credits. The key won't work until you prepay credits in their billing settings. This is on the provider's side, not ours.

### Does camelAI charge a markup on hosted credits?

No. We pass through the provider rates at cost. The monthly subscription covers the platform; credits cover model usage at the provider's rate.

### Can I see how much I've spent?

Yes. **Settings → Billing** shows your current plan, credit balance, and usage history.

### Do you support Microsoft Azure OpenAI or Google Vertex AI?

Not directly, but you can route through OpenRouter to use them. See [Using a provider we don't support directly](#using-a-provider-we-dont-support-directly-azure-vertex-etc) above for the setup walk-through.
