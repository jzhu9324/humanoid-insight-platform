# 配置管理系统使用指南

## 🎉 功能说明

现在你可以通过网页界面**直接保存配置**到 `config/sources.json` 文件，无需手动下载和替换！

## 🚀 启动方法

### 方式 1：使用启动脚本（推荐）

```bash
cd /Users/joana/humanoid-insight-platform
./start-with-config.sh
```

这会同时启动：
- ✅ VitePress 开发服务器（端口 5173）
- ✅ 配置 API 服务器（端口 3001）

### 方式 2：手动启动

```bash
# 终端 1：启动 API 服务器
python3 scripts/config_api.py

# 终端 2：启动 VitePress
npm run docs:dev
```

## 🌐 访问配置管理页面

启动后，打开浏览器访问：

**http://localhost:5173/config**

## ✨ 使用方法

### 1. 添加新公司

1. 在"监控公司"部分，点击 **"+ 添加公司"** 按钮
2. 填写表单：
   - 公司名称（英文）：如 `Fourier Intelligence`
   - 公司名称（中文）：如 `傅利叶智能`
   - 官网地址：如 `https://www.fftai.com/`
   - RSS订阅源：可选，如 `https://www.fftai.com/rss`
   - 关键词：如 `GR-1, humanoid, rehabilitation`
3. 点击 **"确认添加"**
4. 配置会**自动保存**到 `config/sources.json`！

### 2. 添加论文关键词

1. 在"论文关键词"部分，点击 **"+ 添加关键词"**
2. 输入关键词，如 `mobile manipulation`
3. 点击 **"确认添加"**
4. 自动保存！

### 3. 添加微信公众号

1. 在"微信公众号"部分，点击 **"+ 添加公众号"**
2. 填写：
   - 公众号名称：如 `机器人前沿`
   - 关键词：如 `人形机器人, 机器人技术`
3. 点击 **"确认添加"**
4. 自动保存！

### 4. 删除项目

- 每个项目右侧都有 **"删除"** 按钮
- 点击删除后会**自动保存**

### 5. 保存状态提示

- ✅ 成功：绿色提示框 "配置已成功保存到 config/sources.json！"
- ❌ 失败：红色提示框显示错误信息
- ⚠️ 警告：黄色提示框提示连接问题

## 🎯 优势

### 之前的方式
1. 在页面上修改
2. 点击"下载配置文件"
3. 手动将下载的文件保存到 `config/sources.json`
4. 容易出错

### 现在的方式
1. 在页面上修改
2. **自动保存**到 `config/sources.json`
3. 立即生效！
4. 不会出错

## 🔄 验证配置生效

修改配置后，运行数据收集脚本验证：

```bash
python scripts/collect_company_news.py
```

你会看到：
```
✓ Loaded 9 companies from config file
```

说明脚本正在使用你刚才在网页上配置的公司列表！

## 🎨 界面特点

- ✅ **VitePress 原生风格**：完全融入项目设计
- ✅ **实时保存**：修改后自动保存到文件
- ✅ **状态提示**：清晰的成功/失败提示
- ✅ **响应式设计**：适配各种屏幕尺寸
- ✅ **统一导航**：和其他页面一样的导航栏

## 🛠️ 技术架构

```
┌─────────────────┐
│  浏览器界面      │
│  (VitePress)    │
│  localhost:5173 │
└────────┬────────┘
         │ HTTP API
         │ (fetch)
         ↓
┌─────────────────┐
│  API 服务器      │
│  (Python)       │
│  localhost:3001 │
└────────┬────────┘
         │ 文件读写
         ↓
┌─────────────────┐
│ config/         │
│ sources.json    │
└─────────────────┘
```

## 📝 注意事项

1. **必须同时运行两个服务器**
   - VitePress（前端界面）
   - API 服务器（处理文件保存）

2. **使用启动脚本最方便**
   - `./start-with-config.sh` 会自动启动两个服务器

3. **停止服务**
   - 按 `Ctrl+C` 会同时停止两个服务器

4. **端口占用**
   - 如果端口被占用，需要先停止其他服务

## 🐛 故障排除

### 问题：页面显示"无法连接到配置服务器"

**解决方法：**
1. 确认 API 服务器正在运行：
   ```bash
   lsof -i :3001
   ```
2. 如果没有运行，启动它：
   ```bash
   python3 scripts/config_api.py
   ```

### 问题：保存失败

**解决方法：**
1. 检查 `config/sources.json` 文件权限
2. 查看 API 服务器日志
3. 确认配置格式正确

### 问题：修改后数据收集脚本没有使用新配置

**解决方法：**
1. 确认配置已成功保存（看到绿色提示）
2. 检查 `config/sources.json` 文件内容
3. 重新运行数据收集脚本

## 🎓 示例操作

### 添加一家新公司（傅利叶智能）

1. 访问 http://localhost:5173/config
2. 点击"+ 添加公司"
3. 填写：
   - 公司名称（英文）：`Fourier Intelligence`
   - 公司名称（中文）：`傅利叶智能`
   - 官网地址：`https://www.fftai.com/`
   - 关键词：`GR-1, humanoid, rehabilitation, exoskeleton`
4. 点击"确认添加"
5. 看到绿色提示："✅ 配置已成功保存到 config/sources.json！"
6. 完成！

### 验证配置

```bash
# 查看配置文件
cat config/sources.json | grep "Fourier"

# 运行数据收集
python scripts/collect_company_news.py
```

你会看到 Fourier Intelligence 出现在公司列表中！

## 📚 相关文档

- [项目 README](../README.md)
- [数据收集脚本说明](../README.md#数据收集)
- [VitePress 文档](https://vitepress.dev/)

---

**享受全新的配置管理体验！** 🎉
