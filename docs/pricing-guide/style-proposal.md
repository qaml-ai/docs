# Pricing Guide — Style Proposal

A plan for translating [`copy-doc.md`](./copy-doc.md) into two Mintlify MDX pages. This is the design hand-off for the implementing agent.

---

## Design goals

1. **Match the existing house style.** Both pages should feel like siblings of [`getting-started/quickstart.mdx`](../../getting-started/quickstart.mdx) and [`features/email-and-slack.mdx`](../../features/email-and-slack.mdx) — short prose, Steps for procedures, callouts for warnings/tips, CardGroups for parallel options, Accordions for "details users only need on demand."
2. **Make the plan tiers scannable.** A user landing on Plans & Pricing should be able to compare tiers in 10 seconds without reading any prose. Cards do this well; the copy doc's CardGroup layout is honored.
3. **Lead with the choice users actually have to make.** On both pages, the credits-vs-BYOK decision is the load-bearing question. The page should surface it visually rather than burying it inside prose.
4. **Use accordions to manage page length.** Page 2 is long. AccordionGroup keeps it browsable rather than a wall of headings.

I'm following the copy doc's component suggestions verbatim except where noted in **Deviations** below.

---

## Files to create

```
docs/
├── plans/                       ← NEW folder at repo root, alongside getting-started/ and features/
│   ├── overview.mdx             ← "Plans & Pricing"
│   └── model-providers.mdx      ← "Model Providers"
└── docs.json                    ← updated nav (see below)
```

Existing folder `docs/pricing-guide/` stays put — it holds the source copy and this plan, not published content.

---

## Page 1 — `plans/overview.mdx`

### Structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Title:    Plans & Pricing                                            │
│  Subhead:  What's included on each plan, how credits work,           │
│            and how to top up.                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  [intro paragraph — bills two things separately, two ways to pay]    │
│                                                                       │
│  ## Plans                                                             │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│  │   Free       │  │  Starter     │  │  Pro         │                │
│  │   $0/mo      │  │  $40/mo      │  │  $150/mo     │                │
│  │              │  │              │  │  ★ Most      │                │
│  │  • BYOK      │  │  • $10 cred. │  │    popular   │                │
│  │  • 1 wksp    │  │  • 1 wksp    │  │              │                │
│  │  • 5 GB      │  │  • 50 GB     │  │  • $30 cred. │                │
│  │  • 3 apps    │  │  • 30 apps   │  │  • 100 GB    │                │
│  │  • 2 crons   │  │  • 10 crons  │  │  • Unlim apps│                │
│  └──────────────┘  └──────────────┘  └──────────────┘                │
│                                                                       │
│  ┌────────────────────────┐  ┌────────────────────────┐              │
│  │  Team                  │  │  Enterprise            │              │
│  │  $50/seat/mo (3 min)   │  │  Custom                │              │
│  │                        │  │                        │              │
│  │  • $10 cred./seat      │  │  • SSO/SAML            │              │
│  │  • 2 wksp, 100 GB ea.  │  │  • Bring your cloud    │              │
│  │  • Workspace roles     │  │  • HIPAA / SOC 2       │              │
│  │  [link: Contact sales] │  │  [link: Contact sales] │              │
│  └────────────────────────┘  └────────────────────────┘              │
│                                                                       │
│  ## How model usage works                                             │
│                                                                       │
│  ┌──────────────────────┬──────────────────────────┐                 │
│  │ camelAI credits      │ Bring your own API key   │                 │
│  ├──────────────────────┴──────────────────────────┤                 │
│  │ [active tab content — short prose paragraph]    │                 │
│  └─────────────────────────────────────────────────┘                 │
│                                                                       │
│  [callout-style paragraph: "You pick one or the other..."]           │
│                                                                       │
│  ## Why prepaid              [plain prose]                           │
│  ## Topping up credits       [<Steps>]                               │
│  ## Free trial               [plain prose]                           │
│  ## Changing plans           [plain prose]                           │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Component map (Page 1)

| Section | Component | Notes |
|---|---|---|
| Intro paragraph | Plain prose | One sentence per beat, no callout. Mirrors `quickstart.mdx` opener. |
| **Plans** — Free / Starter / Pro | `<CardGroup cols={3}>` with three `<Card>` | See "Card content pattern" below. |
| **Plans** — Team / Enterprise | `<CardGroup cols={2}>` with two `<Card>` | Enterprise card has `href` set to the Contact sales URL. |
| "Most popular" on Pro | Bold text inline at top of Pro card body — `**Most popular**` on its own line. | Mintlify's `<Card>` has no badge prop. Bold text is the cleanest in-component option and reads well in both light/dark mode. **Open question for review** (see below). |
| **How model usage works** | `<Tabs>` with two `<Tab>` ("camelAI credits", "Bring your own API key") | Each tab is ~3 sentences from the copy doc, verbatim. |
| "You pick one or the other…" paragraph | `<Note>` callout | Promotes the constraint above the line so users don't miss it. The copy doc says plain prose, but this is a sharp-edge fact users will trip over — see **Deviations** below. |
| Link out to Model Providers | Plain inline link, `[Model Providers](/plans/model-providers)` | |
| **Why prepaid** | Plain prose | |
| **Topping up credits** | `<Steps>` with 3 `<Step>` | The copy doc's numbered list maps 1:1. |
| **Free trial** | Plain prose | |
| **Changing plans** | Plain prose | |

### Card content pattern

Each tier card uses this shape so they're visually consistent:

```mdx
<Card title="Pro" icon="rocket">
  **$150 / month**

  For power users.

  - $30 of model credits / month
  - Bring your own API key (optional)
  - 1 workspace, 100 GB of storage
  - Unlimited deployed apps
  - Unlimited custom domains
  - 50 cron jobs, 5-minute frequency
  - Email inbox
  - 7-day free trial
</Card>
```

- **Title** = tier name only (no price). Price goes in the body so it can be bold and own its own line.
- **Icon** suggestions (Lucide / Font Awesome names that already work elsewhere in this repo):
  - Free → `circle-dot` (entry-level)
  - Starter → `seedling`
  - Pro → `rocket`
  - Team → `users`
  - Enterprise → `building`
- **Body** opens with bold price, then a one-line "For ___" tagline, then the bullet list. This matches the copy doc's structure.
- Enterprise card additionally gets `href="https://book-demo--camelai-team-d9e.camelai.app/"` so the whole card is clickable.

### Deviations from the copy doc (Page 1)

1. **"You pick one or the other…" wrapped in `<Note>`.** Copy doc says plain prose. I think this single sentence is the load-bearing constraint of the entire pricing page and deserves visual weight. Easy to revert if you disagree.
2. **"Most popular" rendered as bold inline text rather than a true badge.** Mintlify's `<Card>` has no native badge. Alternatives we could use instead: (a) prefix the title — `title="Pro — Most popular"`, (b) put it in an icon position with a colored accent, (c) skip it entirely on the docs page since the in-app paywall already establishes it. **Wants your call.**

---

## Page 2 — `plans/model-providers.mdx`

### Structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Title:    Model Providers                                            │
│  Subhead:  How to use your own API key with camelAI, and what each    │
│            provider unlocks.                                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  [intro: model-agnostic, four BYOK providers, what page covers]      │
│  [paragraph: which models exist + model picker switcher]             │
│                                                                       │
│  ⚠  WARNING                                                           │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Bringing your own key replaces hosted credits entirely.        │  │
│  │ You can't mix and match. If you need multiple model            │  │
│  │ families on one key, use OpenRouter.                           │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ## When to bring your own key  vs  When camelAI credits are simpler │
│                                                                       │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐  │
│  │ Bring your own key when…     │  │ camelAI credits when…        │  │
│  │ • You're on Free             │  │ • No provider account yet    │  │
│  │ • You have provider credits  │  │ • Want one bill              │  │
│  │ • Your company requires it   │  │ • Want all models on one     │  │
│  │ • Want an unsupported prov.  │  │   plan                       │  │
│  └──────────────────────────────┘  └──────────────────────────────┘  │
│                                                                       │
│  ## Supported providers                                               │
│  ▸ Anthropic       (Claude models)                                     │
│  ▸ OpenAI          (GPT-5.5, GPT-5.4, GPT-5.4 Mini)                   │
│  ▸ OpenRouter      (everything camelAI supports, on one key)          │
│  ▸ AWS Bedrock     (models served from your AWS account)              │
│  [each row is an Accordion that expands to show key URL + notes]      │
│                                                                       │
│  ## Using a provider we don't support directly (Azure, Vertex, etc.) │
│  [intro paragraph]                                                    │
│  ### How it works                                                     │
│  - Microsoft Azure OpenAI                                             │
│  - Google Vertex AI                                                   │
│  - AWS Bedrock                                                        │
│  - Others                                                             │
│  ### Setup with Azure as the example                                  │
│  [<Steps> with 5 steps]                                               │
│                                                                       │
│  ℹ  NOTE                                                              │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Native Azure or Vertex support isn't on the near-term roadmap. │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ## Adding a key            [<Steps>, 4 steps]                        │
│                                                                       │
│  ## Using camelAI on the cheap                                        │
│  💡 TIP                                                                │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Cheap models are 10–50× less expensive and handle most         │  │
│  │ everyday work just as well. Pair a cheap model with a small   │  │
│  │ OpenRouter top-up = lowest cost.                               │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  The playbook:    [<Steps>, 5 steps]                                  │
│                                                                       │
│  ## FAQ                                                               │
│  ▸ Can I use my key for one model and credits for another?           │
│  ▸ Do plan credits roll over?                                         │
│  ▸ Why does my new key say "billing error"?                          │
│  ▸ Does camelAI charge a markup?                                      │
│  ▸ Can I see how much I've spent?                                     │
│  ▸ Do you support Azure OpenAI or Vertex AI?                          │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Component map (Page 2)

| Section | Component | Notes |
|---|---|---|
| Intro + model list paragraph | Plain prose | |
| "Bringing your own key replaces…" | `<Warning>` | Verbatim from copy doc. |
| **When to BYOK** + **When credits are simpler** | Two `<Card>` side-by-side inside a `<CardGroup cols={2}>` | See **Deviations** — copy doc suggests two prose blocks or Tabs; I'm proposing parallel Cards because the comparison is the whole point of the section. Tabs hide one side; prose buries it. |
| "Supported providers" | `<AccordionGroup>` of four `<Accordion>` | Title pattern: `title="OpenRouter — every model camelAI supports, on one key"` so the user sees what each unlocks without expanding. |
| Inside each provider Accordion | Plain prose + bold "Get a key" link | Keep tight. No nested components. |
| **Using a provider we don't support directly** intro | Plain prose | |
| Provider list (Azure / Vertex / Bedrock / Others) | Plain bulleted list | Matches copy doc. |
| **Setup with Azure as the example** | `<Steps>` with 5 `<Step>` | |
| "Native Azure or Vertex support isn't on the roadmap" | `<Note>` | Verbatim from copy doc. |
| **Adding a key** | `<Steps>` with 4 `<Step>` | |
| "Using camelAI on the cheap" lead | `<Tip>` | Verbatim. |
| The playbook | `<Steps>` with 5 `<Step>` | The 4 cheap-model bullets in step 4 stay as a nested unordered list inside that `<Step>`. |
| **FAQ** | `<AccordionGroup>` with 6 `<Accordion>` | Title = the question, body = the answer. |

### Deviations from the copy doc (Page 2)

1. **BYOK-vs-credits decision rendered as parallel Cards** rather than two prose blocks or Tabs. Reason: the whole section exists to help users compare the two options. Tabs require a click to see the other side; stacked prose makes the comparison hard. Two Cards side-by-side put the trade-off in one glance. This deviation is the one I'd most like your sign-off on.
2. **"Supported providers" Accordion titles include what each unlocks.** E.g., `OpenRouter — every model camelAI supports, on one key` rather than just `OpenRouter`. Lets users skim and pick without expanding every accordion. The detail prose inside stays the same.

Everything else on Page 2 follows the copy doc's component plan exactly.

---

## `docs.json` change

Insert a new group between **Core Concepts** and **Features** in the Getting Started tab:

```json
{
  "group": "Plans & Billing",
  "pages": [
    "plans/overview",
    "plans/model-providers"
  ]
}
```

No other navigation changes. Verbatim from the copy doc.

---

## Cross-link updates to existing pages

After the two new pages are published:

1. **[`getting-started/overview.mdx`](../../getting-started/overview.mdx)** — extend the bottom "Live Examples" section, OR add a new Card to the "What's next?"-style group at the bottom. The copy doc says "bottom CardGroup" — I'll add it to a new "Get Started" CardGroup near the top instead, since the bottom is currently example apps. **Open question:** confirm placement. Card:
   ```mdx
   <Card title="Plans & pricing" icon="credit-card" href="/plans/overview">
     What's included on each plan, how credits work
   </Card>
   ```

2. **[`getting-started/quickstart.mdx:11`](../../getting-started/quickstart.mdx#L11)** — replace `No credit card required — the beta is free.` with `Free tier available with your own API key. See [plans and pricing](/plans/overview).`

3. **[`getting-started/connections.mdx`](../../getting-started/connections.mdx)** — in the AI Services tab (currently line 73-75), add a `<Note>` after the provider list:
   ```mdx
   <Note>
     These connections let apps the agent builds call AI models. They don't power
     the agent itself — for that, see [Model Providers](/plans/model-providers).
   </Note>
   ```

4. **[`getting-started/publishing.mdx:62-65`](../../getting-started/publishing.mdx#L62-L65)** — the "Custom domains" Accordion currently says they're "coming soon." Rewrite to reflect that they're live, with per-plan caps linked from `/plans/overview`. Suggested replacement:
   ```mdx
   <Accordion title="Custom domains">
     Bring your own domain and serve apps from it. Available on Starter, Pro, Team,
     and Enterprise plans — see [plans and pricing](/plans/overview) for per-plan
     limits. Configure under **Settings → Domains** in your workspace.
   </Accordion>
   ```

---

## Open questions for you

Three small calls I want your sign-off on before implementation. None block, all reversible.

1. **"Most popular" on the Pro card** — bold text inline (proposed), title prefix, or skip on the docs page? Mintlify has no native badge.
2. **`<Note>` around "You pick one or the other…"** on Page 1 — is the visual weight worth deviating from the copy doc's plain-prose suggestion?
3. **Side-by-side Cards for BYOK-vs-credits** on Page 2 — is the parallel comparison better than the copy doc's prose-or-Tabs suggestion?

If you say "go ahead" I'll default to the proposed answers above (bold inline / yes Note / yes side-by-side).

---

## What the implementing agent gets

When this plan is approved, the implementing agent will have:

- The verbatim copy in [`copy-doc.md`](./copy-doc.md) (Pages 1 and 2 sections).
- This component map and structural plan.
- The `docs.json` patch.
- The four cross-link edits with exact strings to find/replace.

Source citations for fact-checking are in the copy doc's "Source citations" section and don't need to be re-read during build — copy is already reconciled to shipped code.
