#!/usr/bin/env bash
set -u

PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

EXPECTED_OPENCLAW_HOME=${EXPECTED_OPENCLAW_HOME:-/root/.openclaw}
EXPECTED_SYSTEMD_DIR=${EXPECTED_SYSTEMD_DIR:-/root/.config/systemd/user}
EXPECTED_BACKUP_ROOT=${EXPECTED_BACKUP_ROOT:-/www/manmanai/openclaw/backup}
EXPECTED_PROXY=${EXPECTED_PROXY:-http://192.168.50.2:5898}

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  printf '[PASS] %s\n' "$*"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  printf '[WARN] %s\n' "$*"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  printf '[FAIL] %s\n' "$*"
}

check_cmd() {
  local name="$1"
  local required="${2:-required}"
  local actual
  actual=$(command -v "$name" 2>/dev/null || true)
  if [ -n "$actual" ]; then
    pass "$name 可用: $actual"
  else
    if [ "$required" = "required" ]; then
      fail "缺少命令: $name"
    else
      warn "缺少建议命令: $name"
    fi
  fi
}

check_dir_parent_writable() {
  local p="$1"
  local parent
  parent=$(dirname "$p")
  if [ -d "$p" ]; then
    pass "目录已存在: $p"
    return
  fi
  if [ -d "$parent" ] && [ -w "$parent" ]; then
    pass "可创建目标目录: $p"
  else
    warn "目标目录当前不存在，且父目录不可写或不存在: $p"
  fi
}

check_linux() {
  if [ "$(uname -s 2>/dev/null || true)" = "Linux" ]; then
    pass "系统为 Linux"
  else
    fail "当前不是 Linux，无法按现有迁移文档直接复用"
  fi
}

check_root_user() {
  local user
  user=$(id -un 2>/dev/null || true)
  if [ "$user" = "root" ]; then
    pass "当前用户为 root，与现有路径基线一致"
  else
    warn "当前用户不是 root（当前为 $user），需自行调整 /root 路径基线"
  fi
}

check_systemd_user() {
  if ! command -v systemctl >/dev/null 2>&1; then
    fail "缺少 systemctl"
    return
  fi
  if systemctl --user status >/dev/null 2>&1; then
    pass "systemctl --user 可用"
  else
    warn "systemctl 存在，但 systemctl --user 当前不可用，后续可能需要正确登录 session / linger"
  fi
}

check_node_version() {
  if ! command -v node >/dev/null 2>&1; then
    fail "缺少 node，无法继续检查版本"
    return
  fi
  local version
  version=$(node -v 2>/dev/null || true)
  if [ -n "$version" ]; then
    pass "Node 版本: $version"
  else
    warn "node 存在，但无法读取版本"
  fi
}

check_proxy_reachability() {
  if ! command -v curl >/dev/null 2>&1; then
    warn "缺少 curl，跳过代理可达性检查"
    return
  fi
  if curl -x "$EXPECTED_PROXY" -I -sS --max-time 8 https://api.telegram.org >/dev/null 2>&1; then
    pass "参考代理可达: $EXPECTED_PROXY"
  else
    warn "参考代理当前不可达: $EXPECTED_PROXY，新机器若使用相同代理需人工确认"
  fi
}

check_backup_root_hint() {
  if [ -d "$EXPECTED_BACKUP_ROOT" ]; then
    pass "发现备份根目录: $EXPECTED_BACKUP_ROOT"
  else
    warn "未发现备份根目录: $EXPECTED_BACKUP_ROOT，如在新机器恢复前需先拷入备份"
  fi
}

print_install_hints() {
  cat <<'EOF'

== 建议安装目标 ==
必装：
- node
- openclaw
- systemctl（通常随 systemd）

强烈建议：
- clawhub
- jq
- agent-browser

辅助增强：
- git
- python3
- curl

== 推荐流程 ==
1. 先让本脚本尽量达到“无 FAIL”。
2. 再准备 backup/、RESTORE.md、SYSTEM-STATE.md、MIGRATION.md、CLI-INVENTORY.md。
3. 再运行 scripts/check-migration-prereqs.sh。
4. 最后按需执行 scripts/migrate-openclaw-from-backup.sh。
EOF
}

printf '== New machine readiness check for OpenClaw migration ==\n\n'

printf '## 一、系统基础\n'
check_linux
check_root_user
check_cmd bash required
check_cmd systemctl required
check_systemd_user

printf '\n## 二、核心命令\n'
check_cmd node required
check_node_version
check_cmd openclaw required
check_cmd npm optional
check_cmd npx optional

printf '\n## 三、建议命令\n'
check_cmd clawhub optional
check_cmd jq optional
check_cmd agent-browser optional
check_cmd git optional
check_cmd python3 optional
check_cmd curl optional

printf '\n## 四、目录与路径\n'
check_dir_parent_writable "$EXPECTED_OPENCLAW_HOME"
check_dir_parent_writable "$EXPECTED_SYSTEMD_DIR"
check_backup_root_hint

printf '\n## 五、网络与恢复条件\n'
check_proxy_reachability

printf '\n== 汇总 ==\n'
printf 'PASS=%s WARN=%s FAIL=%s\n' "$PASS_COUNT" "$WARN_COUNT" "$FAIL_COUNT"

if [ "$FAIL_COUNT" -gt 0 ]; then
  printf '结论：新机器当前还不满足最小迁移前置条件，先补 FAIL。\n'
else
  if [ "$WARN_COUNT" -gt 0 ]; then
    printf '结论：新机器基本可继续准备迁移，但仍有兼容性风险，建议先处理 WARN。\n'
  else
    printf '结论：新机器准备度良好，可进入恢复与迁移步骤。\n'
  fi
fi

print_install_hints

exit 0
