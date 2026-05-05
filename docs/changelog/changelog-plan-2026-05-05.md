# Changelog Update Plan — May 5, 2026

## Recommendation summary

Add a single `<Update label="May 5, 2026" description="Beta Updates">` entry to [changelog/platform.mdx](../../changelog/platform.mdx). One entry (rather than splitting into multiple dated releases) matches the cadence of a continuously-shipping beta and keeps the page scannable. The current page only has the March 10 launch entry, so this becomes the second entry on the page.

The biggest items to lead with are **Custom Domains** (which was listed as "coming soon" in the launch entry — shipping it closes that loop), **Team plans / seat-based billing**, and **GPT models in chat**. Everything else slots underneath as minor features or fixes.

## Filter logic — what I included and what I cut

**Included:** anything a user can see, click, configure, or hit a paywall for. New models, new integrations, new UI surfaces, billing/plan changes, sandbox tools the agent can now use on their behalf, user-visible bug fixes.

**Cut entirely:**
- Internal admin endpoints / dashboard metrics (#436, #443, #458, #461, #476, #488, #509, #514, #520, #531, #555) — users will never touch these.
- Worker log infra, lazy-loading, KV deploy fixes, sandbox-host staging targets, SDK bumps, React Router patterns docs, `AdminIndexDO` — all infra-only.
- AgentOS desktop prototype and DO transcript persistence removal — internal tracks, already flagged in the audit as not for the public changelog.
- External API migration off Cap'n Web RPC — implementation detail; the user-visible part (public MCP server with OAuth) is what gets surfaced.
- Most low-level bug fixes that users would never have noticed (analytics race conditions, DCV delegation internals, OrgDO schema self-healing, etc.)

**Borderline cases I'm including:**
- Pricing dollar amounts (Starter $10, Pro $30, Team $10/seat) named directly in the credits section.
- The legacy-user transition pop-up — only relevant to old `app.camelai.com` users, not new users. Skipping.

---

## Proposed entry — draft copy

Below is the draft of what I'd add to [changelog/platform.mdx](../../changelog/platform.mdx). Written in camel voice (direct, no em dashes, no hype). Review and tell me what to cut, expand, or rephrase.

---

```mdx
<Update label="May 5, 2026" description="Beta Updates">
### Custom Domains

Published apps can now run on your own domain instead of `*.camelai.app`. Setup is self-serve from the workspace settings page, and the agent can read setup instructions, validate DNS, and refresh records on your behalf through new MCP tools. One DNS setup per organization covers all your apps.

### Team Plans

camelAI now has a Team plan with per-seat billing. Admins can invite teammates in bulk by pasting a list of emails, and the invite dialog shows the billing impact (covered seats vs. paid seats) before you confirm. Seat counts sync to Stripe automatically as members join or leave. Pending invitations get a "Copy invite link" action, and removing a member now requires confirmation.

### GPT Models in Chat

GPT models are now available in the model picker alongside Claude. They run on the same workspace, with the same MCP tools and the same prompt setup. Default model for new chats is Claude Sonnet.

### Public MCP Server

camelAI now exposes a public MCP server so other tools can connect to your workspace. Authentication is OAuth 2.1 with standard discovery, so any MCP-compatible client can connect without custom integration work.

### Bring Your Own Key

You can now use camelAI for free by bringing your own model provider key. The new "Bring Your Own Key" option routes through OpenRouter, so any key it supports works with the agent. If you'd rather not manage a provider, camelAI's hosted models are available on any paid plan.

### Subscription Credits

Paid plans now include monthly credits for camelAI's hosted models: $10 on Starter, $30 on Pro, and $10 per seat on Team. One-time top-ups stack on top of your monthly allowance and don't expire with the billing cycle. The billing page shows your current balance with a progress bar and warns you when you're running low.

### In-Chat Connections

Type `@` in the chat composer to pick from your existing connections inline. No more leaving the input to attach a database or service mid-thought.

### Spreadsheet and Markdown Previews

When the agent produces a CSV or spreadsheet output, it now renders as a previewable table instead of raw text. Markdown outputs render with formatting preserved. Both formats are included in PDF and report exports.

### Settings Refresh

The Billing, Usage, AI Provider, BYOK, and Custom Domains pages all got a visual pass for a denser, more consistent layout. The credit status card now shows a progress bar with inline links to view usage or top up.

### Minor Features

- **BigQuery client libraries** pre-installed in the sandbox Python environment, so the agent can query BigQuery without an install step.
- **PDF tooling** (`poppler-utils`) added to the sandbox container, so the agent can extract text and images from PDFs out of the box.
- **Sandbox outbound IP** (`20.46.233.68`) is now shown in the connection setup UI for Postgres, MySQL, ClickHouse, MongoDB, Redis, and Snowflake. Add it to your VPC or firewall allowlist to let the agent reach private databases.
- **IP allowlisting plan** documented for enterprise deployments that need a dedicated outbound IP.
- **Long pastes** in the chat composer auto-convert to file attachments. You can also send a message with attachments only, no text required.
- **Chat history** gained pagination and per-creator filter tabs for finding old threads in shared workspaces.
- **Keyboard-first AskUserQuestion**: pick options with 1–9 / 0, navigate with ↑/↓, toggle with Space, submit with Enter, dismiss with Escape.
- **Composer state persists** across page reloads, so an in-progress message survives an accidental refresh.
- **Clickable file and app preview links** in the chat transcript when the agent uses `set_file_preview` or `set_app_preview`.

### Bug Fixes

- Screenshot tool no longer hangs on slow-loading apps, and it waits for the app to be ready before capturing.
- Pressing Enter while the agent is streaming is now ignored instead of sending a stop signal.
- Long chat composer now caps to viewport height on mobile.

</Update>
```

---

## Resolved feedback

- One entry, dated May 5, 2026.
- Header + paragraph style retained; previous changelog entries are not edited.
- "Free credits on signup" claim removed (it was beta-only and is no longer true). BYOK is the only free path.
- "Default spend limits halved" cut entirely (beta-only; current model is pay-for-usage).
- Pricing dollar amounts ($10 / $30 / $10-per-seat) named directly in the credits section.
- Bug fix list trimmed to three items users actually hit in production. Trial-checkout, Stripe portal 404, BYOK spinner, OAuth consent listing, modal `\n`, and email-turn auth fixes were all cut as too small or too rare to be worth a line.
