# Bear Clicker - 在线游戏平台 (v1.0.0)

Bear Clicker 是一个提供多种点击类游戏的在线游戏平台，用户可以在这里体验各种有趣的点击游戏，包括农场模拟、动物收集、冒险等多种类型。

## 功能特点

### 1. 游戏内容
- 丰富多样的游戏类型（包括 Capybara Clicker, Little Farm Clicker, Cookie Clicker 等40+款游戏）
- 每个游戏都有独特的视觉设计和游戏机制
- 支持在线游玩和体验
- 游戏内嵌功能，提供沉浸式体验

### 2. 平台功能
- 响应式设计，完美支持移动端和桌面端
- SEO优化，提高游戏在搜索引擎中的可见性
- 动态FAQ系统，为用户提供游戏相关问答
- 多语言支持（通过翻译文件配置）
- 游戏API集成，支持多种访问方式

### 3. 技术特性
- 现代化UI设计，使用渐变色和动画效果
- 优化的游戏加载机制
- 完善的错误处理和日志系统
- 支持Vercel部署，简化发布流程

## 技术栈

- **后端**：Flask (Python)
- **前端**：HTML + Tailwind CSS + Alpine.js
- **部署**：Vercel
- **分析**：Google Analytics, Plausible Analytics, Microsoft Clarity
- **其他**：Jinja2模板引擎

## 项目结构

```
bearclicker/
├── app.py              # Flask应用主文件，包含所有路由
│   # 主要功能：首页、游戏页面路由、用户认证、API集成
├── api/                # API目录
│   └── game_api.py     # 游戏API实现
│       # 主要功能：加载游戏配置、处理游戏请求、返回游戏内容
├── config/             # 配置文件目录
│   └── logging_config.py # 日志配置
├── models.py           # 数据模型
│   # 主要模型：User(用户)、Message(消息)、ImageGeneration(图片生成)、Payment(支付)
├── static/             # 静态资源
│   ├── css/            # 样式文件
│   │   └── tailwind.css  # Tailwind CSS样式
│   ├── js/             # JavaScript文件
│   │   ├── alpine.js    # Alpine.js框架
│   │   └── analytics.js # 分析跟踪脚本
│   ├── images/         # 图片资源
│   │   ├── games/      # 游戏预览图
│   │   └── favicon/    # 游戏图标
│   ├── data/           # 配置数据
│   │   ├── faqs.json    # FAQ数据
│   │   ├── paper.json   # 纸张游戏配置
│   │   └── translations.json # 多语言翻译
│   └── game-config/    # 游戏配置
│       └── games.json   # 游戏列表配置
├── templates/          # HTML模板
│   ├── base.html       # 基础模板（包含SEO标签、样式、脚本）
│   ├── components/     # 可重用组件
│   │   ├── hero.html        # 英雄区域（游戏标题、描述、按钮）
│   │   ├── nav.html         # 导航栏
│   │   ├── footer.html      # 页脚
│   │   ├── faq_section.html # FAQ部分
│   │   ├── trending_games.html # 热门游戏推荐
│   │   ├── trending_videos.html # 热门视频
│   │   ├── paper.html       # 纸张游戏组件
│   │   └── affiliate_banner.html # 联盟营销横幅
│   ├── index.html      # 首页模板
│   ├── game-template.html # 纯游戏页面模板
│   └── *.html          # 各游戏介绍页面模板
├── vercel.json         # Vercel部署配置
│   # 包含路由、环境变量、构建命令等
├── requirements.txt    # Python依赖
├── .env                # 环境变量（本地开发用）
└── .env.example        # 环境变量示例
```

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
- 复制 `.env.example` 为 `.env`
- 填写必要的环境变量（如SECRET_KEY等）

3. 运行应用：
```bash
python app.py
```
应用将在 http://localhost:5002 运行

## 访问方式

### 游戏介绍页面
- URL格式：`https://bearclicker.net/[game-id]`
- 示例：`https://bearclicker.net/little-farm-clicker`
- 内容：游戏介绍、游戏嵌入框、相关游戏推荐、FAQ等

### 纯游戏页面
- URL格式：`https://bearclicker.net/game/[game-id]`
- 示例：`https://bearclicker.net/game/little-farm-clicker`
- 内容：纯游戏页面，使用game-template.html模板
- 特点：沉浸式游戏体验，底部有链接回到主站

## 添加新游戏

1. 在 `templates/` 目录下创建新的游戏页面模板（如 `new-game-clicker.html`）
2. 在 `app.py` 中添加对应的路由函数
3. 在 `static/images/games/` 目录下添加游戏预览图
4. 在 `static/images/favicon/` 目录下添加游戏图标
5. 如需通过API访问，在 `static/game-config/games.json` 中添加游戏配置

## 自动化工具

当前仓库中的自动化主链路已经从早期方案演进为以 `automation/daily_update.py` 为核心的生产流程。

如需了解完整实现细节，可参考：

- `自动抓取游戏内页逻辑说明.md`
- `自动化抓取与AI优化方案.md`

### 当前实际使用的自动化入口

- **生产定时任务**：`.github/workflows/auto_scraper.yml`
- **实际执行脚本**：`automation/daily_update.py`
- **执行频率**：每天 1 次
- **执行时间**：UTC 23:45，约等于北京时间 07:45

GitHub Actions 会在脚本跑完后自动：

1. 提交生成的页面和资源变更
2. 推送到 `main`

如需同时自动通知 Google Search Console 提交 sitemap，请配置以下 GitHub Secrets：

- `GOOGLE_SEARCH_CONSOLE_SITE_URL`
- `GOOGLE_SEARCH_CONSOLE_SITEMAP_URL`（可选，默认 `https://bearclicker.net/sitemap.xml`）
- `GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_JSON`

说明：

- `GOOGLE_SEARCH_CONSOLE_SITE_URL` 可以是 URL-prefix property，例如 `https://bearclicker.net/`
- 也可以是 Domain property，例如 `sc-domain:bearclicker.net`
- Search Console 中需要把对应 service account 加为该站点属性的 owner

### 当前自动化流程

1. 从源站 `cookie-clicker2.com/new-games` 获取最新游戏 slug
2. 用 `static/game-config/games.json` 判断哪些游戏已经发布过
3. 如果当天新游戏不足目标数，就从 `automation/pending_games_list.txt` 补足
4. 抓取详情页，提取标题、描述、正文、图片和 iframe 地址
5. 递归解析 iframe，尽量拿到真实游戏源地址
6. 调用 AI 生成 TDK 和 FAQ
7. 生成站内详情页模板、缩略图、favicon、FAQ 数据和 sitemap
8. 更新 `static/game-config/games.json`，让 `/game/<slug>` 可以加载真实游戏
9. 提交 IndexNow、向 Google Search Console 提交 sitemap，并发送飞书通知

### 关键自动化文件

```text
automation/
├── daily_update.py       # 当前生产主入口
├── scraper.py            # 单页抓取、iframe 下钻、sitemap 辅助逻辑
├── build_image_map.py    # 从竞品列表页建立 slug -> 图片映射
├── ai_optimizer.py       # 生成 SEO 标题、描述、关键词和 FAQ
├── template_generator.py # 生成模板、图片、路由、games.json 和 sitemap
├── webhook_sender.py     # 飞书通知
├── pending_games_list.txt # 新游戏不足时的补位队列
└── main.py               # 旧入口，保留作 legacy / 本地测试参考
```

### 当前状态口径

- **已发布游戏集合**：以 `static/game-config/games.json` 为准
- **游戏详情页 URL**：`/<slug>`
- **纯游戏容器页 URL**：`/game/<slug>`

### 关于旧代码

`automation/main.py` 和 `automation/processed_games.json` 属于早期自动化链路遗留内容。当前生产环境不再依赖它们判断每日抓取目标，主逻辑以 `daily_update.py` 和 `static/game-config/games.json` 为准。

## 最近工作

- 梳理并文档化了当前“竞品游戏详情页抓取 -> 站内页生成 -> 自动发布”的真实实现链路，新增了 `自动抓取游戏内页逻辑说明.md`
- 更新了 README 中的自动化说明，明确当前生产入口是 `automation/daily_update.py`，而不是旧的 `automation/main.py`
- 核对了当前定时任务来源，确认生产环境由 GitHub Actions `.github/workflows/auto_scraper.yml` 每天执行自动更新
- 补充了 Google Search Console 自动提交通道：发布新内页后会自动向 GSC 提交 `sitemap.xml`
- 为 GitHub Actions 增加了 GSC 相关环境变量说明和依赖配置，便于后续直接接入 service account
- 对抓取覆盖率做了基线核对：当前项目已发布页数以 `static/game-config/games.json` 为准，和竞品目录页口径之间仍存在较大缺口

## 待办

- 在 GitHub Secrets 中补齐 `GOOGLE_SEARCH_CONSOLE_SITE_URL`、`GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_JSON` 等配置，并完成一次真实 GSC 提交验证
- 将 `automation/Cron_Setup.md` 改写为和当前生产流程一致，避免继续引用旧的 `main.py`
- 继续清理自动化冗余代码，逐步弱化 `automation/main.py`、`automation/processed_games.json` 等 legacy 入口
- 建立“缺失竞品页列表”的持续更新机制，方便按优先级回补还未抓取的游戏内页
- 评估是否要提高每日抓取数量或拆分任务并行执行，否则按当前节奏追平竞品仍需要较长周期

## 部署

项目使用Vercel进行部署，详细部署方案见 `Vercel部署方案.md`。

### 自定义域名

项目支持使用自定义域名，如 `game.bearclicker.net`，配置步骤包括：

1. 在配置文件中添加域名设置
2. 在Vercel平台配置自定义域名
3. 在DNS提供商添加相应的CNAME或A记录

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 许可证

版权所有 © 2025 Bear Clicker
