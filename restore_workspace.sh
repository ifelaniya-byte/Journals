#!/usr/bin/env bash
# Restore the split workspace for a new Arena chat.
# Catalogs → /tmp. Pipeline + hub → /home/user. Never mix trees.
set -euo pipefail

REPO="git@github.com:ifelaniya-byte/Journals.git"
KEY="${GIT_SSH_KEY:-$HOME/.ssh/github_journals_deploy}"

if [[ -f "$KEY" ]]; then
  chmod 600 "$KEY" || true
  export GIT_SSH_COMMAND="ssh -i $KEY -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
fi

here="$(cd "$(dirname "$0")" && pwd)"

echo "== clone catalogs to /tmp (not the pipeline tree) =="
if [[ ! -d /tmp/qmp-adhd/.git ]]; then
  git clone --single-branch --branch ADHD-Journals "$REPO" /tmp/qmp-adhd
else
  git -C /tmp/qmp-adhd fetch origin ADHD-Journals
  git -C /tmp/qmp-adhd checkout ADHD-Journals
  git -C /tmp/qmp-adhd pull --ff-only origin ADHD-Journals || true
fi

if [[ ! -d /tmp/Journals-remote/.git ]]; then
  git clone --single-branch --branch Range-Band "$REPO" /tmp/Journals-remote
else
  git -C /tmp/Journals-remote fetch origin Range-Band
  git -C /tmp/Journals-remote checkout Range-Band
  git -C /tmp/Journals-remote pull --ff-only origin Range-Band || true
fi

echo "== pipeline already at $here =="
if [[ "$here" != /home/user/pipeline && ! -d /home/user/pipeline/.git ]]; then
  mkdir -p /home/user
  if [[ -d "$here/.git" ]]; then
    ln -sfn "$here" /home/user/pipeline 2>/dev/null || cp -a "$here" /home/user/pipeline
  fi
fi

if [[ -f "$here/SELL_HUB.md" ]]; then
  cp -f "$here/SELL_HUB.md" /home/user/SELL_HUB.md
fi
if [[ -f "$here/NEW_CHAT.md" ]]; then
  cp -f "$here/NEW_CHAT.md" /home/user/NEW_CHAT.md
fi

echo
echo "== SHAs (do not merge these) =="
printf "ADHD-Journals          %s\n" "$(git -C /tmp/qmp-adhd rev-parse --short HEAD) $(git -C /tmp/qmp-adhd log -1 --format=%s)"
printf "Range-Band             %s\n" "$(git -C /tmp/Journals-remote rev-parse --short HEAD) $(git -C /tmp/Journals-remote log -1 --format=%s)"
printf "Agent-Seller-Pipeline  %s\n" "$(git -C "$here" rev-parse --short HEAD 2>/dev/null || echo 'not a git dir') $(git -C "$here" log -1 --format=%s 2>/dev/null || true)"
echo
echo "Books stay in /tmp. Pipeline stays in $here."
echo "Do not merge. Do not force-push catalogs. Do not copy PDFs into the pipeline."
