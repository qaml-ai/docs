# Style Proposal — Organizations and Workspaces

> **For the next agent (me, on implementation pass):** This plan turns [copy-plan.md](copy-plan.md) into a Mintlify MDX page. Copy lands mostly verbatim from the source. Component choices below are deliberate — keep formatting light, since this page is conceptual and mostly text. Don't add components that aren't in this plan.

---

## Goal

Make the org/workspace distinction crystal clear in two minutes of reading. The page is a reference users hit right after signup. Optimize for skim-ability over polish.

## Guiding rules for this page

1. **Default to prose + bullets.** Use Mintlify components only where they add clarity. Resist the urge to convert every list into cards.
2. **Two callouts max in the body, plus the FAQ accordion at the bottom.** Anything more makes a text-heavy page feel busy.
3. **No em dashes.** Per the camelAI-voice skill. Use commas, periods, or parentheses.
4. **Inline links, not "click here."** Match existing tone in `getting-started/workspace.mdx`.
5. **Do not invent copy.** If something feels missing, flag it back to me — don't fill the gap.

---

## Files to change

| File | Change | Notes |
|---|---|---|
| `getting-started/organizations.mdx` | **Create** | New page, full copy from source |
| `getting-started/workspace.mdx` | Edit | Collapse "Workspaces and organizations" accordion to a one-line cross-link |
| `plans/overview.mdx` | Edit | Inline link to new page; rename "Workspace roles" row to "Per-workspace access"; clarify "Custom domains" row |
| `plans/model-providers.mdx` | Edit | Add one FAQ entry linking to new page |
| `docs.json` | Edit | Add `getting-started/organizations` to Core Concepts, listed first |

---

## ASCII layout of the new page

```
┌──────────────────────────────────────────────────────────────┐
│ Organizations and workspaces                                 │  ← title + description
│ How camelAI separates billing and access from the actual     │     (frontmatter)
│ computer your work lives on.                                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Lead paragraph: two layers of structure...                   │  ← plain prose
│                                                              │
│  • Organization — billing and access boundary                │  ← 2-item bulleted list
│  • Workspace — the actual computer                           │
│                                                              │
│ "If you're a solo user..." paragraph                         │  ← plain prose
│                                                              │
│ ── What lives where ─────────────────────────────────────    │  ← H2
│                                                              │
│   At the org level                                           │  ← H4 (bold subhead)
│   • Plan and payment method                                  │     bullets, plain prose
│   • LLM provider and API key                                 │
│   • Members, invitations, and roles                          │
│   • Admin controls for custom domains                        │
│                                                              │
│   At the workspace level                                     │  ← H4 (bold subhead)
│   • The agent's persistent computer                          │     bullets, plain prose
│   • Chats and chat history                                   │
│   • Connections                                              │
│   • Published apps and *.camelai.app URLs                    │
│   • Workspace email + Slack                                  │
│   • Cron jobs                                                │
│                                                              │
│ "Anything you create with the agent..." closing line         │  ← plain prose
│                                                              │
│ ── Organizations ────────────────────────────────────────    │  ← H2
│                                                              │
│ Intro paragraph + 4 separation bullets                       │
│ "You can create a new org..." paragraph w/ inline link       │
│                                                              │
│ When to create a second org:                                 │
│ • Hard wall between contexts                                 │
│ • Contractor + client billing                                │
│ • Separate billing for two parts of a company                │
│                                                              │
│ ╭──────────────────────────────────────────────────────╮     │  ← <Tip>
│ │ 💡  If you don't need a hard wall, stay on one org   │     │     (one of two body
│ │     and use multiple workspaces instead. Almost      │     │     callouts)
│ │     always the right move.                           │     │
│ ╰──────────────────────────────────────────────────────╯     │
│                                                              │
│ ── Workspaces ───────────────────────────────────────────    │  ← H2
│                                                              │
│ Intro paragraph w/ inline link to workspace page             │
│                                                              │
│ ┌───────────┬──────────────────────┐                         │  ← markdown table
│ │ Plan      │ Workspaces included  │                         │
│ ├───────────┼──────────────────────┤                         │
│ │ Free      │ 1                    │                         │
│ │ Starter   │ 1                    │                         │
│ │ Pro       │ 1                    │                         │
│ │ Team      │ 2                    │                         │
│ │ Enterprise│ Unlimited            │                         │
│ └───────────┴──────────────────────┘                         │
│                                                              │
│ "Need more? Email support@camelai.com..." plain paragraph    │  ← per Illiana: NOT a Note
│                                                              │
│ ── Why have more than one workspace ─────────────────────    │  ← H2
│                                                              │
│ "Two reasons." lead-in                                       │
│                                                              │
│ 1. Project isolation                                         │  ← H3
│    Body paragraph                                            │
│                                                              │
│ 2. Per-workspace access for teams                            │  ← H3
│    Body paragraph + 3-bullet marketing/finance example       │
│    Closing paragraph about credentials being scoped          │
│                                                              │
│ ── Roles and team members ───────────────────────────────    │  ← H2
│                                                              │
│ "Multiple seats are only available..." lead paragraph        │
│                                                              │
│ Org roles:                                                   │
│ • Owner — full control                                       │  ← bullet list
│ • Admin — invites, workspaces, connections, billing          │
│ • Member — chat + granted workspaces                         │
│                                                              │
│ Closing paragraph on workspace access being binary           │
│                                                              │
│ ── Custom domains ───────────────────────────────────────    │  ← H2
│                                                              │
│ "Custom domains are per app." opening                        │
│ Body paragraph on org admin view                             │
│ Plan limits paragraph w/ inline link to /plans/overview      │
│                                                              │
│ ── FAQ ──────────────────────────────────────────────────    │  ← H2
│                                                              │
│ ┌──────────────────────────────────────────────────────┐     │  ← <AccordionGroup>
│ │ ▸ Does my LLM provider key work across all my orgs?  │     │     10 accordions,
│ ├──────────────────────────────────────────────────────┤     │     copy verbatim
│ │ ▸ If I switch workspaces, does my chat history come? │     │     from source
│ ├──────────────────────────────────────────────────────┤     │
│ │ ▸ Can two workspaces share files or connections?     │     │
│ ├──────────────────────────────────────────────────────┤     │
│ │ ▸ Can a connection be at the org level instead?      │     │
│ ├──────────────────────────────────────────────────────┤     │
│ │ ▸ Are custom domains attached to my org or apps?     │     │
│ ├──────────────────────────────────────────────────────┤     │
│ │ ▸ Can I move an app from one workspace to another?   │     │
│ ├──────────────────────────────────────────────────────┤     │
│ │ ▸ Do I need a separate org for personal vs. work?    │     │
│ ├──────────────────────────────────────────────────────┤     │
│ │ ▸ Who can create a new workspace?                    │     │
│ ├──────────────────────────────────────────────────────┤     │
│ │ ▸ What does an admin get that a member doesn't?      │     │
│ ├──────────────────────────────────────────────────────┤     │
│ │ ▸ I created a second org and don't see old           │     │
│ │   workspaces — is that a bug?                        │     │
│ └──────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

---

## Section-by-section component map

For each section I list **the section title**, **what's in it**, and **the components used**.

### Frontmatter

```yaml
---
title: 'Organizations and workspaces'
description: 'How camelAI separates billing and access from the actual computer your work lives on.'
---
```

No `icon` field. None of the existing Core Concepts pages set one in frontmatter.

### Hero / opening

- Lead paragraph (verbatim).
- 2-item bulleted list (`- **Organization** ...` / `- **Workspace** ...`).
- "If you're a solo user..." paragraph.

**Components:** none. Plain Markdown.

### What lives where

Two H4 headings with bullet lists below each. **Not a CardGroup.** I considered cards (would parallel `getting-started/workspace.mdx`) but the user asked for simple, and dense bullets read better in a list than crammed into cards.

```mdx
**At the org level**

- Plan and payment method
- LLM provider and API key (or camelAI hosted credits)
- Members, invitations, and roles
- Admin controls for any custom domains attached to apps in the org

**At the workspace level**

- ...
```

Closing line ("Anything you create with the agent...") as plain prose.

**Components:** none.

### Organizations

Prose + bullets per source. End the section with a `<Tip>` containing the "If you don't need a hard wall..." sentence. This is **callout #1 of 2** in the body.

```mdx
<Tip>
  If you don't need a hard wall, stay on one org and use multiple workspaces instead. That's almost always the right move.
</Tip>
```

The "[camelai.dev/settings/organizations](https://camelai.dev/settings/organizations)" inline link stays inline.

### Workspaces

- Lead paragraph with inline link `[More on the workspace itself.](/getting-started/workspace)` (parens preserved as in source).
- Markdown table for plan workspace counts.
- Plain prose paragraph for "Need more?" — explicitly **not** a `<Note>` per Illiana's confirmed decision.

**Components:** none beyond a Markdown table.

### Why have more than one workspace

- "Two reasons." lead.
- Two H3 subheadings: `### 1. Project isolation` and `### 2. Per-workspace access for teams`.
- Body bullets for the marketing / finance example as a normal `-` list.

**Components:** none. (I considered making the marketing/finance split a `<Columns>` or two-card group. Skipped: it's prose, not a feature comparison, and the simple bullet list reads cleaner.)

### Roles and team members

- Lead paragraph.
- Bullet list for the three roles, with the role name bolded.
- Closing paragraph on per-workspace access being binary.

**Components:** none.

### Custom domains

Three short paragraphs per source. The link to `/plans/overview` is inline.

**Components:** none. Considered an `<Info>` callout for "Custom domains are per app." Skipped — the H2 already foregrounds it; a callout would be redundant.

### FAQ

`<AccordionGroup>` with one `<Accordion title="...">` per question. Ten total. Copy lands verbatim from source. This is **callout #2 of 2** counted as one component group.

```mdx
<AccordionGroup>
  <Accordion title="Does my LLM provider key work across all my orgs?">
    No. LLM provider keys are set per org. ...
  </Accordion>
  ...
</AccordionGroup>
```

---

## Cross-page edits

### `getting-started/workspace.mdx`

Replace [workspace.mdx:57-65](../../getting-started/workspace.mdx#L57-L65) — the entire `## Workspaces and organizations` section plus its accordion — with:

```mdx
## Workspaces and organizations

See [Organizations and workspaces](/getting-started/organizations) for how workspaces fit into the org structure.
```

Keep the "What happens when the workspace is idle?" accordion as-is. (That accordion currently sits inside the "Workspaces and organizations" section in the source; lift it back out under its own H2 if needed so it isn't orphaned. Confirm structure when implementing.)

### `plans/overview.mdx`

Three edits:

1. In the lead paragraph for the plans table (or the sentence that introduces workspace counts), add an inline link to `[Organizations and workspaces](/getting-started/organizations)`.
2. Rename the **"Workspace roles"** row to **"Per-workspace access"**. The values stay the same (✓ on Team only).
3. Clarify the **"Custom domains"** row. Two acceptable options — pick the cleaner one at implementation time:
   - Rename the row label to **"Apps with a custom domain"** (preferred — most explicit).
   - Or keep "Custom domains" and add a one-line caption directly under the table: *Custom domain numbers refer to the count of apps in your org that can have a custom domain attached.*

### `plans/model-providers.mdx`

Add one entry to the existing `<AccordionGroup>` FAQ ([model-providers.mdx:169-188](../../plans/model-providers.mdx#L169-L188)). Suggested placement: right after the "Can I use my own API key for one model and camelAI credits for another?" accordion.

```mdx
<Accordion title="Does my API key work across multiple orgs?">
  No. LLM provider keys are scoped to one org. If you have more than one org, set up a key for each. See [Organizations and workspaces](/getting-started/organizations) for the full breakdown.
</Accordion>
```

### `docs.json`

Add `getting-started/organizations` to the Core Concepts group, **listed first**:

```json
{
  "group": "Core Concepts",
  "pages": [
    "getting-started/organizations",
    "getting-started/workspace",
    "getting-started/publishing",
    "getting-started/connections"
  ]
}
```

---

## Things I deliberately did NOT do

So you can second-guess these in review:

- **No CardGroup for "What lives where."** Cards add visual weight; a flat bulleted list reads faster on a text-heavy page. Happy to flip if you'd rather mirror the workspace page's card style.
- **No Steps component anywhere.** This page describes concepts, not workflows. No procedure to walk through.
- **No Tabs.** Nothing toggles between two parallel options here.
- **Only one `<Tip>` callout in the body.** Resisted adding `<Info>` to "Custom domains are per app" and `<Note>` to the support@ paragraph (latter explicitly per Illiana's decision in the copy plan).
- **No icons in CardGroup, because there's no CardGroup.** If you change your mind on cards: `building` for org, `desktop` or `server` for workspace.
- **No screenshots.** Confirmed in the copy plan — page is text-heavy by design, no clean visual.

---

## Open questions before implementation

1. **Custom domains row in the plans table:** rename to "Apps with a custom domain" (my pick) or keep label + add caption? Either is fine; flag if you want me to default differently.
2. **Workspace page restructure:** the current `## Workspaces and organizations` H2 wraps both the org accordion and the idle-workspace accordion. After collapsing the org one to a one-liner, do you want the H2 to stay (with just the cross-link line under it and the idle accordion below), or should I lift "What happens when the workspace is idle?" up to its own H2 and remove the wrapping section entirely? Leaning toward the latter for cleanliness.
3. **Anything in the copy you'd want softened?** I'll port verbatim unless you flag specifics.
