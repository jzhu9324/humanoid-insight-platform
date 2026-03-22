# 数据源扩展计划

## 当前状态
- 10 家公司 RSS
- 11 个通用新闻源
- 9 个微信公众号

## 可选扩展方案

### 方案 A：添加 Reddit 数据源
**优点：**
- 社区讨论活跃，内容丰富
- 可以获取行业内人士的真实观点

**实现方式：**
- 使用 Reddit RSS（无需 API）
- 监控 subreddits：
  - r/robotics
  - r/MachineLearning
  - r/artificial
  - r/Futurology

**示例 RSS：**
```
https://www.reddit.com/r/robotics/.rss
https://www.reddit.com/r/robotics/search.rss?q=humanoid&restrict_sr=1&sort=new
```

### 方案 B：添加 YouTube 频道监控
**优点：**
- 视频内容更直观
- 公司官方发布的演示视频

**实现方式：**
- 使用 YouTube RSS（无需 API）
- 监控公司官方频道

**示例 RSS：**
```
https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID
```

### 方案 C：添加 Twitter/X 监控
**优点：**
- 实时性最强
- 公司官方账号第一时间发布

**缺点：**
- 需要 Twitter API（可能需要付费）
- RSS 支持已被移除

**替代方案：**
- 使用 Nitter 实例（Twitter 的开源前端）
- 或使用第三方 Twitter RSS 服务

### 方案 D：Web Scraping（网页爬虫）
**优点：**
- 可以直接爬取公司官网
- 不受 RSS 限制

**缺点：**
- 需要为每个网站写专门的解析器
- 维护成本高
- 可能被反爬虫机制阻止

**建议实现：**
- 只针对重点公司（Tesla、Boston Dynamics、Figure AI）
- 使用 BeautifulSoup 或 Playwright

### 方案 E：添加学术会议和期刊 RSS
**优点：**
- 高质量学术内容
- 了解最新研究方向

**数据源：**
- ICRA (International Conference on Robotics and Automation)
- IROS (International Conference on Intelligent Robots and Systems)
- RSS (Robotics: Science and Systems)
- IEEE Transactions on Robotics

## 推荐优先级

1. **优先级 1：Reddit** — 实现简单，内容丰富
2. **优先级 2：YouTube** — 视频内容有价值，RSS 易获取
3. **优先级 3：学术会议** — 提升内容质量
4. **优先级 4：Twitter** — 实时性强但实现复杂
5. **优先级 5：Web Scraping** — 最后考虑，维护成本高

## 实施建议

### 第一步：先观察当前效果
等待今天 20:00 的自动运行结果，看看：
- 11 个通用新闻源能抓到多少内容
- 去重是否有效
- 内容质量如何

### 第二步：根据效果决定
- 如果内容已经足够丰富 → 保持现状
- 如果内容还是太少 → 添加 Reddit
- 如果想要更多视频内容 → 添加 YouTube

### 第三步：持续优化
- 定期检查哪些数据源效果好
- 移除长期没有内容的源
- 根据用户反馈调整
