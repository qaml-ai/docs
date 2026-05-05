# Organizations and Workspaces — Copy Plan

> **For the next agent:** This is a copy plan for a new docs page covering the difference between organizations and workspaces. The next pass will format this into Mintlify MDX with proper components. The copy below should land mostly verbatim; structure and headings may shift to match the existing docs style.

---

## TL;DR for the next agent

1. **One new page:** `getting-started/organizations.mdx`. Place it in the **Core Concepts** group in `docs.json`, immediately above the existing `workspace.mdx` page. The org is the higher-level container, so it should come first.
2. **Update `getting-started/workspace.mdx`:** trim the existing "Workspaces and organizations" accordion down to a one-line cross-link, since the new page will own that material.
3. **Light cross-links** from `plans/overview.mdx` and `plans/model-providers.mdx` to the new page where workspace counts and provider scope come up.
4. **Voice rule from the camelAI-voice skill:** no em dashes. The current docs use them anyway — I've avoided them in the draft below; the next agent should hold that line on the new page even if other pages drift.

---

## Recommended placement and why

This is a **net new page**, not a section bolted onto an existing page.

Reasoning:
- It cross-cuts. The org/workspace split touches billing, model providers, roles, connections, and custom domains. Folding it into any one page would either bloat that page or hide the topic somewhere users won't look.
- The current `workspace.mdx` page hints at orgs in a single accordion at the bottom, but stops short of explaining the relationship. We'll move that material here and link.
- Users hit this question right after signup, when they see "create a new org" in the workspace switcher. It belongs in Core Concepts alongside Workspace, Publishing, and Connections.

`docs.json` change: add `getting-started/organizations` to the Core Concepts group, listed first (above `workspace`).

```json
"group": "Core Concepts",
"pages": [
  "getting-started/organizations",
  "getting-started/workspace",
  "getting-started/publishing",
  "getting-started/connections"
]
```

---

## Codebase research — what I confirmed

I did this research before drafting copy, against the chiridion-app repo. Anything below that contradicts your original notes is grounded in the code.

| Question | Answer | Source |
|---|---|---|
| LLM provider scope | **Org-level.** Stored in the org Durable Object and gated by `requireOrgAdmin()`. | `src/routes/api/orgs.$id.llm-provider.ts:32-51`, `src/lib/llm-provider-config.ts:236-243` |
| Custom domain scope | **Per published app.** Each `WorkerScript` has its own `custom_domain_hostname`. The org-scoped admin endpoint just lists every script in the org so an admin can manage them in one place. There is no separate org-level domain. | `src/types.ts:479-484`, `src/routes/api/orgs.$id.custom-domain.ts:43-66` |
| Workspaces per plan | Free 1, Starter 1, Pro 1, Team 2, Enterprise unlimited. | `src/lib/billing-plans.ts:3-9` and `includedWorkspaceCount` field |
| Org roles | `owner`, `admin`, `member`, `viewer` (4 roles, not 3). | `OrgRole` in `src/types.ts:190` |
| Workspace access | **Binary, not role-based.** Each member is granted `full` or `none` access to a given workspace. There is no member-vs-admin role *within* a workspace. | `WorkspaceAccessLevel` in `src/types.ts:191` |
| Where files / chats / apps / connections live | All workspace-scoped. | Multiple, see report |
| Org-level state | Billing, plan, payment method, member list, **LLM provider config**, app domain administration. | Various |

Two things to flag from this:

1. **Your notes had a self-contradiction on LLM provider scope.** Early in your message you said org-level; in the FAQ section you said workspace-level. The code confirms **org-level**, so I've written the FAQ that way. If you create two orgs, you set up an LLM provider for each one separately. That's the answer.
2. **Custom domains are per-app, full stop.** Not per-org and not per-workspace. The admin UI surfaces them at the org level only because admins are the ones who manage them across all apps, not because the domain itself attaches to the org. I've written this carefully in the FAQ.

---

## Decisions confirmed with Illiana

These were open questions in the first draft. Captured here so the next agent doesn't reopen them.

1. **`viewer` role: leave out.** It exists in code but doesn't actually work yet. Page covers owner / admin / member only.
2. **"Workspace roles" plans-table row: clarify in this pass.** Every org technically has workspace roles, but Free / Starter / Pro plans don't allow more than one person on the org, so per-workspace access controls only become useful on Team and Enterprise. Rename the row on `plans/overview.mdx` to **"Per-workspace access"** with a `✓` only on Team / Enterprise. Same meaning, less misleading.
3. **RBAC framing: stay with "per-workspace access."** No prominent RBAC mention; the parenthetical-only treatment in the draft is fine.
4. **A la carte workspaces: mention as plain prose, not a `<Note>`.** A `<Note>` block would over-emphasize it. The "Self-serve a la carte workspaces are coming soon." sentence stays as regular paragraph text under the workspaces table.
5. **Custom domain plans-table wording: adjust in this pass.** The "10 / Unlimited" numbers are the count of apps in the org that can have a custom domain attached. Update the row label to make that explicit, e.g., **"Apps with a custom domain"** or keep "Custom domains" but add a one-line caption clarifying the unit. Next agent picks the cleaner of the two.

---

## The copy

> Title: **Organizations and workspaces**
> Slug: `getting-started/organizations`
> Description: How camelAI separates billing and access from the actual computer your work lives on.

---

### Hero / opening

camelAI has two layers of structure: **organizations** and **workspaces**. They serve different purposes, and getting them straight up front saves headaches later.

- An **organization** is your billing and access boundary. Your plan, your payment method, your team members, and your LLM provider all attach to the org.
- A **workspace** is the actual computer your agent works on. Files, chats, apps, and connections all live inside a workspace. You can have more than one workspace inside an org.

If you're a solo user on a single plan, you may never think about this distinction. You sign up, and we provision one org with one workspace, and that's everything. The split matters once you want to keep two projects fully separate, or once you want a teammate to see one workspace but not another.

---

### What lives where

**At the org level**

- Plan and payment method
- LLM provider and API key (or camelAI hosted credits)
- Members, invitations, and roles
- Admin controls for any custom domains attached to apps in the org

**At the workspace level**

- The agent's persistent computer (files, folders, storage)
- Chats and chat history
- Connections (databases, SaaS tools, APIs)
- Published apps and their `*.camelai.app` URLs
- The workspace's email address and Slack integration
- Cron jobs

Anything you create *with* the agent lives in a workspace. Anything that decides *who can do what and who pays for it* lives at the org.

---

### Organizations

An org is a fully separate entity. Two orgs owned by the same person have nothing to do with each other:

- Separate plans and billing.
- Separate LLM providers. A key you add to Org A does not work for Org B.
- Separate members. Adding someone to Org A does not give them any visibility into Org B.
- Separate workspaces, files, apps, and connections.

You can create a new org any time from [camelai.dev/settings/organizations](https://camelai.dev/settings/organizations). New orgs start on the Free plan and need their own payment setup before you can move to a paid plan.

When to create a second org:

- You want a hard wall between two contexts. Personal projects on one org, client work on another.
- You're a contractor and a client wants to pay for camelAI directly. They create their own org and invite you.
- You want completely separate billing for two parts of a company.

If you don't need a hard wall, stay on one org and use multiple workspaces instead. That's almost always the right move.

---

### Workspaces

A workspace is a real Linux computer your agent lives on. It is persistent: files survive across sessions, chats stay in their threads, deployed apps keep running. ([More on the workspace itself.](/getting-started/workspace))

Every plan includes at least one workspace:

| Plan | Workspaces included |
|---|---|
| Free | 1 |
| Starter | 1 |
| Pro | 1 |
| Team | 2 |
| Enterprise | Unlimited |

Need more than your plan includes? Email **[support@camelai.com](mailto:support@camelai.com)** and we'll add more to your org. Self-serve a la carte workspaces are coming soon.

---

### Why have more than one workspace

Two reasons.

**1. Project isolation.**
Each workspace is its own computer. Files, connections, and chats from one workspace are not visible from another. Use this when you don't want two projects sharing a filesystem or environment.

**2. Per-workspace access for teams.**
On the Team plan and above, you can grant individual members access to specific workspaces. The most common use of this is splitting a team by function:

- A **Marketing** workspace, with the Stripe, HubSpot, and Mailchimp connections marketing needs.
- A **Finance** workspace, with the QuickBooks, BigQuery, and bank connections finance needs.
- People on the marketing team get access to the marketing workspace. People on the finance team get access to the finance workspace. Admins keep access to both.

Same org, same bill, same team, but the underlying data and connections stay separated by function. If a marketer asks the agent to pull revenue numbers, the agent only has the connections in their workspace to work with. They literally cannot reach finance data, because the credentials aren't in the workspace they're chatting in.

---

### Roles and team members

Multiple seats are only available on the **Team** and **Enterprise** plans. On Free, Starter, and Pro, you're the only person on your org.

Org roles:

- **Owner.** The person who created the org. Full control, including billing and ownership transfer.
- **Admin.** Can invite and remove members, manage workspaces, manage connections, manage app custom domains, and adjust billing.
- **Member.** Can chat with the agent and use any workspace they've been granted access to. Can't invite or remove team members. (We're tightening up the exact list of admin-vs-member gating soon, so the precise boundary may shift.)

Workspace access on Team plans is granted per workspace, per member. An admin chooses which workspaces each member can see. There's no "viewer vs. editor" distinction inside a workspace: if a member has access, they can do anything the agent can do in that workspace.

---

### Custom domains

**Custom domains are per app.** Each app you publish gets its own `*.camelai.app` URL by default, and you can attach a custom domain to any individual app from its settings. Different apps in the same workspace can have different custom domains, or none at all.

Org admins can see and manage custom domains across every app in the org from a single admin view. The domain itself attaches to the app.

Plan limits on custom domains (Starter: 10, Pro and up: unlimited) refer to the number of apps that can have one attached. ([Full plan details.](/plans/overview))

---

### FAQ

The next agent should render these as `<AccordionGroup>` with `<Accordion title="...">` for each.

**Does my LLM provider key work across all my orgs?**
No. LLM provider keys are set per org. If you have two orgs, you'll set up a provider for each one separately. This is intentional: the LLM provider determines who pays for model usage, and orgs have separate billing.

**If I switch workspaces, does my chat history come with me?**
No. Chats live in the workspace they were created in. Switching to a different workspace gives you that workspace's chat history.

**Can two workspaces share files or connections?**
No. Workspaces are isolated. If you need the same connection in two workspaces, you can clone any connection to a workspace within your org from the [connections page](https://camelai.dev/connections).

**Can a connection be at the org level instead?**
No. Connections are workspace-scoped. This is what makes per-workspace access useful: you can give marketing access to a workspace with marketing connections without giving them finance connections. You can clone any connection to a workspace within your org from the [connections page](https://camelai.dev/connections).

**Are custom domains attached to my org or to my apps?**
To your apps. Each published app can have its own custom domain. Org admins manage them all from one place, but the domain itself belongs to the app. See the section above.

**Can I move an app from one workspace to another?**
Not currently. If you need an app in a different workspace, the cleanest path right now is to ask the agent to zip the file, download the zip, and then upload that to your workspace.

**Do I need a separate org for personal vs. work projects?**
Only if you want them billed separately or kept fully isolated. If shared billing is fine, two workspaces inside one org will give you all the project separation you need.

**Who can create a new workspace?**
Owners and admins. Members can't add workspaces. New workspaces beyond what your plan includes require either an upgrade or a request to support@camelai.com.

**What does an admin get that a member doesn't?**
Admins can invite and remove team members, create new workspaces, manage which members have access to which workspaces, manage connections, and manage billing. Members can chat in workspaces they have access to and use any connection the workspace has.

**I created a second org and I don't see my old workspaces — is that a bug?**
No. Orgs are fully separate. Workspaces in your first org aren't visible from your second org. Use the org switcher to jump between them. Go to [your Org list](https://camelai.dev/settings/organizations) to see which Org's you are a part of.

---

## What changes outside this page

Small follow-up edits the next agent should make in the same pass:

1. **`getting-started/workspace.mdx`** — replace the existing `<Accordion title="How workspaces relate to organizations">` block with a one-line "See [Organizations and workspaces](/getting-started/organizations) for how workspaces fit into the org structure." Keep the "What happens when the workspace is idle?" accordion as-is.
2. **`plans/overview.mdx`** — in the section that introduces the workspace count, add an inline link to the new page. Rename the **"Workspace roles"** row to **"Per-workspace access"** (still ✓ on Team / Enterprise only). Update the **"Custom domains"** row so it's clear the number refers to apps in the org that can have a custom domain attached, either by renaming the row to "Apps with a custom domain" or by keeping the label and adding a one-line caption under the table. Next agent picks the cleaner option.
3. **`plans/model-providers.mdx`** — in the FAQ, add an entry: "Does my API key work across multiple orgs?" with a link to the new page.

No new screenshots needed for this pass. The page is text-heavy by design and the concepts don't have a clean visual.
