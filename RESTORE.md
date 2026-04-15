# RESTORE.md

更新时间：2026-04-15

这份文档说明如何从当前备份目录恢复 OpenClaw 关键数据。

备份根目录：
- `/www/manmanai/openclaw/backup`

最近一次快照：
- `/www/manmanai/openclaw/backup/snapshots/2026-04-15-152820`

> 说明：当前备份脚本主要备份的是 `/root/.openclaw` 下的关键内容，并额外纳入 systemd 用户服务文件 `openclaw-gateway.service`。它适合恢复 OpenClaw 配置、workspace、memory、agents，以及当前 gateway 服务定义；但仍不负责恢复操作系统本身、Node 运行时或 npm 全局包。

---

## 一、当前备份覆盖范围

### 1. 配置
来源：
- `/root/.openclaw/openclaw.json`

备份位置：
- 当前副本：`/www/manmanai/openclaw/backup/config/openclaw.json`
- 快照副本：`/www/manmanai/openclaw/backup/snapshots/<时间>/openclaw.json`

### 2. Workspace
来源：
- `/root/.openclaw/workspace`

备份位置：
- 当前副本：`/www/manmanai/openclaw/backup/workspace/current`
- 快照副本：`/www/manmanai/openclaw/backup/snapshots/<时间>/workspace`

### 3. Memory
来源：
- `/root/.openclaw/memory`

备份位置：
- 当前副本：`/www/manmanai/openclaw/backup/memory/current`
- 快照副本：`/www/manmanai/openclaw/backup/snapshots/<时间>/memory`

### 4. Agents
来源：
- `/root/.openclaw/agents`

备份位置：
- 当前副本：`/www/manmanai/openclaw/backup/agents/current`
- 快照副本：`/www/manmanai/openclaw/backup/snapshots/<时间>/agents`

### 5. systemd 用户服务文件
来源：
- `/root/.config/systemd/user/openclaw-gateway.service`

备份位置：
- 当前副本：`/www/manmanai/openclaw/backup/systemd/openclaw-gateway.service`
- 快照副本：`/www/manmanai/openclaw/backup/snapshots/<时间>/openclaw-gateway.service`

---

## 二、恢复前原则

### 先确认的事
1. 恢复目标机器上已经安装了 OpenClaw 基本运行环境。
2. 目标路径仍然是：`/root/.openclaw`
3. 如果目标路径里已有新数据，先额外备份，避免覆盖掉更新内容。

### 不要直接跳过的安全动作
- 先看要恢复的是“当前副本”还是“历史快照”。
- 优先恢复到临时目录核对，再正式覆盖。
- 涉及运行中服务时，恢复后再验活。

---

## 三、推荐恢复策略

## 方案 A，恢复最新状态
适合：机器刚重装完，想恢复到最近一次备份状态。

使用这些路径：
- 配置：`/www/manmanai/openclaw/backup/config/openclaw.json`
- workspace：`/www/manmanai/openclaw/backup/workspace/current`
- memory：`/www/manmanai/openclaw/backup/memory/current`
- agents：`/www/manmanai/openclaw/backup/agents/current`
- systemd 服务文件：`/www/manmanai/openclaw/backup/systemd/openclaw-gateway.service`

## 方案 B，恢复某个历史时间点
适合：最近状态有误，想回退到某个具体快照。

示例快照：
- `/www/manmanai/openclaw/backup/snapshots/2026-04-15-143902`

使用这些路径：
- 配置：`.../openclaw.json`
- workspace：`.../workspace`
- memory：`.../memory`
- agents：`.../agents`
- systemd 服务文件：`.../openclaw-gateway.service`

---

## 四、手动恢复步骤

> 注意：下面是恢复思路，不是要求现在立刻执行。真正执行前，最好先再做一次现场备份。

### 1. 准备目标目录
确保目标目录存在：
- `/root/.openclaw`

### 2. 恢复配置
把备份文件恢复到：
- `/root/.openclaw/openclaw.json`

### 3. 恢复 workspace
把备份目录恢复到：
- `/root/.openclaw/workspace`

### 4. 恢复 memory
把备份目录恢复到：
- `/root/.openclaw/memory`

### 5. 恢复 agents
把备份目录恢复到：
- `/root/.openclaw/agents`

### 6. 恢复 systemd 服务文件
把备份文件恢复到：
- `/root/.config/systemd/user/openclaw-gateway.service`

### 7. 恢复后核对
至少检查：
- `openclaw.json` 是否在位
- `workspace` 是否完整
- `MEMORY.md` / `PROJECTS.md` / `SESSION-STATE.md` 是否在位
- `memory/YYYY-MM-DD.md` 是否在位
- `openclaw-gateway.service` 是否在位

### 8. 服务验活
恢复后，确认 OpenClaw gateway 是否正常运行，并检查：
- 本地监听
- RPC probe
- 关键渠道是否在线

---

## 五、建议的恢复顺序

### 轻度问题，只丢工作区文件
优先恢复：
1. `workspace`
2. `memory`

### 配置损坏
优先恢复：
1. `openclaw.json`
2. `workspace`
3. `memory`

### 整个 `/root/.openclaw` 丢失
恢复顺序建议：
1. `openclaw.json`
2. `workspace`
3. `memory`
4. `agents`
5. `openclaw-gateway.service`
6. 再做服务验活

---

## 六、当前恢复能力边界

这套备份当前**能恢复**：
- OpenClaw 主配置
- workspace 文件
- memory 文件
- agents 状态目录
- `/root/.config/systemd/user/openclaw-gateway.service`

这套备份当前**不能单独恢复**：
- 操作系统本身
- Node / npm 全局环境
- `clawhub` CLI 的全局安装
- 其他手工改过但不在 `/root/.openclaw` 与该 systemd 服务文件内的系统文件

所以，如果以后要把恢复能力做得更完整，下一步应考虑把以下内容也纳入备份策略：
- 关键全局 CLI 清单
- 代理相关服务配置
- 其他 systemd 或 crontab 级别的自定义项

---

## 七、最小恢复清单

真出问题时，优先记住这 5 个恢复源：

- 配置：`/www/manmanai/openclaw/backup/config/openclaw.json`
- workspace：`/www/manmanai/openclaw/backup/workspace/current`
- memory：`/www/manmanai/openclaw/backup/memory/current`
- agents：`/www/manmanai/openclaw/backup/agents/current`
- systemd 服务文件：`/www/manmanai/openclaw/backup/systemd/openclaw-gateway.service`

如果要回到某个历史点，就去：
- `/www/manmanai/openclaw/backup/snapshots/`

按时间目录挑快照。
