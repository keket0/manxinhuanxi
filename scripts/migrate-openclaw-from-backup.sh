#!/usr/bin/env bash
set -euo pipefail

BACKUP_ROOT=${BACKUP_ROOT:-/www/manmanai/openclaw/backup}
TARGET_OPENCLAW_HOME=${TARGET_OPENCLAW_HOME:-/root/.openclaw}
TARGET_SYSTEMD_DIR=${TARGET_SYSTEMD_DIR:-/root/.config/systemd/user}
SERVICE_NAME=${SERVICE_NAME:-openclaw-gateway.service}
TS=$(date +%F-%H%M%S)
PRE_RESTORE_BACKUP_ROOT=${PRE_RESTORE_BACKUP_ROOT:-/tmp/openclaw-pre-restore-$TS}
MODE=current
SNAPSHOT_NAME=
APPLY=0
RESTART_SERVICE=0
SKIP_AGENTS=0
ONLY_ITEMS=

usage() {
  cat <<'EOF'
Usage:
  migrate-openclaw-from-backup.sh [options]

Options:
  --apply                 真正执行恢复。默认仅 dry-run 预览。
  --restart-service       恢复完成后执行 systemctl --user daemon-reload + restart。
  --current               使用 current 副本（默认）。
  --latest-snapshot       使用 snapshots 下最新快照。
  --snapshot NAME         使用指定快照名，例如 2026-04-15-152820。
  --skip-agents           跳过 agents 目录恢复。
  --only ITEMS            只恢复指定内容，逗号分隔。
                           可选：config,workspace,memory,agents,service,skills
  --backup-root PATH      指定备份根目录，默认 /www/manmanai/openclaw/backup。
  --target-home PATH      指定目标 OpenClaw 主目录，默认 /root/.openclaw。
  --target-systemd PATH   指定目标 systemd 用户目录，默认 /root/.config/systemd/user。
  -h, --help              显示帮助。

Examples:
  bash scripts/migrate-openclaw-from-backup.sh --current
  bash scripts/migrate-openclaw-from-backup.sh --latest-snapshot --apply
  bash scripts/migrate-openclaw-from-backup.sh --snapshot 2026-04-15-152820 --apply --restart-service

Notes:
  1. 默认只打印将要执行的动作，不实际写入。
  2. 执行前会把目标侧现有文件移动到 PRE_RESTORE_BACKUP_ROOT 里做现场备份。
  3. 该脚本不会安装 Node / OpenClaw / clawhub / agent-browser，本机基础环境需自行准备。
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --restart-service) RESTART_SERVICE=1 ;;
    --current) MODE=current ;;
    --latest-snapshot) MODE=latest-snapshot ;;
    --snapshot)
      MODE=snapshot
      SNAPSHOT_NAME="${2:-}"
      shift
      ;;
    --skip-agents) SKIP_AGENTS=1 ;;
    --only)
      ONLY_ITEMS="${2:-}"
      shift
      ;;
    --backup-root)
      BACKUP_ROOT="${2:-}"
      shift
      ;;
    --target-home)
      TARGET_OPENCLAW_HOME="${2:-}"
      shift
      ;;
    --target-systemd)
      TARGET_SYSTEMD_DIR="${2:-}"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [ "$MODE" = "snapshot" ] && [ -z "$SNAPSHOT_NAME" ]; then
  echo "--snapshot 需要提供快照名" >&2
  exit 2
fi

resolve_source_root() {
  case "$MODE" in
    current)
      printf '%s\n' "$BACKUP_ROOT"
      ;;
    latest-snapshot)
      local latest
      latest=$(find "$BACKUP_ROOT/snapshots" -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\n' | sort -n | tail -n 1 | cut -d' ' -f2-)
      if [ -z "$latest" ]; then
        echo "未找到任何 snapshot" >&2
        exit 1
      fi
      printf '%s\n' "$latest"
      ;;
    snapshot)
      local snapshot_dir="$BACKUP_ROOT/snapshots/$SNAPSHOT_NAME"
      if [ ! -d "$snapshot_dir" ]; then
        echo "指定快照不存在: $snapshot_dir" >&2
        exit 1
      fi
      printf '%s\n' "$snapshot_dir"
      ;;
    *)
      echo "未知模式: $MODE" >&2
      exit 2
      ;;
  esac
}

SOURCE_ROOT=$(resolve_source_root)

if [ "$MODE" = "current" ]; then
  SRC_CONFIG="$SOURCE_ROOT/config/openclaw.json"
  SRC_WORKSPACE="$SOURCE_ROOT/workspace/current"
  SRC_MEMORY="$SOURCE_ROOT/memory/current"
  SRC_AGENTS="$SOURCE_ROOT/agents/current"
  SRC_SERVICE="$SOURCE_ROOT/systemd/$SERVICE_NAME"
else
  SRC_CONFIG="$SOURCE_ROOT/openclaw.json"
  SRC_WORKSPACE="$SOURCE_ROOT/workspace"
  SRC_MEMORY="$SOURCE_ROOT/memory"
  SRC_AGENTS="$SOURCE_ROOT/agents"
  SRC_SERVICE="$SOURCE_ROOT/$SERVICE_NAME"
fi

DST_CONFIG="$TARGET_OPENCLAW_HOME/openclaw.json"
DST_WORKSPACE="$TARGET_OPENCLAW_HOME/workspace"
DST_MEMORY="$TARGET_OPENCLAW_HOME/memory"
DST_AGENTS="$TARGET_OPENCLAW_HOME/agents"
DST_SERVICE="$TARGET_SYSTEMD_DIR/$SERVICE_NAME"

say() {
  printf '%s\n' "$*"
}

need_path() {
  local p="$1"
  if [ ! -e "$p" ]; then
    echo "缺少恢复源: $p" >&2
    exit 1
  fi
}

run() {
  if [ "$APPLY" -eq 1 ]; then
    eval "$@"
  else
    printf '[DRY-RUN] %s\n' "$*"
  fi
}

want_item() {
  local item="$1"
  if [ -z "$ONLY_ITEMS" ]; then
    return 0
  fi
  case ",$ONLY_ITEMS," in
    *",$item,"*) return 0 ;;
    *) return 1 ;;
  esac
}

backup_existing() {
  local src="$1"
  local dest_backup="$2"
  if [ -e "$src" ] || [ -L "$src" ]; then
    run "mkdir -p \"$(dirname "$dest_backup")\""
    run "mv \"$src\" \"$dest_backup\""
  fi
}

restore_file() {
  local src="$1"
  local dst="$2"
  local backup_dst="$3"
  backup_existing "$dst" "$backup_dst"
  run "mkdir -p \"$(dirname "$dst")\""
  run "cp -a \"$src\" \"$dst\""
}

restore_dir() {
  local src="$1"
  local dst="$2"
  local backup_dst="$3"
  backup_existing "$dst" "$backup_dst"
  run "mkdir -p \"$(dirname "$dst")\""
  run "cp -a \"$src\" \"$dst\""
}

restore_subdir() {
  local src="$1"
  local dst="$2"
  local backup_dst="$3"
  backup_existing "$dst" "$backup_dst"
  run "mkdir -p \"$(dirname "$dst")\""
  run "cp -a \"$src\" \"$dst\""
}

if want_item config; then need_path "$SRC_CONFIG"; fi
if want_item workspace || want_item skills; then need_path "$SRC_WORKSPACE"; fi
if want_item memory; then need_path "$SRC_MEMORY"; fi
if want_item service; then need_path "$SRC_SERVICE"; fi
if want_item agents && [ "$SKIP_AGENTS" -ne 1 ]; then need_path "$SRC_AGENTS"; fi

say "== OpenClaw migration restore helper =="
say "MODE=$MODE"
say "SOURCE_ROOT=$SOURCE_ROOT"
say "TARGET_OPENCLAW_HOME=$TARGET_OPENCLAW_HOME"
say "TARGET_SYSTEMD_DIR=$TARGET_SYSTEMD_DIR"
say "PRE_RESTORE_BACKUP_ROOT=$PRE_RESTORE_BACKUP_ROOT"
say "APPLY=$APPLY"
say "RESTART_SERVICE=$RESTART_SERVICE"
say "SKIP_AGENTS=$SKIP_AGENTS"
say "ONLY_ITEMS=${ONLY_ITEMS:-all}"
say ""

if want_item config; then
  restore_file "$SRC_CONFIG" "$DST_CONFIG" "$PRE_RESTORE_BACKUP_ROOT/openclaw/openclaw.json"
else
  say "[SKIP] 跳过 config 恢复"
fi

if want_item skills; then
  if [ ! -d "$SRC_WORKSPACE/skills" ]; then
    echo "缺少 skills 恢复源: $SRC_WORKSPACE/skills" >&2
    exit 1
  fi
  restore_subdir "$SRC_WORKSPACE/skills" "$DST_WORKSPACE/skills" "$PRE_RESTORE_BACKUP_ROOT/openclaw/workspace-skills"
else
  if want_item workspace; then
    restore_dir "$SRC_WORKSPACE" "$DST_WORKSPACE" "$PRE_RESTORE_BACKUP_ROOT/openclaw/workspace"
  else
    say "[SKIP] 跳过 workspace 恢复"
  fi
fi

if want_item memory; then
  restore_dir "$SRC_MEMORY" "$DST_MEMORY" "$PRE_RESTORE_BACKUP_ROOT/openclaw/memory"
else
  say "[SKIP] 跳过 memory 恢复"
fi

if want_item agents; then
  if [ "$SKIP_AGENTS" -ne 1 ]; then
    restore_dir "$SRC_AGENTS" "$DST_AGENTS" "$PRE_RESTORE_BACKUP_ROOT/openclaw/agents"
  else
    say "[SKIP] 已请求跳过 agents 恢复"
  fi
else
  say "[SKIP] 跳过 agents 恢复"
fi

if want_item service; then
  restore_file "$SRC_SERVICE" "$DST_SERVICE" "$PRE_RESTORE_BACKUP_ROOT/systemd/$SERVICE_NAME"
else
  say "[SKIP] 跳过 service 恢复"
fi

if [ "$RESTART_SERVICE" -eq 1 ]; then
  run "systemctl --user daemon-reload"
  run "systemctl --user enable $SERVICE_NAME"
  run "systemctl --user restart $SERVICE_NAME"
  run "systemctl --user status $SERVICE_NAME --no-pager | sed -n '1,12p'"
  run "openclaw gateway status"
else
  say "[INFO] 未请求自动重启服务，如需执行请追加 --restart-service"
fi

say ""
if [ "$APPLY" -eq 1 ]; then
  say "恢复已执行。"
  say "现场旧文件备份目录: $PRE_RESTORE_BACKUP_ROOT"
  say "建议下一步: 运行 scripts/check-migration-prereqs.sh，并人工核对 service 的 ExecStart / 代理 / PATH。"
else
  say "当前为 dry-run，仅预览动作。"
  say "确认无误后可追加 --apply；若还要自动重载服务，再追加 --restart-service。"
fi
