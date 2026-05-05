# Parking Lot — OpenRouter Free Model Variants

> **Status:** Not for inclusion in the v1 pricing docs. Saved here for use after the model picker exposes free model variants (or before, if we want to seed expectations alongside the Grok and Kimi launch).
>
> **Why this is in the parking lot:** As of writing, the camelAI model picker only exposes Sonnet, Haiku, Opus, GPT-5.4, and GPT-5.4 Mini ([`src/lib/llm-provider-config.ts:15-32`](file:///Users/illiana/Projects/chiridion-app/src/lib/llm-provider-config.ts#L15-L32)). None of those are OpenRouter `:free` model variants, so a user with an unfunded OpenRouter key has no path to actually run the agent. Once the picker exposes free variants — or once Grok/Kimi ship and we decide to lean into "use camelAI cheaply via OpenRouter" — this section can drop into the Model Providers page.

---

## When to use this content

Three scenarios that would unlock this writeup:

1. **camelAI exposes OpenRouter `:free` model variants in the picker.** The shipped model list grows beyond the current five, and the user can route to a `:free` model directly. Drop this section under "Can I use camelAI without paying anyone?" on `/plans/model-providers`.
2. **Grok and Kimi ship through OpenRouter.** If those land as paid options first, this writeup still has value as the "low-budget OpenRouter playbook" — pair Kimi or a `:free` Grok variant with a $5 OpenRouter top-up for near-zero spend. Use it as a sidebar or supporting paragraph alongside the Grok/Kimi launch announcement.
3. **A "Free path" or "Tightest budget" page is added later.** This block can stand alone as a short standalone page if support requests show users keep asking the same question.

---

## Draft section: "Using OpenRouter for the lowest possible spend"

> _The next agent should drop this in as a block under the OpenRouter section on `/plans/model-providers`, or as a standalone subsection. Keep the tone matter-of-fact: this is a power-user path, not a marketing claim._

OpenRouter offers a pool of free model variants, identified by a `:free` suffix on the model slug (for example, `deepseek/deepseek-r1:free`). Accounts that have never purchased credits can use these models with strict daily limits. If you've topped up at least once, the daily ceiling rises significantly.

**The path to running camelAI for as close to $0 as possible:**

1. Sign up for camelAI (no payment method required).
2. Create an OpenRouter account at [openrouter.ai](https://openrouter.ai). Don't add a payment method.
3. Generate an OpenRouter API key.
4. Add the key to camelAI under **Settings → AI Provider → OpenRouter.**
5. In the model picker, select a free model variant.

### What to expect

OpenRouter's free models share capacity across all users and route to whichever upstream is available, so they can be unavailable, slow, or heavily throttled at peak times. As of OpenRouter's [API rate limits page](https://openrouter.ai/docs/api-reference/limits) at the time of writing:

- **About 50 free-model requests per day** for accounts that have never purchased credits, with a per-minute cap on top.
- **About 1,000 free-model requests per day** once the account has purchased $10 or more in OpenRouter credits at any point in the past.

Free models are **not reliable for production work.** If you hit the limit or need consistent uptime, three paths forward:

- **Top up OpenRouter** with as little as $5–$10 to lift the daily cap and gain access to paid models on your own bill.
- **Switch to a different BYOK provider** (Anthropic, OpenAI, or Bedrock) with prepaid credits.
- **Upgrade to a paid camelAI plan** to use hosted credits instead.

> _Verify both OpenRouter URLs and the daily-request numbers at publish time. OpenRouter's docs use templated values that shift._

---

## Tie-in for the Grok / Kimi launch

If Grok and Kimi ship through OpenRouter, this writeup pairs naturally with that announcement. Two angles to consider:

- **"OpenRouter just got Grok and Kimi."** Lead with the new model availability, then add a sentence pointing at the `:free` variant playbook for budget-conscious users.
- **"The cheapest way to use camelAI."** Lead with the playbook, position Grok and Kimi as the latest reasons OpenRouter is the most flexible BYOK option.

Either way, the existing Model Providers page already has the OpenRouter section set up to absorb this content without restructuring.

---

## Source citations

- **Model picker options (current state):** `chiridion-app/src/lib/llm-provider-config.ts:15-32`
- **OpenRouter API key validation:** `chiridion-app/src/routes/api/orgs.$id.llm-provider.ts:180, 295`
- **OpenRouter free-model rate limits:** [openrouter.ai/docs/api-reference/limits](https://openrouter.ai/docs/api-reference/limits)
- **OpenRouter free model variants:** [openrouter.ai/docs/guides/routing/model-variants/free](https://openrouter.ai/docs/guides/routing/model-variants/free)
- **OpenRouter BYOK guide:** [openrouter.ai/docs/use-cases/byok](https://openrouter.ai/docs/use-cases/byok)
