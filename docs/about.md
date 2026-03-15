---
title: 项目说明
---

# 项目说明

## 基本信息

- GitHub: [jzhu9324/humanoid-insight-platform](https://github.com/jzhu9324/humanoid-insight-platform)
- 网站: [jzhu9324.github.io/humanoid-insight-platform](https://jzhu9324.github.io/humanoid-insight-platform/)
- 技术栈: VitePress + Python + GitHub Actions + MiniMax AI

## 自动化更新

| 时间 | 任务 |
|------|------|
| 每天 08:00 北京时间 | 论文 + 公司动态 + 微信文章 + 日报 |
| 每天 20:00 北京时间 | 公司动态 + 微信文章（第二次） |

## 论文收集逻辑

优先级从高到低：

1. **HuggingFace Papers** — 社区投票热门论文
2. **Semantic Scholar** — 顶级机构/高引用论文
3. **arXiv** — 关键词搜索兜底

## 公司动态收集

- 每家公司配置 RSS + Google News 全网搜索
- 无 RSS 时自动生成 Google News 搜索源
- 覆盖最近 2 天内容

## 配置管理

在 [配置管理页面](/config) 可以在线管理：
- 监控公司列表
- 论文搜索关键词
- 微信公众号列表

需要 GitHub Personal Access Token（repo 权限）。

## 本地开发

```bash
# 安装依赖
npm install
pip install -r requirements.txt

# 本地预览
npm run docs:dev

# 构建测试（push 前必须通过）
npm run docs:build

# 手动收集数据
python scripts/collect_papers.py
python scripts/collect_company_news.py
python scripts/generate_report.py --type daily
```

## 环境变量

| 变量 | 用途 |
|------|------|
| `MINIMAX_API_KEY` | MiniMax AI 分析（GitHub Secret） |
