# SYSTEM-STATE.md

更新时间：2026-04-15 15:33

这个文件记录当前机器上与 OpenClaw 运行直接相关的系统级事实，目的是为了：
- 迁移时少踩坑
- 重装后更快恢复
- 出问题时能快速核对“现在到底跑在什么上面”

---

## 1. 核心路径

- OpenClaw 主目录：`/root/.openclaw`
- Workspace：`/root/.openclaw/workspace`
- 配置文件：`/root/.openclaw/openclaw.json`
- Gateway systemd 用户服务文件：`/root/.config/systemd/user/openclaw-gateway.service`
- 大文件目录：`/www/manmanai/openclaw`
- 备份根目录：`/www/manmanai/openclaw/backup`
- Agent Browser runtime：`/root/.agent-browser/browsers/chrome-147.0.7727.56`

---

## 2. 可执行文件路径

- `node`：`/www/server/nodejs/v24.14.0/bin/node`
- `openclaw`：`/www/server/nodejs/v24.14.0/bin/openclaw`
- `clawhub`：`/www/server/nodejs/v24.14.0/bin/clawhub`
- `agent-browser`：`/www/server/nodejs/v24.14.0/bin/agent-browser`
- `jq`：`/usr/bin/jq`

---

## 3. 版本与运行态

- Node 版本：`v24.14.0`
- Gateway 服务：`openclaw-gateway.service`
- Gateway 当前状态：`active (running)`
- 最近一次核对时间：2026-04-15 15:33
- 当前监听：`127.0.0.1:18789`
- Dashboard：`http://127.0.0.1:18789/`
- 日志文件：`/tmp/openclaw/openclaw-2026-04-15.log`

---

## 4. Gateway 启动命令

当前 systemd 服务中的核心启动命令：

```bash
/www/server/nodejs/v24.14.0/bin/node /www/server/nodejs/v24.14.0/lib/node_modules/openclaw/dist/index.js gateway --port 18789
```

说明：
- 当前 gateway 绑定在 loopback，仅本机可访问。
- 外部通道能力由 OpenClaw 自身插件链路处理，不代表开放公网 dashboard。

---

## 5. 当前 systemd 服务关键环境变量

### 代理
- `http_proxy=http://192.168.50.2:5898`
- `https_proxy=http://192.168.50.2:5898`
- `HTTP_PROXY=http://192.168.50.2:5898`
- `HTTPS_PROXY=http://192.168.50.2:5898`
- `ALL_PROXY=http://192.168.50.2:5898`
- `no_proxy=localhost,127.0.0.1,::1,192.168.0.0/16,192.168.50.100`
- `NO_PROXY=localhost,127.0.0.1,::1,192.168.0.0/16,192.168.50.100`

### 其他关键变量
- `HOME=/root`
- `TMPDIR=/tmp`
- `OPENCLAW_GATEWAY_PORT=18789`
- `OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service`
- `OPENCLAW_SERVICE_KIND=gateway`
- `OPENCLAW_SERVICE_VERSION=2026.4.14`

---

## 6. 当前配置中的关键业务状态

### Telegram
- `channels.telegram.enabled = true`
- `channels.telegram.proxy = http://192.168.50.2:5898`
- `channels.telegram.commands.native = true`
- `channels.telegram.commands.nativeSkills = true`

### 模型
- 已启用 `nvidia` provider
- `models.providers.nvidia.baseUrl = https://integrate.api.nvidia.com/v1`

---

## 7. 当前备份覆盖范围

当前备份已覆盖：
- `openclaw.json`
- `workspace`
- `memory`
- `agents`
- `openclaw-gateway.service`

对应备份位置：
- 配置：`/www/manmanai/openclaw/backup/config/openclaw.json`
- workspace：`/www/manmanai/openclaw/backup/workspace/current`
- memory：`/www/manmanai/openclaw/backup/memory/current`
- agents：`/www/manmanai/openclaw/backup/agents/current`
- systemd 服务文件：`/www/manmanai/openclaw/backup/systemd/openclaw-gateway.service`

最新快照：
- `/www/manmanai/openclaw/backup/snapshots/2026-04-15-152820`

---

## 8. 当前恢复时最值得先核对的项目

如果以后迁移、重装或故障恢复，优先确认：
1. `node` 路径是否仍然存在
2. `openclaw` / `clawhub` 命令是否还在 PATH
3. `/root/.openclaw/openclaw.json` 是否恢复到位
4. `/root/.config/systemd/user/openclaw-gateway.service` 是否恢复到位
5. 代理地址 `http://192.168.50.2:5898` 是否仍可用
6. `127.0.0.1:18789` 是否成功监听
7. Telegram 代理配置与菜单能力是否仍保持启用

---

## 9. 当前仍未纳入系统级备份的东西

还没有单独结构化备份的系统侧信息包括：
- 全局 npm / CLI 安装清单
- 其他 systemd 用户服务或 crontab 自定义项
- 更完整的系统代理依赖链
- 宝塔 / 面板侧与 Node 安装链的外部上下文

后续若要继续提高可恢复性，优先补这几项。
