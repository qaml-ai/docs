#!/usr/bin/env bash
set -euo pipefail

should_sync_search() {
  local files="$1"
  while IFS= read -r file; do
    [[ -n "$file" ]] || continue
    case "$file" in
      package.json|package-lock.json|wrangler.jsonc|.gitignore|scripts/ci-search-sync.sh)
        ;;
      .github/*)
        ;;
      *)
        return 0
        ;;
    esac
  done <<<"$files"
  return 1
}

trigger_lazy_sync() {
  local url="${DOCSFLARE_SEARCH_SYNC_URL:-https://camelai.com/docs/api/search/sync}"
  curl -fsS --retry 5 --retry-delay 2 --retry-all-errors "$url"
  echo
}

if ! command -v git >/dev/null 2>&1 || ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Git metadata unavailable; triggering lazy search sync."
  trigger_lazy_sync
  exit 0
fi

if ! git rev-parse HEAD^ >/dev/null 2>&1; then
  branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
  if [[ -z "$branch" || "$branch" == "HEAD" ]]; then
    branch="main"
  fi
  git fetch --depth=2 origin "$branch" >/dev/null 2>&1 || true
fi

if ! git rev-parse HEAD^ >/dev/null 2>&1; then
  echo "No parent commit available after fetching history; triggering lazy search sync."
  trigger_lazy_sync
  exit 0
fi

changed_files="$(git diff --name-only HEAD^ HEAD)"
if [[ -z "$changed_files" ]]; then
  echo "No changed files detected; skipping search sync."
  exit 0
fi

if should_sync_search "$changed_files"; then
  echo "Docs content changed; triggering lazy search sync."
  trigger_lazy_sync
else
  echo "No docs content changes detected; skipping search sync."
fi
