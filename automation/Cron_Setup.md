# 如何将自动化抓取部署为定时任务 (Cron Job)

你提到希望这个工具是**“定时自动执行”**的。针对我们现在的系统架构，最简单且免费的方案是使用 **GitHub Actions** 配合 **Vercel** 发布。

每次脚本运行完抓取新游戏后，只需要把新生成的网页文件、图片自动提交（commit）到 GitHub 代码库，Vercel 就会自动捕捉到更新并为你发布新版本。

## 配置步骤：使用 GitHub Actions (推荐)

在我们的项目目录下，创建一个 `.github/workflows/auto_scraper.yml` 文件。这段代码会告诉服务器：“每天早上 8 点钟，自动运行我们的 `main.py` 脚本寻找新游戏，然后更新网站”。

### 步骤 1: 创建配置文件

你可以直接将这个文件内容放在项目中：
`bearclicker.net/.github/workflows/auto_scraper.yml`

```yaml
name: Auto Game Scraper

on:
  schedule:
    # 每天 UTC 时间 0:00 (北京时间早上 8:00) 自动执行
    - cron: '0 0 * * *'
  # 同时也保留手动点击触发的按钮（方便你随时想立刻抓游戏测试）
  workflow_dispatch:

jobs:
  scrape-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: 检出代码
        uses: actions/checkout@v3

      - name: 设置 Python 环境
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: 安装运行必需插件
        run: |
          pip install requests beautifulsoup4 python-dotenv openai

      - name: 运行自动化抓取与部署脚本
        env:
          # 如果你的AI优化用到了API密钥，在这里传入
          OPENAI_API_KEY: ${{{{ secrets.OPENAI_API_KEY }}}} 
        run: |
          python automation/main.py

      - name: 提交新游戏文件并推送到 GitHub
        run: |
          git config --global user.name "Auto Bot"
          git config --global user.email "bot@bearclicker.net"
          # 如果脚本没有生成新文件，就不会报错
          git add .
          git commit -m "Auto: Added new games via Scraper bot" || echo "No changes to commit"
          git push
```

### 步骤 2: 它是怎么运作的？

1. **自动执行**：每天北京时间早上 8 点，GitHub 会自动启动一台虚拟电脑。
2. **抓取**：在这台虚拟电脑上运行我们的 `automation/main.py` 脚本，去 `cookie-clicker2.com` 找最近的1-2个新游戏。
3. **AI生成**：它会联网生成符合字数要求（标题 < 60个字，描述 < 160个字）的顶级 TDK 和 常见问答 FAQ。
4. **生成代码**：生成你经常看到的漂亮的新内页 `templates/新游戏.html`。
5. **保存并发布**：它把这些新代码和图片推送回主代码库。由于你之前部署在了 Vercel，Vercel 只要看到主库有代码进来，就会立刻在几秒钟内把新游戏上线到玩家的面前！

这套方案**完全不需要你每天手动开电脑去跑脚本**，全自动实现了“监控 -> 下载 -> AI 重写文案 -> 建网页 -> 发布上线”的全自动化流水线。
