# 不夜源标准模板整理（2026-04-15）

## 一、不夜影视源标准模板

适用：
- 普通网页影视站
- HTML 列表页 + 详情页
- 可选接入网盘驱动
- 需要分类 / 筛选 / 搜索 / 详情 / 播放

### 1. 推荐骨架

```js
const axios = require("axios");
const cheerio = require("cheerio");
const zlib = require("zlib"); // 按需
const CryptoJS = require("crypto-js"); // 按需

let log = () => {};

const SITE_CONFIG = {
  title: "站点名",
  host: "https://example.com",

  debug: true,
  recommend: false,

  class_name: '电影&电视剧&综艺&动漫',
  class_url: '1&2&3&4',

  url: '/show/fyfilter.html',
  searchUrl: '/search/**-------------.html',

  headers: {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://example.com/'
  },

  filterable: 1,
  filter_url_type: 'list',
  filter_url: '{{fl.cateId}}-{{fl.area}}-{{fl.by}}----fypage---{{fl.year}}',

  double: true,
  limit: 20,

  play_parse: true,
  searchable: 1,
  quickSearch: 0,

  推荐: '.module-item;... ',
  一级: '.module-item;... ',
  二级: {
    title: '.title&&Text',
    img: '.lazyload&&data-original',
    desc: '.data&&Text',
    content: '.desc&&Text',
    tabs: '.tab-item',
    lists: '.playlist:eq(#id) li'
  },
  搜索: '.module-search-item;... ',

  filter: {
    "1": [
      { "key": "area", "name": "地区", "init": "", "value": [{ "n": "全部", "v": "" }] },
      { "key": "year", "name": "年份", "init": "", "value": [{ "n": "全部", "v": "" }] },
      { "key": "by", "name": "排序", "init": "time", "value": [{ "n": "时间", "v": "time" }] }
    ]
  },

  filter_def: {
    1: { cateId: '1' }
  }
};

function fixJsonWrappedHtml(html) {}
function decompressFilter(filterData) {}
function jinja2_enhanced(template, data) {}
function parseSelector(sel) {}
function extractAttr($elem, selector, $) {}
function fixImg(img, host) {}
function buildUrl(url, host) {}
function matchDriveType(url) {}
function sortLines(lines, priority) {}

async function home() {}
async function category(tid, pg, extend) {}
async function detail(id) {}
async function search(wd, quick, pg) {}
async function play(flag, id, flags) {}

module.exports = async (app, opt) => {
  if (opt?.log) log = (...args) => opt.log.info(args.join(' '));

  const meta = {
    key: 'example_key',
    name: '示例站点',
    type: 4,
    api: '/video/example_key',
    searchable: 1,
    quickSearch: 0,
    filterable: 1,
    changeable: 0,
  };

  app.get(meta.api, async (req, reply) => {
    const { ac, t, pg, wd, ids, play, flag } = req.query || {};

    if (play) return await play(flag, ids);
    if (wd) return await search(wd, 0, pg || 1);
    if (ac === 'detail' && ids) return await detail(ids);
    if (t) return await category(t, pg || 1, req.query || {});
    return await home();
  });

  opt.sites.push(meta);
};
```

### 2. 影视源最稳的职责分层

#### A. 配置层
只放：
- host
- 分类
- URL 模板
- headers
- selectors
- filter/filter_def
- 线路优先级

#### B. 工具层
只放通用函数：
- 模板替换
- selector 解析
- HTML 修复
- 图片 URL 修复
- 网盘识别
- 线路排序

#### C. 业务层
固定 5 件事：
- 首页
- 分类
- 详情
- 搜索
- 播放

### 3. 影视源细分模板选择

#### 模板 A，普通网页站
适合：
- 苹果 CMS / 海洋 CMS / 首途类
- 列表详情清晰
- 搜索和分类 URL 可预测

写法重点：
- `SITE_CONFIG`
- `cheerio`
- `推荐 / 一级 / 二级 / 搜索`
- `filter_url`

#### 模板 B，网页站 + 网盘驱动
适合：
- 页面里能提取网盘链接
- 想让播放统一交给 drive

新增重点：
- 详情阶段提取夸克 / 百度 / UC / 阿里 / 迅雷链接
- 根据网盘类型生成 `vod_play_from` 和 `vod_play_url`
- `play()` 里优先交给 drive 或代理逻辑

#### 模板 C，专用平台型
适合：
- B站这类接口平台
- 需要 Cookie / relay / proxy / dash / mpd

重点：
- 不要硬套 selector 模板
- 直接围绕平台 API 独立写

## 二、不夜盘搜源标准模板

适用：
- 统一盘搜接口
- 多网盘聚合
- 需要链接校验
- 最终交给 drive 解析播放

### 1. 推荐骨架

```js
const axios = require("axios");
const http = require("http");
const https = require("https");
const dayjs = require("dayjs"); // 按需

const _http = axios.create({
  timeout: 60 * 1000,
  httpsAgent: new https.Agent({ keepAlive: true, rejectUnauthorized: false }),
  httpAgent: new http.Agent({ keepAlive: true }),
  baseURL: "https://your-pan-search-host"
});

const meta = {
  key: "pan_example",
  name: "盘搜示例",
  type: 4,
  api: "/video/pan_example",
  searchable: 1,
  quickSearch: 1,
  filterable: 0,
};

const store = {
  init: false,
  redis: null,
  log: console,
  drives: [],
};

const init = async (server) => {
  if (store.init) return;
  store.redis = server.redis;
  store.log = server.log || console;
  store.drives = server.drives || [];
  store.init = true;
};

async function search({ wd, page, quick, pan }) {}
async function detail({ id }) {}
async function play({ flag, id }) {}

module.exports = async (app, opt) => {
  app.get(meta.api, async (req) => {
    const { wd, ids, play, flag } = req.query || {};

    if (play) return await play({ flag, id: ids });
    if (ids) return await detail({ id: ids });
    if (wd) return await search(req.query || {});

    return {
      class: [],
      list: []
    };
  });

  opt.sites.push(meta);
};
```

### 2. 盘搜源稳定流水线

#### search()
固定流程：
1. 调盘搜接口
2. 拉平结果
3. 映射网盘类型
4. 去重链接
5. 调 `links/check`
6. 过滤失效链接
7. 排序
8. 组装 `vod` 列表

#### detail()
固定流程：
1. 判断分享链接属于哪个 drive
2. `drive.matchShare(id)`
3. `drive.getVod(id)`
4. 返回标准详情结构

### 3. 盘搜源最稳的排序策略

建议三级排序：

1. 质量关键词优先
   - HDR
   - DV
   - REMUX
   - 高码
   - 60FPS

2. 网盘优先级
   - 按 `store.drives` 顺序或自定义顺序

3. 时间优先
   - 最近资源优先

### 4. 盘搜源常用扩展

#### A. 分组模式
先返回网盘分类目录：
- 百度网盘
- 夸克网盘
- UC
- 天翼
- 115

用户点进去再看具体资源。

#### B. 直出模式
直接把所有有效链接展开成结果列表。

#### C. 高码过滤模式
搜索后只保留：
- HDR
- DV
- REMUX
- 高码
- 高帧率

### 5. 盘搜源进阶能力

按需再加：
- `runtimeState`
- 登录配置
- Cookie 持久化
- 自动登录
- 链接状态缓存
- 详情缓存
- 配置接口
- 登录接口

## 三、不夜聚合源补充模板

适用：
- 多站并发搜索
- 多站分类浏览
- 域名容灾
- 同名资源聚合

### 最小骨架

```js
const DEFAULT_SITES = [
  {
    id: "site1",
    name: "站点1",
    domains: ["https://a.com", "https://b.com"],
    filterFiles: ["site1.json"],
    listSelector: ".module-item",
    detailPanSelector: ".module-row-info p",
    searchListSelector: ".module-search-item",
    categoryUrl: "/vodshow/{categoryId}--------{page}---.html",
    categoryUrlWithFilters: "/vodshow/{categoryId}-{area}-{by}-{class}-----{page}---{year}.html",
    searchUrl: "/vodsearch/-------------.html?wd={keyword}&page={page}",
    defaultCategories: { "1": "电影", "2": "电视剧" }
  }
];

const DEFAULT_AGG_CONFIG = {
  enableAggregation: true,
  linePriority: { baidu: 1, quark: 2, uc: 3, other: 99 },
  sitePriority: { site1: 1 },
  similarityThreshold: 0.85,
  maxAggregateSites: 5
};
```

重点不是 selector，而是：
- 多站配置化
- 域名健康检查
- 并发超时控制
- 搜索结果去重聚合
- 详情线路合并

## 四、以后写不夜源时的先判定规则

先问自己这几个问题：

1. 这是普通网页影视站，还是专用平台？
2. 详情里有没有网盘链接？
3. 是单站，还是多站聚合？
4. 需要链接校验吗？
5. 需要后台配置接口吗？
6. 需要自动登录和 Cookie 持久化吗？

### 最终选型
- 普通影视站 -> 用“影视源标准模板”
- 影视站带网盘线路 -> 用“影视源 + 网盘驱动模板”
- 统一盘搜接口 -> 用“盘搜源标准模板”
- 多站并发 + 域名容灾 -> 用“聚合源补充模板”
- B站/TMDB/专用 API -> 单独做专用平台型，不套普通模板
