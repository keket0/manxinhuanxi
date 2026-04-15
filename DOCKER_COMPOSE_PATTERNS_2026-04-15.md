# Docker Compose 写法与路径映射学习笔记（2026-04-15）

学习范围：`/www/manmanai/docker` 下现有各项目的 `docker-compose.yml`

## 一、目录组织总规则

你这台机器的 Docker 项目组织方式已经很清晰，后续我应该默认沿用：

- 项目根目录：`/www/manmanai/docker`
- 每个项目独立目录：`/www/manmanai/docker/<项目名>/`
- 该目录内放项目自己的：
  - `docker-compose.yml`
  - `data/`、`config/`、`logs/`、`.env`、脚本文件、文本映射文件等
- 启动时默认进入项目目录执行：
  - `docker-compose up -d`
- 升级时默认进入项目目录执行：
  - `docker-compose pull && docker-compose up -d --remove-orphans`

## 二、当前目录里的主要写法类型

### 1. 单容器 + 相对路径持久化
典型项目：
- `wenfxl_codex`
- `omnibox`
- `qinglong`
- `danmu`
- `CatPawPlay`

常见结构：

```yml
services:
  app:
    image: xxx:latest
    container_name: xxx
    ports:
      - "宿主端口:容器端口"
    restart: unless-stopped
    volumes:
      - ./data:/app/data
```

适合：
- Web 面板类
- 单服务类工具
- 数据只需要保存在项目目录内

我的默认优先级也应是这一类，因为最整洁、最好维护。

---

### 2. 单容器 + 多文件映射
典型项目：
- `wanou_url`
- `CPAMC`
- `cliproxy`

常见结构：
- 把项目目录下的配置文件、脚本文件、文本列表文件逐个映射进容器

例如：

```yml
volumes:
  - ./config.yaml:/app/config.yaml
  - ./proxy.js:/app/proxy.js:ro
  - ./logs:/app/logs
```

适合：
- 配置文件驱动型服务
- 需要热修改脚本/文本源的项目
- 需要把宿主机文件直接作为容器内入口文件的项目

这类项目的核心思路不是“大目录一把挂”，而是：
**哪些文件要长期维护，就显式逐条映射。**

---

### 3. 单容器 + 宿主大目录直挂
典型项目：
- `alist`
- `alist-tvbox`

常见结构：

```yml
volumes:
  - './data:/opt/alist/data'
  - '/www/manmanai:/www/manmanai'
```

适合：
- 文件管理器
- WebDAV / 挂载盘 / 索引服务
- 需要直接访问宿主机大资源目录的项目

后续如果我要给你写这类 yml，重点不是只把应用跑起来，而是先确认：
1. 容器里哪个目录负责程序数据
2. 宿主机哪个大目录需要暴露进去
3. 是否只读挂载

---

### 4. 多容器协同型
典型项目：
- `immich`
- `pansou/pancheck`
- `pansou`（主服务 + autoheal）

常见结构：
- 主服务
- 数据库/缓存
- 健康检查或辅助容器
- `depends_on`
- 分别声明持久化目录

例如：
- `pancheck` = 主程序 + MySQL + Redis
- `immich` = 主服务 + 机器学习 + Redis + Postgres
- `pansou` = 主服务 + autoheal

适合：
- 有数据库依赖的后台
- 有缓存层的服务
- 需要自动恢复或分工明确的完整项目

后续我如果要自己补这类 compose，应该先拆清楚：
1. 主服务是谁
2. 是否需要数据库
3. 是否需要 Redis
4. 数据目录各自落哪里
5. 容器之间服务名如何互相引用

---

### 5. 运行时命令型 / 临时装依赖型
典型项目：
- `wanou_url`
- `zhibo/yspapp`

常见结构：

```yml
command: >
  sh -c "
  npm install ... &&
  node app.js"
```

或者：

```yml
command: >
  sh -c "
  apk add --no-cache ... &&
  /app/xxx"
```

适合：
- 没单独镜像、直接拿基础镜像跑脚本
- 临时补依赖
- 二进制程序直接挂进去运行

这类写法虽然灵活，但稳定性弱于“直接用现成镜像”。
如果后续我来新建项目，除非确实没有更合适镜像，否则不优先走这一类。

## 三、你这套环境里的路径映射方法

### 1. 最常见的相对路径映射
这是你这里最主流、也最推荐我继续沿用的方式：

```yml
volumes:
  - ./data:/app/data
  - ./config:/app/config
  - ./logs:/app/logs
```

优点：
- 项目自包含
- 迁移简单
- 看目录就知道数据在哪
- 手动维护最方便

默认适合：
- 绝大多数新项目

---

### 2. 项目内部子目录做绝对路径映射
典型于已有固定数据目录或子项目目录明确时：

```yml
- /www/manmanai/docker/pansou/data:/app/data
- /www/manmanai/docker/pansou/pancheck/mysql_data:/var/lib/mysql
```

适合：
- 多服务项目
- 需要非常明确区分不同服务数据目录
- 项目本身已经形成固定结构

我后续补写时可以这样判断：
- 单服务项目，优先 `./data`
- 多服务项目，优先项目目录下分子目录，如：
  - `./mysql_data`
  - `./redis-data`
  - `./cache`
  - `./config`

---

### 3. 宿主机系统路径映射
典型映射：

```yml
- /var/run/docker.sock:/var/run/docker.sock
- /etc/localtime:/etc/localtime:ro
```

用途：
- `docker.sock` 给 watchtower、autoheal、面板类容器控制 Docker
- `localtime` 让容器时间和宿主机一致

后续原则：
- 只有确实需要控制 Docker 的项目，才挂 `docker.sock`
- 时间同步可按需要挂 `localtime`
- 不无脑给高权限映射

---

### 4. 单文件映射
典型写法：

```yml
- ./config.yaml:/app/config.yaml
- ./proxy-multi.js:/app/proxy.js:ro
- ./xxx.txt:/app/servers_1.txt:ro
```

适合：
- 配置文件
- 启动脚本
- 规则列表
- 线路清单

这也是你这里很重要的一种“路径映射方法”：
**不是只映射目录，也会把宿主机中的关键单文件直接映射成容器内的标准文件名。**

以后如果项目没有现成 yml，但有：
- 一个主脚本
- 几个配置文件
- 几个文本源

那我就应该优先想到这种写法。

## 四、端口映射风格

你这里几乎统一是：

```yml
ports:
  - "宿主端口:容器端口"
```

特点：
- 宿主端口都比较明确
- 一个项目可能映射多个端口
- 有些项目按序号规律分配，例如 `wanou_url`

以后我补 yml 时应该：
1. 先避开已占用端口
2. 尽量保持同类项目端口有规律
3. 如果一个容器提供多个服务，按功能连续映射更好维护

## 五、命名习惯

### 1. `container_name` 基本都会写
你这里大部分项目都显式写了 `container_name`。

好处：
- 好找
- 好管
- 手动执行 `docker logs` / `docker exec` / `docker inspect` 更方便

所以后续我自己写 yml 时，也应默认补上 `container_name`。

---

### 2. 服务名和容器名不一定一样
例如：
- 服务名：`codex-web`
- 容器名：`wenfxl_codex`

这说明你更看重“容器实际用途名”，而不强制服务名等于容器名。

以后我应这样处理：
- `services` 下的名字用于 compose 内部引用
- `container_name` 用你实际维护时最容易认的名字

## 六、环境变量写法

常见几类：
- 基础环境变量
- 代理变量
- 密码/认证变量
- 时区变量
- 项目业务配置

你这里常用写法是：

```yml
environment:
  - TZ=Asia/Shanghai
  - KEY=value
```

但像 `immich` 这类复杂项目，也会改用：

```yml
env_file:
  - .env
```

后续默认策略：
- 简单项目，直接写 `environment`
- 复杂项目或变量多，优先 `.env`
- 敏感信息尽量集中在 `.env`，不要散在多个地方

## 七、健康检查与自动维护

你这里已经出现了两种重要模式：

### 1. `healthcheck`
适合主服务健康探测。

### 2. `watchtower` / `autoheal`
适合：
- 自动更新
- 自动重启异常容器

说明你这套环境不只是“能跑”，而是已经开始偏“持续维护型”。

以后我写新项目 yml 时，应该评估：
- 需不需要健康检查
- 需不需要自动恢复
- 需不需要显式禁止 watchtower 更新

## 八、我从现有项目里学到的默认生成策略

以后如果一个项目没有现成 yml，我默认按下面顺序思考：

### 情况 A：普通单服务 Web 项目
默认骨架：

```yml
services:
  app:
    image: xxx:latest
    container_name: 项目名
    restart: unless-stopped
    ports:
      - "宿主端口:容器端口"
    volumes:
      - ./data:/app/data
    environment:
      - TZ=Asia/Shanghai
```

### 情况 B：配置驱动型项目
在 A 的基础上加：

```yml
    volumes:
      - ./config:/app/config
      - ./config.yaml:/app/config.yaml
```

### 情况 C：脚本驱动型项目
在 A 的基础上加：

```yml
    working_dir: /app
    command: >
      sh -c "
      安装依赖 &&
      启动脚本"
    volumes:
      - ./main.js:/app/main.js:ro
      - ./data:/app/data
```

### 情况 D：带数据库项目
拆成：
- 主服务
- db
- redis（如果需要）
- 各自独立数据目录

## 九、后续我给你写 yml 时的实际落地规则

以后我会优先遵守下面这些：

1. **先建项目目录，再写 compose**
2. **优先用相对路径挂载项目内数据目录**
3. **需要宿主大目录时，再补绝对路径映射**
4. **需要配置文件时，优先单文件映射**
5. **默认显式写 `container_name`**
6. **默认加 `restart` 策略**
7. **简单项目直接 `environment`，复杂项目再用 `.env`**
8. **尽量把数据、配置、脚本都收在项目目录里**
9. **只有确实需要时才挂 `docker.sock` 或其他高权限路径**
10. **升级时始终按你定的项目目录流程走，不跨目录乱操作**

## 十、特别提醒

这批 yml 里也有一些我已经看到的现实情况，后续写新文件时要避开：

- 有些项目仍带旧的 `version` 字段，当前能用，但新写文件没必要强依赖它
- 个别项目存在格式不够规整、重复环境变量、注释与内容混排等情况
- 个别项目把敏感值直接写在 yml 里，后续如果是我新建项目，除非你明确要求，否则我会更倾向改成 `.env`
- 存在子项目目录，例如：
  - `pansou/p2t`
  - `pansou/pancheck`
  - `zhibo/*`
  说明有些大类项目下还会分功能子项目，后续我也应保留这种层次化组织方式

## 十一、结论

我已经学到你这套 Docker 管理的核心不是“把容器跑起来”，而是三件事：

1. **项目目录独立**
2. **路径映射清晰可维护**
3. **后续升级和手动维护方便**

以后如果遇到没有现成 yml 的项目，我会优先按你现有风格：
- 在 `/www/manmanai/docker/<项目名>/` 建目录
- 优先用相对路径组织 `data/config/logs`
- 需要时再补绝对路径映射
- 写好 `docker-compose.yml` 后在项目目录里启动和升级
