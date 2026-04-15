# OmniBox 影视项目与 T4 源开发学习笔记

更新时间：2026-04-15

## 先说结论

基于你给的三份文档，我现在对 OmniBox 写源这套机制的理解已经够拿来干活了。

对你当前环境最关键的结论是：

1. 你配置里的 **`type: 4`**，本质上就是走 **OmniBox 后端接口型源**。
2. 真正要写的不是前端 JSON 本身，而是 **OmniBox 后端里的爬虫脚本**。
3. 写好脚本后，OmniBox 会把它暴露成接口，然后你在 JSON 里填：
   - `type: 4`
   - `api: https://.../video/某个标识`
   - 必要时加 `header.token`
4. 所以你以后说“写 T4 源”，本质上是两步：
   - 在 OmniBox 里写爬虫脚本
   - 在你的源配置 JSON 里挂接这个接口

---

## 一、我现在对 OmniBox 项目的整体理解

从这三份文档看，OmniBox 的影视爬虫体系大概分三层：

### 第一层，脚本层
开发者写 JS 或 Python 脚本，实现固定的几个方法：
- `home`
- `category`
- `detail`
- `search`
- `play`

这层就是“源逻辑本体”。

### 第二层，运行器层
OmniBox 用运行器把请求分发给这些方法。

也就是：
- 前端或客户端来请求
- Runner 把 `params` 和 `context` 注入给脚本
- 脚本返回标准结构 JSON
- OmniBox 再把结果提供给客户端

### 第三层，客户端接入层
像你现在这些 JSON 文件里的站点项，就是客户端消费层。

例如：
- `type: 3` 更像本地脚本 / 本地 jar / 本地适配器
- `type: 4` 更像标准接口型站点，直接吃 OmniBox 后端提供的接口

所以你现在这些 `不夜自用`、`不夜分享` 里大量：

- `type: 4`
- `api: https://by.keket.cn:7777/video/...`
- `header: { token: "..." }`

这就是很典型的 OmniBox 接口型源接法。

---

## 二、T4 源到底是什么

虽然文档里没有直接写“T4 源”这个口语词，但结合你现有 JSON，可以基本确认：

## T4 源 = `type: 4` 的接口型影视源

它不是把爬虫代码直接塞在 JSON 里运行。

它是：
- 爬虫逻辑在 OmniBox 后端
- JSON 里只挂一个接口入口
- 客户端再通过这个接口拿首页、分类、详情、搜索、播放数据

所以以后你让我“写一个 T4 源”，我应该默认理解成：

### 目标产物包含两部分
#### 1. OmniBox 爬虫脚本
负责：
- 分类
- 列表
- 详情
- 搜索
- 播放

#### 2. 你的影视 JSON 接入项
负责：
- `type: 4`
- `api`
- `searchable`
- `quickSearch`
- `filterable`
- `header.token`
- 展示名称

---

## 三、OmniBox 写源的固定接口

OmniBox 文档给出的核心接口是 5 个。

## 1. `home(params, context)`
作用：
- 返回首页分类
- 返回推荐列表
- 可选返回筛选器 `filters`
- 可选返回轮播 `banner`

典型返回：
- `class`
- `list`
- `filters`
- `banner`

### 适合做什么
- 首页频道
- 推荐影片
- 首页轮播
- 分类入口

---

## 2. `category(params, context)`
作用：
- 返回某个分类下的分页列表

主要入参：
- `categoryId`
- `page`
- `filters`

主要返回：
- `page`
- `pagecount`
- `total`
- `list`

### 适合做什么
- 电影 / 电视剧 / 动漫 / 综艺分页
- 按地区、年份、类型筛选
- 目录型站点的下一层列表

---

## 3. `detail(params, context)`
作用：
- 返回视频详情
- 返回播放线路
- 返回剧集列表

主要入参：
- `videoId`

主要返回：
- `list`
  - `vod_id`
  - `vod_name`
  - `vod_pic`
  - `vod_content`
  - `vod_actor`
  - `vod_director`
  - `vod_area`
  - `vod_year`
  - `vod_play_sources`

其中最关键的是：

### `vod_play_sources`
这是结构化播放源。
每条线路包含：
- `name`
- `episodes`

每个剧集包含：
- `name`
- `playId`
- `size`（可选）
- 一堆剧集元数据（可选）

这意味着 OmniBox 更推荐你把线路和剧集组织成结构化数据，而不是拼传统字符串。

---

## 4. `search(params, context)`
作用：
- 搜索影片

主要入参：
- `keyword`
- `page`
- `quick`

主要返回：
- `page`
- `pagecount`
- `total`
- `list`

### 适合做什么
- 站内搜索
- 聚合搜索
- 网盘资源搜索
- 搜索跳转型源

---

## 5. `play(params, context)`
作用：
- 返回可播放地址
- 可选带请求头
- 可选带弹幕
- 可选告诉客户端是否需要解析

主要入参：
- `playId`
- `flag`

最推荐返回格式：
- `urls`
- `flag`
- `header`
- `danmaku`
- `parse`

其中最关键的理解是：

### `parse`
- `0`：直链，不需要解析
- `1`：需要客户端嗅探解析

但文档明确说了：

### `parse = 1` 只有特定客户端有效
也就是只有支持该能力的客户端才会真正嗅探。
别把它当成万能方案。

所以如果能直接给 `.m3u8` 或 `.mp4`，优先直接给直链。

---

## 四、请求上下文 `context` 很重要

OmniBox 不是只给你业务参数，它还会给 `context`。

文档里关键字段有：
- `baseURL`
- `headers`
- `sourceId`
- `from`

## 最重要的是 `from`
它表示调用端是谁，例如：
- `web`
- `tvbox`
- `uz`
- `catvod`
- `emby`

这意味着：

### 你可以按客户端做差异化返回
比如：
- 网页端隐藏某条线路
- 电视端只保留直链
- 某些客户端不返回复杂字段
- 某些客户端单独处理搜索或播放

这个能力很实用。
因为同一套源，往往不同客户端兼容性不一样。

---

## 五、OmniBox 的数据模型重点

## 1. `VodItem`
这个是最基础的视频项。
常用字段包括：
- `vod_id`
- `link`
- `vod_name`
- `vod_pic`
- `type_id`
- `type_name`
- `vod_remarks`
- `vod_year`
- `vod_douban_score`
- `vod_subtitle`
- `vod_tag`
- `search`

### 这里有两个很有用的点

#### `vod_tag = "folder"`
表示它不是最终影片，而是目录。
点进去是进入下一层分类，不是直接详情页。

这对：
- 网盘目录
- 聚合分类
- 文件夹型资源

很有用。

#### `search`
文档说明这是某些客户端用的行为位。
也就是点击这个条目时，可以让客户端执行搜索而不是普通跳转。

---

## 2. `vod_play_sources`
这是 OmniBox 推荐的播放结构。
相比老式拼接字符串，结构化得多。

更适合你后面做：
- 多线路
- 多清晰度
- 文件大小展示
- 剧集信息展示
- 网盘剧集映射

---

## 六、SDK 能力，哪些对你以后最有用

文档里的 SDK 我分成几组。

## 1. 基础请求组
- `request(url, options)`
- `log(level, message)`
- `getEnv(name)`

### 用途
- 请求目标站
- 打日志排错
- 读环境变量，比如 token、密钥

这里我最看重的是：

### 不要把敏感值硬写进脚本
更稳的做法是：
- token 之类放环境变量
- 脚本里通过 `getEnv` 读取

---

## 2. 源内数据组
- `getSourceFavoriteTags()`
- `getSourceCategoryData(categoryType, page, pageSize)`

### 用途
- 读当前源收藏标签
- 读历史、收藏、追剧、标签分类数据

这说明 OmniBox 不只是“抓网页”，它还带一点平台内部数据联动能力。

如果以后你想做：
- 当前源历史
- 当前源收藏
- 标签聚合

这组接口很有价值。

---

## 3. 网盘能力组
- `getDriveFileList(shareURL, pdirFid)`
- `getDriveVideoPlayInfo(shareURL, fid, flag)`
- `getDriveInfoByShareURL(shareURL)`
- `getDriveShareInfo(shareURL)`

### 这是最值得关注的一组
因为你现在很多源明显和网盘、聚合盘链有关。

这意味着 OmniBox 不是要求你手撸所有网盘逻辑。
它已经内建了不少盘相关能力。

所以以后写：
- 阿里云盘
- 夸克
- 115
- UC
- 盘链聚合

可以优先考虑用这组 SDK，而不是每次从零造轮子。

---

## 4. 刮削能力组
- `processScraping(videoId, keyword, resourceName, videoFiles)`
- `getScrapeMetadata(videoId)`

### 用途
- 触发刮削
- 读刮削结果
- 拿 TMDB 映射

这个能力对剧集源很有用。
因为你可以把：
- 文件名
- 网盘剧集
- TMDB 元数据

映射起来，最终在 `detail` 里把：
- 剧集名
- 简介
- 首播日期
- 剧照
- 评分
- 时长

带回去。

这会让源的观感和完整度高很多。

---

## 5. 播放辅助组
- `sniffVideo(url, headers)`
- `getVideoMediaInfo(playUrl, headers)`
- `getDanmakuByFileName(fileName)`
- `getAnalyzeSites()`
- `addPlayHistory(...)`

### 我对这组的理解

#### `sniffVideo`
适合：
- 播放页里藏真实地址
- 需要从页面里嗅探视频直链

#### `getVideoMediaInfo`
适合：
- 获取时长
- 判断媒体信息
- 给播放记录或详情补数据

#### `getDanmakuByFileName`
适合：
- 根据文件名去匹配弹幕

#### `getAnalyzeSites`
适合：
- 读取解析站配置
- 做站外解析联动

#### `addPlayHistory`
适合：
- 在播放时顺手写入历史记录

---

## 6. 缓存组
- `getCache(key)`
- `setCache(key, value, exSeconds)`
- `deleteCache(key)`

### 这组很重要，但经常被忽略
因为很多源最容易死在：
- 搜索太频繁
- 详情页重复请求
- 目标站限流
- 接口太慢

如果以后写聚合类 T4 源，缓存几乎是必备。

特别适合缓存：
- 搜索结果
- 详情结果
- 盘链解析结果
- 分类页前几页

---

## 七、你现有这几份源配置，和 OmniBox 的关系

结合我刚才看过的几个 JSON，可以做一个很明确的判断：

## `pg分享`、`pg自用`
更偏：
- 本地 `jar`
- 本地相对路径资源
- 本地脚本 / 本地适配器型

所以更像传统本地源体系。

## `不夜自用`、`不夜分享`
更偏：
- 远程 spider
- 远程 logo / wallpaper
- 大量 `type: 4`
- `api: https://by.keket.cn:7777/video/...`
- `header.token`

所以它们和 OmniBox 的接口型思路更贴近。

也就是说：

### 如果你以后要做 OmniBox 风格的 T4 源
最适合参考的不是 `pg分享`，而是：
- `不夜自用`
- `不夜分享`

---

## 八、我对“怎么写一个能用的 T4 源”的实际方法论

如果现在让我实战写，我会按这个顺序来。

## 第一步，先确定源类型
先分清楚你要写的是哪种：

### 1. 直采站点源
比如普通影视站。
特点：
- 有分类
- 有搜索
- 有详情
- 有播放页

### 2. 聚合接口源
比如多个后端接口聚合。
特点：
- 主要是调现成接口
- 重点在数据清洗和统一输出

### 3. 网盘资源源
特点：
- 搜索靠盘链
- 详情靠文件列表
- 播放靠盘 SDK

### 4. 搜索驱动源
特点：
- 没有太强首页
- 主要价值在 search 和 detail/play

不同类型，5 个方法不一定都重要。

文档也明确说了：
- 不是所有方法都必须实现
- 推送类脚本甚至只要 `detail` 和 `play`

---

## 第二步，先打通最小闭环
我会优先实现：
- `search`
- `detail`
- `play`

原因很现实：
- 很多源首页和分类花哨，但不影响能不能看
- 真正决定有没有价值的是：
  - 能不能搜到
  - 能不能展开线路
  - 能不能播

这也是最快的成活路线。

---

## 第三步，再补 `home` 和 `category`
等最小闭环能播了，再做：
- 分类页
- 推荐页
- 筛选器
- 轮播

这样开发效率最高。

---

## 第四步，最后做增强项
例如：
- 弹幕
- 历史记录
- TMDB 刮削
- 缓存
- 按客户端差异化输出
- 解析站联动

---

## 九、写 T4 源时我认为最容易踩的坑

## 1. 把 `play` 当成只返回一个字符串
文档已经明显偏向结构化返回。
最好直接返回：
- `urls`
- `header`
- `flag`
- `parse`
- `danmaku`

这样扩展空间最大。

---

## 2. 忽略 `context.from`
不同客户端兼容性会不一样。
如果不做差异化，很容易出现：
- 网页能播，电视不能播
- 某客户端能解析，另一个不行

---

## 3. 把敏感信息硬编码进脚本
最好改成环境变量读取。

---

## 4. 搜索和详情不做缓存
聚合类、网盘类、第三方接口类很容易被请求打爆。

---

## 5. 想一次做全
正确做法应该是：
- 先让 `search -> detail -> play` 打通
- 再逐步补全

---

## 十、我现在可以直接帮你做什么

基于这次学习，我现在已经能继续做下面这些事：

## 1. 帮你写 OmniBox 的 T4 源骨架
我可以直接给你：
- JavaScript 版
- Python 版

而且会按你现有环境去写，不写成空壳教学模板。

## 2. 帮你把某个现有站点改造成 T4 接口源
比如把你现有某个：
- 搜索站
- 聚合站
- 网盘站

改写成 OmniBox 可接的脚本。

## 3. 帮你把 T4 源挂进你现有 JSON
也就是直接补：
- `type: 4`
- `api`
- `header.token`
- 名称
- 搜索开关
- 快搜开关

## 4. 帮你对照 `不夜自用 / 不夜分享` 的风格做兼容写法
这样你后面接进去会更顺。

---

## 十一、我当前的最小结论

如果后面主人要我真正开始写 OmniBox T4 源，我会默认采用这套策略：

### 默认开发策略
1. 先明确目标站属于直采、聚合、网盘还是搜索驱动。
2. 优先打通 `search -> detail -> play`。
3. `play` 默认返回结构化 `urls`，尽量给直链。
4. 涉及多客户端时，优先使用 `context.from` 做差异化。
5. 涉及网盘时，优先尝试 OmniBox 自带网盘 SDK。
6. 涉及重复请求时，优先加缓存。
7. 最后再补首页、分类、筛选、轮播、弹幕、刮削等增强功能。

---

## 文档来源
- `https://omnibox-doc.pages.dev/spider-development/sdk`
- `https://omnibox-doc.pages.dev/spider-development/getting-started.html`
- `https://omnibox-doc.pages.dev/spider-development/api-reference.html`
