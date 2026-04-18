---
name: backup-openclaw
description: Create a config-only OpenClaw backup for this machine when the user explicitly says "备份龙虾" or clearly asks to back up OpenClaw to local storage and GitHub. Use for the fixed local+GitHub backup workflow, local retention of the latest 3 backups, temporary GitHub clone/push, and avoiding persistent duplicate local GitHub working copies.
---

# Backup OpenClaw

用于这台机器上的“龙虾备份”固定流程。

## 触发条件

只在用户**明确**下达以下意图时使用：
- “备份龙虾”
- 明确要求备份 OpenClaw 到本地
- 明确要求同时同步到 GitHub 私有仓库

不要因为目录有变化、刚整理完、或你觉得应该备份，就自行触发。

## 固定规则

- 本地只保留一套**当前可见配置备份**：`/www/manmanai/openclaw/backups/local-config/root/.openclaw`
- 同时保留**最近 3 次本地历史备份**：`/www/manmanai/openclaw/backups/local-config/history/<时间戳>/root/.openclaw`
- GitHub 是**远程备份目标**，不算本地备份
- GitHub 推送时必须使用**临时工作区**，推送后删除，不能在 `/www/manmanai/openclaw/backups` 下长期保留本地 clone
- 备份内容默认采用“**重要配置 + 学习技能**”方案
- 默认不备份下载、browser-data、logs、cache、tmp、media、artifacts 等运行产物

## 默认保留内容

- `openclaw.json`
- `openclaw.json.bak*`
- `openclaw.json.backup.*`
- `exec-approvals.json`
- `update-check.json`
- `workspace`
- `workspace/skills`
- `workspace-xiaojizhe`
- `workspace-xiaojizhe/skills`
- `agents`
- `identity`
- `devices`
- `telegram`
- `canvas`
- `completions`
- `memory`
- `flows`
- `tasks`

## 默认排除内容

- `downloads`
- `artifacts`
- `browser-data`
- `browser`
- `media`
- `delivery-queue`
- `logs`
- `qqbot`
- `tmp`
- `.git`
- `.openclaw`
- `.agents`
- `state`
- `.clawhub`
- 常见本地开发工具隐藏目录
- `*.sqlite-shm`
- `*.sqlite-wal`
- `*.tar.gz`

## 推荐执行方式

优先使用脚本：

```bash
bash /root/.openclaw/workspace/skills/backup-openclaw/scripts/backup-openclaw.sh
```

## 执行步骤

1. 创建本地历史备份目录，使用时间戳命名
2. 从 `/root/.openclaw` 拷贝配置型内容到历史目录
3. 用同一份内容刷新当前目录 `backups/local-config/root/.openclaw`
4. 清理历史目录，只保留最近 3 个
5. 用临时目录 clone `git@github.com:keket0/backup-private.git`
6. 用同一份配置型内容覆盖仓库内容
7. `git add -A && git commit && git push`
8. 删除临时 clone 目录
9. 汇报本地路径、保留份数、GitHub 提交号

## 关键坑点

- 不要把 GitHub 仓库本地 clone 长期放在 `/www/manmanai/openclaw/backups` 下，否则会和本地备份形成明显重复
- 不要把顶层运行目录误搬到别处，避免破坏既有路径习惯
- 只有用户明确说“备份龙虾”时才能执行
- 如果 GitHub 推送失败，先保住本地备份，再单独修 GitHub 步骤

## 验收结果应包含

- 本地当前备份目录
- 本地历史备份目录数量
- GitHub 是否推送成功
- 远程提交短 SHA
- 若有失败，给出原始报错 + 最小修复
