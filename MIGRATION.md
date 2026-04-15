# MIGRATION.md

更新时间：2026-04-15 15:41

这份文档用于把当前这套 OpenClaw 从一台机器迁移到另一台机器。

目标不是“理论可迁移”，而是尽量做到：
- 知道先装什么
- 知道要拷哪些文件
- 知道恢复后怎么验活
- 知道最容易卡在哪

---

## 1. 当前结论

当前这套环境已经具备**跨机器恢复大部分核心状态**的能力，但还不是完整系统镜像。

### 目前能迁走的
- OpenClaw 主配置
- workspace
- memory
- agents
- gateway 的 systemd 用户服务文件

### 目前不能自动迁走的
- 操作系统本身
- Node / npm 环境
- OpenClaw 程序本体安装
- `clawhub` / `agent-browser` 等全局 CLI 安装
- 新机器上的网络与代理可达性

所以它更准确地说是：

## 当前迁移能力 = 配置 + 数据 + 服务定义迁移

不是：

## 整机环境一键克隆

---

## 2. 迁移前提

新机器建议满足：
- Linux
- 支持 systemd 用户服务
- 有 root 用户环境，或至少有与当前路径兼容的运行用户
- 能安装 Node
- 能安装 OpenClaw

如果新机器路径完全不同，恢复后要手动调整 service 文件与 PATH。

---

## 3. 迁移前先准备什么

### 旧机器上准备好这几类东西
1. 最新备份快照
2. 当前副本备份目录
3. `SYSTEM-STATE.md`
4. `RESTORE.md`
5. 本文件 `MIGRATION.md`

### 当前关键来源
- 备份根目录：`/www/manmanai/openclaw/backup`
- 系统状态文档：`/root/.openclaw/workspace/SYSTEM-STATE.md`
- 恢复文档：`/root/.openclaw/workspace/RESTORE.md`
- CLI 清单：`/root/.openclaw/workspace/CLI-INVENTORY.md`
- 新机器准备检查脚本：`/root/.openclaw/workspace/scripts/check-new-machine-readiness.sh`
- 迁移前置检查脚本：`/root/.openclaw/workspace/scripts/check-migration-prereqs.sh`
- 半自动迁移脚本：`/root/.openclaw/workspace/scripts/migrate-openclaw-from-backup.sh`

---

## 4. 新机器先安装什么

迁移前，新机器至少先补这些基础能力：

### 必装
- Node
- OpenClaw
- systemd 用户服务能力

### 建议装
- `clawhub`
- `jq`
- `agent-browser`（如果后续要继续用浏览器线）

### 至少确认命令存在
- `node`
- `openclaw`
- `systemctl --user`

---

## 5. 需要迁移过去的核心文件

### 1. 配置
来源：
- `/www/manmanai/openclaw/backup/config/openclaw.json`

目标：
- `/root/.openclaw/openclaw.json`

### 2. workspace
来源：
- `/www/manmanai/openclaw/backup/workspace/current`

目标：
- `/root/.openclaw/workspace`

### 3. memory
来源：
- `/www/manmanai/openclaw/backup/memory/current`

目标：
- `/root/.openclaw/memory`

### 4. agents
来源：
- `/www/manmanai/openclaw/backup/agents/current`

目标：
- `/root/.openclaw/agents`

### 5. systemd 用户服务文件
来源：
- `/www/manmanai/openclaw/backup/systemd/openclaw-gateway.service`

目标：
- `/root/.config/systemd/user/openclaw-gateway.service`

---

## 6. 推荐迁移顺序

### 第一步，先装环境
先在新机器安装：
- Node
- OpenClaw
- 必要全局 CLI

建议先运行新机器准备检查脚本：

```bash
bash /root/.openclaw/workspace/scripts/check-new-machine-readiness.sh
```

通过后，再运行迁移前置检查脚本（在目标机器按需调整路径基线后使用）：

```bash
bash /root/.openclaw/workspace/scripts/check-migration-prereqs.sh
```

### 第二步，恢复核心文件
按顺序恢复：
1. `openclaw.json`
2. `workspace`
3. `memory`
4. `agents`
5. `openclaw-gateway.service`

也可以直接用半自动迁移脚本：

```bash
bash /root/.openclaw/workspace/scripts/migrate-openclaw-from-backup.sh --latest-snapshot
bash /root/.openclaw/workspace/scripts/migrate-openclaw-from-backup.sh --latest-snapshot --apply
bash /root/.openclaw/workspace/scripts/migrate-openclaw-from-backup.sh --latest-snapshot --apply --restart-service
```

如果只想选择性恢复一部分内容，也可以这样：

```bash
# 只恢复配置
bash /root/.openclaw/workspace/scripts/migrate-openclaw-from-backup.sh --latest-snapshot --only config

# 只恢复记忆
bash /root/.openclaw/workspace/scripts/migrate-openclaw-from-backup.sh --latest-snapshot --only memory

# 只恢复技能目录（workspace/skills）
bash /root/.openclaw/workspace/scripts/migrate-openclaw-from-backup.sh --latest-snapshot --only skills

# 同时恢复配置 + 记忆 + systemd 服务文件
bash /root/.openclaw/workspace/scripts/migrate-openclaw-from-backup.sh --latest-snapshot --only config,memory,service
```

说明：
- 默认是 dry-run，只预览，不写入。
- `--apply` 才会真正覆盖恢复。
- `--only` 支持：`config,workspace,memory,agents,service,skills`
- `skills` 只恢复 `workspace/skills`，不会覆盖整个 workspace。
- 执行前会把目标机当前文件先移动到临时目录做现场备份。
- `--restart-service` 会执行 `systemctl --user daemon-reload`、`enable`、`restart` 与状态检查。

### 第三步，检查路径兼容性
重点看：
- Node 路径是否还是 `/www/server/nodejs/v24.14.0/bin/node`
- OpenClaw 安装路径是否还是当前路径
- `openclaw-gateway.service` 里的 `ExecStart` 是否需要修改
- PATH 是否包含 `openclaw`、`clawhub`、`agent-browser`

### 第四步，重载并启动服务
一般需要做：
1. `systemctl --user daemon-reload`
2. `systemctl --user enable openclaw-gateway`
3. `systemctl --user restart openclaw-gateway`

### 第五步，验活
至少检查：
- `openclaw gateway status`
- `127.0.0.1:18789` 是否监听
- dashboard 是否打开
- Telegram 是否在线
- 菜单是否正常

---

## 7. 最容易出问题的地方

### 1. Node 路径不一样
当前机器的 Node 路径是：
- `/www/server/nodejs/v24.14.0/bin/node`

如果新机器不同，必须改：
- `/root/.config/systemd/user/openclaw-gateway.service`
里的 `ExecStart`

### 2. OpenClaw 安装路径不一样
当前服务实际执行的是：
- `/www/server/nodejs/v24.14.0/lib/node_modules/openclaw/dist/index.js`

如果新机器的 OpenClaw 不在这个位置，也要改 service 文件。

### 3. 代理不可用
当前关键代理是：
- `http://192.168.50.2:5898`

新机器上如果这地址不可达，Telegram 与外部请求链路可能出问题。

### 4. 外部 CLI 没装
例如：
- `clawhub`
- `agent-browser`
- `jq`

这些没装会影响技能安装、浏览器线、部分脚本验证。

### 5. systemd 用户环境不同
如果新机器没有对应用户环境、用户 session、或 `systemctl --user` 不可用，就不能直接照搬当前服务方式。

---

## 8. 迁移后优先检查的业务点

### Telegram
检查：
- 代理是否仍可用
- `channels.telegram.proxy` 是否仍保留
- 菜单是否正常
- 图片接收是否正常

### 模型
检查：
- `nvidia` provider 是否仍存在
- API key 是否还在配置里
- `/models` 页面是否能看到模型

### 技能
检查：
- workspace 下 skill 目录是否齐全
- 主力技能是否还能用
- 外部依赖型技能是否缺 CLI / runtime

### 记忆
检查：
- `MEMORY.md`
- `PROJECTS.md`
- `SESSION-STATE.md`
- `memory/YYYY-MM-DD.md`

---

## 9. 建议的最小迁移核对清单

迁移完成后，逐项确认：

- [ ] `node -v` 正常
- [ ] `openclaw` 命令存在
- [ ] `/root/.openclaw/openclaw.json` 已恢复
- [ ] `/root/.openclaw/workspace` 已恢复
- [ ] `/root/.openclaw/memory` 已恢复
- [ ] `/root/.openclaw/agents` 已恢复
- [ ] `/root/.config/systemd/user/openclaw-gateway.service` 已恢复
- [ ] service 文件里的 `ExecStart` 路径可用
- [ ] `systemctl --user daemon-reload` 成功
- [ ] `openclaw-gateway` 能启动
- [ ] `127.0.0.1:18789` 在监听
- [ ] Telegram 在线
- [ ] 代理可用

---

## 10. 当前最推荐的迁移资料包

如果以后真要迁机器，最值得一起带走的是：
- `/www/manmanai/openclaw/backup`
- `/root/.openclaw/workspace/RESTORE.md`
- `/root/.openclaw/workspace/SYSTEM-STATE.md`
- `/root/.openclaw/workspace/MIGRATION.md`
- `/root/.openclaw/workspace/CLI-INVENTORY.md`
- `/root/.openclaw/workspace/scripts/check-new-machine-readiness.sh`
- `/root/.openclaw/workspace/scripts/check-migration-prereqs.sh`
- `/root/.openclaw/workspace/scripts/migrate-openclaw-from-backup.sh`

这样新机器上不会只有“备份文件”，还会有：
- 恢复说明
- 当前系统状态说明
- 跨机器迁移说明

---

## 11. 后续还能怎么继续增强

如果要把迁移能力继续提高，下一步建议补：
- 更完整的 systemd / crontab 自定义项清单
- 一份针对新机器环境的安装前置脚本

做到这一步，跨机器恢复会更接近可重复执行，而不只是“手工迁移可行”。
