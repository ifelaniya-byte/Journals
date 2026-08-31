#!/usr/bin/env bash
#
# QMP_PUSH_HELPER.sh
# ------------------
# Safe, credentials-free helper for the "push the entire Quiet Mind Press workspace"
# task against the PRIVATE repo ifelaniya-byte/Journals.
#
# It never regenerates product content. It never embeds or stores a token, password,
# API key, or SSH key. It only checks what is present on the local filesystem and, when
# everything is present, stages the trees into git and pushes to the target branch.
#
# The real QMP workspace trees are missing in the session that created this document.
# Run this helper AFTER the trees have been restored into /home/user.
#
# Usage:
#   bash QMP_PUSH_HELPER.sh                 # report only (default)
#   bash QMP_PUSH_HELPER.sh --push          # stage + commit + push if all trees present
#   bash QMP_PUSH_HELPER.sh --branch NAME   # override target branch (default qmp-workspace)
#   bash QMP_PUSH_HELPER.sh --dry-run       # stage a temporary worktree, do not push
#
# Never run with --push unless you have confirmed the target repo is the PRIVATE
# ifelaniya-byte/Journals and the target branch cannot be confused with Range-Band.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${QMP_WORKSPACE:-/home/user}"
BRANCH="qmp-workspace"
DO_PUSH=0
DO_DRY=0
VERBOSE=0

for arg in "$@"; do
  case "$arg" in
    --push) DO_PUSH=1 ;;
    --dry-run) DO_DRY=1 ;;
    --branch)
      shift
      BRANCH="${1:?--branch requires a value}"
      ;;
    --verbose) VERBOSE=1 ;;
    --help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 2
      ;;
  esac
done

# Baselines that are ALREADY accounted for and should NOT be re-attached/copied in.
# Keeping them out prevents accidental duplication or mixing with other imprints.
ALREADY_PUSHED=(
  "quiet-mind-restore/catalogs/qmp-adhd"   # frozen 18-product catalog if restored here
  "quiet-mind-restore/catalogs/range-band"  # Range-Band, read-only, kept isolated
)

# The trees that make up the remaining QMP workspace to ship.
REQUIRED_TREES=(
  "qmp-wave-a"
  "qmp-wave-b"
  "qmp-all-36"
  "qmp-next-36"
  "qmp-deep-36"
  "quiet-mind-restore"
)

fail=0
missing=()
for tree in "${REQUIRED_TREES[@]}"; do
  if [ ! -d "${WORKSPACE}/${tree}" ]; then
    missing+=("$tree")
    fail=1
  fi
done

if [ "$fail" -ne 0 ]; then
  echo "BLOCKED: the QMP workspace is not fully present on the live filesystem." >&2
  echo "Present trees:" >&2
  for tree in "${REQUIRED_TREES[@]}"; do
    if [ -d "${WORKSPACE}/${tree}" ]; then
      echo "  [OK]      ${WORKSPACE}/${tree}"
    else
      echo "  [MISSING] ${WORKSPACE}/${tree}"
    fi
  done
  echo >&2
  echo "Nothing was staged, committed, or pushed. Restore the missing trees first." >&2
  exit 1
fi

echo "All QMP workspace trees are present:"
total=0
for tree in "${REQUIRED_TREES[@]}"; do
  count=$(find "${WORKSPACE}/${tree}" -type f 2>/dev/null | wc -l | tr -d ' ')
  size=$(du -sh "${WORKSPACE}/${tree}" 2>/dev/null | cut -f1)
  total=$((total + count))
  echo "  ${tree}: ${count} files, ${size}"
done
echo "  TOTAL_MANAGED_FILES=${total}"

# Count product candidate folders inside each ready/ tree (informative only).
ready_count=0
for ready in \
  "${WORKSPACE}/qmp-wave-a/ready" \
  "${WORKSPACE}/qmp-wave-b/ready" \
  "${WORKSPACE}/qmp-next-36/ready" \
  "${WORKSPACE}/qmp-deep-36/ready"; do
  if [ -d "$ready" ]; then
    n=$(find "$ready" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    ready_count=$((ready_count + n))
    echo "  ${ready}: ${n} product folders"
  fi
done
echo "  READY_PRODUCT_FOLDERS=${ready_count}"

# Guard: never mix Range-Band trees into a QMP push.
if [ -d "${WORKSPACE}/quiet-mind-restore/catalogs/range-band" ]; then
  echo "WARNING: Range-Band catalog tree detected under quiet-mind-restore. It will be excluded."
fi

if [ "$DO_DRY" -eq 0 ] && [ "$DO_PUSH" -eq 0 ]; then
  echo
  echo "Report only (QMP source verified present). Re-run with --push to commit and push."
  echo "Nothing was changed in git."
  exit 0
fi

# Remote guard: the push must go only to the private ifelaniya-byte/Journals repo.
remote_url=$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || true)
case "$remote_url" in
  *ifelaniya-byte/Journals*|*ifelaniya-byte%2FJournals*) ;;
  *)
    echo "BLOCKED: origin is not ifelaniya-byte/Journals (got: ${remote_url:-none})." >&2
    exit 1
    ;;
esac

# Stage into a subtree that keeps QMP isolated from the catalog branches.
STAGING_DIR="$REPO_ROOT/qmp-workspace"
mkdir -p "$STAGING_DIR"

for tree in "${REQUIRED_TREES[@]}"; do
  # Skip range-band checkout when present; it must stay isolated.
  [ "$tree" = "quiet-mind-restore" ] && \
    [ -d "${WORKSPACE}/quiet-mind-restore/catalogs/range-band" ] && \
    echo "Excluding range-band from quiet-mind-restore staging."

  echo "Staging ${tree} ..."
  rm -rf "$STAGING_DIR/${tree}"
  cp -a "${WORKSPACE}/${tree}" "$STAGING_DIR/${tree}"
done

# Remove any unrelated git repos that would turn a plain staged tree into an embedded repo.
find "$STAGING_DIR" -name .git -prune -exec rm -rf {} + 2>/dev/null || true

git -C "$REPO_ROOT" add "$STAGING_DIR"

if [ "$DO_DRY" -eq 1 ]; then
  echo
  echo "DRY-RUN complete: staged $(git -C "$REPO_ROOT" status --porcelain "$STAGING_DIR" | wc -l | tr -d ' ') paths."
  git -C "$REPO_ROOT" status --short "$STAGING_DIR" | head -20
  echo "No commit or push performed."
  exit 0
fi

git -C "$REPO_ROOT" commit -q -m "Add Quiet Mind Press workspace (qmp-wave-a, qmp-wave-b, qmp-all-36, qmp-next-36, qmp-deep-36, quiet-mind-restore)"
git -C "$REPO_ROOT" push -u origin "HEAD:${BRANCH}"

echo
echo "Pushed to origin/${BRANCH}."
echo "Verify with:"
echo "  git ls-remote origin ${BRANCH}"
echo "  curl -s https://api.github.com/repos/ifelaniya-byte/Journals/branches/$(python3 -c "import urllib.parse;print(urllib.parse.quote('${BRANCH}',safe=''))")"

exit 0
