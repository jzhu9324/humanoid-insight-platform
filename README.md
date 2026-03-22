# 人形机器人洞察平台

> 基于 Claude AI 的人形机器人行业洞察与分析平台

[![Deploy](https://github.com/jzhu9324/humanoid-insight-platform/workflows/Deploy%20VitePress%20Site/badge.svg)](https://github.com/jzhu9324/humanoid-insight-platform/actions)
[![Data Collection](https://github.com/jzhu9324/humanoid-insight-platform/workflows/Data%20Collection%20Workflow/badge.svg)](https://github.com/jzhu9324/humanoid-insight-platform/actions)

## 📖 项目简介

人形机器人洞察平台是一个自动化的行业分析工具，利用 Claude AI 的强大分析能力，为您提供人形机器人领域的全方位洞察。

### ✨ 核心特性

- 🤖 **AI 驱动分析**: 使用 MiniMax M2.5 进行智能内容分析和总结
- 📚 **学术论文追踪**: 自动收集 Semantic Scholar、HuggingFace Papers 和 arXiv 最新论文，深度解读核心观点和技术亮点
- 🏢 **公司动态监控**: 追踪 10 家头部公司（Tesla、Boston Dynamics、Figure AI 等）的最新进展
- 📰 **全网新闻聚合**: 13 个专业新闻源（TechCrunch、IEEE Spectrum、Reddit 等）+ Google News 全网搜索
- 📱 **行业资讯汇总**: 9 个微信公众号优质内容，覆盖行业分析和市场趋势
- 📊 **智能报告生成**: 自动生成日报，提供趋势分析和行业洞察
- ⚡ **每日自动更新**: 每天 2 次自动化数据收集（08:00 和 20:00 北京时间）
- 🔄 **智能去重**: 自动过滤重复内容，确保信息新鲜度
- 🎨 **优雅的界面**: 基于 VitePress，简洁现代
- ⚙️ **在线配置管理**: 通过网页直接编辑数据源配置

## 🚀 快速开始

### 在线访问

🌐 **网站**: https://jzhu9324.github.io/humanoid-insight-platform/

⚙️ **配置管理**: https://jzhu9324.github.io/humanoid-insight-platform/config

📚 **完整文档**: [维护指南](docs/maintenance-guide.md) | [快速参考](docs/quick-reference.md)

### 前置要求

- Node.js 18+
- Python 3.11+
- MiniMax API Key (用于 AI 分析)

### 安装

1. 克隆仓库

```bash
git clone https://github.com/jzhu9324/humanoid-insight-platform.git
cd humanoid-insight-platform
```

2. 安装 Node.js 依赖

```bash
npm install
```

3. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

4. 配置环境变量

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 本地开发

启动开发服务器:

```bash
npm run docs:dev
```

访问 http://localhost:5173 查看网站。

### 构建部署

构建生产版本:

```bash
npm run docs:build
```

预览构建结果:

```bash
npm run docs:preview
```

## 📊 数据收集

### 数据源统计

**总计：28 个 RSS 源**

#### 🏢 公司数据源（10 家公司，15 个 RSS）
- Tesla (Optimus)
- Boston Dynamics (Atlas)
- Figure AI
- Agility Robotics (Digit)
- Sanctuary AI (Phoenix)
- Unitree Robotics
- 优必选 (UBTECH Walker)
- 小米机器人 (CyberOne)
- 1X Technologies (NEO)
- Sunday Robotics

#### 📰 通用新闻源（13 个）
- TechCrunch Robotics
- IEEE Spectrum Robotics
- The Verge Robotics
- VentureBeat AI
- MIT News AI
- Ars Technica Robotics
- Wired AI
- ZDNet Robotics
- ScienceDaily Robotics
- Robotics Business Review
- The Robot Report
- Reddit r/robotics
- Reddit r/robotics humanoid search

#### 💬 微信公众号（9 个）
- 机器人大讲堂、机器人在线、高工机器人
- 智东西、量子位、机器之心
- 新智元、36氪、钛媒体

### 自动收集时间表

| 时间 | 任务 |
|------|------|
| **08:00 北京时间** | 📄 论文 + 🏢 公司动态 + 💬 微信 + 📊 日报 |
| **20:00 北京时间** | 🏢 公司动态 + 💬 微信（第二次） |

### 手动收集

收集学术论文:

```bash
python scripts/collect_papers.py
```

收集公司动态:

```bash
python scripts/collect_company_news.py
```

收集微信文章:

```bash
# 首先在 config/wechat_urls.txt 中添加文章链接
python scripts/collect_wechat_articles.py
```

生成报告:

```bash
# 生成周报
python scripts/generate_report.py --type weekly

# 生成日报
python scripts/generate_report.py --type daily
```

### 自动收集

项目配置了 GitHub Actions 工作流，自动运行数据收集和报告生成。

#### 核心特性

- ✅ **智能去重**: 自动检查过去 14 天的历史，避免重复收录
- ✅ **多源聚合**: 28 个 RSS 源 + Google News 全网搜索
- ✅ **AI 分析**: MiniMax M2.5 自动生成摘要和分析
- ✅ **自动部署**: 数据更新后自动触发网站重新部署
- ✅ **错误处理**: 单个源失败不影响整体收集

#### GitHub Actions 配置

- **运行时间**: 每天 00:00 和 12:00 UTC（北京时间 08:00 和 20:00）
- **工作流文件**: `.github/workflows/data-collection.yml`
- **必需配置**: 在 GitHub 仓库设置中添加 `MINIMAX_API_KEY` secret

#### 手动触发

1. 访问 [GitHub Actions](https://github.com/jzhu9324/humanoid-insight-platform/actions/workflows/data-collection.yml)
2. 点击 "Run workflow" 按钮
3. 等待 5-10 分钟查看结果

## 🏗️ 项目结构

```
humanoid-insight-platform/
├── .github/
│   └── workflows/          # GitHub Actions 工作流
│       ├── data-collection.yml  # 数据收集工作流
│       └── deploy.yml           # 网站部署工作流
├── docs/                   # VitePress 文档目录
│   ├── .vitepress/        # VitePress 配置
│   │   ├── config.js      # 站点配置
│   │   └── theme/         # 自定义主题
│   ├── public/            # 静态资源
│   │   └── admin/         # Netlify CMS 配置
│   ├── daily/             # 每日精选
│   ├── papers/            # 学术论文
│   ├── company-news/      # 公司动态
│   ├── wechat/            # 微信文章
│   ├── reports/           # 行业报告
│   └── index.md           # 首页
├── scripts/               # Python 脚本
│   ├── utils/             # 工具模块
│   │   └── ai_analyzer.py      # AI 分析工具
│   ├── collect_papers.py       # 论文收集脚本
│   ├── collect_company_news.py # 公司动态收集脚本
│   ├── collect_wechat_articles.py # 微信文章收集脚本
│   └── generate_report.py      # 报告生成脚本
├── cache/                 # 数据缓存（JSON格式）
├── config/                # 配置文件
│   └── wechat_urls.txt    # 微信文章URL列表
├── logs/                  # 日志文件
├── tests/                 # 测试文件
├── package.json           # Node.js 依赖
├── requirements.txt       # Python 依赖
└── README.md              # 项目文档
```

## 🔧 配置

### MiniMax API

1. 获取 API Key: https://platform.minimaxi.com/
2. 设置环境变量:
   ```bash
   export MINIMAX_API_KEY="your-api-key-here"
   ```
3. 或在 GitHub 仓库设置中添加 Secret (用于 GitHub Actions)

### 在线配置管理

访问 https://jzhu9324.github.io/humanoid-insight-platform/config 可以直接在网页上编辑数据源配置，无需手动修改 JSON 文件。

### 数据源配置文件

配置文件位置：`config/sources.json`

#### 添加新公司

```json
{
  "name": "公司名称",
  "name_cn": "中文名称",
  "rss_feeds": [
    "https://example.com/rss",
    "https://news.google.com/rss/search?q=公司名称+humanoid+robot"
  ],
  "website": "https://example.com",
  "keywords": ["humanoid", "robot"]
}
```

#### 添加新闻源

```json
{
  "name": "新闻源名称",
  "rss_feed": "https://example.com/feed/",
  "keywords": ["humanoid", "robot", "robotics"]
}
```

详细配置说明请参考 [维护指南](docs/maintenance-guide.md)。

## 📝 内容管理

### 在线配置

访问 `/config` 路径使用在线配置管理器，支持：
- 添加/编辑公司数据源
- 添加/编辑通用新闻源
- 管理微信公众号
- 配置论文关键词

所有修改会自动提交到 GitHub 仓库。

## 📚 文档

- 📖 [完整维护指南](docs/maintenance-guide.md) - 详细的使用和维护说明
- 🚀 [快速参考](docs/quick-reference.md) - 常用操作和故障排查
- 📈 [数据源扩展计划](docs/data-sources-expansion-plan.md) - 未来扩展方向

## 🎯 最近更新 (2026-03-22)

### 新增功能
- ✅ 添加 13 个通用新闻源（TechCrunch、IEEE Spectrum、Reddit 等）
- ✅ 添加 Reddit 数据源（r/robotics）
- ✅ 智能去重系统（检查过去 14 天历史）
- ✅ 自动生成 index 页面
- ✅ 在线配置管理器
- ✅ 完整的维护文档

### 优化改进
- ✅ 收集时间范围从 2 天扩大到 7 天
- ✅ 在收集阶段就过滤重复内容
- ✅ 没有新内容时不生成空文件
- ✅ 改进 RSS 抓取的错误处理
- ✅ 优化日志输出，添加统计信息

### 修复问题
- ✅ 修复网站不自动更新的问题（移除 `[skip ci]`）
- ✅ 修复 papers/company-news/reports 列表不更新
- ✅ 修复 sources.json merge conflict
- ✅ 修复重复收录旧新闻的问题

## 🧪 测试

运行测试:

```bash
pytest tests/ -v
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

- GitHub: [@jzhu9324](https://github.com/jzhu9324)
- 项目地址: https://github.com/jzhu9324/humanoid-insight-platform

## 🙏 致谢

- [Claude AI](https://claude.ai) - 提供强大的 AI 分析能力
- [VitePress](https://vitepress.dev) - 优秀的静态站点生成器
- [Anthropic](https://anthropic.com) - 设计灵感来源

---

**由 Claude Opus 4.5 协助构建** 🤖
