# open-mdx-docs component redesign — implementation plan

> **For the implementing agent:** This plan restyles the docs framework at
> `/Users/illiana/Projects/open-mdx-docs` (Part A — ~95% of the work) and makes small content
> edits in this repo (Part B). open-mdx-docs is ours to own and will be open sourced, so every
> change there must stay **generic and config-driven** — nothing camelAI-specific hardcoded.
> All visual decisions have been made for you and are specified with exact Tailwind classes /
> CSS. Where a spec says "exact," copy it. Where it says "approximately" or gives intent, use
> judgment on mechanics but not on appearance. Do not invent new visual treatments not in this
> plan. File:line references were verified against both repos on 2026-07-21; re-verify before
> editing, they may have drifted.

---

## Goal

Get the docs visually to parity with (and past) the old Mintlify site. The reference images:

- **Today:** `.context/attachments/YN8tGe/image.png` — one giant sidebar with collapsible
  groups, indent rail lines, mixed green/blue accents, heavy filled cards, boxy accordions,
  pill tabs.
- **Target feel:** `.context/attachments/sTVUMy/image.png` — the old Mintlify site. Horizontal
  tab bar, calm flat sidebar with an accent-outlined active pill, one indigo accent everywhere,
  quiet bordered cards, centered search, CTA button in the navbar.

The design doctrine in one line: **the page is the surface; borders define regions; one accent
color does all the pointing.**

Five rules that resolve most decisions below:

1. **One decorative accent.** Everything decorative (icons, active states, links on hover,
   badges, focus rings) uses `--primary`, which comes from `docs.json` `colors`. No other hue
   appears anywhere decorative. Semantic hues survive only inside callouts (Warning = amber,
   etc.) and even there only on icon + tint, never on body text.
2. **No fills where a border will do.** Cards, code blocks, FAQ groups: transparent or
   near-transparent backgrounds, 1px `--border` lines, `rounded-xl`.
3. **Hover changes the container or the color — never adds an underline.** Inline prose links
   are the single exception: they are *always* underlined (foreground color) and hover shifts
   them to the accent.
4. **Navigation is flat.** No collapsible groups, no chevrons, no indent rail lines, anywhere.
   Tabs move to a horizontal bar; groups are plain labels; hierarchy is expressed with
   whitespace and type weight.
5. **Type does the hierarchy.** 14px UI chrome, 13px tertiary chrome (TOC, code), semibold
   labels, muted-by-default items. No uppercase eyebrows in the sidebar anymore.

---

## How the two repos fit together (read before starting)

- The framework renders this content repo via the `open-mdx-docs` package
  (`package.json` dev dep `github:Vercantez/open-mdx-docs`).
- **To develop:** in `/Users/illiana/Projects/open-mdx-docs` run `bun install && bun run dev`
  — it serves its own sample site from its `docs/` dir. To test against the real camelAI
  content, point this repo's dependency at the local checkout
  (`"open-mdx-docs": "file:../../../Projects/open-mdx-docs"` or `bun link`), then follow
  `.agents/skills/running-camelai-docs/SKILL.md` (`bun install`, `bun run dev -- --port
  "${CONDUCTOR_PORT:-3000}"`, open `http://localhost:<port>/docs/`, run the bundled
  `verify-preview.mjs`). Revert the dependency pin before committing this repo.
- Almost everything visual lives in five framework files:
  `app/app.css`, `app/lib/mdx-components.tsx`, `app/components/docs/sidebar.tsx`,
  `app/routes/docs-layout.tsx`, `app/routes/docs-page.tsx` — plus `app/components/ui/tabs.tsx`
  and small new components.

### P0 bug found during audit (fix first)

The changelog pages use `<Update>` 8× (`changelog/platform.mdx`, `changelog/legacy.mdx`) but
the framework's `mdxComponents` map (`app/lib/mdx-components.tsx:369-391`) has **no `Update`
component** — MDX throws for undefined components, so these pages almost certainly crash into
the root ErrorBoundary today. Verify by opening `/docs/changelog/platform` on current main,
then implement the `Update` component per §A12 regardless of what you find.

---

# Part A — open-mdx-docs framework

## A0. The page shell (target layout)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│  ☰  🐫 camelAI          ┌──────────────────────────┐      Support  (Try camelAI →) ◐ │  row 1: h-14
│                         │ 🔍 Search…           ⌘K  │                                │  search centered
│                         └──────────────────────────┘                               │
│  Getting Started   Changelog   API (Legacy)   API Reference (Legacy)              │  row 2: h-11 tab bar
│  ━━━━━━━━━━━━━━━                                                                  │  accent underline
├─────────────┬──────────────────────────────────────────────────┬─────────────────┤  border-b under row 2 only
│ ┌─┐         │                                                  │                 │
│ │⌂│ camelAI │  Start Here                        ← eyebrow     │  On this page   │
│ └─┘         │  What is camelAI?                 ← h1           │  Platform Cap…  │ ← active = accent
│ ┌─┐ Legacy  │  Describe anything. camelAI builds…← description │  What Can You…  │   no rail lines
│ │⏱│ App     │                                                  │  Get Started    │
│ └─┘         │  camelAI is a coding agent with a persistent     │  Live Examples  │
│ ┌─┐ Legacy  │  computer…                                       │                 │
│ │⌨│ API     │                                                  │                 │
│ └─┘ Console │  ┌────────────────────────────────────────────┐  │                 │
│             │  │ 🚀 Try camelAI                          ↗  │  │                 │
│ Start Here  │  │ No credit card required. Start building…   │  │                 │
│ ╭─────────╮ │  └────────────────────────────────────────────┘  │                 │
│ │What is  │←│─ active: accent ring + tint pill                 │                 │
│ │camelAI? │ │                                                  │                 │
│ ╰─────────╯ │  ## Platform Capabilities                        │                 │
│  Build Your │  ┌──────────────────┐  ┌──────────────────┐      │                 │
│  First App  │  │ ⌁                │  │ ⊕                │      │                 │
│             │  │ Build Full-Stack │  │ Publish Instantly│      │                 │
│ Core        │  │ Apps             │  │ Deploy any…      │      │                 │
│ Concepts    │  │ Chat with the…   │  │                  │      │                 │
│  Organiza…  │  └──────────────────┘  └──────────────────┘      │                 │
│  Your Work… │       transparent bg · border · accent icon      │                 │
└─────────────┴──────────────────────────────────────────────────┴─────────────────┘
  sidebar: flat, no chevrons,        content: prose max-w-3xl        toc: 13px, flat
  no indent rails, plain labels
```

---

## A1. Design tokens, accent pipeline, fonts

**File: `app/app.css`** (tokens at lines 7-53) and **`app/root.tsx`** (runtime injection at
lines 46-52).

### Keep (already correct)

- The accent pipeline: `docs.json colors.primary/light/dark` → `primaryColors()`
  (`app/lib/docs.ts:134-141`) → inline `<style>` setting `--docs-primary(-light/-dark)` →
  `--primary` / `--ring` (`app.css:17,29,40,52`). This is exactly the "one accent the user can
  assign" mechanism the redesign leans on. Keep the OSS default `#0d9373`.
- The zinc neutral scale, `--radius: 0.5rem`, dark `--border: oklch(1 0 0 / 10%)`.

### Add

1. **Code surface tokens** (shiki's GitHub themes bring a blue-cast `#0d1117` background that
   clashes with the zinc page — replace the background, keep the token colors):

   ```css
   :root  { --code-bg: oklch(0.975 0.003 286); }   /* a hair below the page, light */
   .dark  { --code-bg: oklch(0.185 0.005 286); }   /* a hair above the page, dark */
   ```

2. **Selection + focus, accent-driven** (append near end of file):

   ```css
   ::selection { background-color: color-mix(in oklab, var(--primary) 22%, transparent); }
   :where(a, button, summary):focus-visible {
     outline: 2px solid var(--ring);
     outline-offset: 2px;
     border-radius: var(--radius-sm);
   }
   ```

3. **Configurable fonts.** New `docs.json` field, typed in `app/lib/docs-types.ts` next to
   `colors`:

   ```ts
   fonts?: { family?: string; mono?: string; source?: 'google' | 'none' };
   ```

   - In `root.tsx`, alongside the color `<style>` injection: when `fonts.family` and/or
     `fonts.mono` are set, extend the inline style with
     `--docs-font-sans: '<family>', ui-sans-serif, system-ui, sans-serif` and
     `--docs-font-mono: '<mono>', ui-monospace, SFMono-Regular, Menlo, monospace`, and (unless
     `source: 'none'`) emit `<link rel="preconnect" href="https://fonts.googleapis.com">`,
     `<link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous">`, and
     one `<link rel="stylesheet">` to
     `https://fonts.googleapis.com/css2?family=<Family>:wght@400..700&family=<Mono>&display=swap`
     (URL-encode spaces as `+`).
   - In `app.css`: change the `body` font-family (lines 93-101) to
     `var(--docs-font-sans, ui-sans-serif, system-ui, …existing stack)`, and add
     `pre, code, kbd, samp { font-family: var(--docs-font-mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace); }`.
   - Defaults unchanged when the field is absent (OSS behavior identical to today).

### Typography scale (single source of truth for every component below)

| Element | Spec |
|---|---|
| Page h1 | `text-3xl font-semibold tracking-tight` (unchanged) |
| Page description | `mt-2 text-lg text-muted-foreground` (unchanged) |
| **NEW group eyebrow above h1** | `text-sm font-semibold text-primary` (see §A6) |
| Prose body | typography-plugin defaults, 16px (unchanged) |
| Sidebar group label | 14px `font-semibold text-foreground`, sentence case — never uppercase |
| Sidebar item | 14px `text-muted-foreground`; active `font-medium text-primary` |
| Tab bar item | 14px `font-medium` |
| TOC title + items | 13px (`text-[13px]`) |
| Card title | 16px `font-semibold`; card body 14px `text-muted-foreground leading-relaxed` |
| Callouts, accordion rows, steps body | 14px, `leading-relaxed` bodies |
| Code blocks | 13px / 1.6 (unchanged); inline code `0.85em` |
| Pager | caption 13px muted; title 14px `font-medium` |

---

## A2. Link & hover doctrine (fixes the green-underline complaint)

**File: `app/app.css:178-185`.** Today: `.prose-docs a { text-decoration: none }` +
`.prose-docs a:hover { text-decoration: underline }`. Because Cards and the Pager are `<a>`
elements *inside* `.prose-docs`, hovering a card underlines every line of text in it. Delete
both rules and replace with:

```css
/* Inline prose links: always underlined, foreground ("highlight") color, accent on hover.
   The :not(:where(.not-prose …)) exclusion mirrors @tailwindcss/typography so block-level
   interactive components (cards, pager) opt out with `not-prose`. */
.prose-docs :where(a):not(:where([class~='not-prose'], [class~='not-prose'] *)) {
  color: var(--foreground);
  font-weight: 500;
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
  text-decoration-color: color-mix(in oklab, var(--foreground) 35%, transparent);
  transition: color 0.15s ease, text-decoration-color 0.15s ease;
}
.prose-docs :where(a):not(:where([class~='not-prose'], [class~='not-prose'] *)):hover {
  color: var(--primary);
  text-decoration-color: currentColor;
}
```

Also:

- Set `--tw-prose-links: var(--foreground)` in the `.prose-docs` block (`app.css:109`).
- **Keep the `.heading-anchor` rules physically after this block** — they must keep winning
  (`text-decoration: none`).
- Add `not-prose` to every block-level anchor rendered inside the article: the Card link
  wrapper (`mdx-components.tsx` Card, the `href` branch), and the Pager links (§A13). Their
  hover feedback is **container-level only** (border/color per their specs) — never underline.

Doctrine for the implementing agent: any new clickable block = `not-prose`, hover on the box;
any clickable inline text = underlined foreground, hover to accent. No other hover treatments.

---

## A3. Navbar (row 1)

**File: `app/routes/docs-layout.tsx:122-168`.**

Restructure the header row into three zones — left cluster, centered search, right cluster:

```
☰  🐫 camelAI     |        🔍 Search…                ⌘K        |   Support  (Try camelAI →)  ◐
```

- Container: keep `sticky top-0 z-40 bg-background/85 backdrop-blur` on the `<header>`, but
  **move `border-b` off the header onto the tab bar row** (§A4). When there's only one tab
  (no tab bar), keep `border-b` on the header.
- Left zone: mobile menu button + logo, unchanged markup, wrap in `flex items-center gap-3`.
- Center zone: `<div className="hidden flex-1 justify-center px-6 md:flex">` containing the
  search trigger. Restyle the trigger (`app/components/docs/search-dialog.tsx:75-85`):
  `h-9 w-full max-w-md justify-start gap-2 rounded-lg border bg-muted/40 px-3 text-sm
  font-normal text-muted-foreground hover:bg-muted/70 hover:text-foreground`, icon swapped
  from `FileText` to lucide `Search` (`size-4`), keep the `⌘K` kbd chip pushed right. On
  `< md`, render an icon-only ghost button (`Search` icon) in the right cluster instead — give
  `SearchDialog` a `variant: 'bar' | 'icon'` prop.
- Right zone (`ml-auto flex items-center gap-2`):
  1. `navbar.links` ghost buttons — unchanged behavior (keep the mailto/window-open handling,
     `docs-layout.tsx:149-157`).
  2. **Render `navbar.primary` — typed at `docs-types.ts:70` but currently never rendered.**
     When `{type: 'button', label, href}` present:
     `<Button size="sm" className="hidden rounded-full px-4 sm:inline-flex">` with the label +
     `ArrowRight` `size-3.5`. Default shadcn `bg-primary text-primary-foreground` — this is
     the accent CTA pill from the old site. Same mailto/window-open handling as links.
  3. Theme toggle, unchanged.

---

## A4. Horizontal tab bar (row 2) — NEW component

**New file: `app/components/docs/tab-bar.tsx`; wire into `docs-layout.tsx`.** This replaces
the current "all tabs stacked in one sidebar with uppercase eyebrows" rendering
(`docs-layout.tsx:171-180`) — delete the eyebrow rendering entirely.

```
   Getting Started    Changelog    API (Legacy)    API Reference (Legacy)
   ━━━━━━━━━━━━━━━
───────────────────────────────────────────────────────────────────────────  ← border-b
```

- Render inside the sticky `<header>`, below row 1, only when `navTabs().length > 1`.
- Container: `border-b`. Inner: `mx-auto flex h-11 max-w-screen-2xl items-center gap-7
  overflow-x-auto px-4 lg:px-6` (scrollable on mobile; hide scrollbar with
  `scrollbar-width: none` utility class in app.css if needed).
- Each tab is a `<Link>` to its **first page** — compute with the existing flatten logic
  (`flattenNodes`, `app/lib/docs.ts:98-103`) applied to `tab.nodes`.
- Item classes, exact:
  `relative flex h-11 shrink-0 items-center text-sm font-medium transition-colors` +
  inactive `text-muted-foreground hover:text-foreground` / active `text-foreground`.
- Active indicator: `<span className="absolute inset-x-0 bottom-0 h-0.5 rounded-t-full
  bg-primary" />` rendered only on the active tab. Set `aria-current="page"`.
- **Active-tab resolution** (new helper in `app/lib/docs.ts`, also used by the sidebar):
  `activeTab(slug)` = the tab whose flattened slugs include the current slug, else `tabs[0]`.
- The main grid (`docs-layout.tsx:169-181`) then renders `<SidebarNav>` with **only the active
  tab's nodes** — one sidebar, one tab's content.
- **Sticky-offset ripple:** the header grows from 56px to 100px (h-14 + h-11). Update every
  hardcoded offset together: `html { scroll-padding-top }` `5rem → 7.5rem` (`app.css:87`),
  the sidebar `top-16`/`max-h` (§A5), the TOC `sticky top-16` (`toc.tsx:38`) and its
  scroll-spy threshold `112px → ~148px` (`toc.tsx:17`), and the `Update` rail `lg:top-32`
  (§A12). Single-tab sites keep today's offsets — derive them from `multiTab`, don't fork the
  components.
- Mobile drawer (`MobileNav`, `docs-layout.tsx:38-110`): replace the stacked
  eyebrow-per-tab list with (1) a plain vertical list of tab links at the top (14px medium,
  active `text-primary`), then a `border-t my-4`, then the active tab's `<SidebarNav>`.

---

## A5. Sidebar — flat, calm, no rails

**File: `app/components/docs/sidebar.tsx` (full rewrite of the render logic, keep the
props/recursion shape).**

Delete, everywhere: the `<details>`/`<summary>` collapsible mechanism (`sidebar.tsx:40-48`),
the `ChevronRight` import, and the indent rail `'ml-3 border-l pl-3'` (`sidebar.tsx:22`).
Groups are **always expanded, not interactive**.

```
BEFORE (per group)                     AFTER (per group)

 Start Here                    ˅       Start Here                ← label, semibold, not a button
 │  What is camelAI?                    ╭──────────────────────╮
 │  Build Your First App                │ What is camelAI?     │ ← active pill
 ↑ rail line, indented                  ╰──────────────────────╯
                                        Build Your First App    ← same x-position as label
```

- Wrapper `<nav>`: keep `docs-sidebar-scroll sticky top-16 …` but the `top-*` offset must
  account for the new tab bar height — with row 1 (h-14) + row 2 (h-11) the header is 100px:
  use `top-[6.25rem] max-h-[calc(100svh-6.25rem)]` when multiTab, `top-14
  max-h-[calc(100svh-3.5rem)]` otherwise (pass a prop or compute in layout).
- **Anchors block (NEW, top of sidebar).** `docs.json navigation.global.anchors` (camelAI has
  3: camelAI / Legacy App / Legacy API Console) is currently parsed for slugs but never
  rendered. Render it above the groups, desktop sidebar and mobile drawer both:

  ```
  ┌──┐
  │⌂ │  camelAI          ← row: group flex items-center gap-2.5 px-2 py-1.5
  └──┘                      text-sm font-medium text-muted-foreground hover:text-foreground
  ```

  - Icon chip, exact: `flex size-6 shrink-0 items-center justify-center rounded-md border
    text-muted-foreground transition-colors group-hover:border-primary/40
    group-hover:text-primary`, icon via existing `resolveIcon()` (`app/lib/icons.tsx:63`),
    `size-3.5`.
  - External anchors get `target="_blank" rel="noreferrer"`. Read anchors via a new
    `globalAnchors()` helper in `app/lib/docs.ts` (shape:
    `navigation.global.anchors: {anchor, href, icon?}[]`; add to `docs-types.ts`).
  - After the block: `mb-6`, no divider line.
- **Groups container:** `flex flex-col gap-7` (whitespace separates groups — no borders).
- **Group label,** exact: `px-2 pb-1.5 text-sm font-semibold text-foreground`. Sentence case
  as authored in docs.json. Never uppercase, never a chevron.
- **Items list:** `flex flex-col gap-0.5`.
- **Item,** exact: `block rounded-md px-2 py-1.5 text-sm transition-colors` +
  - inactive: `text-muted-foreground hover:text-foreground` — **no hover background** (the
    color shift is the whole hover state; this is the calm).
  - active: `bg-primary/10 font-medium text-primary ring-1 ring-primary/30 ring-inset`
    — the accent-outlined pill from the Mintlify screenshot.
- **Nested groups** (a group inside a group — legal in the schema, unused by camelAI): render
  the child group label as a plain item-height label (`px-2 pt-3 pb-1 text-[13px] font-semibold
  text-foreground`) with its pages beneath at `pl-4` (padding only — **never** `border-l`).

---

## A6. Content header + TOC

**Files: `app/routes/docs-page.tsx:39-49`, `app/components/docs/toc.tsx`.**

1. **Group eyebrow above the h1** (the accent "Start Here" line in the Mintlify screenshot).
   Add a helper `groupOf(slug)` in `app/lib/docs.ts` returning the containing group name from
   the active tab. Render inside the existing `not-prose` header, above the `<h1>`:
   `<p className="mb-2 text-sm font-semibold text-primary">{group}</p>` (omit when none).
2. **TOC** — remove the rail. Today (`toc.tsx:45-50`) each item is `-ml-px block border-l pl-4`
   with `border-primary` when active. Replace:
   - Container: `flex flex-col gap-2.5 text-[13px]` (drop `border-l`, drop `gap-2`).
   - Title: `mb-3 text-[13px] font-semibold` (was `text-sm font-medium`).
   - Item, exact: `block text-muted-foreground transition-colors hover:text-foreground` +
     active `font-medium text-primary` (no borders, no `pl-4`; depth-3 headings get `pl-3`
     padding for hierarchy).
   - Keep the scroll-spy exactly as is.

---

## A7. Card + CardGroup (kill the fill)

**File: `app/lib/mdx-components.tsx:76-131` (Card + `CardIcon`), 147-156 (CardGroup).**
70 Cards across 15 content files — the highest-traffic component.

```
BEFORE                                  AFTER
┌────────────────────────────┐          ┌────────────────────────────┐
│ ▩ elevated bg-card fill    │          │  ⌁                         │ ← bare icon, size-5,
│ [▣] Build Full-Stack Apps  │          │                            │   text-primary, no chip
│  ↑ icon chip + inline title│          │  Build Full-Stack Apps     │ ← text-base font-semibold
│ Chat with the agent to     │          │  Chat with the agent to    │ ← mt-1.5 text-sm muted
│ build complete web apps…   │          │  build complete web apps…  │   leading-relaxed
└────────────────────────────┘          └────────────────────────────┘
                                          bg-transparent · border · rounded-xl · p-5
                                          linked: hover:border-primary/50
                                          external link: ↗ pinned top-right
```

- **Container,** exact: `h-full rounded-xl border bg-transparent p-5 shadow-none` — replace
  the current `UiCard` usage's inherited `bg-card` (this is the "busy background"). Simplest
  implementation: stop composing shadcn `UiCard` for the MDX Card and render a plain `<div>`
  with these classes (leave `ui/card.tsx` untouched for other consumers).
- **Icon:** delete the chip wrapper (`inline-flex size-7 … rounded-md bg-primary/10`,
  `mdx-components.tsx:80`). Render the bare icon `size-5 text-primary` on its own line.
  Keep the `color` prop working (sets the icon's `color` style only — no more tinted chip
  background); camelAI content stops using it (Part B).
- **Layout:** stacked — icon block, then `mt-3` title `text-base font-semibold text-foreground`
  (no icon → no top margin), then body `mt-1.5 text-sm leading-relaxed text-muted-foreground`.
  Remove the inline `ChevronRight` after the title.
- **Linked cards:** wrapper `<a>`/`<Link>` gets `not-prose block h-full no-underline` (§A2)
  and the container additionally `transition-colors hover:border-primary/50`. External `href`
  (http/https): pin `ArrowUpRight` `size-4 text-muted-foreground` at `absolute top-5 right-5`
  (container `relative`), always visible — matches the old "Try camelAI" card.
- **CardGroup:** keep the auto-fit grid; bump `gap-4` → `gap-3`.

The "Try camelAI" CTA on the overview page is just a `cols={1}` linked Card — with this
restyle it needs no special component.

## A8. Accordion + AccordionGroup (the FAQ block)

**File: `app/lib/mdx-components.tsx:216-239`; shadcn base `app/components/ui/accordion.tsx`.**
41 Accordions / 7 groups in content; every FAQ (4 pages) is an `AccordionGroup` of title-only
`Accordion`s.

```
BEFORE (each Q its own box)             AFTER (one block component)
┌───────────────────────────┐           ┌─────────────────────────────────────┐
│ Does my key work…?      ˅ │           │ Does my LLM key work across orgs? ˅ │
└───────────────────────────┘           ├─────────────────────────────────────┤
┌───────────────────────────┐           │ Can workspaces share files?       ˅ │
│ Can workspaces share…?  ˅ │           ├─────────────────────────────────────┤
└───────────────────────────┘           │ Who can create a workspace?       ˄ │
┌───────────────────────────┐           │                                     │
│ Who can create…?        ˅ │           │   Anyone with the Admin or Owner    │
└───────────────────────────┘           │   role. Members can only…           │
                                        ├─────────────────────────────────────┤
                                        │ Do I need a separate org…?        ˅ │
                                        └─────────────────────────────────────┘
                                          one rounded-xl border, rows divide-y
```

- **Mechanism:** add an `AccordionGroupContext` (boolean). `AccordionGroup` provides it and
  renders `my-6 overflow-hidden rounded-xl border divide-y divide-border` (replacing today's
  bare `<div className="my-4">`). Each `Accordion` keeps its own Radix root/state (unchanged
  behavior, multiple can be open) but styles by context:
  - **Inside a group:** no own border/rounding/margin — the wrapper `div` is just the row.
  - **Standalone:** keep a single-box look, updated to `my-4 rounded-xl border` (drop `px-4`
    from the wrapper; padding moves to trigger/content so the hover state can reach the edges).
- **Trigger,** exact (both variants): `flex w-full items-center justify-between gap-4 px-4
  py-3.5 text-left text-sm font-medium transition-colors hover:bg-muted/50 hover:no-underline`
  with the shadcn `ChevronDown` `size-4 shrink-0 text-muted-foreground` rotating 180° when
  open (keep the `[&[data-state=open]>svg]:rotate-180` mechanism from `ui/accordion.tsx:32`).
- **Content,** exact: `px-4 pb-4 pt-0 text-sm leading-relaxed text-muted-foreground` (keep the
  existing first/last `<p>` margin-stripping selectors).
- Row hover = background tint on the row (`hover:bg-muted/50`) — container feedback, no
  underline (§A2 doctrine; the trigger is a button so prose rules don't hit it, but keep
  `hover:no-underline` as belt-and-braces since shadcn's default trigger underlines).
- `Expandable` (`mdx-components.tsx:270-272`) aliases Accordion and inherits all of this.

## A9. Tabs — line tablist

**Files: `app/components/ui/tabs.tsx` (restyle in place — its only consumers are the MDX Tabs
and CodeGroup) and `app/lib/mdx-components.tsx:167-188`.** Fixes the pill tabs on
`getting-started/connections` ("Adding a connection", 2 tabs; "Available integrations",
8 tabs).

```
BEFORE                                   AFTER
╭──────────────────────────╮
│ ▓Through Settings▓ │ Thru │            Through Settings   Through the agent
╰──────────────────────────╯             ━━━━━━━━━━━━━━━━
  filled pill container                  ─────────────────────────────────────── ← full-width
                                                                                    hairline
                                         [tab content]
```

- **TabsList,** exact (replaces `ui/tabs.tsx:22`'s `inline-flex h-9 … rounded-lg bg-muted
  p-[3px]`): `flex h-auto w-full items-center justify-start gap-6 overflow-x-auto rounded-none
  border-b bg-transparent p-0 text-muted-foreground`.
- **TabsTrigger,** exact (replaces the `data-[state=active]:bg-background …shadow` treatment):
  `relative -mb-px rounded-none border-0 bg-transparent px-0 pb-2.5 pt-1 text-sm font-medium
  text-muted-foreground shadow-none transition-colors hover:text-foreground
  data-[state=active]:text-foreground data-[state=active]:shadow-none
  after:absolute after:inset-x-0 after:bottom-0 after:h-0.5 after:rounded-t-full
  after:bg-transparent data-[state=active]:after:bg-primary`.
- **TabsContent:** `mt-4` (in the MDX wrapper, `mdx-components.tsx:181-185`).
- Long tab sets (the 8-tab integrations block) scroll horizontally; triggers get `shrink-0`.
- This intentionally matches the top-level tab bar (§A4) — same visual language, one level
  down.

## A10. Code — blocks, inline, CodeGroup

**Files: `app/app.css:143-176`, `app/lib/mdx-components.tsx:315-345` (`PreWithCopy`),
`:190-214` (CodeGroup), `vite/mdx-docs-plugin.ts:303-310` (shiki config — unchanged).**

### Code block chrome

```
WITH header (title or language present)         WITHOUT (bare fence)
┌──────────────────────────────────────┐        ┌──────────────────────────────┐
│ app/server.ts                    ⧉   │        │ SELECT * FROM orders     ⧉   │
├──────────────────────────────────────┤        │ WHERE created_at > now() -   │
│ import { serve } from 'bun'          │        │   interval '7 days';         │
│                                      │        └──────────────────────────────┘
│ const app = serve({ port: 3000 })    │          copy floats top-right,
└──────────────────────────────────────┘          reveals on hover/focus
  header h-10 · bg-muted/40 · mono 12px label
  copy button always visible in header
```

- **Container** (new wrapper rendered by `PreWithCopy`): `group relative my-5 overflow-hidden
  rounded-xl border`. The `<pre>` inside loses its own border/rounding:
  update `pre.shiki` (app.css:155-162) to `border: 0; border-radius: 0; margin: 0;
  padding: 0.875rem 1rem;` keep `font-size: 0.8125rem; line-height: 1.6; overflow-x: auto`.
- **Background:** replace the shiki theme backgrounds with our surface —
  `pre.shiki { background-color: var(--code-bg); }` and change the span rules
  (app.css:143-153) to color-only: `.shiki span { background-color: transparent; }` (keep the
  `--shiki-light`/`--shiki-dark` color switching exactly as is).
- **Header bar** — render when the fence has a title/filename meta *or* a language:
  `flex h-10 items-center justify-between border-b bg-muted/40 px-4`, label
  `font-mono text-xs text-muted-foreground` (filename verbatim; else the language lowercase).
  The meta/title currently reaches only CodeGroup labels — plumb it through to `pre` props in
  the MDX pipeline (the shiki rehype handler already carries `title`/`meta`; mirror the
  extraction CodeGroup does at `mdx-components.tsx:196-204`).
- **Copy button** (exists today, `mdx-components.tsx:328-341` — keep the clipboard + 1.5s
  swap logic):
  - In-header variant: `inline-flex size-7 items-center justify-center rounded-md
    text-muted-foreground transition-colors hover:bg-muted hover:text-foreground` — **always
    visible**, no opacity game.
  - Headerless variant: same button `absolute top-2 right-2 border bg-background/80
    backdrop-blur opacity-0 transition-opacity group-hover:opacity-100 focus-visible:opacity-100`.
  - Success state: `Check` icon in `text-primary` (not green — accent doctrine).
  - Before client mount render it disabled instead of hidden (discoverability).

### Inline code

Replace `app.css:164-171` — monospace, background, **no outline**:

```css
code:not(pre code) {
  background-color: var(--muted);
  border: none;
  border-radius: var(--radius-sm);
  padding: 0.15em 0.35em;
  font-size: 0.85em;
  font-weight: 500;
}
```

(Mono family arrives via the global `pre, code, kbd, samp` rule from §A1. Keep the
`::before/::after { content: none }` rules.)

### CodeGroup

Multi-file/tab code gets the same chrome, tabs living in the header (do **not** reuse the
§A9 line style here — an underline inside a bordered header reads as clutter):

```
┌────────────────────────────────────────────────┐
│ ▐server.ts▌  agent-workflow.js             ⧉   │ ← active: soft chip bg-muted
├────────────────────────────────────────────────┤    text-foreground; inactive muted
│ …highlighted code of active tab…               │
└────────────────────────────────────────────────┘
```

- Container as §A10 block. Header: `flex h-10 items-center gap-1 border-b bg-muted/40 px-2`.
- Tab trigger, exact: `rounded-md px-2.5 py-1 font-mono text-xs font-medium
  text-muted-foreground transition-colors hover:text-foreground
  data-[state=active]:bg-muted data-[state=active]:text-foreground` (override the §A9 base
  via className — `cn()` merge handles it; verify the `after:` underline is neutralized, else
  pass a variant prop to TabsTrigger).
- Copy button right-aligned in the header (`ml-auto`), copies the **active** tab's code.
- Nested `<pre>`s: strip their own chrome — `[&_pre]:my-0 [&_pre]:rounded-none [&_pre]:border-0`
  on the content wrapper (the nested `PreWithCopy` should also skip its own header/copy when
  inside a CodeGroup — add a `CodeGroupContext` mirroring §A8's pattern).

## A11. Callouts (Note / Tip / Warning / Info / Check)

**File: `app/lib/mdx-components.tsx:24-51`.** 51 uses in content, Warning the most common
(28). Today the entire body text is hue-tinted (`text-blue-700 dark:text-blue-300` etc.) —
loud, and Note(blue)/Info(sky) are nearly identical.

```
BEFORE                                      AFTER
╭──────────────────────────────╮            ╭──────────────────────────────╮
│ ⚠ Everything in amber text,  │            │ ⚠  Body text in normal       │
│   border amber, bg amber     │            │    foreground; only the icon │
╰──────────────────────────────╯            │    and tint carry the hue.   │
                                            ╰──────────────────────────────╯
```

- **Container,** exact: `my-5 flex gap-3 rounded-xl border border-transparent px-4 py-3.5
  text-sm leading-relaxed` + per-kind background tint (below). No colored borders.
- **Icon:** `mt-0.5 size-4 shrink-0` in the kind's hue. **Title** (when present):
  `mb-1 font-medium` in the kind's hue. **Body:** `text-foreground/90` — never hue-tinted.
- Per-kind (icons unchanged from today):

  | Kind | bg | icon/title color |
  |---|---|---|
  | Note | `bg-muted/60` | `text-muted-foreground` (neutral aside) |
  | Tip | `bg-primary/[0.07]` | `text-primary` (accent — the "pro tip") |
  | Info | `bg-sky-500/[0.08]` | `text-sky-600 dark:text-sky-400` |
  | Warning | `bg-amber-500/[0.08]` | `text-amber-600 dark:text-amber-400` |
  | Check | `bg-emerald-500/[0.08]` | `text-emerald-600 dark:text-emerald-400` |

- This is the **only** place non-accent hues are permitted, and only on icon/title/tint.

## A12. `Update` component — NEW (changelog)

**File: `app/lib/mdx-components.tsx`** — implement and register in `mdxComponents`. Fixes the
P0 (§ top). Content shape: `<Update label="March 10, 2026" description="Beta Launch">…markdown…</Update>`.

```
────────────────────────────────────────────────────────────────  ← border-t between entries
 March 10, 2026     │   New: Persistent workspaces
 ╭─────────────╮    │   Files and databases now survive across
 │ Beta Launch │    │   sessions. Pick up where you left off.
 ╰─────────────╯    │
 (sticky on lg)     │   - Cron jobs run while you sleep
                    │   - …
```

- Wrapper: `not-prose`-free (children are markdown and must keep prose styling) —
  `flex flex-col gap-3 border-t py-10 first:border-t-0 first:pt-0 lg:flex-row lg:gap-10`.
- Left rail: `lg:w-44 lg:shrink-0 lg:sticky lg:top-32 lg:self-start` containing
  `label` as `text-sm font-medium text-foreground` and `description` as an accent badge:
  `mt-2 inline-flex w-fit rounded-full border border-primary/25 bg-primary/10 px-2.5 py-0.5
  text-xs font-medium text-primary`.
- Right: `min-w-0 flex-1` wrapping `children`.
- On mobile the rail stacks above the content (the `flex-col` default).

## A13. Steps, Pager, and remaining polish

**Steps** (`mdx-components.tsx:241-255`; 15 groups / 50 steps in content). Replace the
left-border rail + dot with numbered markers and a hairline connector between markers only:

```
 ┌─┐
 │1│  Open workspace settings      ← marker: size-7 rounded-md border bg-muted/50,
 └─┘  Click the gear icon in…         font-mono text-[13px] font-medium text-muted-foreground
  │                                ← connector: w-px flex-1 bg-border (not a full-height rail)
 ┌─┐
 │2│  Pick a service
 └─┘  Choose from 50+ services…
```

- `Steps`: `my-6 flex flex-col` (drop `ml-2 border-l pl-8 gap-8`). Number the children by
  index (`React.Children`).
- `Step`: `flex gap-4` + marker column (`flex flex-col items-center`: the numbered chip, then
  the connector `w-px flex-1 bg-border`, omitted on the last step) + content column
  (`pb-8 min-w-0`, last step `pb-1`). Title `text-base font-semibold mt-0.5 mb-2`; body
  `text-sm leading-relaxed text-muted-foreground` (unchanged).

**Pager** (`app/components/docs/pager.tsx`) — drop the two bordered cards for quiet text
links over a hairline:

```
──────────────────────────────────────────────────────────────
 ← Previous                                            Next →
   What is camelAI?                       Build Your First App
```

- Wrapper: `not-prose mt-14 flex items-start justify-between gap-6 border-t pt-6`.
- Each link: `group flex flex-col gap-1 no-underline` (next: `items-end text-right ml-auto`);
  caption `flex items-center gap-1 text-[13px] text-muted-foreground` with `ArrowLeft`/
  `ArrowRight` `size-3.5`; title `text-sm font-medium text-foreground transition-colors
  group-hover:text-primary`.

**Misc (small, do last):**

- **ParamField/ResponseField** (`mdx-components.tsx:274-313`): align chrome — `rounded-xl`,
  `bg-transparent`, type badges `rounded-md bg-muted px-1.5 py-0.5 font-mono text-xs`;
  otherwise unchanged. (Unused by camelAI content but part of the OSS surface.)
- **Frame** (`:257-268`): `rounded-xl` for consistency; otherwise unchanged.
- **Search dialog list**: show each result's group as a `text-xs text-muted-foreground`
  suffix; no other changes.
- **Footer** (`docs-layout.tsx:186-203`): `text-[13px]`; unchanged otherwise.
- **Error page** (`root.tsx:99-119`): already on-doctrine (accent eyebrow); no change.
- **open-mdx-docs sample content + README/AGENTS.md**: document the new `fonts` config, the
  `Update` component, and anchor rendering; add an `Update` + FAQ example to the sample
  `docs/` site so OSS users see the new blocks.

---

# Part B — this repo (content) changes

Small, and only after Part A lands:

1. **Unify icon color — remove all 8 per-card `color=` props** (the entire source of the
   mixed green/blue icons):
   - `getting-started/overview.mdx` — 1 (`color="#3b82f6"` on the "Try camelAI" card).
   - `dev_api/introduction.mdx` — 7 (`#3b82f6` ×4, `#10b981`, `#f59e0b`, `#8b5cf6`, `#ef4444`).
   Every icon then inherits the accent. `docs.json` `colors` are already the old Mintlify
   indigo — `primary`/`dark` `#3F60C1`, `light` `#5F83F0` (used in dark mode) — keep them.
2. **Adopt the brand fonts** once §A1 ships — add to `docs.json`:
   `"fonts": { "family": "Figtree", "mono": "Geist Mono" }` (both on Google Fonts; matches
   the product and sales site).
3. **No MDX restructuring needed.** The FAQ pages (4), `connections.mdx` tabs, changelog
   `<Update>` pages, and all 70 cards pick up the redesign automatically.
4. **Hygiene (optional, confirm with Illiana first):** delete the 18 stray `*.mdx.tmp` files
   under `dev_api/` — unreferenced by docs.json, but they shadow real pages during bulk edits.

---

# Implementation order

Each step leaves the site shippable; screenshot after each against the reference image.

1. **A12 `Update`** — unbreaks the changelog (P0), independent of all styling.
2. **A1 tokens + fonts** — foundation every later step reads from.
3. **A2 link doctrine** — global CSS; verify cards/pager before their restyles (expect
   temporary always-underlined card text until step 6 adds `not-prose`).
4. **A3 + A4 + A5 + A6 navbar, tab bar, sidebar, eyebrow/TOC** — the shell, one PR; this is
   the "calmer nav" bucket and the biggest visible shift.
5. **A9 line tabs** — small, high-visibility (`/docs/getting-started/connections`).
6. **A7 cards + A8 accordions** — the two block components.
7. **A10 code** — block chrome, inline code, CodeGroup.
8. **A11 callouts + A13 steps/pager/misc.**
9. **Part B content edits**, then final side-by-side pass.

## Verification checklist (run after steps 4, 8, and 9)

Light **and** dark mode, at `lg` and mobile widths:

- `/docs/getting-started/overview` — tab bar active state, sidebar pill, eyebrow, CTA card
  arrow, 6-card grid (all icons one color), pager.
- `/docs/getting-started/connections` — line tabs (2-tab and 8-tab sets), steps inside tabs.
- `/docs/plans/model-providers` — 11-accordion FAQ block, steps, callouts.
- `/docs/changelog/platform` and `/docs/changelog/legacy` — `Update` layout, sticky rail.
- `/docs/dev_api/camel-api-quickstart` — code blocks w/ header + copy, inline code, CodeGroup
  (`partners/resend` has the true multi-tab one).
- Keyboard pass: tab through navbar → tab bar → sidebar → TOC; focus rings visible and
  accent-colored; search opens on `⌘K` and `/`.
- `bun run typecheck` in open-mdx-docs; the `verify-preview.mjs` script against the local run.
- Framework sample site (`open-mdx-docs dev`) still renders with **no** docs.json `colors` /
  `fonts` set (OSS defaults intact).

---

# Things I deliberately did NOT do

- **No line numbers in code blocks** — noise for this content (mostly short SQL/bash); the
  header + copy button carry the polish.
- **No forced-dark code blocks in light mode** — kept dual GitHub themes on our own surface
  token; revisit only if light mode looks flat.
- **No breadcrumbs** beyond the group eyebrow — path depth is 2, a trail would repeat the
  sidebar.
- **No sidebar group icons** (schema supports them; camelAI doesn't use them) — icon chips
  stay exclusive to anchors so the sidebar reads as text.
- **No OpenAPI reference rendering** — the "API Reference (Legacy)" tab's `openapi` group is
  skipped by `resolveGroup` today (`docs.ts:53`); that's a separate project. The tab simply
  won't render in the tab bar until it has pages (correct behavior).
- **No new "block" components beyond `Update`** — the Try-camelAI CTA, FAQ, and capability
  grids all fall out of the restyled primitives; a bespoke `Hero`/`CTA` component would be
  camelAI-specific in an OSS repo.
- **Didn't touch** search backend, llms.txt/raw-markdown pipeline, deploy scripts, or the
  `navTabs()` data layer (only its rendering).

# Open questions for Illiana (defaults chosen; flag to change)

1. **OSS default accent** stays Mintlify-green `#0d9373` (camelAI overrides to indigo via
   docs.json). Want a different out-of-box default?
2. **Search placement**: I moved it to the navbar center like the old site. If you'd rather
   keep it right-aligned, §A3's center zone collapses into the right cluster unchanged.
3. **Steps markers**: numbered squares (chosen) vs. the old dot-on-rail. Numbered reads better
   for the 14-step model-provider page, but it's a taste call.
4. **`appearance.default`**: both reference screenshots are dark. Set
   `"appearance": { "default": "dark" }` in docs.json, or leave system-default? (Currently
   unset → system.)
5. **The 18 `.mdx.tmp` strays** — delete in Part B, or leave?
