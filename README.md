# 人形机器人洞察平台

> 基于 Claude AI 的人形机器人行业洞察与分析平台

[![Deploy](https://github.com/jzhu9324/humanoid-insight-platform/workflows/Deploy%20VitePress%20Site/badge.svg)](https://github.com/jzhu9324/humanoid-insight-platform/actions)
[![Data Collection](https://github.com/jzhu9324/humanoid-insight-platform/workflows/Data%20Collection%20Workflow/badge.svg)](https://github.com/jzhu9324/humanoid-insight-platform/actions)

## 📖 项目简介

人形机器人洞察平台是一个自动化的行业分析工具，利用 Claude AI 的强大分析能力，为您提供人形机器人领域的全方位洞察。

### ✨ 核心特性

- 🤖 **AI 驱动分析**: 使用 Claude Opus 4 和 Haiku 进行智能内容分析和总结
- 📚 **学术论文追踪**: 自动收集 arXiv 最新论文，深度解读核心观点和技术亮点
- 🏢 **公司动态监控**: 追踪 Tesla、Boston Dynamics、Figure AI 等头部公司的最新进展
- 📱 **行业资讯汇总**: 精选微信公众号优质内容，覆盖行业分析和市场趋势
- 📊 **智能报告生成**: 自动生成周报，提供趋势分析和行业洞察
- ⚡ **每日自动更新**: 通过 GitHub Actions 自动化数据收集和内容生成
- 🎨 **优雅的界面**: 基于 VitePress 和 Anthropic 设计风格，简洁现代

## 🚀 快速开始

### 前置要求

- Node.js 18+
- Python 3.11+
- Anthropic API Key

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

项目配置了 GitHub Actions 工作流，自动运行数据收集和报告生成:

#### 更新频率设置

- **论文收集**: 每 3-4 天（半周）更新一次，只收集半周内新发布的论文
- **公司动态**: 每天更新，获取最新行业新闻
- **微信文章**: 根据配置文件手动添加，每天检查
- **行业报告**: 每周生成一次

#### GitHub Actions 配置

- 运行时间: 每天 00:00 UTC (北京时间 08:00)
- 工作流文件: `.github/workflows/data-collection.yml`
- 需要配置: 在 GitHub 仓库设置中添加 `MINIMAX_API_KEY` secret（用于 AI 分析）

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

### 数据收集配置

#### 论文收集 (collect_papers.py)

- 关键词: 在脚本中的 `HUMANOID_KEYWORDS` 列表中配置
- 相关性阈值: `RELEVANCE_THRESHOLD` (默认 0.6)
- **查询范围**: `days_back` (默认 3-4 天，半周更新)
- **建议更新频率**: 每 3-4 天运行一次，确保覆盖最新发布的论文

#### 公司动态 (collect_company_news.py)

- 监控公司: 在脚本中的 `COMPANIES` 字典中配置
- RSS 订阅源: 为每个公司配置 `rss_feeds`
- 关键词过滤: 为每个公司配置 `keywords`
- **查询范围**: `days_back` (默认 1 天，每日更新)
- **建议更新频率**: 每天运行一次，获取最新行业动态

#### 微信文章 (collect_wechat_articles.py)

- 文章链接: 在 `config/wechat_urls.txt` 中添加（每行一个）
- 关键词过滤: 在脚本中的 `HUMANOID_KEYWORDS` 列表中配置

## 📝 内容管理

### Netlify CMS

访问 `/admin/` 路径使用 Netlify CMS 进行内容管理（需要配置 Git Gateway）。

支持管理:
- 学术论文
- 公司动态
- 微信文章
- 行业报告
- 页面内容

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
