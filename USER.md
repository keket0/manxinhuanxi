# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name:**
- **What to call them:**
- **Pronouns:** _(optional)_
- **Timezone:**
- **Notes:** prefers replies in Chinese (set on 2026-04-14); response style preferences added on 2026-04-15: conclusion first, concise, transparent failure reporting, confirm before high-risk ops, and follow established safety process for config/core-skill changes; prioritize approved search routes and state uncertainty when unsure; on 2026-04-15 explicitly required long-term memory, memory retrieval, and regular daily summaries/journaling of completed work; free skills may be installed from the official skill site or high-star GitHub sources when genuinely useful; on 2026-04-15 clarified that the JS learning material is independent and must not be associated with 不夜自用 / 不夜分享 / Pg自用 / pg分享 or those four JSON files; the user may keep sending JS as study material and will label whether each example is 不夜源写法 or omnibox/monibox 写法; the user has defined shorthand aliases for four interface files, so when asked to modify or sync by alias I should use the mapped path directly without asking for the path again; before writing any source from a provided website, I must first confirm or follow the user's stated target type, then write the dedicated source accordingly and must not mix the two styles; when the user asks to modify `不夜自用` / `不夜分享` / `pg自用` / `pg共享(分享)` with only a source keyword, I should first search that alias file and list matching candidate sources, then wait for the user to specify which exact one to replace; on 2026-04-15 the user also defined a Docker project management convention: all Docker projects live under `/www/manmanai/docker/<项目名>/docker-compose.yml`; when creating a new project, I should create the project folder, place/edit the compose file there, then run `docker-compose up -d` in that directory; when the user asks to upgrade a container, I should go to that project's compose directory and run `docker-compose pull && docker-compose up -d --remove-orphans`; on 2026-04-16 the user explicitly required that I must not push to GitHub on my own, and only push when the user clearly says to do so; if a proxy is needed later, I should add it only per command/tool as needed, and should not restore a global proxy by default; these proxy helper commands are mainly for me to use during execution, not something I should push onto the user unless the user explicitly asks; the user has also explicitly confirmed the long-term proxy strategy distinction: global proxy affects many programs by default and is easier but higher-risk, while per-tool/per-command proxy is more controllable and is the preferred long-term approach on this machine; the currently used proxy address to remember is `http://192.168.50.2:5898`, used for Telegram and for per-command/per-tool proxy when needed; Telegram 专用代理必须长期保持，不要触碰，后续我不得擅自改动这条配置; GitHub CLI `gh` 已完成持久登录，后续我应优先复用现有登录态，不默认重复要求设备码授权; browser 问题后续必须先区分整体故障、单次超时、站点策略拦截，不能再混为一谈，目前已确认 browser 可成功打开并读取 `example.com`、`python.org`、`github.com`; 2026-04-16 已确认 Lucky 可将 `http://192.168.50.100:18789/` 稳定反代为 `https://claw.keket.cn:7788/` 并正常密码登录，后续不得漏掉 `gateway.controlUi.allowedOrigins` 中的 `https://claw.keket.cn:7788`。

## Context

- User is using me to learn JS patterns for later source writing.
- User wants strict separation: learning material must not be tied to 不夜自用 / 不夜分享 / Pg自用 / pg分享 or the four related JSON files.
- User may keep sending JS examples and will indicate whether each one is 不夜源写法 or omnibox/monibox 写法.
- When the user later gives a site to turn into a source, I must confirm the target type first if not already stated: 不夜源 or monibox/omnibox 源, and I must not mix the two.

_(What do they care about? What projects are they working on? What annoys them? What makes them laugh? Build this over time.)_

---

The more you know, the better you can help. But remember — you're learning about a person, not building a dossier. Respect the difference.
