#!/usr/bin/env bash
set -euo pipefail

SRC=/root/.openclaw
BASE=/www/manmanai/openclaw/backups/local-config
CURRENT="$BASE/root/.openclaw"
HISTORY="$BASE/history"
STAMP=$(date +%Y-%m-%d-%H%M%S)
SNAP="$HISTORY/$STAMP/root/.openclaw"
TMP_PARENT=/tmp
REPO_URL=git@github.com:keket0/backup-private.git

copy_config_tree() {
  local dst="$1"

  mkdir -p "$dst"

  cp -a "$SRC/openclaw.json" "$dst/"
  cp -a "$SRC/exec-approvals.json" "$dst/" 2>/dev/null || true
  cp -a "$SRC/update-check.json" "$dst/" 2>/dev/null || true
  find "$SRC" -maxdepth 1 -type f \( -name 'openclaw.json.bak*' -o -name 'openclaw.json.backup.*' \) -exec cp -a {} "$dst/" \;

  cp -a "$SRC/workspace" "$dst/"
  cp -a "$SRC/workspace-xiaojizhe" "$dst/"
  cp -a "$SRC/agents" "$dst/"
  cp -a "$SRC/identity" "$dst/"
  cp -a "$SRC/devices" "$dst/"
  cp -a "$SRC/telegram" "$dst/"
  cp -a "$SRC/canvas" "$dst/" 2>/dev/null || true
  cp -a "$SRC/completions" "$dst/" 2>/dev/null || true
  cp -a "$SRC/memory" "$dst/" 2>/dev/null || true
  cp -a "$SRC/flows" "$dst/" 2>/dev/null || true
  cp -a "$SRC/tasks" "$dst/" 2>/dev/null || true

  rm -rf \
    "$dst/workspace/.git" \
    "$dst/workspace-xiaojizhe/.git" \
    "$dst/workspace/tmp" \
    "$dst/workspace-xiaojizhe/tmp" \
    "$dst/workspace/.openclaw" \
    "$dst/workspace-xiaojizhe/.openclaw" \
    "$dst/workspace/.agents" \
    "$dst/workspace/state" \
    "$dst/workspace/.clawhub" \
    "$dst/workspace-xiaojizhe/.clawhub"

  find "$dst" -type d \( \
    -name '.qoder' -o -name '.mcpjam' -o -name '.pochi' -o -name '.augment' -o -name '.windsurf' -o -name '.crush' -o -name '.neovate' -o -name '.trae' -o -name '.kilocode' -o -name '.cortex' -o -name '.codebuddy' -o -name '.factory' -o -name '.junie' -o -name '.iflow' -o -name '.mux' -o -name '.bob' -o -name '.kiro' -o -name '.zencoder' -o -name '.commandcode' -o -name '.roo' -o -name '.kode' -o -name '.qwen' -o -name '.continue' -o -name '.claude' -o -name '.goose' -o -name '.adal' -o -name '.openhands' -o -name '.vibe' \
  \) -prune -exec rm -rf {} +

  rm -rf \
    "$dst/browser-data" \
    "$dst/browser" \
    "$dst/media" \
    "$dst/delivery-queue" \
    "$dst/logs" \
    "$dst/qqbot"

  find "$dst" -type f \( -name '*.sqlite-shm' -o -name '*.sqlite-wal' -o -name '*.tar.gz' \) -delete
}

mkdir -p "$HISTORY"
mkdir -p "$(dirname "$CURRENT")"

copy_config_tree "$SNAP"

rm -rf "$(dirname "$CURRENT")"
mkdir -p "$(dirname "$CURRENT")"
cp -a "$SNAP" "$CURRENT"

mapfile -t old_dirs < <(find "$HISTORY" -mindepth 1 -maxdepth 1 -type d | sort)
if [ "${#old_dirs[@]}" -gt 3 ]; then
  remove_count=$((${#old_dirs[@]} - 3))
  for ((i=0; i<remove_count; i++)); do
    rm -rf "${old_dirs[$i]}"
  done
fi

TMP_REPO=$(mktemp -d "$TMP_PARENT/backup-openclaw.XXXXXX")
cleanup() {
  rm -rf "$TMP_REPO"
}
trap cleanup EXIT

git clone "$REPO_URL" "$TMP_REPO/repo" >/dev/null 2>&1
cd "$TMP_REPO/repo"
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
mkdir -p root/.openclaw
cp -a "$SNAP/." root/.openclaw/

cat > README.md <<'EOF'
# backup-private

这是龙虾（OpenClaw）配置型私有备份仓库。
EOF

cat > .gitignore <<'EOF'
root/.openclaw/browser-data/
root/.openclaw/browser/
root/.openclaw/media/
root/.openclaw/delivery-queue/
root/.openclaw/logs/
root/.openclaw/qqbot/
root/.openclaw/downloads/
root/.openclaw/artifacts/
**/tmp/
**/.git/
**/.openclaw/
**/.agents/
**/state/
**/.clawhub/
**/*.sqlite-shm
**/*.sqlite-wal
EOF

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "Backup OpenClaw config snapshot" >/dev/null
  git push origin main >/dev/null
fi

printf 'LOCAL_CURRENT %s\n' "$CURRENT"
printf 'LOCAL_SNAPSHOT %s\n' "$SNAP"
printf 'LOCAL_HISTORY_COUNT %s\n' "$(find "$HISTORY" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
printf 'REMOTE_COMMIT %s\n' "$(git rev-parse --short HEAD)"
