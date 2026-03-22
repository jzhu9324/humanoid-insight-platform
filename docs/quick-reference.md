# 人形机器人洞察平台 - 快速参考

## 🚀 快速链接

| 功能 | 链接 |
|------|------|
| 🌐 网站首页 | https://jzhu9324.github.io/humanoid-insight-platform/ |
| ⚙️ 在线配置 | https://jzhu9324.github.io/humanoid-insight-platform/config |
| 🔄 GitHub Actions | https://github.com/jzhu9324/humanoid-insight-platform/actions |
| 📊 数据收集 Workflow | https://github.com/jzhu9324/humanoid-insight-platform/actions/workflows/data-collection.yml |
| 🚀 部署 Workflow | https://github.com/jzhu9324/humanoid-insight-platform/actions/workflows/deploy.yml |
| 📝 完整文档 | [maintenance-guide.md](./maintenance-guide.md) |
| 📈 扩展计划 | [data-sources-expansion-plan.md](./data-sources-expansion-plan.md) |

---

## 📊 当前配置一览

```
📦 数据源总计: 28 个 RSS 源
├─ 🏢 公司 RSS: 15 个（10 家公司）
├─ 📰 通用新闻: 13 个
├─ 💬 微信公众号: 9 个
└─ 📄 论文关键词: 12 个
```

### 公司列表
1. Tesla (Optimus)
2. Boston Dynamics (Atlas)
3. Figure AI
4. Agility Robotics (Digit)
5. Sanctuary AI (Phoenix)
6. Unitree Robotics
7. 优必选 (UBTECH Walker)
8. 小米机器人 (CyberOne)
9. 1X Technologies (NEO)
10. Sunday Robotics

### 通用新闻源
1. TechCrunch Robotics
2. IEEE Spectrum Robotics
3. The Verge Robotics
4. VentureBeat AI
5. MIT News AI
6. Ars Technica Robotics
7. Wired AI
8. ZDNet Robotics
9. ScienceDaily Robotics
10. Robotics Business Review
11. The Robot Report
12. Reddit r/robotics
13. Reddit r/robotics humanoid search

---

## ⏰ 自动化时间表

| 时间 | 任务 |
|------|------|
| **08:00 北京时间** | 📄 论文 + 🏢 公司动态 + 💬 微信 + 📊 日报 |
| **20:00 北京时间** | 🏢 公司动态 + 💬 微信（第二次） |

---

## 🛠️ 常用操作

### 手动触发数据收集

```bash
# 方法 1: 通过 GitHub 网页
1. 访问 Actions 页面
2. 选择 "Data Collection Workflow"
3. 点击 "Run workflow"

# 方法 2: 通过 gh CLI（如果已安装）
gh workflow run data-collection.yml
```

### 本地测试脚本

```bash
# 测试公司动态收集
python3 scripts/collect_company_news.py

# 测试论文收集
python3 scripts/collect_papers.py

# 测试日报生成
python3 scripts/generate_report.py --type daily

# 生成 index 页面
python3 scripts/generate_indexes.py

# 验证配置文件
python3 -c "import json; json.load(open('config/sources.json')); print('✓ JSON valid')"
```

### 本地预览网站

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run docs:dev

# 构建生产版本
npm run docs:build

# 预览构建结果
npm run docs:preview
```

---

## 🔍 故障排查速查表

| 问题 | 快速检查 | 解决方案 |
|------|----------|----------|
| 网站没更新 | 查看 Actions 状态 | 强制刷新浏览器 (Cmd+Shift+R) |
| 数据收集失败 | 查看 workflow 日志 | 检查 API 配额 / 网络连接 |
| 重复内容 | 查看去重日志 | 手动删除重复文件 |
| RSS 源失败 | 测试 RSS URL | 移除或替换失效源 |
| 构建失败 | 本地运行 `npm run docs:build` | 检查 markdown 语法错误 |

---

## 📝 快速编辑配置

### 添加新公司

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

### 添加新闻源

```json
{
  "name": "新闻源名称",
  "rss_feed": "https://example.com/feed/",
  "keywords": ["humanoid", "robot", "robotics"]
}
```

### 添加微信公众号

```json
{
  "name": "公众号名称",
  "keywords": ["人形机器人", "机器人技术"]
}
```

---

## 📈 性能指标

### 预期数据量

| 类型 | 每天预期 | 每周预期 |
|------|----------|----------|
| 论文 | 5-15 篇 | 30-100 篇 |
| 公司动态 | 2-10 条 | 10-50 条 |
| 微信文章 | 3-10 篇 | 20-70 篇 |

### 运行时间

| 任务 | 预计时间 |
|------|----------|
| 数据收集 | 3-5 分钟 |
| 网站部署 | 2-3 分钟 |
| 总计 | 5-8 分钟 |

---

## 🎯 优化建议

### 如果内容太少

1. ✅ 添加更多新闻源（参考扩展计划）
2. ✅ 增加收集时间范围（改为 14 天）
3. ✅ 放宽关键词过滤条件
4. ✅ 添加 Reddit、YouTube 等新数据源

### 如果内容太多

1. ✅ 缩短收集时间范围（改为 3 天）
2. ✅ 严格关键词过滤
3. ✅ 移除低质量数据源
4. ✅ 提高 AI 摘要质量要求

### 如果重复内容多

1. ✅ 检查去重逻辑是否生效
2. ✅ 增加去重检查范围（改为 30 天）
3. ✅ 手动清理历史重复内容

---

## 🔐 安全注意事项

### GitHub Secrets

确保以下 Secret 已配置：

```
MINIMAX_API_KEY - MiniMax API 密钥（必需）
```

### 权限设置

确保 GitHub Actions 有以下权限：

```yaml
permissions:
  contents: write  # 允许 commit 和 push
  pages: write     # 允许部署到 GitHub Pages
  id-token: write  # 允许 OIDC 认证
```

---

## 📞 获取帮助

### 遇到问题？

1. 📖 查看[完整文档](./maintenance-guide.md)
2. 🔍 搜索 [GitHub Issues](https://github.com/jzhu9324/humanoid-insight-platform/issues)
3. 🆕 创建新 Issue 描述问题
4. 💬 在 Issue 中附上：
   - 问题描述
   - 错误日志
   - 复现步骤

### 有建议？

欢迎通过 GitHub Issues 提出：
- 新功能建议
- 数据源推荐
- 优化建议
- Bug 报告

---

## 📚 相关文档

- [完整维护指南](./maintenance-guide.md) - 详细的使用和维护说明
- [数据源扩展计划](./data-sources-expansion-plan.md) - 未来扩展方向
- [项目说明](../README.md) - 项目概述和介绍

---

**最后更新：2026-03-22**
**版本：v2.0**
