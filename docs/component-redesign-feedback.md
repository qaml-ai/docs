# Component redesign — review feedback (round 2)

> **Superseded in part:** follow-up fixes to this round's implementation live in
> `component-redesign-feedback-2.md`. This file is the record of what the round-2 agent
> worked from — do not re-implement from it.

> **For the implementing agent:** This is the review of the redesign you implemented from
> `component-redesign-plan.md` (working-tree changes in `/Users/illiana/Projects/open-mdx-docs`
> plus this repo). The implementation is faithful to the plan — nav shell, cards, line tabs,
> code chrome, callouts, steps, pager, `Update`, search, and the link doctrine all landed
> correctly, and `stripBase` in the layout was a good catch. Do not rework those. This file is
> the fix list from design review + Illiana's feedback, ranked. Each item has a verified root
> cause where relevant. Same rules as before: exact specs are exact; don't invent new visual
> treatments. Re-verify file:line refs before editing (checked 2026-07-22).

---

## F1. Accent color: compile the theme into the stylesheet at build time

**Symptom:** the site renders Mintlify-green everywhere even though `docs.json` has custom
colors.

**Root cause:** `app/root.tsx` renders the `:root{--docs-primary:…}` `<style>` **before**
`<Links />`. The built `app.css` arrives later in `<head>` and its own
`:root { --docs-primary: #0d9373 }` (app.css:8-10) has equal specificity but later position —
the stylesheet always wins and the injected values are dead code. (Predates the redesign;
it's why the deployed site was green before it, too.)

**The insight that makes the fix clean:** `docs.json` is a *build-time* input — the Vite
plugin already reads it (`loadConfig()`, `vite/mdx-docs-plugin.ts:203`) and bakes it into the
bundle as `virtual:mdx-docs/config` (`:418-419`). Runtime `<style>` injection was solving a
problem that doesn't exist. Compile the user's theme into the CSS instead — then `:root`
genuinely holds the user's accent, there is no cascade race, no inline styles on `<html>`,
and no flash of default-then-brand (the values ship inside the one stylesheet).

**Mechanism (framework):**

1. The plugin generates a new virtual CSS module, **`virtual:mdx-docs/theme.css`**
   (resolve it to an id ending in `.css` — e.g. `\0mdx-docs:theme.css` — so Vite's CSS
   pipeline processes it). Its contents, in order, each block emitted only when configured:
   - From `docs.json` `colors`:
     `:root{--docs-primary:…;--docs-primary-light:…;--docs-primary-dark:…}`
   - From `docs.json` `fonts`: `:root{--docs-font-sans:…;--docs-font-mono:…}` (same
     family+fallback strings root.tsx builds today).
   - `:root{--docs-scroll-padding:7.5rem}` when the config has more than one navigation tab,
     else `5rem` (tab count is derivable from the config at build time).
   - **Verbatim contents of an optional `theme.css`** sitting next to `docs.json` in the
     content repo — always last, so it can override anything, including the `--primary`
     mapping itself.
2. `app/root.tsx`: after `import './app.css'`, add `import 'virtual:mdx-docs/theme.css'`.
   Import order = bundle order = cascade order, deterministic in dev and production.
3. **Delete the runtime injection**: the `dangerouslySetInnerHTML` `<style>` block and the
   `colors`/`fontStyle`/`multiTab` plumbing in the loader/Layout that fed it. The loader
   keeps only favicon + the Google Fonts `<link>`s (it still reads `docsConfig.fonts` for
   the href).
4. **De-Mintlify the defaults:** change `app.css:8-10` from the greens to neutral shadcn
   zinc, so the fallback for a completely unconfigured install is tasteful monochrome — the
   green ceases to exist in the codebase:

   ```css
   --docs-primary: oklch(0.21 0.006 285.885);        /* zinc-900 */
   --docs-primary-light: oklch(0.92 0.004 286.32);   /* zinc-200 (dark-mode accent) */
   --docs-primary-dark: oklch(0.21 0.006 285.885);
   ```

5. **Dev DX:** the plugin already reloads config on change (`:398`); extend that to
   invalidate `virtual:mdx-docs/theme.css` and `addWatchFile` the consumer `theme.css`, so
   accent edits hot-reload.

**Why `theme.css` is the OSS story:** consumers install open-mdx-docs as a package — all
Tailwind/shadcn config lives inside it, and a content repo has no CSS entry point, so running
`shadcn init` there does nothing. But every component consumes standard shadcn tokens
(`--primary`, `--background`, `--border`, `--radius`, …), so a pasted shadcn theme block
(ui.shadcn.com/themes, tweakcn, or their own app's `globals.css`) rethemes the entire site —
shadcn theming working the way shadcn users expect. Precedence, lowest → highest: framework
zinc defaults → `docs.json` `colors` (Mintlify-compat shortcut, sets the `--docs-primary`
trio only) → `theme.css` (full control over any token). Document both paths with a
copy-paste example in README/AGENTS + `docs/guides/theming.mdx`.

**camelAI (this repo):** accent becomes **sky**. Create `theme.css` next to `docs.json`:

```css
/* camelAI docs theme — sky accent on zinc neutrals */
:root {
  --primary: oklch(0.5 0.134 242.749);   /* sky-700 — AA on white for links/pills */
  --primary-foreground: oklch(0.985 0 0);
  --ring: oklch(0.5 0.134 242.749);
}
.dark {
  --primary: oklch(0.746 0.16 232.661);  /* sky-400 — pops on zinc-950 */
  --primary-foreground: oklch(0.141 0.005 285.823);
  --ring: oklch(0.746 0.16 232.661);
}
```

and **remove the `colors` block from `docs.json`** (one source of truth; `fonts` stays).
Deliberate: sky-700 in light mode, not sky-600 — sky-600 on white is 3.98:1 and fails AA for
link text; sky-700 is 5.5:1. If it reads too deep in light mode, flag it rather than swapping
hues silently.

## F2. Brand: new logos + favicon, logo-only header

Assets in `/Users/illiana/Desktop/camelAI-new-branding/NEW-BRANDING-06-2026/` (verified:
fullname lightmode SVG = black paths → for light mode; darkmode = white paths; `qwaml-box`
= 466×466 rounded-square mark):

1. Copy into this repo: `camelAI-fullname-logo-lightmode.svg` → `logo/light.svg`,
   `camelAI-fullname-logo-darkmode.svg` → `logo/dark.svg`, `qwaml-box light-mode.svg` →
   `favicon.svg` (the boxed mark carries its own background, so it stays legible on any tab
   color). Delete the old `logo/light.png`, `logo/dark.png`, `favicon.png`.
2. `docs.json`: `"logo": { "light": "/logo/light.svg", "dark": "/logo/dark.svg" }`,
   `"favicon": "/favicon.svg"`. Keep `"name"` (it feeds `<title>` and the footer), but the
   header must render **logo only — no text**: `Logo()` (`docs-layout.tsx:20-37`) already
   does this when logo files resolve, so the "camelAI Documentation" text in the header
   screenshot means the images 404'd. Verify the rendered `<img src>` resolves under the
   `/docs` base path (assetUrl → `withBase`) in the running preview, not just that the code
   looks right.
3. The wordmark is wide (~4.15:1) — keep `className="h-6"` (renders ~100px wide). If it
   crowds the mobile row, drop to `h-5` at `< md` only.

## F3. "Try camelAI" card: add a `horizontal` card variant

**Symptom:** the overview CTA spans the full content column as a stacked icon-over-title
block — reads as one gigantic empty button.
**Cause:** it's a standalone `<Card>` outside any `CardGroup` (getting-started/overview.mdx:11-17),
so the §A7 stacked layout stretches edge-to-edge with three sparse lines.
**Fix (framework):** support Mintlify's `horizontal` prop on Card (`mdx-components.tsx` Card):

```
<Card horizontal>
┌──────────────────────────────────────────────────────────────┐
│ 🚀   Try camelAI                                          ↗  │
│      **No credit card required.** Start building in minutes. │
└──────────────────────────────────────────────────────────────┘
```

- `horizontal`: container swaps to `flex items-start gap-3 p-4` (tighter than p-5); icon
  `size-5 text-primary mt-0.5 shrink-0`; text column (`min-w-0 flex-1`): title
  `text-base font-semibold` (no `mt-3`), body `mt-1 text-sm leading-relaxed
  text-muted-foreground`; external arrow stays pinned `top-4 right-4`.
- Everything else (border, transparent bg, hover, `not-prose` link wrapper) identical to the
  stacked variant. Add a `horizontal` example to the framework sample docs.

**Fix (this repo):** add `horizontal` to the Try camelAI card in
`getting-started/overview.mdx`. Also check the two other standalone full-width linked cards
found in the census (`dev_api/introduction.mdx` "Ready to get started?", `plans` pages) and
apply `horizontal` where they look like banners.

## F4. FAQ block: kill the phantom padding, then polish

**Root cause (verified):** `AccordionTrigger` wraps the button in
`AccordionPrimitive.Header` — an `<h3>` (`ui/accordion.tsx:28`). Inside the `.prose-docs`
article, the typography plugin gives it `h3` treatment: ~32px top margin, 12px bottom,
1.25em font size. That's exactly the dead zone above each question (and why the questions
render oversized) in the screenshot.

**Fix:** exclude the header element itself from prose — `ui/accordion.tsx`:

```tsx
<AccordionPrimitive.Header className="not-prose flex">
```

Do **not** put `not-prose` on the AccordionGroup container — answers contain markdown links
and must keep prose/link styling.

**Polish pass (with the margins gone, exact spec):**

- Trigger: `px-4 py-4 text-[15px] font-medium` (bump from `text-sm`/`py-3.5` — the question
  is the primary interactive text; 15px/py-4 gives ~48px rows like the reference).
- Answer: keep `px-4 pb-4 text-sm leading-relaxed text-muted-foreground`, and add `pt-0.5`
  so the first line doesn't hug the question.
- Keep: one `rounded-xl border` container, `divide-y`, `hover:bg-muted/50` row hover,
  chevron rotate. Standalone Accordion gets the same trigger/content spec automatically.

## F5. Changelog: "On this page" lists the dates, not the inner headings

**Problem:** `<Update>` children are full markdown; their `##`/`###` headings flood the TOC.
For a changelog the TOC should be the release dates.

**Fix (all framework):**

1. `vite/mdx-docs-plugin.ts`, in the existing TOC extraction pass: also visit
   `mdxJsxFlowElement` nodes with `name === 'Update'`; for each, read the `label` string
   attribute and push `{ depth: 2, text: label, id: slugger.slug(label) }` into a separate
   `updates` list (same `GithubSlugger` instance/behavior as headings). After the walk: **if
   `updates.length > 0`, the page's toc = the updates list only** (drop heading entries).
2. `Update` component (`mdx-components.tsx`): derive the same id from `label` (module-scope
   `new GithubSlugger()` per render won't match dedup counters — use `github-slugger`'s
   exported `slug(label)` function in both places) and set it on the wrapper:
   `<div id={id} data-update …>`. Document in the sample docs that `label`s should be unique
   per page (dates are).
3. `toc.tsx` needs no changes — the scroll-spy is `getElementById`-based and the global
   `scroll-padding-top` already handles anchor offset. Verify clicking a date scrolls with
   correct offset and the spy tracks entries as you scroll `/docs/changelog/legacy`.

## F6. Heading anchors: make it read as "copy link"

Replace the `#` glyph with a copy-link affordance:

1. In the `rehype-autolink-headings` options (`vite/mdx-docs-plugin.ts`), set `content` to a
   hast `<svg>` of the lucide **`link`** (chain) icon — 16×16, `fill="none"`,
   `stroke="currentColor"`, `stroke-width="2"` — and `properties: { className:
   ['heading-anchor'], 'aria-label': 'Copy link to this section', title: 'Copy link' }`.
2. CSS (`app.css`, replacing the current `.heading-anchor` block; keep it after the link
   doctrine rules):

   ```css
   .heading-anchor { … existing opacity/margin rules … ; position: relative; }
   .heading-anchor svg { width: 0.8em; height: 0.8em; display: inline; vertical-align: -0.08em; }
   .heading-anchor:hover { color: var(--primary); }
   .heading-anchor[data-copied]::after {
     content: 'Copied';
     position: absolute; left: calc(100% + 0.5rem); top: 50%; translate: 0 -50%;
     padding: 2px 8px; border-radius: 9999px;
     background: var(--primary); color: var(--primary-foreground);
     font-size: 11px; font-weight: 500; white-space: nowrap;
   }
   ```

3. Behavior (`docs-page.tsx`): a `useEffect` with one delegated click listener on the
   article — on `.heading-anchor` click, *don't* preventDefault (hash nav still happens);
   additionally write `location.origin + withBase('/' + slug) + '#' + id` to the clipboard,
   set `data-copied` on the anchor, remove it after 1.5s.

## F7. Sidebar active item: no outline, rounder

`sidebar.tsx` `SidebarPage`: drop `ring-1 ring-primary/30 ring-inset` from the active state
and change the shared base from `rounded-md` to `rounded-lg`. Result — active:
`rounded-lg bg-primary/10 font-medium text-primary`; inactive unchanged.

## F8. Theme toggle: three-way segmented control

*(Note: superseded by `component-redesign-feedback-2.md` §1 — kept here as the record of
what this round implemented.)*

The dropdown works but is a heavy interaction for a three-state choice. Replace it with an
inline segmented control (rewrite `app/components/docs/theme-toggle.tsx`; drop the
DropdownMenu import entirely):

```
╭─────────────╮
│ ☀ │ ▢ │ ☾ │      ← Light · System · Dark, active segment filled
╰─────────────╯
```

- Container: `flex items-center gap-0.5 rounded-full border p-0.5`, `role="radiogroup"`
  `aria-label="Theme"`.
- Each segment: a `<button>` with `flex size-6 items-center justify-center rounded-full
  text-muted-foreground transition-colors hover:text-foreground`, icons `Sun` / `Monitor` /
  `Moon` at `size-3.5`, order Light → System → Dark, `role="radio"`,
  `aria-checked={theme === value}`, `aria-label` "Light theme" / "System theme" /
  "Dark theme", `onClick={() => setTheme(value)}`.
- Active segment: `bg-muted text-foreground` — deliberately **monochrome**, not accent; this
  is utility chrome, not content (accent doctrine applies to pointing, not controls).
- Keep the `strict → return null` behavior.

## F9. Card grids must never leave an empty cell

**Symptom:** the Plans page renders 2, 1, 2 with a hole in the grid.
**Root cause:** the content is authored correctly — `plans/overview.mdx:12-28` is a
`cols={3}` group (Free/Starter/Pro) followed by a `cols={2}` group (Team/Enterprise), which
is exactly the old Mintlify 3-then-2 layout in the reference screenshot. But the redesigned
`CardGroup` ignores `cols` and lays out with
`repeat(auto-fit, minmax(min(100%, 16rem), 1fr))` — in the 48rem content column, three 16rem
tracks don't fit, so the cols-3 group wraps 2+1.

**Fix (`CardGroup`, `mdx-components.tsx`):** honor `cols` with explicit responsive classes,
and add orphan-fill rules so **the last row always stretches to fill the width** — Illiana's
rule: a card grid never shows a blank cell, even if some cards end up bigger than others.
Drop the inline `gridTemplateColumns` style entirely.

- `cols={1}`: `my-4 grid grid-cols-1 gap-3`
- `cols={2}` (and the default): `my-4 grid grid-cols-1 gap-3 sm:grid-cols-2
  sm:[&>*:last-child:nth-child(odd)]:col-span-full`
  (odd count → last card spans the full row)
- `cols={3}`: use a 6-track grid so two orphans can split the row evenly:
  `my-4 grid grid-cols-1 gap-3 sm:grid-cols-2
  sm:max-lg:[&>*:last-child:nth-child(odd)]:col-span-full lg:grid-cols-6 lg:[&>*]:col-span-2
  lg:[&>*:last-child:nth-child(3n+1)]:col-span-6
  lg:[&>*:nth-last-child(2):nth-child(3n+1)]:col-span-3
  lg:[&>*:last-child:nth-child(3n+2)]:col-span-3`
  (count %3==1 → last spans full; %3==2 → last two span half each; the `max-lg` cap keeps
  the 2-col odd rule from leaking into the 6-track layout)
- `cols` ≥ 4: treat as 3 (unused in content; note it in the sample docs).

Copy the selector strings exactly — they're fiddly. Add a test page to the framework sample
docs with 3, 4, 5, and 7 cards in `cols={3}` and 3 in `cols={2}` and eyeball every breakpoint.

Result on `/docs/plans/overview` with **no content edit**:

```
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Free    │ │ Starter │ │ Pro     │      ← cols={3}, three across
└─────────┘ └─────────┘ └─────────┘
┌───────────────┐ ┌───────────────┐
│ Team          │ │ Enterprise    │      ← cols={2}, two wide
└───────────────┘ └───────────────┘
```

---

## Smaller findings from the diff review

- **N1 — suppress useless `text` header labels.** `codeLabel()` falls back to the fence
  language, so every bare ```` ```text ```` block gets a header reading "text" (11 such
  fences in content). When the resolved label is just the language and it's
  `text`/`txt`/`plaintext`, return `undefined` → headerless variant with floating copy.
- **N2 — callout paragraph spacing.** `[&_p]:m-0` flattens multi-paragraph callouts into one
  wall. Add `[&_p+p]:mt-2` alongside it (Callout body div, `mdx-components.tsx`).
- **N3 — verify light-mode syntax highlighting.** The redesign removed the
  `color: var(--shiki-light)` rule and now relies on `@shikijs/rehype`'s default
  `defaultColor: 'light'` inlining. Confirm tokens are colored in **light** mode on
  `/docs/dev_api/camel-api-quickstart`; if not, set `defaultColor: 'light'` explicitly in the
  rehype-shiki options.
- **N4 — sample site + README.** New surface added this round (`theme.css`, `horizontal`
  cards, Update TOC behavior, copy-link anchors) must land in the framework's `docs/` sample
  + README the same way the round-1 features did.

## Verify before handing back

Run this repo against the local framework checkout (symlink already in place), light + dark:

1. Accent is **sky** everywhere: tab-bar underline, sidebar pill, TOC active, eyebrow, links
   on hover, Tip callout, copy-success check, focus rings, `::selection`. Zero green
   anywhere; framework sample site (no theme.css) renders monochrome zinc. View source:
   **no** inline `<style>`/`style=` carrying `--docs-primary` — the values live in the built
   stylesheet. Edit `theme.css` while `dev` is running and confirm the accent hot-reloads.
2. Header: camelAI wordmark only (no text), correct logo per theme, favicon in the tab.
3. Overview: Try camelAI renders as a one-row horizontal banner card.
4. `/docs/getting-started/organizations` FAQ: no dead space above questions, 15px questions,
   compact rows.
5. `/docs/changelog/legacy`: TOC shows only the seven dates; clicking scrolls correctly.
6. Hover any `##` heading: chain icon appears, click copies the deep link and flashes
   "Copied", URL hash updates.
7. `/docs/plans/overview`: Free/Starter/Pro three across, Team/Enterprise two wide — no
   empty grid cell at any viewport width. Sample-docs grid test page: 4 cards in `cols={3}`
   → 3 + one full-width; 5 → 3 + two halves.
8. Theme toggle: three segments, active state survives reload, `strict` mode hides it, no
   layout shift while hydrating.
9. `bun run typecheck` in open-mdx-docs; `verify-preview.mjs` passes.
