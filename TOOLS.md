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

备注：
- 后续如果主人说“修改 pg分享 / pg自用 / 不夜自用 / 不夜分享”，默认就是改上面对应文件，不再重复确认路径。
- 这几份文件里含有敏感字段（如 token、cookie、账号类配置等），后续修改时不主动回显敏感值。
- 结构上都属于影视源配置 JSON，核心是 `spider`、`logo` / `wallpaper`、`sites` 列表，以及每个站点下的 `key`、`name`、`type`、`api`、`searchable`、`quickSearch`、`changeable`、`ext/header` 等字段。

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

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
