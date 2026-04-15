# 不夜源深度学习笔记：各类写法与适用场景

更新时间：2026-04-15

## 先说结论

不夜源和 OmniBox 不是一套东西，不能混用。

我这次重新按你给的真实不夜源配置去拆，当前最小正确认识是：

- OmniBox 重点是写 `home/category/detail/search/play` 这类 JS / SDK handler
- 不夜源重点是 **配置挂源**，通过 `type`、`api`、`ext`、`header`、`proxy`、`timeout` 等字段，把不同后端能力挂到统一源列表里
- 不夜源里同一个“业务类型”，既可能有 `type: 3` 写法，也可能有 `type: 4` 写法
- 所以以后不能再说“某类站就一定按 OmniBox 那样写”，也不能把不夜源 JSON 当 OmniBox JS 模板

---

## 一、不夜源的核心思路

不夜源更像“统一挂载层”。

它不是先问“这个 JS handler 怎么写”，而是先问：

1. 这个源要挂到哪种运行方式
2. 是本地插件型、脚本型，还是远端接口型
3. 需要哪些附加参数
4. 搜索、筛选、快搜、代理、超时这些能力怎么在配置层打开

所以不夜源里最重要的不是某个函数，而是这几个字段组合：

- `type`
- `api`
- `ext`
- `header`
- `proxy`
- `timeout`
- `style`
- `playerType`
- `changeable/searchable/quickSearch/filterable`

---

## 二、不夜源里当前看到的两大主干

## 1. `type: 3` 本地插件 / 本地脚本 / jar / py / 内置模块挂法

这是不夜源里最典型、最老牌、也是最重的一类。

典型例子：
- `csp_Douban`
- `csp_Bili`
- `csp_Wogg`
- `csp_Wobg`
- `csp_Guanying`
- `csp_FourKZN`
- `csp_TGYunPanLocal`
- `./jar/emby_proxy.py`
- `./jar/世纪音乐.py`
- `./libs/drpy2.min.js + ./js/88ball.js`

### 这类写法的核心特征
- `api` 往往不是远端 URL，而是本地模块名、jar/py 路径、drpy 入口
- `ext` 经常承载大量参数
- 很多能力不是靠统一 HTTP header 传，而是通过 `ext` 或本地文件喂进去
- 适合“有状态”“有本地依赖”“要吃配置文件”“要调用本地能力”的源

### 这类源最常见的几种子写法

#### 1. 内置 `csp_*` 模块型
例子：
- `csp_Douban`
- `csp_Bili`
- `csp_Wogg`
- `csp_TGYunPanLocal`

特点：
- `api` 直接写模块名
- `ext` 里经常用 `$$$` 拼接多个参数
- 通常依赖 `./lib/*.json`、`./lib/*.txt` 等本地配置

说明：
这类不是 OmniBox 那种“我自己写 handler”，而是把参数喂给现成模块。

#### 2. Python / jar 代理型
例子：
- `./jar/emby_proxy.py`
- `./jar/世纪音乐.py`

特点：
- `api` 指向本地脚本
- `ext` 常常是对象，承载 server、username、password、proxy 等
- 适合 Emby、音乐站、需要独立脚本逻辑的后端

#### 3. drpy 挂脚本型
例子：
- `api: ./libs/drpy2.min.js`
- `ext: ./js/88ball.js`

特点：
- `api` 是统一运行时
- `ext` 才是真正的站点脚本
- 适合把一类 JS 规则挂到统一执行器里

这个和 OmniBox 也不能混，因为这里不是 OmniBox SDK handler，而是 drpy 规则脚本接到 drpy runtime。

---

## 2. `type: 4` 远端接口型

这类更像“把远端后端服务直接挂进来”。

典型例子：
- `https://by.keket.cn:7777/video/bili_all_mix`
- `https://by.keket.cn:7777/video/wanou_sites`
- `https://by.keket.cn:7777/video/panlian_auto_check`
- `https://by.keket.cn:7777/video/HuyaLive`
- `https://by.keket.cn:7777/video/webdav_client`

### 这类写法的核心特征
- `api` 是完整 URL
- 常配 `header.token`
- 逻辑大部分已经在服务端
- 本地 JSON 主要负责挂载、命名、开关和参数开闭
- 很适合统一接入远端能力池

### 这类写法不是 OmniBox 的原因
虽然看起来也像“后端接口型”，但这里的关注点仍然是：
- 如何挂载远端接口
- token 怎么传
- quickSearch/filterable/searchable 怎么开
- 哪些源适合做聚合、盘搜、直播、推送

而不是 OmniBox 那套 JS handler 开发方法。

---

## 三、不夜源里我当前总结出的主要业务类型

## 1. 内容入口 / 配置中心型
例子：
- 豆瓣
- 配置中心
- 本地
- 急救知识

### 特征
- 不一定强调搜索
- 更像首页入口、聚合入口、辅助页
- 常配 `indexs`、`style`

### 写法重点
- 名字和展示形态重要
- `style.type`、`style.ratio` 控制展示
- 不一定需要 `quickSearch`

---

## 2. B站 / 内容平台型
例子：
- `csp_Bili`
- `bili_all_mix`

### 这里能看出一个关键事实
同样是“B站”，在不夜源里就已经有两种完全不同接法：

#### A. 本地插件型
- `type: 3`
- `api: csp_Bili`
- `ext` 里带分类和 cookie

#### B. 远端接口型
- `type: 4`
- `api: https://.../video/bili_all_mix`
- `header.token`

### 结论
不夜源里判断写法，不能只看业务名，还要看：
- 是本地模块跑
- 还是远端接口跑

这比 OmniBox 更“挂载导向”。

---

## 3. Emby 型
例子：
- `./jar/emby_proxy.py`

### 特征
- `type: 3`
- `api` 指向本地 py
- `ext` 是结构化账号配置
- `changeable: 1`

### 写法重点
- server / username / password / proxy / thread 这些是核心
- 不是 HTML 抓站
- 也不是 OmniBox handler
- 本质是“把一个专门的 Emby 代理脚本挂上来”

---

## 4. 4K 站 / 玩偶系 / 站群复用型
例子：
- `csp_Wogg`
- `csp_Wobg`
- 玩偶 / 木偶 / 二小 / 至臻 / 多多 / 虎斑

### 这是不夜源里很典型的一种写法
本体逻辑是同一套或近似同一套，区别只在：
- base URL 不同
- 配套配置文件不同
- 名字不同

### 常见形态
- `api` 共用同一个模块
- `ext` 里第 2 段换成不同站地址
- 其余参数尽量复用

### 结论
这类源的核心能力不是“重新开发一个源”，而是：

## 同模板多站复用

以后遇到同站群结构，很可能只要换：
- 站点地址
- token 文件
- 配套配置文件

而不是重写整套逻辑。

---

## 5. 网盘分享型
例子：
- `PushShare`
- `AlistShare`
- `AliShare`
- `QuarkShare`
- `115Share`
- `189Share`
- `UCShare`
- `ThunderShare`

### 特征
- 多为 `type: 3`
- `api` 是 `csp_*Share`
- `ext` 里常带 token 文件、资源列表文件、数据库标识等
- `style` 常用 `list`

### 写法重点
- 不一定强调分类页
- 更强调资源聚合、分享链接整理、列表展示
- timeout 往往更大

### 结论
这类属于：

## 资源库 / 分享集合挂法

重点不在爬网页，而在接现成分享数据源。

---

## 6. p2t / 电报盘搜型
例子：
- `csp_TGYunPanLocal`
- `p2t`
- `pansougaoma`
- `quarkp2t`
- `aliyunp2t`
- `ucp2t`
- `115p2t`

### 特征
- 多为 `type: 3`
- `api` 共用 `csp_TGYunPanLocal`
- 差异主要放在 `ext`
- `ext` 是对象，不再是简单字符串
- 常含：
  - `token`
  - `json`
  - `keywords`
  - `tgsearch_url`
  - `tgsearch_media_url`
  - `channellist`
  - `proxy`
  - `danmu`
  - `douban`

### 这是不夜源非常重要的一种模式
也就是：

## 同一个后端模块 + 不同 ext 策略 = 不同业务源

比如：
- 全局盘搜
- 高码盘搜
- 按网盘类型切分

其实 backend 可能是同一套，只是过滤条件不同。

---

## 7. 网盘搜索远端接口型
例子：
- `panbaidu`
- `panso115`
- `pansoquarkpancheck`
- `pansoucpancheck`
- `panso123pancheck`
- `panso139pancheck`
- `pansogyingpancheck`
- `pansotianyipancheck`
- `pansoupancheck`
- `盘搜高码`

### 特征
- 多为 `type: 4`
- `api` 是远端 `/video/...`
- `header.token` 统一鉴权
- 名字上按网盘类型或过滤策略拆分

### 和 p2t 型的区别
- p2t 型更像本地模块接远端搜索服务
- 这里更像直接把远端“成品接口”挂上来

---

## 8. 聚合站 / 网盘+磁力型
例子：
- `Guanying`
- `FourKZN`
- `FourKFox`
- `FourKFM`
- `wanou_sites`
- `panlian_auto_check`

### 特征
- 既有 `type: 3` 版本，也有 `type: 4` 版本
- 常见关键词：聚合、网盘+磁力、自动检测
- 一般启用 `quickSearch`、`filterable`

### 结论
这类源通常追求：
- 结果覆盖面
- 线路整合
- 过滤能力
- 一次挂出多个内容来源

---

## 9. 直播型
例子：
- `HuyaLive`
- `DouyuLive`
- `DouyinLive`
- `88看球`

### 特征
- 既有 `type: 4` 的纯远端接口直播源
- 也有 `type: 3` 的 drpy 规则挂法
- 有的带 `playable: 1`

### 结论
直播在不夜源里也不是固定一种写法。
可能是：
- 远端接口直播源
- 本地规则执行器挂直播脚本

所以不能只看“直播”就判断它怎么写。

---

## 10. 推送 / WebDAV / 工具型
例子：
- `push_agent`
- `webdav_client`

### 特征
- 更像工具能力入口
- 不一定以普通影视检索逻辑为主
- 常见 `type: 4` 远端接口挂法

### 结论
这类不是内容站，而是功能站。
以后看到类似名字，要先按“工具入口”理解，而不是按影视站理解。

---

## 四、不夜源里最重要的几个判断维度

以后看到一个不夜源条目，我先判断这 6 件事：

## 1. 它是 `type: 3` 还是 `type: 4`
这是第一层分水岭。

### `type: 3`
优先按：
- 本地模块
- 本地脚本
- 本地运行时
- 参数喂给现成能力

### `type: 4`
优先按：
- 远端接口挂载
- token 鉴权
- 本地只负责接入和开关

---

## 2. `api` 是什么形态
### 模块名
如 `csp_Bili`
说明是内置 / 预置模块

### 本地文件
如 `./jar/emby_proxy.py`
说明是脚本型

### 运行时入口
如 `./libs/drpy2.min.js`
说明真正业务在 `ext` 指向的脚本

### 完整 URL
说明是远端接口型

---

## 3. `ext` 是字符串还是对象
### 字符串
常见于：
- `$$$` 拼接参数
- 旧式模块喂参

### 对象
常见于：
- Emby
- p2t
- 结构化配置更多的源

说明这类源参数语义更清楚，也更适合精细配置。

---

## 4. 是否有 `header.token`
有的话通常说明：
- 这是远端接口服务
- 本地只是接入层

---

## 5. 是否有 `proxy: noproxy`
说明：
- 该源对代理策略敏感
- 可能需要强制直连
- 这是不夜源实战里很关键的部署细节

---

## 6. 是否有 `style` / `playerType` / `timeout`
这些说明：
- 不夜源不仅管数据源，还管展示和行为细节
- 它是“配置驱动接入层”，不是纯开发框架

---

## 五、我现在形成的不夜源写法地图

## A. 本地模块挂法
适用：
- `csp_*`
- 现成能力模块
- 站群复用

## B. 本地脚本挂法
适用：
- py / jar
- Emby / 音乐等专用能力

## C. 运行时 + 规则脚本挂法
适用：
- drpy 这类执行器 + JS 规则

## D. 远端接口挂法
适用：
- 已有后端服务
- token 鉴权
- 聚合服务
- 直播 / 盘搜 / 工具型后端

## E. 同模块多配置复用挂法
适用：
- 玩偶系站群
- p2t 多筛选版本
- 同一后端不同渠道版本

---

## 六、这次学习后最关键的纠偏

之前容易混的点是：
- 看到 `type: 4` 就往 OmniBox 接口型源上靠
- 看到 JS / 接口 / 搜索 / 详情 就误以为能直接套 OmniBox 思维

现在要纠正为：

## 不夜源先看“挂法”
不是先看“站点 handler 怎么写”。

也就是先问：
- 这是本地模块
- 本地脚本
- 运行时规则
- 还是远端接口

再看它属于：
- B站
- Emby
- 盘搜
- 聚合
- 直播
- 工具

---

## 七、以后我处理不夜源的默认方法

如果主人让我学不夜源或改不夜源，我会按这个顺序：

1. 先认清这是不夜源，不套 OmniBox 术语
2. 先看 `type`
3. 再看 `api` 形态
4. 再拆 `ext` / `header` / `proxy` / `timeout`
5. 再判断它属于哪种业务类型
6. 最后才决定是替换、复用、改参数，还是换挂法

---

## 最小结论

不夜源的本质不是“写一个站点 JS”，而是：

## 把不同运行方式的能力，统一挂进一个源配置体系里

所以以后：
- OmniBox 我按开发框架来学
- 不夜源我按挂载体系、参数结构、运行方式来学

这两条线我会彻底分开，不再混。