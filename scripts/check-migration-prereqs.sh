#!/usr/bin/env bash
set -u

EXPECTED_NODE_PATH="/www/server/nodejs/v24.14.0/bin/node"
EXPECTED_OPENCLAW_BIN="/www/server/nodejs/v24.14.0/bin/openclaw"
EXPECTED_CLAWHUB_BIN="/www/server/nodejs/v24.14.0/bin/clawhub"
EXPECTED_AGENT_BROWSER_BIN="/www/server/nodejs/v24.14.0/bin/agent-browser"
EXPECTED_JQ_BIN="/usr/bin/jq"
EXPECTED_SERVICE_FILE="/root/.config/systemd/user/openclaw-gateway.service"
EXPECTED_CONFIG_FILE="/root/.openclaw/openclaw.json"
EXPECTED_PROXY="http://192.168.50.2:5898"
EXPECTED_GATEWAY_PORT="18789"

PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

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
  local expected="${2:-}"
  local required="${3:-required}"
  local actual
  actual=$(command -v "$name" 2>/dev/null || true)
  if [ -z "$actual" ]; then
    if [ "$required" = "required" ]; then
      fail "缺少命令: $name"
    else
      warn "缺少建议命令: $name"
    fi
    return
  fi

  if [ -n "$expected" ] && [ "$actual" != "$expected" ]; then
    warn "$name 存在，但路径与当前机器不同: $actual (期望参考: $expected)"
  else
    pass "$name 可用: $actual"
  fi
}

check_file() {
  local path="$1"
  local required="${2:-required}"
  if [ -e "$path" ]; then
    pass "文件存在: $path"
  else
    if [ "$required" = "required" ]; then
      fail "缺少文件: $path"
    else
      warn "文件不存在: $path"
    fi
  fi
}

check_systemctl_user() {
  if ! command -v systemctl >/dev/null 2>&1; then
    fail "缺少 systemctl，无法复用当前 systemd 用户服务模型"
    return
  fi

  if systemctl --user status >/dev/null 2>&1; then
    pass "systemctl --user 可用"
  else
    warn "systemctl 存在，但 systemctl --user 当前不可用，可能需要用户 session / linger / 正确登录环境"
  fi
}

check_service_execstart() {
  if [ ! -f "$EXPECTED_SERVICE_FILE" ]; then
    fail "缺少 service 文件，无法检查 ExecStart"
    return
  fi

  local exec_line
  exec_line=$(grep -E '^ExecStart=' "$EXPECTED_SERVICE_FILE" 2>/dev/null || true)
  if [ -z "$exec_line" ]; then
    fail "service 文件中未找到 ExecStart"
    return
  fi

  pass "service 文件中存在 ExecStart"

  if printf '%s' "$exec_line" | grep -F "$EXPECTED_NODE_PATH" >/dev/null 2>&1; then
    pass "ExecStart 仍指向当前机器参考 Node 路径"
  else
    warn "ExecStart 未指向当前机器参考 Node 路径，迁移后可能需要手动修改"
  fi

  if printf '%s' "$exec_line" | grep -F 'openclaw/dist/index.js gateway --port 18789' >/dev/null 2>&1; then
    pass "ExecStart 包含 OpenClaw gateway 启动命令"
  else
    warn "ExecStart 与当前参考启动命令不完全一致，建议人工复核"
  fi
}

check_proxy_in_config() {
  if [ ! -f "$EXPECTED_CONFIG_FILE" ]; then
    fail "缺少配置文件，无法检查 Telegram 代理"
    return
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    warn "缺少 python3，跳过配置内容检查"
    return
  fi

  local output
  output=$(python3 - <<'PY'
import json
p='/root/.openclaw/openclaw.json'
try:
    with open(p,'r',encoding='utf-8') as f:
        data=json.load(f)
    tg=((data.get('channels') or {}).get('telegram') or {})
    print('enabled=%s' % tg.get('enabled'))
    print('proxy=%s' % tg.get('proxy'))
    cmds=tg.get('commands') or {}
    print('native=%s' % cmds.get('native'))
    print('nativeSkills=%s' % cmds.get('nativeSkills'))
except Exception as e:
    print('error=%s' % e)
PY
)

  if printf '%s' "$output" | grep -F 'error=' >/dev/null 2>&1; then
    warn "配置文件读取失败: $output"
    return
  fi

  if printf '%s' "$output" | grep -F 'enabled=True' >/dev/null 2>&1; then
    pass "Telegram 通道已启用"
  else
    warn "Telegram 通道未明确启用"
  fi

  if printf '%s' "$output" | grep -F "proxy=$EXPECTED_PROXY" >/dev/null 2>&1; then
    pass "Telegram 代理与当前参考一致"
  else
    warn "Telegram 代理与当前参考不一致，需人工确认"
  fi

  if printf '%s' "$output" | grep -F 'native=True' >/dev/null 2>&1; then
    pass "Telegram 原生命令菜单已启用"
  else
    warn "Telegram 原生命令菜单未明确启用"
  fi

  if printf '%s' "$output" | grep -F 'nativeSkills=True' >/dev/null 2>&1; then
    pass "Telegram nativeSkills 已启用"
  else
    warn "Telegram nativeSkills 未明确启用"
  fi
}

check_gateway_port() {
  if command -v ss >/dev/null 2>&1; then
    if ss -ltn 2>/dev/null | grep -F ":$EXPECTED_GATEWAY_PORT " >/dev/null 2>&1; then
      pass "检测到监听端口 :$EXPECTED_GATEWAY_PORT"
    else
      warn "当前未检测到监听端口 :$EXPECTED_GATEWAY_PORT，若这是新机器迁移前状态可忽略"
    fi
  else
    warn "缺少 ss，跳过监听端口检查"
  fi
}

printf '== OpenClaw migration prereq check ==\n'
printf '参考基线来自当前工作区文档：SYSTEM-STATE.md / MIGRATION.md / CLI-INVENTORY.md\n\n'

printf '## 一、必装命令\n'
check_cmd node "$EXPECTED_NODE_PATH" required
check_cmd openclaw "$EXPECTED_OPENCLAW_BIN" required
check_cmd systemctl /usr/bin/systemctl required

printf '\n## 二、建议命令\n'
check_cmd clawhub "$EXPECTED_CLAWHUB_BIN" optional
check_cmd agent-browser "$EXPECTED_AGENT_BROWSER_BIN" optional
check_cmd jq "$EXPECTED_JQ_BIN" optional
check_cmd git /usr/bin/git optional
check_cmd python3 /usr/bin/python3 optional
check_cmd curl /usr/bin/curl optional

printf '\n## 三、文件与 systemd\n'
check_file "$EXPECTED_CONFIG_FILE" required
check_file "$EXPECTED_SERVICE_FILE" required
check_systemctl_user
check_service_execstart

printf '\n## 四、配置与运行态\n'
check_proxy_in_config
check_gateway_port

printf '\n== 汇总 ==\n'
printf 'PASS=%s WARN=%s FAIL=%s\n' "$PASS_COUNT" "$WARN_COUNT" "$FAIL_COUNT"

if [ "$FAIL_COUNT" -gt 0 ]; then
  printf '结论：当前不满足“接近原机状态迁移”的最小前置条件，先修 FAIL。\n'
  exit 1
fi

if [ "$WARN_COUNT" -gt 0 ]; then
  printf '结论：可继续迁移，但有兼容性风险，建议先处理 WARN。\n'
  exit 0
fi

printf '结论：前置条件良好，可按 MIGRATION.md 继续执行。\n'
exit 0
