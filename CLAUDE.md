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

## Product names

The coding agent product is **camelCode**. Its tabs are **camelCode** and
**Self-host camelCode**, and the matching global anchor and header button in `docs.json`
read "camelCode" and "Open camelCode" (all four said "Coding Agent" until October 2026).
Use "camelCode" wherever the product is named. Keep the lowercase generic term, as in
"a coding agent such as Claude Code or Codex," and don't rename URL paths or files.

## Partner guides

Per-tool integration guides live in the **Partners** group under the **camelCode** tab
(one `getting-started/partners/<tool>.mdx` page per guide). The first guide is Resend;
OpenRouter is planned next.

Every partner page follows the same structure so the next one is quick to add and the
section stays consistent: **Intro + disambiguation → What you can build (agent prompts) →
Connect (Steps, both Settings and agent paths) → Use it (no-code prompt first, code second)
→ How it works → FAQ → Stop using or remove.** When you add a guide, register it in the
Partners group in `docs.json` and link it from the relevant tab in
`getting-started/connections.mdx`. Verify connection details (UI labels, the
`CONNECTIONS.find()` signature, code examples) against the product repo before publishing.

## camelBot documentation

The **camelBot** tab (`camelbot/`, after camelRun) documents camelBot, the Discord
bot builder at bots.camelai.com. The product repository is
`/Users/illiana/Projects/camel-discord-bots`. Take UI labels, quoted exactly, from
`web/src/pages/discord/**`, `web/src/pages/bot/**`, `web/src/lib/*.ts` and
`web/src/components/discord/token-field.tsx`, and limits from `docs/builder.md` and
`docs/bot-authoring.md`. The sales site's fact sheet, with sources, is
`app/components/bot/content.ts` in camelai-salessite.

- Names: the app calls itself "Camel"; the shared Discord app is "Camel's app" (its bot
  user is "camel"); the assistant is "camel-builder". camelRun's Camel Discord bot
  (`camelrun/channels.mdx`) is a different thing.
- camelBot is free while in beta, and AI draws on daily allowances (one per bot, one per
  person for camel-builder and AI in tests). Never state dollar amounts.
- A bot can only send, edit its own messages, and react. Never claim moderation actions,
  role changes, member-join events, private ticket channels, or web dashboards.
- People use camelBot through the web app and Discord, not an API. Don't document
  internals (runtime, sandbox, storage engine, infrastructure, internal APIs).

## Hidden: Changelog

The Changelog tab is hidden from the navigation (October 2026) because it hasn't
been kept up to date. Its pages (`changelog/platform`, `changelog/legacy`) stay in
the repo. To bring it back, add a "Changelog" tab to `docs.json` with an
"Updates" group listing those two pages.

## Redirects

open-mdx-docs ignores a `redirects` list in `docs.json`, and the root `worker.ts` is an
unused stub, so redirects are added to the renderer's own Worker entry
(`node_modules/open-mdx-docs/workers/app.ts`) by `scripts/prepare-open-mdx-docs.mjs`. That
script runs on `bun install` and before `dev`, `build` and `deploy`, and the same Worker
entry serves the dev server and production. Today there is one redirect: `/docs/stream` and
every path under it go permanently (301) to `https://camelai.com/stream`, the sales site's
page for the retired Stream product, so old links still land somewhere useful. Don't add
pages under `stream/`; the redirect would hide them. If an open-mdx-docs update changes the
Worker entry, the script stops with an error instead of skipping the redirect.
