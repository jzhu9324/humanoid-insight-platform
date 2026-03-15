export default {
  title: '人形机器人洞察平台',
  description: '追踪人形机器人领域的最新论文、公司动态和行业观点',

  lang: 'zh-CN',

  ignoreDeadLinks: true,

  markdown: {
    html: true
  },

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '学术论文', link: '/papers/' },
      { text: '公司动态', link: '/company-news/' },
      { text: '行业资讯', link: '/wechat/' },
      { text: '周度总结', link: '/reports/' },
      { text: '配置管理', link: '/config' }
    ],

    sidebar: {
      '/papers/': [],
      '/company-news/': [],
      '/wechat/': [],
      '/reports/': []
    },

    search: {
      provider: 'local'
    },

    outline: {
      level: [2, 3],
      label: '目录'
    },

    docFooter: {
      prev: '上一页',
      next: '下一页'
    },

    lastUpdated: {
      text: '最后更新'
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/jzhu9324/humanoid-insight-platform' }
    ],

    footer: {
      message: 'Powered by Claude & VitePress',
      copyright: 'Copyright © 2026 朱俊荣'
    }
  },

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', {
      rel: 'stylesheet',
      href: 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Lora:wght@400;500;600&display=swap'
    }]
  ]
}
