# Pass 3: Changelog Restructure — Implementation Plan

> **Context for implementing agent:** camelAI has pivoted from a BI/analytics product to a coding agent with a persistent computer. The docs changelog needs to reflect this. The embedded analytics offering is dead. The legacy BI product still runs at ~$200k ARR but won't receive updates. This pass restructures the Changelog tab to separate the old product's history from the new product's updates.

---

## Current State

The Changelog tab currently has two pages:

| Page | File | Content |
|------|------|---------|
| `changelog/app` | `changelog/app.mdx` | 7 updates (Apr 2025 – Oct 2025) covering the legacy BI product. Has an `<Info>` banner noting pre-2026 entries are legacy. |
| `changelog/embedded` | `changelog/embedded.mdx` | 2 updates (Aug – Oct 2025) covering the embedded analytics/API offering. Already has a `<Warning>` banner marking it as legacy. |

### Problems

1. **`changelog/embedded` should be removed entirely.** The embedded/API offering is dead — no customers should be directed here, and the dedicated API changelog tab adds confusion.
2. **`changelog/app` mixes old and new product context.** All 7 entries are legacy BI content, but the page is titled just "Changelog" — implying it's the current product.
3. **There is no changelog for the new camelAI product** (the coding agent). The new product is in beta and needs its own changelog to communicate updates to beta users.

---

## Target State

The Changelog tab should have **two pages** under a single "Changelog" tab:

```
Changelog (tab)
├── Updates (group)
│   ├── changelog/platform        ← NEW — the new camelAI product (beta)
│   └── changelog/legacy          ← RENAMED — old BI product history
```

### What gets removed
- `changelog/embedded.mdx` — deleted entirely. This page covers the embedded analytics/API offering which is no longer being updated. Its content does not need to be preserved in the docs (it's in git history if ever needed).

### What gets renamed/moved
- `changelog/app.mdx` → `changelog/legacy.mdx` — all existing entries stay, but the page gets a new title, description, and prominent banner marking it as the legacy BI product.

### What gets created
- `changelog/platform.mdx` — net new page for the current camelAI product (coding agent with persistent computer), marked as **Beta**.

---

## Detailed Page Specs

### 1. `changelog/platform.mdx` — NEW

**Purpose:** Communicate updates to beta users of the new camelAI product.

**Frontmatter:**
```yaml
---
title: 'Changelog'
description: 'Updates to camelAI — your coding agent with a persistent computer'
icon: 'megaphone'
---
```

**Top banner:** Use a Mintlify `<Info>` callout to flag the product as in beta:

```mdx
<Info>
  camelAI is currently in **beta**. We're shipping fast — check back often
  for new features and improvements.
</Info>
```

**Initial entry:** A single launch entry announcing the beta. This communicates to users that the changelog is alive and sets the format for future entries. Content should summarize the core platform capabilities at beta launch — not re-document them (that's what the Getting Started pages are for), but give a high-level "here's what you're getting" entry.

```mdx
<Update label="March 2026" description="Beta Launch">
### camelAI Beta

The new camelAI is live. A coding agent with a persistent computer — describe what you want, the agent builds it, and it's live on the internet.

#### What's included in beta

- **Persistent workspace** — a real Linux computer with 100GB storage. Files, databases, and projects survive across sessions.
- **Auto-deploy** — apps go live at `*.camelai.app` URLs automatically as the agent builds them. No publish step.
- **50+ integrations** — connect databases (Postgres, MySQL, Snowflake, BigQuery, and more), SaaS tools (Notion, Slack, Stripe, HubSpot, and more), and dev tools (GitHub, Linear, Sentry).
- **Cron jobs** — schedule the agent to run autonomously on any recurring schedule. Full workspace access on every run.
- **Email inbox** — every workspace gets a unique email address. Email the agent from your inbox without opening camelAI.
- **Slack integration** — message the agent from Slack. DM or mention it in a channel.
- **AI-powered apps** — build apps that use text models, image generation, and other AI features without managing API keys.
- **Multiplayer** — team members share workspace access. Multiple people can chat with the same agent.
- **Image generation** — the agent can generate images on demand using Google Gemini via Cloudflare AI Gateway.

#### Coming soon

- Custom domains for published apps
- Agent wallet (X402 payments)
- Additional templates and starter projects

<Tip>
  camelAI beta is free. [Sign up at app.camelai.com](https://app.camelai.com) to get started.
</Tip>
</Update>
```

**Mintlify components used:** `<Info>`, `<Update>`, `<Tip>`

---

### 2. `changelog/legacy.mdx` — RENAMED from `changelog/app.mdx`

**Changes from current file:**

1. **Update frontmatter** — new title and description that clearly label this as the legacy product:

```yaml
---
title: 'Legacy Changelog'
description: 'Update history for camelAI Legacy — our original AI-powered business intelligence product'
icon: 'clock-rotate-left'
---
```

2. **Replace the existing `<Info>` banner** with a more prominent `<Warning>` banner:

```mdx
<Warning>
  **camelAI Legacy** — This changelog covers our original AI-powered business
  intelligence product. camelAI Legacy is still available but is no longer
  receiving new features. For the current product — a coding agent with a
  persistent computer — see the [main changelog](/changelog/platform).
</Warning>
```

3. **All existing `<Update>` entries stay exactly as-is.** No content changes to the 7 existing entries. They are accurate history for the legacy product.

**Mintlify components used:** `<Warning>`, existing `<Update>` entries unchanged

---

### 3. `changelog/embedded.mdx` — DELETE

Remove this file entirely. The embedded analytics/API offering is dead and should not appear in the docs navigation. Git history preserves the content if ever needed.

---

## `docs.json` Navigation Changes

Replace the current Changelog tab config:

**Current:**
```json
{
  "tab": "Changelog",
  "groups": [
    {
      "group": "Updates",
      "pages": [
        "changelog/app",
        "changelog/embedded"
      ]
    }
  ]
}
```

**Target:**
```json
{
  "tab": "Changelog",
  "groups": [
    {
      "group": "Updates",
      "pages": [
        "changelog/platform",
        "changelog/legacy"
      ]
    }
  ]
}
```

No other `docs.json` changes needed. The Getting Started tab, API (Legacy) tab, API Reference (Legacy) tab, global anchors, navbar, logo, and footer all stay the same.

---

## Implementation Steps

1. Create `changelog/platform.mdx` with the beta launch entry
2. Rename `changelog/app.mdx` → `changelog/legacy.mdx` (copy content, update frontmatter and banner)
3. Delete `changelog/embedded.mdx`
4. Delete `changelog/app.mdx` (now replaced by `legacy.mdx`)
5. Update `docs.json` changelog tab navigation
6. Verify with `mintlify dev`

---

## Decisions (Confirmed)

1. **Beta launch date label** — March 10, 2026
2. **"Coming soon" items** — Custom domains only. No mention of wallet or templates.
3. **Legacy changelog icon** — `clock-rotate-left` ✓
4. **Embedded changelog** — Delete fully. Git history preserves it.

---

## What This Plan Does NOT Cover

- Writing future changelog entries (this just sets up the structure)
- Removing the API (Legacy) or API Reference (Legacy) tabs (separate decision)
- Changelog RSS/notification setup (Mintlify supports this but it's not configured currently)
