export default {
  title: '人形机器人洞察平台',
  description: '追踪人形机器人领域的最新论文、公司动态和行业观点',

  lang: 'zh-CN',

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '每日洞察', link: '/daily/' },
      { text: '管理后台', link: '/admin/' }
    ],

    sidebar: {
      '/daily/': []
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
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ]
}
