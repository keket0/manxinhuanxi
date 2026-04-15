#!/usr/bin/env bash
set -euo pipefail

BACKUP_ROOT=${BACKUP_ROOT:-/www/manmanai/openclaw/backup}
SOURCE_ROOT=${SOURCE_ROOT:-/root/.openclaw}
SYSTEMD_SERVICE_FILE=${SYSTEMD_SERVICE_FILE:-/root/.config/systemd/user/openclaw-gateway.service}
TS=$(date +%F-%H%M%S)
SNAPSHOT_DIR="$BACKUP_ROOT/snapshots/$TS"

mkdir -p \
  "$BACKUP_ROOT/config" \
  "$BACKUP_ROOT/workspace" \
  "$BACKUP_ROOT/memory" \
  "$BACKUP_ROOT/agents" \
  "$BACKUP_ROOT/systemd" \
  "$BACKUP_ROOT/snapshots"

copy_dir_current() {
  local src="$1"
  local dest_base="$2"
  local current="$dest_base/current"
  rm -rf "$current"
  mkdir -p "$dest_base"
  if [ -e "$src" ]; then
    cp -a "$src" "$current"
  else
    mkdir -p "$current"
  fi
}

copy_dir_snapshot() {
  local src="$1"
  local dest_dir="$2"
  if [ -e "$src" ]; then
    cp -a "$src" "$dest_dir/"
  fi
}

cp -a "$SOURCE_ROOT/openclaw.json" "$BACKUP_ROOT/config/openclaw.json"
copy_dir_current "$SOURCE_ROOT/workspace" "$BACKUP_ROOT/workspace"
copy_dir_current "$SOURCE_ROOT/memory" "$BACKUP_ROOT/memory"
copy_dir_current "$SOURCE_ROOT/agents" "$BACKUP_ROOT/agents"
if [ -e "$SYSTEMD_SERVICE_FILE" ]; then
  cp -a "$SYSTEMD_SERVICE_FILE" "$BACKUP_ROOT/systemd/openclaw-gateway.service"
fi

mkdir -p "$SNAPSHOT_DIR"
cp -a "$SOURCE_ROOT/openclaw.json" "$SNAPSHOT_DIR/"
copy_dir_snapshot "$SOURCE_ROOT/workspace" "$SNAPSHOT_DIR"
copy_dir_snapshot "$SOURCE_ROOT/memory" "$SNAPSHOT_DIR"
copy_dir_snapshot "$SOURCE_ROOT/agents" "$SNAPSHOT_DIR"
if [ -e "$SYSTEMD_SERVICE_FILE" ]; then
  cp -a "$SYSTEMD_SERVICE_FILE" "$SNAPSHOT_DIR/openclaw-gateway.service"
fi

echo "Backup completed"
echo "BACKUP_ROOT=$BACKUP_ROOT"
echo "SNAPSHOT_DIR=$SNAPSHOT_DIR"
du -sh \
  "$BACKUP_ROOT/config/openclaw.json" \
  "$BACKUP_ROOT/workspace/current" \
  "$BACKUP_ROOT/memory/current" \
  "$BACKUP_ROOT/agents/current" \
  "$BACKUP_ROOT/systemd/openclaw-gateway.service" \
  "$SNAPSHOT_DIR"
