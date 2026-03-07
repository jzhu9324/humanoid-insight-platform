---
title: 每日精选
---

# 每日精选

汇集人形机器人领域的每日精华内容，包括最新论文、公司动态和行业资讯。

## 📅 按日期浏览

<script setup>
import { data as dailyData } from './daily.data.js'
</script>

<div v-for="item in dailyData" :key="item.date" class="daily-item">
  <h3>{{ item.date }}</h3>
  <div class="daily-content">
    <div v-if="item.papers.length > 0" class="section">
      <h4>📚 学术论文 ({{ item.papers.length }})</h4>
      <ul>
        <li v-for="paper in item.papers" :key="paper.link">
          <a :href="paper.link">{{ paper.title }}</a>
        </li>
      </ul>
    </div>

    <div v-if="item.news.length > 0" class="section">
      <h4>🏢 公司动态 ({{ item.news.length }})</h4>
      <ul>
        <li v-for="news in item.news" :key="news.link">
          <a :href="news.link">{{ news.title }}</a>
        </li>
      </ul>
    </div>

    <div v-if="item.articles.length > 0" class="section">
      <h4>📱 行业资讯 ({{ item.articles.length }})</h4>
      <ul>
        <li v-for="article in item.articles" :key="article.link">
          <a :href="article.link">{{ article.title }}</a>
        </li>
      </ul>
    </div>
  </div>
</div>

<style scoped>
.daily-item {
  margin-bottom: 40px;
  padding: 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
}

.daily-item h3 {
  margin-top: 0;
  color: var(--vp-c-brand);
  border-bottom: 2px solid var(--vp-c-brand);
  padding-bottom: 10px;
}

.daily-content {
  margin-top: 20px;
}

.section {
  margin-bottom: 20px;
}

.section h4 {
  margin-bottom: 10px;
  font-size: 1.1em;
}

.section ul {
  list-style: none;
  padding-left: 0;
}

.section li {
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
}

.section li:before {
  content: "→";
  position: absolute;
  left: 0;
  color: var(--vp-c-brand);
}
</style>
