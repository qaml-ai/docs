# camelAI Docs - Agent Documentation

> **Note to agents:** Keep this file up to date. When you add new features, routes, components, or make significant architectural changes, update the relevant sections of this document.

## Overview

This is the **docs page** for camelAI — not the product itself.

**What is camelAI?** An AI coding assistant built on Cloudflare's edge infrastructure. Users chat with a Codex-powered agent that has a persistent workspace where files survive across sessions. Users create applications by having the agent write code, then publish them to live `*.camelai.app` URLs. The product repo is at `/Users/illiana/Projects/camelai` (internal codename: chiridion). Please feel free to access and explore the repo at anytime to research, plan, or audit how we do things in that codebase.

For additional context on camelAI, our sales site is available in this machine at `/Users/illiana/Projects/camelai-salessite`.

If you need in depth Company context (for building content, writing copy, etc.), please read - docs/camelAI-company-context.md

You have complete access to the codebase that these docs cover at /Users/illiana/Projects/camelai. Chiridion is the internal name for camelAI. (live site link is camelai.dev)

We also have 2 legacy offerings covered in these docs that are no longer actively maintained. 
/Users/illiana/Projects/camel-app - our old product offering was a data analytics chat where users could connect a database and “chat with their data” (live site link is app.camelai.com)
/Users/illiana/Projects/camel-api - our API product offering that creates an embedded data chat so users can embed our data chat into their own product (live site link is console.camelai.com)

## Tech Stack

The content uses Mintlify-compatible `docs.json` and MDX, but the current renderer is
`open-mdx-docs`. Mintlify hosting and the Mintlify CLI preview are legacy. Never use
`mint dev` or `mintlify dev` to run this site.

Site-specific shadcn tokens live in `theme.css` next to `docs.json`. The header wordmarks
are `logo/light.svg` and `logo/dark.svg`; the boxed brand mark is `favicon.svg`.

For local setup, preview, verification, and troubleshooting, use the project-local
`running-camelai-docs` skill. The normal Conductor command is:

```bash
bun install --frozen-lockfile
bun run dev -- --port "$CONDUCTOR_PORT"
```

Open `http://localhost:$CONDUCTOR_PORT/docs/`.

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

`stream/fleet.mdx` is the canonical fleet list for every camelAI property. When the fleet
or a model version changes, update the table and the "Last updated" line. Use `auto` as the
model ID everywhere. Document the legacy `deepseek-v4-flash` ID only in the fleet-page
migration FAQ.

## Self-hosting guides

Operator documentation lives in the **Self-hosting** tab under `self-hosting/`.
Keep it aligned with `SELF_HOSTING.md`, `infra/selfhost/README.md`, the Compose
files, and the deployment scripts in the public `qaml-ai/camelAI` repository.
The product repository is the source of truth for exact variables and release
behavior. Never imply that outbound SMTP, multi-node failover, or a release
artifact exists unless the product repository provides it.
