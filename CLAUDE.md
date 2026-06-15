# camelAI Sales Site - Agent Documentation

> **Note to agents:** Keep this file up to date. When you add new features, routes, components, or make significant architectural changes, update the relevant sections of this document.

## Overview

This is the **docs page** for camelAI — not the product itself.

**What is camelAI?** An AI coding assistant built on Cloudflare's edge infrastructure. Users chat with an agent powered by their selected model, with a persistent workspace where files survive across sessions. Users create applications by having the agent write code, then publish them to live `*.camelai.app` URLs. The product repo is at `/Users/illiana/Projects/chiridion-app` (internal codename: chiridion). Please feel free to access and explore the repo at anytime to research, plan, or audit how we do things in that codebase.

For additional context on camelAI, our sales site is available in this machine at `/Users/illiana/Projects/camelai-salessite`.

If you need in depth Company context (for building content, writing copy, etc.), please read - docs/camelAI-company-context.md

You have complete access to the codebase that these docs cover at /Users/illiana/Projects/chiridion-app. Chiridion is the internal name for camelAI. (live site link is camelai.dev)

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
