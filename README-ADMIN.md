# 后台管理使用指南

## 🎯 功能说明

现在你可以通过网页后台管理所有配置，包括：

- ✅ 添加/删除监控公司
- ✅ 管理论文关键词
- ✅ 配置微信公众号
- ✅ 编辑文章内容
- ✅ 自动提交到 Git

## 🚀 本地开发使用

### 1. 启动管理后台

```bash
./start-admin.sh
```

或者手动启动：

```bash
# 终端 1: 启动 CMS 代理服务器
npx netlify-cms-proxy-server

# 终端 2: 启动 VitePress
npm run docs:dev
```

### 2. 访问后台

打开浏览器访问：
- **网站**: http://localhost:5173
- **后台管理**: http://localhost:5173/admin/

### 3. 编辑配置

在后台管理界面：
1. 点击左侧菜单 **"数据源配置"**
2. 点击 **"数据源配置"** 条目
3. 编辑公司、关键词、微信公众号
4. 点击 **"保存"** - 会自动保存到 `config/sources.json`
5. 点击 **"发布"** - 会自动提交到 Git

### 4. 查看效果

配置保存后，运行数据收集脚本会自动使用新配置：

```bash
python scripts/collect_company_news.py
python scripts/collect_papers.py
```

## 🌐 生产环境部署

### 部署到 Netlify

1. **连接 GitHub 仓库**
   - 登录 [Netlify](https://app.netlify.com)
   - 点击 "Add new site" → "Import an existing project"
   - 选择你的 GitHub 仓库

2. **配置构建设置**
   ```
   Build command: npm run docs:build
   Publish directory: docs/.vitepress/dist
   ```

3. **启用 Netlify Identity**
   - 在 Netlify 站点设置中，找到 "Identity"
   - 点击 "Enable Identity"
   - 在 "Registration preferences" 中选择 "Invite only"

4. **启用 Git Gateway**
   - 在 Identity 设置中，找到 "Services"
   - 点击 "Enable Git Gateway"

5. **邀请用户**
   - 在 Identity 标签页，点击 "Invite users"
   - 输入你的邮箱
   - 查收邮件并设置密码

6. **访问后台**
   - 访问 `https://你的站点.netlify.app/admin/`
   - 使用邮箱和密码登录
   - 开始管理内容和配置

## 📝 使用技巧

### 添加新公司

1. 进入后台 → 数据源配置
2. 在 "监控公司" 部分点击 "Add 监控公司"
3. 填写：
   - 公司名称（英文）：如 "Xiaomi Robotics"
   - 公司名称（中文）：如 "小米机器人"
   - 官网地址：如 "https://www.mi.com/"
   - RSS订阅源：可选，如有则填写
   - 关键词：如 "cyberone", "人形机器人"
4. 保存并发布

### 添加论文关键词

1. 进入后台 → 数据源配置
2. 在 "论文关键词" 部分点击 "Add 论文关键词"
3. 输入关键词，如 "embodied AI"
4. 保存并发布

### 添加微信公众号

1. 进入后台 → 数据源配置
2. 在 "微信公众号" 部分点击 "Add 微信公众号"
3. 填写公众号名称和关键词
4. 保存并发布

## 🔧 故障排除

### 本地后台无法访问

确保两个服务都在运行：
```bash
# 检查 CMS 代理服务器
curl http://localhost:8081

# 检查 VitePress
curl http://localhost:5173
```

### 保存后配置未生效

1. 检查 `config/sources.json` 是否已更新
2. 重新运行数据收集脚本
3. 查看脚本输出，确认读取了新配置

### 生产环境无法登录

1. 确认 Netlify Identity 已启用
2. 确认 Git Gateway 已启用
3. 确认已收到邀请邮件并设置密码
4. 清除浏览器缓存后重试

## 📚 更多信息

- [Netlify CMS 文档](https://www.netlifycms.org/docs/)
- [VitePress 文档](https://vitepress.dev/)
- [项目 GitHub](https://github.com/jzhu9324/humanoid-insight-platform)
