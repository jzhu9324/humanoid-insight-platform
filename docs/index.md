---
layout: home

hero:
  name: 人形机器人洞察平台
  text: Humanoid Robotics Insight Platform
  tagline: 追踪最新论文 · 公司动态 · 行业观点

features:
  - icon: 📄
    title: 学术论文追踪
    details: 自动收集 arXiv 最新论文，AI 深度解读核心观点、技术亮点和应用场景
    link: /papers/

  - icon: 🏢
    title: 公司动态监控
    details: 追踪国内外领先公司的产品发布、技术进展和战略动向
    link: /company-news/

  - icon: 💬
    title: 社交媒体洞察
    details: 汇总微信公众号、Twitter、Reddit 的行业讨论和专家观点
    link: /wechat/
---

<script setup>
import { ref, onMounted } from 'vue'

const latestUpdates = ref({
  papers: [],
  companyNews: [],
  wechat: []
})

const loading = ref(true)

// 加载最新更新
onMounted(async () => {
  try {
    const response = await fetch('/latest-updates.json')
    if (response.ok) {
      const data = await response.json()
      latestUpdates.value = data
    }
  } catch (error) {
    console.error('加载最新更新失败:', error)
  } finally {
    loading.value = false
  }
})
</script>

## 📰 最近更新

<div class="updates-container">
  <div class="update-section">
    <h3>📄 最新论文</h3>
    <div class="update-list">
      <div v-if="latestUpdates.papers.length === 0" class="empty-state">
        暂无内容
      </div>
      <div v-for="item in latestUpdates.papers" :key="item.title" class="update-item">
        <a :href="item.link">{{ item.title }}</a>
        <span class="update-date">{{ item.date }}</span>
      </div>
    </div>
    <a href="/papers/" class="view-more">查看更多 →</a>
  </div>

  <div class="update-section">
    <h3>🏢 公司动态</h3>
    <div class="update-list">
      <div v-if="latestUpdates.companyNews.length === 0" class="empty-state">
        暂无内容
      </div>
      <div v-for="item in latestUpdates.companyNews" :key="item.title" class="update-item">
        <a :href="item.link">{{ item.title }}</a>
        <span class="update-date">{{ item.date }}</span>
      </div>
    </div>
    <a href="/company-news/" class="view-more">查看更多 →</a>
  </div>

  <div class="update-section">
    <h3>💬 行业资讯</h3>
    <div class="update-list">
      <div v-if="latestUpdates.wechat.length === 0" class="empty-state">
        暂无内容
      </div>
      <div v-for="item in latestUpdates.wechat" :key="item.title" class="update-item">
        <a :href="item.link">{{ item.title }}</a>
        <span class="update-date">{{ item.date }}</span>
      </div>
    </div>
    <a href="/wechat/" class="view-more">查看更多 →</a>
  </div>
</div>

<style scoped>
.updates-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.update-section {
  background: var(--vp-c-bg-soft);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--vp-c-divider);
  transition: all 0.3s;
}

.update-section:hover {
  border-color: var(--vp-c-brand);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.update-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  color: var(--vp-c-text-1);
}

.update-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
  min-height: 120px;
}

.update-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background 0.2s;
}

.update-item:hover {
  background: var(--vp-c-bg);
}

.update-item a {
  color: var(--vp-c-text-1);
  text-decoration: none;
  font-size: 0.95rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.update-item a:hover {
  color: var(--vp-c-brand);
}

.update-date {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
}

.empty-state {
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
  text-align: center;
  padding: 2rem 0;
}

.view-more {
  display: inline-block;
  color: var(--vp-c-brand);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
}

.view-more:hover {
  text-decoration: underline;
  transform: translateX(4px);
}
</style>
