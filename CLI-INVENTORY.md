# CLI-INVENTORY.md

更新时间：2026-04-15 15:43

这个文件记录当前机器上与 OpenClaw 运行、迁移、验证相关的关键 CLI。

用途：
- 换机器时知道哪些命令必须先装
- 出问题时知道缺哪个命令会影响哪条能力线
- 避免只记“要装很多东西”，却不知道优先级

---

## 1. 当前已确认存在的关键 CLI

### Node / npm 体系
- `node`：`/www/server/nodejs/v24.14.0/bin/node`
- `npm`：`/www/server/nodejs/v24.14.0/bin/npm`
- `npx`：`/www/server/nodejs/v24.14.0/bin/npx`

版本：
- Node：`v24.14.0`
- npm：`11.9.0`

### OpenClaw 体系
- `openclaw`：`/www/server/nodejs/v24.14.0/bin/openclaw`
- `clawhub`：`/www/server/nodejs/v24.14.0/bin/clawhub`

### 浏览器 / 自动化相关
- `agent-browser`：`/www/server/nodejs/v24.14.0/bin/agent-browser`

### 常用辅助工具
- `jq`：`/usr/bin/jq`
- `git`：`/usr/bin/git`
- `python3`：`/usr/bin/python3`
- `pip3`：`/usr/bin/pip3`
- `systemctl`：`/usr/bin/systemctl`
- `curl`：`/usr/bin/curl`

版本：
- Python：`3.11.2`
- git：`2.39.5`
- curl：`7.88.1`

---

## 2. 必装 CLI

这些命令是当前环境最核心的，缺了会明显影响恢复或运行。

### 1. `node`
作用：
- OpenClaw gateway 运行时依赖
- systemd 服务里的 `ExecStart` 直接调用 node

缺失后果：
- gateway 无法启动
- 迁移后 systemd 服务直接失效

### 2. `openclaw`
作用：
- 查看状态
- 管理 gateway
- 使用内置 CLI 能力

缺失后果：
- 无法直接做 `openclaw gateway status`
- 无法方便验活和管理服务

### 3. `systemctl`
作用：
- 管理 `openclaw-gateway.service`

缺失后果：
- 当前这套 systemd 用户服务模型无法直接复用

---

## 3. 强烈建议安装的 CLI

这些不是“没有就绝对跑不起来”，但缺了会严重影响日常能力。

### 1. `clawhub`
作用：
- 登录 ClawHub
- 安装技能
- 绕过匿名安装时的部分限流问题

缺失后果：
- 技能安装能力明显变弱
- 无法直接复用当前已验证过的登录态安装路线

### 2. `agent-browser`
作用：
- 当前浏览器线主力 CLI
- 用于网页打开、快照、截图、详情页验证

缺失后果：
- 浏览器自动化主线能力大幅下降
- 电商详情页验证、网页快照能力会受影响

### 3. `jq`
作用：
- 处理 JSON
- 已用于 `openai-tts` 等脚本和调试

缺失后果：
- 部分技能脚本直接失效
- JSON 管道分析会变麻烦

---

## 4. 建议保留的辅助 CLI

### 1. `git`
作用：
- 提交 workspace 变更
- 保留可审计历史

缺失后果：
- 无法方便记录配置和文档变更

### 2. `python3`
作用：
- 临时探测脚本
- 数据提取脚本
- 辅助排障

缺失后果：
- 很多轻量级调试脚本不好跑

### 3. `curl`
作用：
- 连通性验证
- API 调试
- 代理链验证

缺失后果：
- 网络排障效率明显下降

### 4. `npx`
作用：
- 运行某些一次性 npm 工具
- 临时执行包内能力

缺失后果：
- 某些依赖型技能或临时验证步骤会不方便

---

## 5. 当前 CLI 与能力线映射

### Gateway 运行线
依赖：
- `node`
- `openclaw`
- `systemctl`

### 技能安装线
依赖：
- `openclaw`
- `clawhub`
- `npm` / `npx`

### 浏览器自动化线
依赖：
- `agent-browser`
- `node`

### 脚本 / 调试线
依赖：
- `jq`
- `python3`
- `curl`
- `git`

---

## 6. 迁移到新机器时的最小安装建议

### 最小可运行集
如果目标只是把 OpenClaw 跑起来，至少先装：
- `node`
- `openclaw`
- `systemctl`

### 接近当前能力集
如果希望尽量接近当前环境，再补：
- `clawhub`
- `agent-browser`
- `jq`
- `git`
- `python3`
- `curl`

---

## 7. 当前值得注意的小问题

### npm 警告
当前执行 `npm -v` 时出现：
- `npm warn Unknown global config "--init.module". This will stop working in the next major version of npm.`

这不是当前主阻塞，但说明 npm 全局配置里可能有遗留项，未来升级 npm 大版本时需要留意。

---

## 8. 迁移时优先核对的命令

到新机器后，先跑这些最有价值：

```bash
command -v node
command -v openclaw
command -v clawhub
command -v agent-browser
command -v jq
node -v
openclaw gateway status
```

如果不想手工逐项看，也可以直接运行：

```bash
bash /root/.openclaw/workspace/scripts/check-new-machine-readiness.sh
bash /root/.openclaw/workspace/scripts/check-migration-prereqs.sh
```

如果这些都正常，再继续看 systemd、代理和业务能力。

---

## 9. 最简结论

如果以后换机器，至少记住：

### 必装
- `node`
- `openclaw`
- `systemctl`

### 强烈建议装
- `clawhub`
- `agent-browser`
- `jq`

### 辅助增强
- `git`
- `python3`
- `curl`
- `npx`

### 对应检查脚本
- 新机器准备度：`/root/.openclaw/workspace/scripts/check-new-machine-readiness.sh`
- 恢复前置条件：`/root/.openclaw/workspace/scripts/check-migration-prereqs.sh`

这样迁移时就不会陷入“文件都恢复了，但工具链没起来”的假恢复状态。
