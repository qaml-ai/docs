# Pass 1: Docs Cleanup Plan — Remove Legacy, Deprecate API/Embedded, Remove MCP & Self-Hosting

> **Context for implementing agent:** This plan covers the first pass of a docs overhaul for camelAI. The company has pivoted from a deep research BI agent to a coding agent with a persistent computer. This pass is about **removing** dead content (MCP, self-hosting), **deprecating** the API/Embedded offering (still has paying customers), and **rewriting** the landing page. A second pass will follow to add new content for the new product. Read `camelAI-company-context.md` for full product context.

---

## Summary of What's Changing

camelAI was a BI/analytics product (text-to-SQL, dashboards, embedded iframe analytics). It is now a **coding agent with a persistent computer** — users chat with an agent powered by their selected model that builds, deploys, and maintains web applications on Cloudflare's edge infrastructure.

**DELETE entirely (no active users):**
- **MCP Server** (all integration pages)
- **Self-Hosting** (Docker installation, all config pages)

**DEPRECATE with warnings (still has paying customers, being migrated off):**
- **Embedded API / iframe offering** (the entire `dev_api/` section)
- **askCamel API** (text-to-SQL endpoint)
- **API Reference** (OpenAPI auto-generated docs)
- **Developer Console** references (`console.camelai.com`)
- **Embedded Changelog**

**REWRITE:**
- **Getting Started overview** — new product description
- **App Changelog** — reframed as legacy history

---

## 1. Navigation Overhaul — `docs.json`

### Current tabs (5):
1. Getting Started
2. API
3. API Reference
4. Self-Hosting
5. Changelog

### Target tabs (4):
1. **Getting Started** — rewritten overview page (Pass 2 will add more pages here)
2. **Changelog** — kept, simplified to one page
3. **API (Legacy)** — existing API docs preserved with deprecation warnings, moved to end
4. **API Reference (Legacy)** — existing OpenAPI docs preserved, moved to end

### Changes to `docs.json`:

#### Remove these tabs entirely:
- **Self-Hosting** tab (Docker Installation group, Configuration group)

#### Move and rename these tabs to the end of the tab list:
- **API** → rename to **"API (Legacy)"** — keep all existing groups and pages as-is
- **API Reference** → rename to **"API Reference (Legacy)"** — keep the OpenAPI spec reference

#### Update the Getting Started tab:
```json
{
  "tab": "Getting Started",
  "groups": [
    {
      "group": "Start Here",
      "pages": [
        "getting-started/overview"
      ]
    }
  ]
}
```
- Remove `getting-started/for-developers` from navigation (page will be deleted)

#### Update the Changelog tab:
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
- Keep `changelog/embedded` — it documents the embedded offering that still has customers. Add a deprecation notice (see Section 3).

#### Final tab order in `docs.json`:
```json
"tabs": [
  { "tab": "Getting Started", ... },
  { "tab": "Changelog", ... },
  { "tab": "API (Legacy)", ... },
  { "tab": "API Reference (Legacy)", ... }
]
```

#### Update global anchors:
Remove these anchors:
- **GitHub** (`https://github.com/qaml-ai/camelAI-docker-compose`) — this was the self-hosted Docker repo

Keep these anchors:
- **Agent App** (`https://app.camelai.com`) — still valid, this is the new product
- **Developer Console** (`https://console.camelai.com`) — still needed by legacy API customers
- **Website** (`https://camelai.com`) — still valid

#### Update footer:
- Remove the GitHub social link (`https://github.com/qaml-ai/camelAI-docker-compose`)

#### Update navbar primary CTA:
- Keep "Try camelAI" pointing to `https://app.camelai.com` — this is correct for the new product

---

## 2. Pages to DELETE

These files should be deleted from the repo entirely. They document dead offerings with no active users.

### MCP Server (6 files)
- `mcp_server/introduction.mdx`
- `mcp_server/getting-started.mdx`
- `mcp_server/claude-integration.mdx`
- `mcp_server/cursor-integration.mdx`
- `mcp_server/windsurf-integration.mdx`
- `mcp_server/mircosoft-copilot-integration.mdx`

### Self-Hosting — Installation (8 files)
- `installation/quickstart.mdx`
- `installation/prerequisites.mdx`
- `installation/docker-compose.mdx`
- `installation/environment-variables.mdx`
- `installation/azure-openai-setup.mdx`
- `installation/creating-superuser.mdx`
- `installation/logging-in.mdx`
- `installation/initial-setup.mdx`

### Self-Hosting — Configuration (2 files)
- `setup/rbac.mdx`
- `setup/datasource-setup.mdx`

### Self-Hosting / App intro (2 files)
- `app/introduction.mdx`
- `app/plans.mdx`

### Developer-focused Getting Started
- `getting-started/for-developers.mdx`

### Snippets (conditional)
- `snippets/snippet-intro.mdx` — check if this is referenced by any remaining pages. If not, delete it.

### Total: ~20 files to delete

---

## 3. Pages to Add Deprecation Warnings To

These pages stay in the repo and remain navigable, but each one gets a prominent `<Warning>` banner at the top (immediately after the frontmatter) to make it clear this offering is no longer being updated.

### Standard deprecation banner

Add this exact block to the **top of every page listed below**, right after the frontmatter `---`:

```mdx
<Warning>
  **camelAI Legacy Product** — This documentation covers camelAI's embedded analytics offering, which is no longer being actively developed. We are migrating existing customers to the new camelAI platform. For the current product, visit [camelAI](https://app.camelai.com).
</Warning>
```

### Pages to add the banner to:

#### API / Embedded — General (2 files)
- `dev_api/introduction.mdx`
- `dev_api/pricing.mdx`

#### API / Embedded — Quick Start (1 file)
- `dev_api/camel-api-quickstart.mdx`

#### API / Embedded — Row Level Security (4 files)
- `dev_api/row-level-security/introduction.mdx`
- `dev_api/row-level-security/postgresql.mdx`
- `dev_api/row-level-security/clickhouse.mdx`
- `dev_api/row-level-security/bigquery.mdx`

#### API / Embedded — Best Practices (3 files)
- `dev_api/knowledge-base-guide.mdx`
- `dev_api/reference-query-guide.mdx`
- `dev_api/model-selection-guide.mdx`

#### API / Embedded — Custom Themes (6 files)
- `dev_api/custom-themes/introduction.mdx`
- `dev_api/custom-themes/default-theme.mdx`
- `dev_api/custom-themes/appearance.mdx`
- `dev_api/custom-themes/response-modes.mdx`
- `dev_api/custom-themes/start-chat-message.mdx`
- `dev_api/custom-themes/recommendations.mdx`

#### Embedded Changelog (1 file)
- `changelog/embedded.mdx`

#### Stale dev_api files not in nav but still in repo (2 files)
- `dev_api/bigquery-rls.mdx` — add banner if keeping, or delete if it's just a leftover redirect
- `dev_api/row-level-security.mdx` — same, check if it's a redirect/duplicate

### Total: ~19 pages get the deprecation banner

### Note on the API Reference (Legacy) tab
The API Reference tab is auto-generated from the OpenAPI spec at `https://api.camelai.com/api/schema/`. We can't inject a `<Warning>` into auto-generated pages. Instead, the tab name "API Reference (Legacy)" serves as the signal. If Mintlify supports a tab-level description or banner, add one there. Otherwise the tab rename is sufficient.

---

## 4. Pages to REWRITE

### `getting-started/overview.mdx` — Full Rewrite

**Current:** Describes camelAI as "AI-powered business intelligence for everyone" with links to web app, developer docs, and a note about connecting databases.

**New content should:**
- Update title/description: "camelAI — A coding agent with a persistent computer"
- Describe the new product: chat with an agent powered by your selected model, build apps, publish to live URLs
- Hero CTA: "Try camelAI" → `https://app.camelai.com` (keep this)
- Replace "What We Offer" cards with cards highlighting new platform capabilities
- Remove the Note about starting with the web app before integrating (no longer relevant)
- Add a brief "What can you build?" section with use case examples

**Suggested Mintlify layout:**

```mdx
---
title: 'What is camelAI?'
description: 'A coding agent with a persistent computer'
---

camelAI is a coding agent with a persistent computer. Pick the model you want to
use, then chat with an agent that builds, deploys, and maintains web applications
connected to your data, your tools, and AI models.

<Card
  title="Try camelAI"
  icon="rocket"
  color="#3b82f6"
  href="https://app.camelai.com"
>
  **No credit card required.** Start building in minutes.
</Card>

## Platform Capabilities

<CardGroup cols={2}>
  <Card title="Build Full-Stack Apps" icon="code">
    Chat with the agent to build complete web applications with React,
    TypeScript, and Tailwind. Production-quality UI is included from the start.
  </Card>
  <Card title="Publish Instantly" icon="globe">
    Deploy any project to a live URL with one click. DNS, SSL, and CDN handled
    automatically.
  </Card>
  <Card title="Persistent Workspace" icon="hard-drive">
    Your files, databases, and projects survive across sessions. Pick up where
    you left off anytime.
  </Card>
  <Card title="50+ Integrations" icon="plug">
    Connect to Postgres, Snowflake, Stripe, Slack, GitHub, Notion, and dozens
    more. Credentials are securely injected into your apps.
  </Card>
  <Card title="AI-Powered Apps" icon="brain">
    Build apps that themselves use AI — chatbots, summarizers, content generators.
    Native AI bindings included in every project.
  </Card>
  <Card title="Autonomous Agents" icon="clock">
    Schedule cron jobs for recurring tasks. The agent runs autonomously —
    generating reports, syncing data, monitoring metrics.
  </Card>
</CardGroup>

## What Can You Build?

<CardGroup cols={2}>
  <Card title="AI-Powered Apps" icon="robot">
    Customer support chatbots, AI writing assistants, lead qualification tools,
    meeting notes summarizers
  </Card>
  <Card title="Internal Tools" icon="wrench">
    Admin panels, multi-source dashboards, bug report portals — connected to
    your real data
  </Card>
  <Card title="Automated Workflows" icon="arrows-spin">
    Daily reports from your data warehouse, Slack alerts from Stripe events,
    hourly metric monitors
  </Card>
  <Card title="Sites & Forms" icon="browser">
    Landing pages, feedback forms, booking pages, portfolio sites — all with
    live backends
  </Card>
</CardGroup>
```

### `changelog/app.mdx` — Light Edit

**Current:** Contains version history from 0.1.x through 0.5.0, all describing the Legacy BI product features.

**Changes:**
- Update the page title and description:
  - Title: `"Changelog"` (drop "App" since it's now the primary changelog)
  - Description: `"Updates to camelAI"` (generic — will cover both legacy history and new product going forward)
- Add an `<Info>` callout at the very top (before the first `<Update>`) explaining that entries before a certain date reflect camelAI Legacy:

```mdx
<Info>
  Entries dated before 2026 reflect **camelAI Legacy**, our original AI-powered
  business intelligence product. camelAI has since evolved into a coding agent
  with a persistent computer.
</Info>
```

- Remove the MCP-specific section from the October 2, 2024 update — specifically the `### MCP (Model Context Protocol) Support` header and its two bullet points. The rest of that update entry (Chat History, Connections Redesign, etc.) stays as historical record.
- Remove the Docker-specific `<Warning>` tag in the May 26, 2025 entry ("Enterprise users must request access to Claude Sonnet 4 in AWS Bedrock before updating Docker.") since self-hosting is dead.

### `changelog/embedded.mdx` — Light Edit

**Changes:**
- Add the standard deprecation banner (from Section 3) at the top
- Update title to: `"Embedded Changelog (Legacy)"`
- Update description to: `"Updates to camelAI's embedded analytics offering (no longer actively developed)"`

---

## 5. Config & Metadata Cleanup

### Check for broken internal links
After deletions, grep the remaining files for any links that point to deleted pages. Common patterns to search for:
- `/installation/`
- `/setup/`
- `/mcp_server/`
- `/getting-started/for-developers`
- `/app/introduction`
- `/app/plans`
- `/embedded/`
- `camelAI-docker-compose` (GitHub repo references)

For links found in **remaining active pages** (overview, changelog): remove or replace with appropriate alternatives.
For links found in **deprecated legacy pages** (dev_api/*): leave as-is — these are frozen docs, don't need link hygiene.

### Remove MCP references from non-MCP pages
Grep all remaining files for "MCP" and remove any cross-references to the deleted MCP section. The only MCP mention that should survive is the historical changelog entry header (if we decide to keep it as historical record — but per section 4, we're removing it from the app changelog).

---

## 6. Implementation Order

Execute in this order to minimize broken states:

1. **Update `docs.json`** — Remove Self-Hosting tab. Remove `for-developers` from Getting Started. Rename and reorder API tabs to end. Remove GitHub anchor and footer link. Remove `changelog/embedded` from the Changelog group (it moves to the legacy section mentally, but stays in Changelog tab).
2. **Delete files from Section 2** (~20 files) — MCP, Self-Hosting, app intro/plans, for-developers.
3. **Add deprecation banners from Section 3** (~19 files) — Add the `<Warning>` block to every legacy API/Embedded page.
4. **Rewrite `getting-started/overview.mdx`** — Replace BI messaging with new product description using the suggested layout.
5. **Edit `changelog/app.mdx`** — Update title/description, add Legacy `<Info>` callout, remove MCP section, remove Docker warning.
6. **Edit `changelog/embedded.mdx`** — Add deprecation banner, update title/description.
7. **Grep for broken links** — Search remaining active pages for references to deleted paths. Fix any found.
8. **Verify** — Run `mintlify dev` locally to confirm no build errors or broken references.

---

## 7. What This Plan Does NOT Cover (Deferred to Pass 2)

These are explicitly **out of scope** for this pass and will be handled in a follow-up plan:

- New documentation pages for the new product (workspace, publishing, integrations, cron jobs, email inbox, image generation, etc.)
- Updated pricing/plans page for the new product
- New changelog entries for the new product
- Any new navigation structure beyond the current setup
- Updated branding, logos, or color scheme
- SEO redirects for deleted pages
- New screenshots or demo videos
- Eventually removing the Legacy tabs entirely (once all customers are migrated)
