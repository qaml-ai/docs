# Pass 2: New Product Documentation — Implementation Plan

> **Context for implementing agent:** This plan covers adding new documentation pages for the current camelAI product — a coding agent with a persistent computer. Pass 1 stripped legacy content. This pass adds the essential pages users need during beta. Keep it lean — we don't yet know where users get confused, so we're covering the fundamentals and nothing more.

---

## Philosophy

- **Minimal viable docs.** A handful of focused pages, not an encyclopedia.
- **Show, don't lecture.** Use Mintlify interactive components (Cards, Steps, Tabs, Accordions) to make pages scannable and actionable.
- **Match the sales site voice.** Confident, direct, no jargon. The sales site says "Describe anything. camelAI builds it, deploys it, keeps it running." — docs should feel like the same product.
- **Answer "how do I..." not "what is..."** — users in beta already know what camelAI is. They need help doing specific things.

---

## Proposed Site Structure

### Navigation (`docs.json`)

```
Getting Started (tab)
├── Start Here (group)
│   ├── overview              ← exists, light refresh
│   └── quickstart            ← NEW
│
├── Core Concepts (group)
│   ├── workspace             ← NEW
│   ├── publishing            ← NEW
│   └── connections           ← NEW
│
├── Features (group)
│   ├── cron-jobs             ← NEW
│   └── email-and-slack       ← NEW

Changelog (tab)                ← unchanged from pass 1
API (Legacy) (tab)             ← unchanged from pass 1
API Reference (Legacy) (tab)   ← unchanged from pass 1
```

### Global Anchors Update
- Keep: **Agent App** (`https://app.camelai.com`), **Website** (`https://camelai.com`)
- Remove: **Developer Console** (`https://console.camelai.com`) — this is the legacy embedded console. No new users should be directed here.

**Total new pages: 5** (plus light refresh of overview)

---

## Page Skeletons with Full Copy

### 1. `getting-started/overview.mdx` — Light Refresh (exists)

The current page is solid. Changes needed:

- Update the hero description to better match the sales site: "Describe anything. camelAI builds it, deploys it, keeps it running."
- Add a `<Steps>` block at the bottom that links to the quickstart
- Add a "Learn More" `<CardGroup>` at the bottom linking to the new Core Concepts pages
- Link to live demo apps from the sales site in the "What Can You Build?" section so users can click through and see real examples

**Suggested additions at bottom of page:**

```mdx
## Get Started

<Steps>
  <Step title="Build your first app">
    Follow the [quickstart guide](/getting-started/quickstart) to go from idea to
    live URL in minutes.
  </Step>
  <Step title="Explore the platform">
    Learn about your [workspace](/getting-started/workspace), [publishing](/getting-started/publishing),
    and [connections](/getting-started/connections).
  </Step>
</Steps>

## Live Examples

Every app below was built and deployed entirely by camelAI.

<CardGroup cols={2}>
  <Card title="WishBoard" icon="bookmark" href="https://wishboard--camelai-team-d9e.camelai.app/">
    A Pinterest-style bookmarking app with automatic Open Graph images
  </Card>
  <Card title="Vela — Stripe Dashboard" icon="chart-line" href="https://vela-dashboard--tools-558.camelai.app/">
    18 months of SaaS revenue, churn, and cohort analysis
  </Card>
  <Card title="Loopform Support Bot" icon="robot" href="https://loopform--camelai-team-d9e.camelai.app/">
    An AI support bot for a form-building SaaS
  </Card>
  <Card title="AI News Daily" icon="newspaper" href="https://ai-news-daily--ms-workspace-b3c.camelai.app">
    A newspaper-style site that posts a roundup of AI news every morning
  </Card>
</CardGroup>
```

**Mintlify components:** `<Card>`, `<CardGroup>`, `<Steps>`, `<Step>`

---

### 2. `getting-started/quickstart.mdx` — NEW

**Purpose:** Get a user from zero to a live app in under 5 minutes.

**Key facts for copy:**
- Signup auto-provisions an org and workspace — no manual creation step
- After signup, user is dropped into a conversation where the agent asks introductory questions to help them get started
- **Apps are auto-deployed** — as soon as the agent builds something, it's live at a `*.camelai.app` URL. There is no separate "publish" step.
- Users iterate by continuing to chat — changes go live automatically
- The agent produces great results reliably — any prompt works
- Good demo prompt candidates from the sales site: bookmark manager (WishBoard), blog platform (Flow Desk), or AI support bot (Loopform)

**Full page copy:**

```mdx
---
title: 'Build Your First App'
description: 'Go from idea to live URL in minutes'
---

Let's build a web app and get it live — all from a single conversation.

<Steps>
  <Step title="Sign up">
    Go to [app.camelai.com](https://app.camelai.com) and create an account. No credit
    card required — the beta is free.

    We automatically set up your organization and workspace — a persistent computer
    where your agent lives. Everything you build here survives across sessions.
  </Step>

  <Step title="Chat with your agent">
    After signup, you're dropped right into a conversation. The agent will ask you a
    few questions to understand what you want to build — just answer naturally.

    Or jump straight in with a request:

    > Build me a personal bookmark manager where I can save links with tags, star
    > my favorites, and search through everything.

    The agent scaffolds a full-stack app with React, TypeScript, Tailwind, and
    shadcn/ui — then starts building. You'll see files appear in your workspace as
    it works.

    <Tip>
      You don't need to be specific about technology choices. The agent picks the right
      tools and builds production-quality UI by default.
    </Tip>
  </Step>

  <Step title="It's already live">
    As soon as the agent builds your app, it's deployed to a live URL at
    `*.camelai.app` — automatically. There's no publish button, no deploy step.
    DNS, SSL, and CDN are all handled for you.

    Copy the URL and share it with anyone. Your app is on the internet.

    <Info>
      Apps stay live even when you're not in camelAI. They're real production services
      on Cloudflare Workers — zero cold start, globally distributed.
    </Info>
  </Step>

  <Step title="Keep iterating">
    Your app is live, but you're not done. Keep chatting to add features, fix things,
    or change the design:

    > Add a dark mode toggle

    > Make the search filter by tags too

    > Change the color scheme to match my brand

    Changes go live automatically as the agent makes them.
  </Step>
</Steps>

## What's next?

<CardGroup cols={3}>
  <Card title="Your Workspace" icon="hard-drive" href="/getting-started/workspace">
    Understand the persistent computer
  </Card>
  <Card title="Your Apps" icon="globe" href="/getting-started/publishing">
    URLs, public vs. private, managing apps
  </Card>
  <Card title="Connections" icon="plug" href="/getting-started/connections">
    Connect to 50+ databases and tools
  </Card>
</CardGroup>
```

**Mintlify components:** `<Steps>`, `<Step>`, `<Tip>`, `<Info>`, `<CardGroup>`, `<Card>`

**Screenshots needed (from Illiana):**
- [ ] Onboarding chat / agent asking intro questions (optional — page works without it)
- [ ] Chat showing agent building an app (optional — nice to have)

---

### 3. `getting-started/workspace.mdx` — NEW

**Purpose:** Explain the persistent computer concept — the single most differentiating feature.

**Key facts for copy:**
- 100GB of XFS storage, fixed for all plans (no tiering yet)
- Users can create unlimited workspaces during beta (no count limit enforced)
- Containers are reaped after ~30s of inactivity, but files persist on host filesystem — users may notice a brief startup delay when returning
- Computer-based, not project-based: any chat can work on any file. This is the key differentiator vs Replit/Lovable/Bolt
- File browser supports: code syntax highlighting (Shiki), notebook rendering (report + notebook modes), image preview, markdown rendering, chart preview (Vega/Plotly), DataFrame tables
- Team members share workspace access — multiplayer by design

**Full page copy:**

```mdx
---
title: 'Your Workspace'
description: 'A persistent computer that never resets'
---

Your workspace is a real Linux computer with 100GB of storage. Files, databases,
and projects survive across sessions. It's not a sandbox that resets — it's your
agent's permanent home.

## What's in a workspace

<CardGroup cols={2}>
  <Card title="Files & folders" icon="folder-open">
    Browse, upload, and download files through the built-in Computer tab. Code gets
    syntax highlighting, notebooks render beautifully, and images preview inline.
  </Card>
  <Card title="Multiple projects" icon="layer-group">
    One workspace can hold many projects. Build a dashboard, a landing page, and
    an internal tool — all in the same place.
  </Card>
  <Card title="Connections" icon="plug">
    Each workspace has its own set of integrations — databases, SaaS tools, and APIs
    that the agent can use in any project.
  </Card>
  <Card title="Chat history" icon="clock-rotate-left">
    Every conversation is saved and resumable. Come back to any thread and pick up
    where you left off.
  </Card>
</CardGroup>

## The Computer tab

The Computer tab is your file browser. From here you can:

- Browse your workspace filesystem
- Preview source code with syntax highlighting
- View rendered notebooks, charts, and data tables
- Preview images and markdown files
- Upload and download files

## Multiple chats, one computer

This is the key difference between camelAI and other AI coding tools. camelAI is
**computer-based, not project-based.** Your workspace is the container — chats
are just conversations about what's in it.

- Start a new chat anytime without losing your work
- Work on different projects from different chats
- If a conversation goes sideways, start fresh — your files are still there

<Tip>
  Think of chats as conversations, not containers. You can always start a new chat
  and say "look at the project in /my-app and fix the login page" — the agent will
  find it.
</Tip>

## Workspaces and organizations

<Accordion title="How workspaces relate to organizations">
  - One organization can have multiple workspaces (no limit during beta)
  - Team members share workspace access — multiple people can chat with the same agent
  - Each workspace has its own files, connections, email address, and published apps
  - In multiplayer chats, messages show author signatures so the agent knows who it's
    talking to
</Accordion>

<Accordion title="What happens when the workspace is idle?">
  Your workspace container sleeps after a period of inactivity to save resources.
  When you return, it wakes up automatically — you may notice a brief startup delay.
  Your files are always preserved regardless of container state.
</Accordion>
```

**Mintlify components:** `<CardGroup>`, `<Card>`, `<Tip>`, `<Accordion>`

**Screenshots needed (from Illiana):**
- [ ] Computer tab showing file browser with a project (optional)

---

### 4. `getting-started/publishing.mdx` — NEW

**Purpose:** Explain how live apps work — URLs, visibility, management. This is NOT a "how to deploy" page because apps auto-deploy.

**Key facts for copy:**
- Apps are automatically deployed when the agent builds them — no manual publish step
- URL format depends on org slug style:
  - New-style orgs (6+ alphanumeric): `{app-name}-{orgSlug}.camelai.app`
  - Old-style orgs (contain hyphens): `{app-name}--{orgSlug}.camelai.app`
- Custom domains: coming soon (stub in settings UI). Mention briefly, don't over-document.
- Apps run as Cloudflare Workers — zero cold start, globally distributed
- Full backend by default — not just static frontends
- Integration credentials are auto-injected as env vars into deployed apps
- AI bindings available in every deployed app
- Managing apps: Apps tab in workspace settings shows published apps, supports delete only. To update, just keep chatting.
- Public vs private toggle exists

**Full page copy:**

```mdx
---
title: 'Your Apps'
description: 'How live apps work on camelAI'
---

When the agent builds an app, it's automatically deployed to a live URL. There's
no publish button, no deploy pipeline, no CI/CD to configure. Your app is on the
internet as soon as it's built — and updates go live as you iterate.

## Your app URL

Every app gets a URL at:

```
{app-name}-{your-org}.camelai.app
```

For example: `my-dashboard-k7m2p3.camelai.app`

This is a permanent, shareable link. Copy it and send it to anyone.

## Auto-deploy

You don't need to do anything to deploy. As the agent builds and updates your app,
changes go live automatically. Just keep chatting:

> Add a dark mode toggle to the dashboard

The agent makes the change, and it's live.

## Public vs. private

- **Public** — anyone with the link can access your app
- **Private** — only your workspace members can access it (requires authentication)

You can toggle visibility anytime from the **Apps** section in workspace settings.

## Managing your apps

Go to **Settings → Apps** in your workspace to:

- View all your live apps with their URLs
- Toggle public/private visibility
- Delete apps you no longer need

To update an app, just keep chatting with the agent — ask for changes and they
go live automatically.

## Under the hood

<Accordion title="Technical details">
  - Apps run as [Cloudflare Workers](https://workers.cloudflare.com) — zero cold start,
    globally distributed on Cloudflare's edge network
  - Every app has a **full backend by default** — not just a static frontend. Your apps
    can have API routes, server-side logic, and database access from the first line of code
  - Integration credentials from your workspace connections are automatically injected as
    environment variables — no manual config needed
  - AI bindings are available in every deployed app, so your apps can use text
    models, image generation, and other AI features without managing API keys
</Accordion>

<Accordion title="Custom domains">
  Custom domain support is coming soon. For now, all apps are served from
  `*.camelai.app`.
</Accordion>

<Info>
  Apps stay live even when you're not in camelAI. They're real production services,
  not previews.
</Info>
```

**Mintlify components:** `<Accordion>`, `<Info>`

**Screenshots needed (from Illiana):**
- [ ] Apps settings page with published apps (optional)

---

### 5. `getting-started/connections.mdx` — NEW

**Purpose:** Explain integrations — how to connect external tools and use them in apps.

**Key facts for copy:**
- Both paths work: users can add connections via Settings → Connections, OR the agent can add them (via `prompt_connection_setup` which shows a UI modal, or `create_integration` which does it directly)
- Credentials are encrypted, injected as env vars into workspace and all deployed apps
- OAuth supported for many services
- The "Custom" / "Other" integration (any HTTP API) is available to all users, no restrictions
- Up to 10 custom credential fields for custom integrations
- When a user selects the "Other" integration in UI, it opens a chat thread to guide setup

**Full page copy:**

```mdx
---
title: 'Connections'
description: 'Connect to 50+ databases and tools'
---

Connections let you plug your existing tools into camelAI. Connect a database,
a SaaS platform, or a cloud provider — then build apps that read from and write
to them. No API plumbing required.

## Adding a connection

You can add connections two ways:

<Tabs>
  <Tab title="Through Settings">
    <Steps>
      <Step title="Open workspace settings">
        Go to **Settings → Connections** in your workspace.
      </Step>
      <Step title="Pick a service">
        Choose from the catalog of 50+ integrations.
      </Step>
      <Step title="Authenticate">
        Enter credentials or sign in via OAuth, depending on the service.
      </Step>
    </Steps>
  </Tab>
  <Tab title="Through the agent">
    Just ask the agent in any chat:

    > Connect my Stripe account

    or

    > I want to pull data from our Snowflake warehouse

    The agent will walk you through setup — it may open a credential entry form
    for you, or handle the configuration directly.
  </Tab>
</Tabs>

## How connections work

- **Encrypted storage** — credentials are encrypted at rest and never exposed in logs or chat
- **Auto-injected** — credentials are available as environment variables in your workspace and
  automatically synced to all deployed apps
- **Any chat, any project** — once connected, the agent can use the integration from any
  conversation in your workspace

## Available integrations

<Tabs>
  <Tab title="Databases">
    PostgreSQL, MySQL, Supabase, MongoDB, Redis, ClickHouse, Snowflake, BigQuery,
    Neon, PlanetScale, Turso, Databricks, SingleStore, MotherduckDB
  </Tab>
  <Tab title="SaaS & Productivity">
    Notion, Airtable, HubSpot, Salesforce, Jira, Zendesk, Intercom, Asana,
    Figma, Shopify, Typeform
  </Tab>
  <Tab title="Communication">
    Slack, Discord, Microsoft Teams, Twilio, SendGrid, Mailchimp
  </Tab>
  <Tab title="Payments">
    Stripe, Square
  </Tab>
  <Tab title="Developer Tools">
    GitHub, Linear, Sentry, Vercel, Netlify
  </Tab>
  <Tab title="Cloud & Analytics">
    AWS, Google Cloud, Microsoft Azure, Cloudflare, PostHog, Mixpanel, Segment, Amplitude
  </Tab>
  <Tab title="AI Services">
    OpenAI, Anthropic, OpenRouter
  </Tab>
  <Tab title="Custom API">
    Connect to **any HTTP API** with bearer, basic, or custom authentication.
    Define up to 10 credential fields. The agent will guide you through setup.
  </Tab>
</Tabs>

## Using connections in your apps

Once connected, just describe what you want in plain English:

> Pull my last 30 days of Stripe charges and show them in a sortable table

> Every morning, query our Snowflake warehouse for yesterday's signups and email
> me a summary

> Build a dashboard that shows our PostHog events alongside Stripe revenue

The agent handles the code. Your credentials are already available — no config files,
no `.env` management, no API key juggling.

<Tip>
  You don't need to know how the API works. Just describe what you want and the
  agent figures out the integration details.
</Tip>
```

**Mintlify components:** `<Tabs>`, `<Tab>`, `<Steps>`, `<Step>`, `<Tip>`

**Screenshots needed (from Illiana):**
- [ ] Connections settings page or integration picker (optional)

---

### 6. `features/cron-jobs.mdx` — NEW

**Purpose:** Explain autonomous agent scheduling.

**Key facts for copy:**
- No UI for managing cron jobs — purely through chat. MCP tools: `list_scheduled_prompts`, `create_scheduled_prompt`, `update_scheduled_prompt`, `delete_scheduled_prompt`, `run_scheduled_prompt_now`
- No limit on number of cron jobs (only limit: max 20 jobs fire per alarm tick)
- Each cron job gets a dedicated thread titled "Scheduled: {name}" that appears in normal chat history
- Context accumulates across runs in the same thread — the agent remembers previous executions
- 5-field UTC cron syntax under the hood, but users speak natural language
- Built on Cloudflare Durable Object alarms — reliable, survives workspace hibernation

**Full page copy:**

```mdx
---
title: 'Cron Jobs'
description: 'Schedule your agent to work autonomously'
---

Tell your agent what to do and when — it sets up a recurring job and runs it
without any user interaction. Each run is a full agent turn with access to your
workspace, files, and connections.

## Setting up a cron job

Just describe the schedule in natural language:

> Every weekday at 8am, pull yesterday's revenue from Stripe, generate a summary,
> and email it to the team.

or

> Every 15 minutes, check if there are new sign-ups in our database and post them
> to the #growth Slack channel.

The agent translates this to a cron schedule and sets it up. You never need to write
cron expressions.

## What happens on each run

Each scheduled job gets its own dedicated chat thread (named "Scheduled: {job name}")
that appears alongside your regular chats. When a job fires:

- The agent runs with **full access** to your workspace, files, and connections — the
  same as if you had typed the message yourself
- **Context accumulates** across runs — the agent remembers what it did last time, can
  compare against previous results, and builds up a history of its work
- Results can be emailed, posted to Slack, saved to files, or published to a live dashboard

<Info>
  Cron jobs are reliable — they're backed by Cloudflare Durable Object alarms and
  survive even when your workspace container is idle.
</Info>

## Example use cases

<CardGroup cols={2}>
  <Card title="Daily reports" icon="chart-line">
    Pull data from your warehouse every morning, generate a formatted report, and
    email it to stakeholders
  </Card>
  <Card title="Monitoring & alerts" icon="bell">
    Check metrics hourly, flag anomalies, and page your team when something looks off
  </Card>
  <Card title="Data syncing" icon="arrows-rotate">
    Keep two systems in sync — new Stripe customers automatically become HubSpot
    contacts every 15 minutes
  </Card>
  <Card title="Content generation" icon="pen-nib">
    Generate weekly newsletter drafts, daily social media posts, or morning news
    roundups on a schedule
  </Card>
</CardGroup>

## Managing cron jobs

Everything is managed through chat. Ask the agent:

- **"List my scheduled jobs"** — see all active cron jobs
- **"Update the daily report to run at 9am instead"** — modify a schedule or prompt
- **"Delete the Stripe sync job"** — remove a scheduled job
- **"Run the daily report now"** — trigger a job immediately without waiting for the next scheduled time

<Tip>
  You can view the execution history of any cron job by opening its dedicated thread
  in your chat history. Each run is logged as a message in the thread.
</Tip>
```

**Mintlify components:** `<CardGroup>`, `<Card>`, `<Info>`, `<Tip>`

---

### 7. `features/email-and-slack.mdx` — NEW

**Purpose:** Explain how to interact with the agent outside the web app.

**Key facts for copy:**
- Email format: `{randomHandle}@camelai.dev` where handle is three words like `bright-mountain-river@camelai.dev` (generated from adjective-noun-noun)
- Only workspace members can email the inbox (spam prevention)
- File attachments are extracted and mounted in workspace
- Standard email threading headers (In-Reply-To / References) keep conversations organized
- Slack integration is inbound-only — agent responds to DMs/mentions but cannot proactively send messages
- Slack is set up via OAuth through the connections page

**Full page copy:**

```mdx
---
title: 'Email & Slack'
description: 'Talk to your agent from your inbox or Slack'
---

You don't have to be in camelAI to talk to your agent. Send an email or a Slack
message — it reads, responds, and takes action on your workspace, just like a
normal chat.

<Tabs>
  <Tab title="Email">
    ## Workspace email

    Every workspace gets a unique email address like:

    ```
    bright-mountain-river@camelai.dev
    ```

    Any workspace member can email this address to start or continue a conversation
    with the agent — directly from their inbox, without opening camelAI.

    ### How it works
    <Steps>
      <Step title="Find your workspace email">
        Go to **Settings → General** in your workspace, or just ask the agent:
        "What's this workspace's email address?"
      </Step>
      <Step title="Send an email">
        Email the workspace address from your work email. Write your request in the
        body — the agent processes it as a chat message.
      </Step>
      <Step title="Get a reply">
        The agent reads your email, takes action in your workspace, and replies to
        your email thread. Reply back to continue the conversation.
      </Step>
    </Steps>

    ### Details
    - **Threading** — standard email threading keeps conversations organized in your
      email client. Replies continue the same camelAI chat thread.
    - **Attachments** — file attachments are automatically uploaded to your workspace.
      The agent can read and use them immediately.
    - **Members only** — only workspace members can email the inbox. Emails from
      non-members are ignored (this is also the spam prevention mechanism).
  </Tab>

  <Tab title="Slack">
    ## Slack integration

    Connect Slack to your workspace and message the agent directly from your team's
    Slack.

    ### Setup
    <Steps>
      <Step title="Add the Slack connection">
        Go to **Settings → Connections** and add the Slack integration, or ask the
        agent to set it up.
      </Step>
      <Step title="Authenticate via OAuth">
        Sign in to your Slack workspace and authorize the camelAI bot.
      </Step>
      <Step title="Start chatting">
        DM the camelAI bot or mention it in a channel. The agent responds in-thread.
      </Step>
    </Steps>

    ### Details
    - **Full agent turns** — Slack messages are processed the same as web chat messages.
      The agent can read files, run code, query databases, and take any action it could
      take from the web app.
    - **Thread continuity** — conversations are maintained across messages in the same
      Slack thread.

    <Note>
      The Slack integration is **inbound-only** — the agent responds to your messages
      but doesn't proactively send messages to Slack. For automated Slack posting, use
      a [cron job](/features/cron-jobs) with a Slack connection.
    </Note>
  </Tab>
</Tabs>

<Tip>
  Email and Slack are great for quick asks without context-switching — "what were
  yesterday's numbers?" or "update the landing page copy to mention the sale."
</Tip>
```

**Mintlify components:** `<Tabs>`, `<Tab>`, `<Steps>`, `<Step>`, `<Note>`, `<Tip>`

---

## docs.json Changes

Replace the full navigation section. The complete target `docs.json` navigation:

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "Getting Started",
        "groups": [
          {
            "group": "Start Here",
            "pages": [
              "getting-started/overview",
              "getting-started/quickstart"
            ]
          },
          {
            "group": "Core Concepts",
            "pages": [
              "getting-started/workspace",
              "getting-started/publishing",
              "getting-started/connections"
            ]
          },
          {
            "group": "Features",
            "pages": [
              "features/cron-jobs",
              "features/email-and-slack"
            ]
          }
        ]
      },
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
      },
      {
        "tab": "API (Legacy)",
        "groups": [
          {
            "group": "General",
            "pages": [
              "dev_api/introduction",
              "dev_api/pricing"
            ]
          },
          {
            "group": "Quick Start",
            "pages": [
              "dev_api/camel-api-quickstart"
            ]
          },
          {
            "group": "Row Level Security",
            "pages": [
              "dev_api/row-level-security/introduction",
              "dev_api/row-level-security/postgresql",
              "dev_api/row-level-security/clickhouse",
              "dev_api/row-level-security/bigquery"
            ]
          },
          {
            "group": "Best Practices",
            "pages": [
              "dev_api/knowledge-base-guide",
              "dev_api/reference-query-guide",
              "dev_api/model-selection-guide"
            ]
          },
          {
            "group": "Custom Themes",
            "pages": [
              "dev_api/custom-themes/introduction",
              "dev_api/custom-themes/default-theme",
              "dev_api/custom-themes/appearance",
              "dev_api/custom-themes/response-modes",
              "dev_api/custom-themes/start-chat-message",
              "dev_api/custom-themes/recommendations"
            ]
          }
        ]
      },
      {
        "tab": "API Reference (Legacy)",
        "groups": [
          {
            "group": "API Reference",
            "openapi": "https://api.camelai.com/api/schema/"
          }
        ]
      }
    ],
    "global": {
      "anchors": [
        {
          "anchor": "Agent App",
          "href": "https://app.camelai.com",
          "icon": "browser"
        },
        {
          "anchor": "Website",
          "href": "https://camelai.com",
          "icon": "globe-pointer"
        }
      ]
    }
  }
}
```

Key changes from current:
- Added `getting-started/quickstart` to Start Here group
- Added Core Concepts group with workspace, publishing, connections
- Added Features group with cron-jobs, email-and-slack
- Removed Developer Console anchor

---

## Screenshots

These are optional but would improve the quickstart and core concept pages. Low priority for beta — the copy works without them.

| Page | Screenshot | Priority |
|------|-----------|----------|
| Quickstart | New chat / empty workspace | Nice to have |
| Quickstart | Agent building an app in chat | Nice to have |
| Workspace | Computer tab file browser | Nice to have |
| Publishing | Apps settings page with published apps | Nice to have |
| Connections | Integration picker / catalog | Nice to have |

**Recommendation:** Skip screenshots for now. Add them later when the UI is more stable. The pages are designed to stand alone without images.

---

## Implementation Order

1. Create `features/` directory
2. Write `getting-started/quickstart.mdx`
3. Write `getting-started/workspace.mdx`
4. Write `getting-started/publishing.mdx`
5. Write `getting-started/connections.mdx`
6. Write `features/cron-jobs.mdx`
7. Write `features/email-and-slack.mdx`
8. Update `getting-started/overview.mdx` (add links to new pages + live examples)
9. Update `docs.json` with new navigation structure and remove Developer Console anchor
10. Verify with `mintlify dev`

---

## What This Plan Does NOT Cover (Future Passes)

- Image generation docs
- Agent wallet docs (X402)
- Notebook rendering / data analysis docs
- Pricing/plans page (beta = free, not worth documenting yet)
- API docs for the new product (none exists yet)
- Troubleshooting / FAQ (need user feedback data first)
- Team management / org admin docs (low priority for beta)
- Migration guide from camelAI Legacy
- Custom domains (stub in UI — document when functional)
