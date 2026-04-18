# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## 影视接口代号

- `pg分享` → `/www/manmanai/PG/jsm🧿.json`
- `pg自用` → `/www/manmanai/pg_zy/jsm🧿.json`
- `不夜自用` → `/www/manmanai/pg_zy/buyezy🧿.json`
- `不夜分享` → `/www/manmanai/pg_zy/buyegg🧿.json`
- `不夜影视组` → `/www/manmanai/buye/vod/routes/影视`

备注：
- 后续如果主人说“修改 pg分享 / pg自用 / 不夜自用 / 不夜分享”，默认就是改上面对应文件，不再重复确认路径。
- 后续如果主人说推送到“`不夜影视组`”，默认就是推送到 `/www/manmanai/buye/vod/routes/影视`。
- 这几份文件里含有敏感字段（如 token、cookie、账号类配置等），后续修改时不主动回显敏感值。
- `不夜影视接口` 当前地址已更新为新的 token 版本，后续按最新代号值理解。
- 但如果只是去影视接口“找源”，默认仍使用源 token `123456`，不要误改成代号地址里的 `1992353`。
- 如果要实际编辑到 `不夜分享` 或 `不夜自用`，写回文件时也应使用 `123456`，不要继续沿用原有的 `1992353`。
- 结构上都属于影视源配置 JSON，核心是 `spider`、`logo` / `wallpaper`、`sites` 列表，以及每个站点下的 `key`、`name`、`type`、`api`、`searchable`、`quickSearch`、`changeable`、`ext/header` 等字段。
- 修改不夜专用 JS 的默认发布流程：先自行做语法检查，语法通过后先给主人一份 JS 下载，再询问是否推送到 `不夜影视组`；若有同名文件，或 JS 中 `key` 与目标目录内现有文件冲突，先自动移动到 `/www/manmanai/buye/Cache` 备份；推送成功后重启 `vod` 容器并检查是否成功启动；仅在启动成功后删除这次移动到 Cache 的备份文件。

## Local Skills (workspace)

- weather
- Agent Browser
- claw-ds-generator
- cn-ecommerce-search
- duckduckgo-search
- find-skills
- openai-tts
- proactive-agent
- self-improvement
- tavily-search

## 影视接口代号路径

- pg分享 → `/www/manmanai/PG/jsm🧿.json`
- pg自用 → `/www/manmanai/pg_zy/jsm🧿.json`
- 不夜自用 → `/www/manmanai/pg_zy/buyezy🧿.json`
- 不夜分享 → `/www/manmanai/pg_zy/buyegg🧿.json`

用户之后可以只报代号，我应直接按对应路径修改或同步，不再要求重复提供路径。

### SSH

- openwrt → `192.168.50.2:22`, user: `root`

### 代理速用

- 代理地址：`http://192.168.50.2:5898`
- 单次带代理：`withproxy <命令>`
- 强制不用代理：`noproxy <命令>`
- 常用快捷：`pcurl`、`pwget`、`ppip`、`ppip3`、`pnpm`、`pgit`、`ppython`、`ppython3`、`ppipx`、`pdocker`、`pdc`
- 代理脚本位置：`/root/.openclaw/workspace/scripts/withproxy`、`/root/.openclaw/workspace/scripts/noproxy`
- 已写入 `/root/.bashrc`，新开 shell 可直接使用

### Browser / 网页自动化速记

- 2026-04-18 起，默认主链路：`agent-browser`（对应 skill：`agent-browser-clawdbot`）
- OpenClaw 内置 `browser` 工具改为备用链路
- 优先使用 `agent-browser` 的场景：
  - 多步网页自动化
  - 稳定 ref 定位
  - 表单填写
  - 连续点击/抓取
  - 会话隔离
- 回退使用内置 `browser` 的场景：
  - 需要内置截图/PDF/可视分析
  - 需要 OpenClaw browser 特有集成
  - `agent-browser` 不适配当前目标站点

- `agent-browser` 已验证可用：
  - 命令：`/www/server/nodejs/v24.14.0/bin/agent-browser`
  - 版本：`0.25.4`
  - 已成功打开并快照 `https://example.com`

- 先看 `browser status`：
  - `running=true`、`cdpReady=true`、`cdpHttp=true` → 内置 browser 本体正常
- 如果只是在某个站点报：`browser navigation blocked by policy`
  - 这通常是站点/策略限制，不是 browser 坏了
- 如果报：`timed out. Restart the OpenClaw gateway...`
  - 先按“一次性超时”看，不要立刻认定 browser 整体损坏
  - 先复查 `browser status`、`18791`、`18800` 是否还在监听
- 当前本机内置 browser 正常时的关键端口：
  - `127.0.0.1:18791` → browser 控制服务
  - `127.0.0.1:18800` → Chrome CDP
- 对主人这台机器，判断优先级：
  1. 先分清是整体故障、单次超时，还是站点策略拦截
  2. 不要把站点限制误报成 browser 整体不可用
  3. 不要为修 browser 去碰 Telegram 专用代理

### GitHub 备份边界

- 以后备份到 GitHub 私有仓库时，只备份“龙虾重要配置”
- 默认应备份：
  - `openclaw.json` 及相关关键配置备份
  - 其他关键配置文件
  - `workspace`
  - `workspace/skills`
  - `workspace-xiaojizhe`
  - `workspace-xiaojizhe/skills`
  - `agents`
  - 记忆文件
  - 关键脚本 / service 配置
- 默认不备份：
  - `downloads`
  - `artifacts`
  - `browser-data`
  - 各类缓存
  - 日志
  - 临时产物
  - 纯运行期大文件
- 原则：GitHub 私有仓库用于“可恢复核心配置”，不是拿大文件归档。

### Docker 项目约定

- Docker 项目根目录：`/www/manmanai/docker`
- 每个项目使用独立目录：`/www/manmanai/docker/<项目名>/`
- 每个项目的 compose 文件固定放在项目目录下：`docker-compose.yml`
- 新建项目默认流程：创建项目目录 → 写/改 `docker-compose.yml` → 在该目录执行 `docker-compose up -d`
- 升级项目默认流程：进入项目目录 → 执行 `docker-compose pull && docker-compose up -d --remove-orphans`

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
