# 人形机器人洞察平台 - 使用和维护指南

## 📋 目录

1. [系统概览](#系统概览)
2. [自动化流程](#自动化流程)
3. [数据源配置](#数据源配置)
4. [常见问题](#常见问题)
5. [维护指南](#维护指南)
6. [故障排查](#故障排查)

---

## 系统概览

### 当前配置

**数据源统计：**
- 🏢 **10 家人形机器人公司**（15 个 RSS 源）
- 📰 **13 个通用新闻源**（包括 Reddit）
- 💬 **9 个微信公众号**
- 📄 **12 个论文关键词**
- **总计：28 个 RSS 源**

**核心功能：**
- ✅ 自动收集论文（Semantic Scholar + HuggingFace + arXiv）
- ✅ 自动收集公司动态（RSS + Google News）
- ✅ 自动收集微信文章
- ✅ 自动生成日报
- ✅ 智能去重（检查过去 14 天）
- ✅ 自动更新网站

---

## 自动化流程

### 定时任务

**每天 00:00 UTC（北京时间 08:00）**
```
1. 收集论文（Semantic Scholar + HuggingFace + arXiv）
2. 收集公司动态（所有 RSS 源）
3. 收集微信文章
4. 生成日报
5. 更新 index 页面
6. 自动 commit + push
7. 触发网站部署
```

**每天 12:00 UTC（北京时间 20:00）**
```
1. 收集公司动态（第二次）
2. 收集微信文章（第二次）
3. 更新 index 页面
4. 自动 commit + push
5. 触发网站部署
```

### 工作流程图

```
┌─────────────────┐
│  定时触发       │
│  (cron)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  收集数据       │
│  - 论文         │
│  - 公司动态     │
│  - 微信文章     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  去重过滤       │
│  (检查14天历史) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI 分析        │
│  (MiniMax API)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  生成 Markdown  │
│  + 更新 Index   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Git Commit     │
│  + Push         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  触发部署       │
│  (GitHub Pages) │
└─────────────────┘
```

---

## 数据源配置

### 配置文件位置

```
config/sources.json
```

### 配置结构

```json
{
  "companies": [
    {
      "name": "公司名称",
      "name_cn": "中文名称",
      "rss_feeds": ["RSS URL 1", "RSS URL 2"],
      "website": "官网 URL",
      "keywords": ["关键词1", "关键词2"]
    }
  ],
  "news_sources": [
    {
      "name": "新闻源名称",
      "rss_feed": "RSS URL",
      "keywords": ["humanoid", "robot"]
    }
  ],
  "paper_keywords": ["关键词1", "关键词2"],
  "wechat_accounts": [
    {
      "name": "公众号名称",
      "keywords": ["关键词1", "关键词2"]
    }
  ]
}
```

### 在线配置管理

访问：https://jzhu9324.github.io/humanoid-insight-platform/config

可以直接在网页上编辑配置，无需手动修改 JSON 文件。

---

## 常见问题

### Q1: 为什么每天收集到的新闻很少？

**原因：**
1. 人形机器人行业本身新闻频率低
2. 去重机制过滤掉了已收录的内容
3. 某些 RSS 源可能暂时无法访问

**解决方案：**
- 查看 GitHub Actions 日志，确认哪些源有内容
- 考虑添加更多数据源（参考 `data-sources-expansion-plan.md`）
- 调整关键词过滤条件

### Q2: 网站没有更新怎么办？

**检查步骤：**
1. 访问 [GitHub Actions](https://github.com/jzhu9324/humanoid-insight-platform/actions)
2. 查看最近的 workflow 运行状态
3. 如果失败，查看错误日志
4. 如果成功但网站没更新，强制刷新浏览器（Cmd+Shift+R）

**常见原因：**
- GitHub Actions 运行失败
- 浏览器缓存
- GitHub Pages 部署延迟（通常 1-5 分钟）

### Q3: 如何手动触发数据收集？

1. 访问：https://github.com/jzhu9324/humanoid-insight-platform/actions/workflows/data-collection.yml
2. 点击右上角 "Run workflow"
3. 选择 `main` 分支
4. 点击绿色 "Run workflow" 按钮
5. 等待 5-10 分钟查看结果

### Q4: 如何添加新的公司或新闻源？

**方法 1：在线编辑**
1. 访问：https://jzhu9324.github.io/humanoid-insight-platform/config
2. 在配置页面直接添加
3. 保存后会自动提交到 GitHub

**方法 2：手动编辑**
1. 编辑 `config/sources.json`
2. 添加新的公司或新闻源配置
3. 提交并 push 到 GitHub

### Q5: MiniMax API 配额用完了怎么办？

**检查配额：**
- 查看 GitHub Actions 日志中的 API 错误信息

**解决方案：**
1. 等待配额重置（通常每月重置）
2. 升级 MiniMax API 套餐
3. 临时禁用 AI 分析（脚本会自动降级到无 AI 模式）

---

## 维护指南

### 定期检查（每周）

1. **查看 GitHub Actions 运行状态**
   - 是否有失败的 workflow
   - 错误日志中是否有异常

2. **检查数据质量**
   - 新闻内容是否相关
   - 是否有重复内容
   - AI 摘要质量如何

3. **监控数据源**
   - 哪些源长期没有内容
   - 哪些源经常失败
   - 考虑移除无效源

### 定期优化（每月）

1. **清理无效数据源**
   ```bash
   # 查看最近 30 天的收集日志
   # 识别长期无内容的源
   # 从 config/sources.json 中移除
   ```

2. **添加新数据源**
   - 关注行业新出现的公司
   - 发现新的优质新闻源
   - 参考 `data-sources-expansion-plan.md`

3. **优化关键词**
   - 根据收集到的内容调整关键词
   - 过滤掉不相关的内容
   - 增加新的关键词

### 备份策略

**自动备份：**
- 所有数据都在 Git 仓库中
- GitHub 自动保存历史版本
- 可以随时回滚到任何历史版本

**手动备份（可选）：**
```bash
# 克隆整个仓库作为备份
git clone https://github.com/jzhu9324/humanoid-insight-platform.git backup-$(date +%Y%m%d)
```

---

## 故障排查

### 问题：数据收集失败

**症状：**
- GitHub Actions 显示红色 ❌
- 没有新的 commit

**排查步骤：**
1. 查看 Actions 日志
2. 检查是否是 API 配额问题
3. 检查是否是网络问题
4. 检查 `sources.json` 是否有语法错误

**解决方案：**
```bash
# 本地测试收集脚本
python3 scripts/collect_company_news.py
python3 scripts/collect_papers.py

# 检查 JSON 语法
python3 -c "import json; json.load(open('config/sources.json'))"
```

### 问题：网站部署失败

**症状：**
- Deploy workflow 显示红色 ❌
- 网站显示 404 或旧内容

**排查步骤：**
1. 查看 Deploy workflow 日志
2. 检查是否是 VitePress 构建错误
3. 检查 GitHub Pages 设置

**解决方案：**
```bash
# 本地测试构建
npm install
npm run docs:build

# 检查构建产物
ls -la docs/.vitepress/dist/
```

### 问题：去重不生效

**症状：**
- 每天都收集到相同的旧新闻
- 新闻列表有重复内容

**排查步骤：**
1. 查看收集日志中的 "跳过已收录" 信息
2. 检查链接是否完全一致
3. 检查去重逻辑是否正确执行

**解决方案：**
```bash
# 手动清理重复内容
# 删除重复的 markdown 文件
# 重新运行收集脚本
```

### 问题：RSS 源无法访问

**症状：**
- 日志显示 "Found 0 entries"
- SSL 证书错误
- 超时错误

**排查步骤：**
1. 手动访问 RSS URL 确认是否可用
2. 检查是否被防火墙阻止
3. 检查 User-Agent 是否被屏蔽

**解决方案：**
```bash
# 测试 RSS 源
curl -L -A "Mozilla/5.0" "RSS_URL" | head -50

# 如果源长期不可用，考虑移除或替换
```

---

## 高级配置

### 调整收集频率

编辑 `.github/workflows/data-collection.yml`:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'    # 每天 00:00 UTC
    - cron: '0 12 * * *'   # 每天 12:00 UTC
    # 添加更多时间点
    - cron: '0 6 * * *'    # 每天 06:00 UTC
```

### 调整收集时间范围

编辑 `scripts/collect_company_news.py`:

```python
days_back = 7  # 改为其他天数，如 14 或 30
```

### 调整去重范围

编辑 `scripts/collect_company_news.py`:

```python
seen_links = get_seen_links(docs_dir, days_back=14)  # 改为其他天数
```

### 禁用某个数据源

在 `config/sources.json` 中注释掉或删除对应的配置项。

---

## 联系和支持

- **GitHub Issues**: https://github.com/jzhu9324/humanoid-insight-platform/issues
- **项目文档**: https://jzhu9324.github.io/humanoid-insight-platform/
- **配置管理**: https://jzhu9324.github.io/humanoid-insight-platform/config

---

## 更新日志

### 2026-03-22
- ✅ 添加 13 个通用新闻源
- ✅ 添加 Reddit 数据源
- ✅ 改进去重逻辑（在收集阶段过滤）
- ✅ 优化日志输出
- ✅ 自动生成 index 页面
- ✅ 移除 `[skip ci]` 让数据更新触发部署

### 2026-03-15
- ✅ 升级论文收集（Semantic Scholar + HuggingFace）
- ✅ 首页展示具体文章标题和摘要
- ✅ 新公司无 RSS 时自动生成 Google News 搜索源

---

**最后更新：2026-03-22**
