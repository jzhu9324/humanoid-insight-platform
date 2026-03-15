import { createContentLoader } from 'vitepress'
import fs from 'fs'
import path from 'path'

export default createContentLoader(['papers/*.md', 'company-news/*.md', 'wechat/*.md'], {
  transform(rawData) {
    // Group content by date
    const dailyMap = new Map()

    rawData.forEach(page => {
      const date = page.frontmatter.date
      if (!date) return

      const dateStr = new Date(date).toISOString().split('T')[0]

      if (!dailyMap.has(dateStr)) {
        dailyMap.set(dateStr, {
          date: dateStr,
          papers: [],
          news: [],
          articles: []
        })
      }

      const dailyData = dailyMap.get(dateStr)
      const item = {
        title: page.frontmatter.title || 'Untitled',
        link: page.url
      }

      const type = page.frontmatter.type
      if (type === 'papers') {
        dailyData.papers.push(item)
      } else if (type === 'company-news') {
        dailyData.news.push(item)
      } else if (type === 'wechat-articles') {
        dailyData.articles.push(item)
      }
    })

    // Convert to array and sort by date (newest first)
    return Array.from(dailyMap.values())
      .sort((a, b) => new Date(b.date) - new Date(a.date))
  }
})
