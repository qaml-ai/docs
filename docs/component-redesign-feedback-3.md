# Component redesign — feedback 3 (fixes to the round-3 implementation)

> **For the implementing agent (assume no prior context):** The docs redesign has gone
> through three passes (`component-redesign-plan.md`, `component-redesign-feedback.md`,
> `component-redesign-feedback-2.md` — background only; do not re-implement from them).
> This doc is the complete work list for this pass: two items, both root-caused against the
> current working tree on 2026-07-22.
>
> **Where things live:** framework = `/Users/illiana/Projects/open-mdx-docs` (uncommitted
> working tree — do not reset). This content repo consumes it via the symlink at
> `node_modules/open-mdx-docs` (leave it; avoid installs that would replace it). Run:
> `bun run dev -- --port "${CONDUCTOR_PORT:-3000}"` → `http://localhost:<port>/docs/`.
> Vite-plugin/config changes need a server restart; app-component changes hot-reload.
> Both items reproduce on a fresh server — no stale-cache caveats this round.

---

## 1. Standalone linked Card inflates to the page height — remove `h-full` from the link wrapper

**Symptom:** the "Try camelAI" card on `/docs/getting-started/overview` renders thousands
of pixels tall. DevTools shows the `<a>` wrapper's `h-full` is responsible.

**First, the design question that came up: the `<a>` wrapper is intentional and stays.**
A Card with `href` must be a single whole-card click target, and the only correct way to
make a block clickable is to wrap it in an anchor (same thing Mintlify does; also what makes
cmd-click/middle-click/right-click-copy-link work). The component isn't misusing `<a>` —
the sizing utility on it is the bug.

**Root cause:** the wrapper class is `not-prose block h-full no-underline`
(`app/lib/mdx-components.tsx:161`). Where the card sits inside a `CardGroup`, the anchor is
a **grid item** — its `h-full` resolves against a small grid-track height and gives the
intended equal-height cards. But a standalone card's anchor is a child of the
`<article>` — a **stretched flex item** of the `flex gap-8` row in `docs-page.tsx` — and
Chrome resolves percentage heights against stretched flex items. The stretched height of
the article is the full article content height, so `h-full` = the entire page's height →
giant card. (This is also why the footer seemed unreachable earlier: the anchor extends
past the viewport.)

**Fix:** drop `h-full` from the anchor only:

```tsx
const className = 'not-prose block no-underline';
```

Equal heights in grids are unaffected: grid items stretch to their track by default, so the
anchor still fills its cell, and the inner `div`'s `h-full` (keep that one) fills the
anchor. In the standalone case the anchor is now content-sized — the horizontal banner
renders at its natural ~90px.

**Verify:** overview page — banner-height CTA card; then a `CardGroup cols={2}` with one
short and one long card (e.g. on `/docs/plans/overview`) — both cards in a row still equal
height; footer reachable.

## 2. "On this page" rail: stop using sticky — pin it with `position: fixed`

**Symptom (accurate report):** after the round-3 padding fix the rail pins correctly at
first, but near the very end of the page it starts moving again and can ride up mostly out
of view.

**Why sticky can never fully satisfy the requirement:** a sticky element is confined to its
containing block — when the bottom of the content row scrolls up past the pinned rail,
sticky *must* push the rail up with it. Any sticky variant only shrinks that push; the
requirement is **the rail never moves at all**, so the positioning scheme has to change.

**Fix (`app/components/docs/toc.tsx`):** keep a placeholder column in flow to preserve the
layout, and make the `<nav>` viewport-fixed. With `top` set and `left`/`right` left `auto`,
a fixed element keeps its **static position** horizontally — it stays exactly in the
column the placeholder reserves, no coordinate math, survives resizes:

```tsx
return (
  <div className="hidden w-56 shrink-0 xl:block">        {/* reserves the column */}
    <nav
      className={cn(
        'docs-sidebar-scroll fixed w-56 overflow-y-auto pt-8 pb-4 pl-6',
        multiTab
          ? 'top-[6.25rem] max-h-[calc(100svh-7.25rem)]'
          : 'top-14 max-h-[calc(100svh-4.5rem)]',
      )}
    >
      …existing title + list…
    </nav>
  </div>
);
```

- Remove `sticky` and the `-mt-8` (that trick existed only for sticky; the `pt-8` stays and
  now provides the pinned breathing room directly).
- The `max-h` is 1rem shorter than the available space so a long list never kisses the
  viewport bottom; when the list is taller than that, it scrolls **inside its own box**
  (`overflow-y-auto`) — exactly the requested behavior for short windows.
- Scroll-spy logic: unchanged.

**Apply the same pattern to the left sidebar** (`app/components/docs/sidebar.tsx` +
the `<aside>` in `docs-layout.tsx`): it has the identical end-of-page push, just less
noticed. The `aside` (`hidden w-60 shrink-0 py-8 lg:block`) becomes the placeholder — drop
its `py-8`; the inner `<nav>` swaps `sticky`/`-mt-8` for `fixed w-60` with the same
top/max-h treatment as above (keep its `pt-8 pb-10` and the mobile-drawer `sticky={false}`
escape hatch working). Rails must behave identically or the asymmetry will read as a bug.

**Trade-off accepted deliberately:** at the very bottom of the page the fixed rails float
over the footer band (within their own side columns). That's the correct cost of
"never moves" — do not add scroll listeners or JS repositioning to avoid it.

**Verify:** on a long page (`/docs/plans/model-providers`) scroll to the absolute bottom —
neither rail moves a single pixel at any scroll position; on a short window, the TOC
scrolls within its own box; at `< xl` the TOC column disappears entirely (placeholder is
hidden too); left sidebar identical; no horizontal jump in either rail while resizing the
window across the `xl` boundary.

---

## Hand-back checklist

1. `bun run typecheck` in open-mdx-docs passes.
2. Overview: natural-height horizontal CTA banner; equal-height card grids elsewhere.
3. Both rails: pinned with 32px header clearance, zero movement at end of page, internal
   scroll when constrained.
4. Quick regression sweep of earlier rounds still green: sky accent, wordmark logo +
   qwaml-box favicon, FAQ block spacing, line tabs on connections, changelog TOC dates,
   sun/moon toggle.
