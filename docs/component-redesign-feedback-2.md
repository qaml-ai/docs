# Component redesign — feedback 2 (fixes to the round-2 implementation)

> **For the implementing agent (assume no prior context):** The docs redesign was
> implemented in two passes from `component-redesign-plan.md` and
> `component-redesign-feedback.md` (both in this `docs/` folder — background reading only;
> do **not** re-implement from them). This doc is the complete, self-contained work list for
> the next pass. Everything below was verified against a live run on 2026-07-22.
>
> **Where things live:** the framework is `/Users/illiana/Projects/open-mdx-docs`
> (uncommitted working-tree changes — do not reset). This content repo consumes it via a
> symlink at `node_modules/open-mdx-docs` (leave the symlink; don't re-run installs that
> would replace it). Run the site from this repo:
> `bun run dev -- --port "${CONDUCTOR_PORT:-3000}"` → `http://localhost:<port>/docs/`.
> Note: changes to `vite/mdx-docs-plugin.ts` or vite config **require a server restart**;
> app-component changes hot-reload. FYI: `…/workspaces/docs/run-docs-locally` is a symlink
> to the `valencia` workspace — same directory; there is only one checkout of this repo.

---

## 0. First action: clean restart, then triage

The previous review session ran against a dev server that had been alive *while* the
framework was edited (plugin changes don't hot-reload, and the module graph can wedge).
Before touching code:

```bash
# kill any running docs dev server, then:
rm -rf node_modules/.vite
bun run dev -- --port "${CONDUCTOR_PORT:-3000}"
# hard-reload the browser (⌘⇧R)
```

On a fresh server these already render correctly (verified in served HTML — expect them
fixed; only debug if one still reproduces): the **Try camelAI card is horizontal** on
`/docs/getting-started/overview` (`flex items-start gap-3 p-4` in the markup, `horizontal`
prop present in `overview.mdx`), and the **footer renders/scrolls normally** on that page.

Items 1-3 below are real code changes.

## 1. Theme toggle: replace the segmented control with a single sun/moon flip

**Current state:** `app/components/docs/theme-toggle.tsx` renders a three-segment
radiogroup (Sun/Monitor/Moon in a bordered pill). It was built to spec, but the spec has
changed: three always-visible options is too much chrome for the navbar.

**New spec — one icon button that flips the rendered theme** (the shadcn-docs pattern;
"system" becomes the invisible default rather than a visible option):

- `const { resolvedTheme, setTheme } = useTheme()` — `resolvedTheme` folds in the system
  preference (component is ClientOnly-wrapped, safe to read).
- Render a `variant="ghost" size="icon"` Button (add `relative`) with
  `onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}`.
- Label names the **action, not the state**: `const label = resolvedTheme === 'dark' ?
  'Switch to light theme' : 'Switch to dark theme'`, applied as both `aria-label` and
  `title` (that title is the hover tooltip Illiana asked for).
- Icon swap driven purely by the `.dark` class, with the shadcn rotate/scale transition:

  ```tsx
  <Sun className="size-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
  <Moon className="absolute size-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
  ```

- Behavior: first visit follows the OS (`appearance.default` still the starting point); the
  first click persists an explicit choice under the existing `theme` storage key. There is
  deliberately **no "back to system" UI**.
- Keep `strict → return null`. The `ClientOnly` fallback in `docs-layout.tsx` should be the
  original `<span className="size-9" />` (button footprint is one icon; if a wider
  segmented-era skeleton is in place, shrink it back).
- The DropdownMenu import chain from the pre-redesign toggle is gone/unused —
  `ui/dropdown-menu.tsx` can stay in the repo.

## 2. Content-repo assets 404 in dev: middleware never strips the base path

**Repro (fresh server):** `GET /docs/logo/light.svg` → **404**, while
`GET /docs/favicon.svg` → 200 **but serves the framework's own `public/favicon.svg`**, not
this repo's camelAI one (byte-compared). Consequences the user sees: no logo in the header —
the broken `<img>` shows its alt text, which is literally the words "camelAI Documentation" —
and the wrong favicon. This repo's side is fully correct (`favicon.svg` is byte-identical to
the approved qwaml-box mark, `logo/light.svg` + `logo/dark.svg` exist, `docs.json` points at
all three).

**Root cause:** the dev asset middleware (`vite/mdx-docs-plugin.ts:544-553`) resolves
`path.join(contentDir, rel)` from the **raw URL**, so with `basePath: '/docs'` the request
`/docs/logo/light.svg` maps to `<contentDir>/docs/logo/light.svg` — no such file →
`staticAssets.includes()` misses → falls through to Vite's public-dir handler (framework
defaults).

**Fix:**

1. Strip the configured base path before resolving:
   `if (basePath !== '/' && url.startsWith(basePath)) url = url.slice(basePath.length)`,
   then resolve as today. Content assets (including `favicon.svg`) are then matched by this
   middleware before Vite's public-dir fallback, so the site's own files win in dev.
2. **Build precedence:** `generateBundle` emits content assets at their relative names while
   Vite also copies the framework `public/` into the output — a same-named `favicon.svg` has
   an undefined winner. Make the content asset win deterministically (skip the framework
   public copy when a content asset shares the name, or rename the framework default so it
   only backs sites with no `favicon` configured). Then `bun run build` and confirm the
   client output's `favicon.svg` is the qwaml-box file and `logo/*.svg` land where the
   base-path nesting step expects.

## 3. Sticky rails pin flush against the header — add pinned breathing room

**Repro:** scroll any long page; the right "On this page" rail pins with its title touching
the header hairline (`top-[6.25rem]`, no internal top padding). The left sidebar has the
same flaw — its 32px offset comes from the aside's `py-8`, which stays behind in flow when
the nav pins.

**Fix (both rails, same trick):** add `-mt-8 pt-8` to the sticky `<nav>` elements in
`app/components/docs/toc.tsx` and `app/components/docs/sidebar.tsx`. Net flow position is
unchanged (the negative margin cancels the padding) but the pinned nav carries 32px of
internal top padding. Keep `top-[6.25rem]` / `max-h-[calc(100svh-6.25rem)]` and the
single-tab variants exactly as they are.

Context on the reported "rail scrolls off the page entirely": it does **not** reproduce on a
fresh server — the nav is `sticky` + `max-h` + `overflow-y-auto`, which is the desired
"pinned, scrolls within its own box" behavior. If it somehow reproduces after §0's clean
restart, the culprit will be an `overflow-*` ancestor between `<body>` and the nav (the
classic sticky killer) — none exists in the current markup.

---

## Verify before handing back

Light **and** dark mode, fresh server per §0:

1. `curl -s localhost:<port>/docs/logo/light.svg | head -c 80` → camelAI SVG (not 404);
   header shows the wordmark in both themes with no alt-text flash; browser tab shows the
   qwaml-box favicon (compare against `/favicon.svg` in this repo, not the framework's).
2. Theme toggle: one button; sun in light, moon in dark; click flips with the rotate
   transition; tooltip reads "Switch to dark/light theme"; choice survives reload;
   `appearance.strict` hides it.
3. Scroll `/docs/getting-started/organizations`: both rails pin with ~32px below the header
   (nothing touching the hairline), stay pinned to the bottom of the page, and scroll
   internally when taller than the viewport.
4. `/docs/getting-started/overview`: horizontal Try camelAI banner, footer reachable.
5. `bun run build` in this repo succeeds; spot-check the output for `favicon.svg` (qwaml-box)
   and `logo/*.svg`. `bun run typecheck` in open-mdx-docs passes.
