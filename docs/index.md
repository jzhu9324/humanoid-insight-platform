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

const latestUpdates = ref({ papers: [], companyNews: [], wechat: [] })
const loading = ref(true)
const base = '/humanoid-insight-platform'

onMounted(async () => {
  try {
    const response = await fetch(`${base}/latest-updates.json`)
    if (response.ok) latestUpdates.value = await response.json()
  } catch (error) {
    console.error('加载最新更新失败:', error)
  } finally {
    loading.value = false
  }
})
</script>

## 最新动态

<div class="updates-container">

  <div class="update-section">
    <div class="section-title">📄 最新论文</div>
    <div v-if="loading" class="empty-state">加载中...</div>
    <div v-else-if="latestUpdates.papers.length === 0" class="empty-state">暂无内容</div>
    <div v-else>
      <div v-for="item in latestUpdates.papers" :key="item.title" class="update-item">
        <a :href="item.link" target="_blank" class="item-title">{{ item.title }}</a>
        <p v-if="item.summary" class="item-summary">{{ item.summary }}</p>
        <span class="item-date">{{ item.date }}</span>
      </div>
    </div>
    <a :href="`${base}/papers/`" class="view-more">查看全部论文 →</a>
  </div>

  <div class="update-section">
    <div class="section-title">🏢 公司动态</div>
    <div v-if="loading" class="empty-state">加载中...</div>
    <div v-else-if="latestUpdates.companyNews.length === 0" class="empty-state">暂无内容</div>
    <div v-else>
      <div v-for="item in latestUpdates.companyNews" :key="item.title" class="update-item">
        <a :href="item.link" target="_blank" class="item-title">{{ item.title }}</a>
        <p v-if="item.summary" class="item-summary">{{ item.summary }}</p>
        <span class="item-date">{{ item.date }}</span>
      </div>
    </div>
    <a :href="`${base}/company-news/`" class="view-more">查看全部动态 →</a>
  </div>

</div>

<style scoped>
.updates-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  margin-top: 1.5rem;
}

.update-section {
  background: var(--vp-c-bg-soft);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--vp-c-divider);
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  color: var(--vp-c-text-1);
}

.update-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--vp-c-divider);
}

.update-item:last-child {
  border-bottom: none;
}

.item-title {
  display: block;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--vp-c-text-1);
  text-decoration: none;
  line-height: 1.5;
  margin-bottom: 0.25rem;
}

.item-title:hover {
  color: var(--vp-c-brand);
}

.item-summary {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  line-height: 1.5;
  margin: 0.25rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-date {
  font-size: 0.8rem;
  color: var(--vp-c-text-3);
}

.empty-state {
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
  padding: 1.5rem 0;
  text-align: center;
}

.view-more {
  display: inline-block;
  margin-top: 1rem;
  color: var(--vp-c-brand);
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
}

.view-more:hover {
  text-decoration: underline;
}
</style>
