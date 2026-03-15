---
title: 配置管理
---

<script setup>
import { ref, onMounted } from 'vue'

const config = ref({
  companies: [],
  paper_keywords: [],
  wechat_accounts: []
})

const newCompany = ref({
  name: '',
  name_cn: '',
  website: '',
  rss_feeds: '',
  keywords: ''
})

const newKeyword = ref('')
const newWechatAccount = ref({
  name: '',
  keywords: ''
})

const showAddCompany = ref(false)
const showAddKeyword = ref(false)
const showAddWechat = ref(false)
const saving = ref(false)
const saveMessage = ref('')

// API 基础地址
const API_BASE = 'http://localhost:3001'

// 加载配置
onMounted(async () => {
  try {
    const response = await fetch(`${API_BASE}/api/config`)
    config.value = await response.json()
  } catch (error) {
    console.error('加载配置失败:', error)
    saveMessage.value = '⚠️ 无法连接到配置服务器，请确保 API 服务器正在运行'
  }
})

// 添加公司
const addCompany = () => {
  const company = {
    name: newCompany.value.name,
    name_cn: newCompany.value.name_cn,
    website: newCompany.value.website,
    rss_feeds: newCompany.value.rss_feeds ? newCompany.value.rss_feeds.split(',').map(s => s.trim()) : [],
    keywords: newCompany.value.keywords ? newCompany.value.keywords.split(',').map(s => s.trim()) : []
  }
  config.value.companies.push(company)
  newCompany.value = { name: '', name_cn: '', website: '', rss_feeds: '', keywords: '' }
  showAddCompany.value = false
  saveConfig()
}

// 删除公司
const removeCompany = (index) => {
  config.value.companies.splice(index, 1)
  saveConfig()
}

// 添加论文关键词
const addKeyword = () => {
  if (newKeyword.value.trim()) {
    config.value.paper_keywords.push(newKeyword.value.trim())
    newKeyword.value = ''
    showAddKeyword.value = false
    saveConfig()
  }
}

// 删除关键词
const removeKeyword = (index) => {
  config.value.paper_keywords.splice(index, 1)
  saveConfig()
}

// 添加微信公众号
const addWechatAccount = () => {
  const account = {
    name: newWechatAccount.value.name,
    keywords: newWechatAccount.value.keywords ? newWechatAccount.value.keywords.split(',').map(s => s.trim()) : []
  }
  config.value.wechat_accounts.push(account)
  newWechatAccount.value = { name: '', keywords: '' }
  showAddWechat.value = false
  saveConfig()
}

// 删除微信公众号
const removeWechatAccount = (index) => {
  config.value.wechat_accounts.splice(index, 1)
  saveConfig()
}

// 保存配置
const saveConfig = async () => {
  saving.value = true
  saveMessage.value = '正在保存...'

  try {
    const response = await fetch(`${API_BASE}/api/config`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config.value)
    })

    const result = await response.json()

    if (response.ok) {
      saveMessage.value = '✅ 配置已成功保存到 config/sources.json！'
      setTimeout(() => {
        saveMessage.value = ''
      }, 3000)
    } else {
      saveMessage.value = `❌ 保存失败: ${result.error}`
    }
  } catch (error) {
    saveMessage.value = '❌ 保存失败: 无法连接到服务器'
    console.error('保存配置失败:', error)
  } finally {
    saving.value = false
  }
}

// 导出配置
const exportConfig = () => {
  const dataStr = JSON.stringify(config.value, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'sources.json'
  link.click()
}
</script>

# 配置管理

管理数据收集的来源和关键词配置。

<div v-if="saveMessage" class="save-message" :class="{ 'success': saveMessage.includes('✅'), 'error': saveMessage.includes('❌'), 'warning': saveMessage.includes('⚠️') }">
  {{ saveMessage }}
</div>

## 监控公司

<div class="config-section">
  <div class="section-header">
    <h3>当前监控 {{ config.companies.length }} 家公司</h3>
    <button @click="showAddCompany = !showAddCompany" class="btn-primary">
      {{ showAddCompany ? '取消' : '+ 添加公司' }}
    </button>
  </div>

  <div v-if="showAddCompany" class="add-form">
    <input v-model="newCompany.name" placeholder="公司名称（英文）" class="input-field" />
    <input v-model="newCompany.name_cn" placeholder="公司名称（中文）" class="input-field" />
    <input v-model="newCompany.website" placeholder="官网地址" class="input-field" />
    <input v-model="newCompany.rss_feeds" placeholder="RSS订阅源（多个用逗号分隔）" class="input-field" />
    <input v-model="newCompany.keywords" placeholder="关键词（多个用逗号分隔）" class="input-field" />
    <button @click="addCompany" class="btn-success">确认添加</button>
  </div>

  <div class="company-list">
    <div v-for="(company, index) in config.companies" :key="index" class="company-item">
      <div class="company-info">
        <h4>{{ company.name }} ({{ company.name_cn }})</h4>
        <p><strong>官网:</strong> {{ company.website }}</p>
        <p><strong>RSS:</strong> {{ company.rss_feeds.join(', ') || '无' }}</p>
        <p><strong>关键词:</strong> {{ company.keywords.join(', ') }}</p>
      </div>
      <button @click="removeCompany(index)" class="btn-danger">删除</button>
    </div>
  </div>
</div>

## 论文关键词

<div class="config-section">
  <div class="section-header">
    <h3>当前 {{ config.paper_keywords.length }} 个关键词</h3>
    <button @click="showAddKeyword = !showAddKeyword" class="btn-primary">
      {{ showAddKeyword ? '取消' : '+ 添加关键词' }}
    </button>
  </div>

  <div v-if="showAddKeyword" class="add-form">
    <input v-model="newKeyword" placeholder="输入论文关键词" class="input-field" />
    <button @click="addKeyword" class="btn-success">确认添加</button>
  </div>

  <div class="keyword-list">
    <div v-for="(keyword, index) in config.paper_keywords" :key="index" class="keyword-item">
      <span>{{ keyword }}</span>
      <button @click="removeKeyword(index)" class="btn-danger-small">×</button>
    </div>
  </div>
</div>

## 微信公众号

<div class="config-section">
  <div class="section-header">
    <h3>当前 {{ config.wechat_accounts.length }} 个公众号</h3>
    <button @click="showAddWechat = !showAddWechat" class="btn-primary">
      {{ showAddWechat ? '取消' : '+ 添加公众号' }}
    </button>
  </div>

  <div v-if="showAddWechat" class="add-form">
    <input v-model="newWechatAccount.name" placeholder="公众号名称" class="input-field" />
    <input v-model="newWechatAccount.keywords" placeholder="关键词（多个用逗号分隔）" class="input-field" />
    <button @click="addWechatAccount" class="btn-success">确认添加</button>
  </div>

  <div class="wechat-list">
    <div v-for="(account, index) in config.wechat_accounts" :key="index" class="wechat-item">
      <div class="wechat-info">
        <h4>{{ account.name }}</h4>
        <p><strong>关键词:</strong> {{ account.keywords.join(', ') }}</p>
      </div>
      <button @click="removeWechatAccount(index)" class="btn-danger">删除</button>
    </div>
  </div>
</div>

## 导出配置

<div class="config-section">
  <button @click="exportConfig" class="btn-primary">下载配置文件</button>
  <p class="help-text">备份配置文件到本地</p>
</div>

<style scoped>
.save-message {
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.save-message.success {
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #10b981;
}

.save-message.error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #ef4444;
}

.save-message.warning {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #f59e0b;
}

.config-section {
  margin: 2rem 0;
  padding: 1.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 {
  margin: 0;
}

.add-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--vp-c-bg-soft);
  border-radius: 4px;
}

.input-field {
  padding: 0.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 4px;
  font-size: 14px;
}

.company-list, .wechat-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.company-item, .wechat-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem;
  background: var(--vp-c-bg-soft);
  border-radius: 4px;
}

.company-info, .wechat-info {
  flex: 1;
}

.company-info h4, .wechat-info h4 {
  margin: 0 0 0.5rem 0;
}

.company-info p, .wechat-info p {
  margin: 0.25rem 0;
  font-size: 14px;
  color: var(--vp-c-text-2);
}

.keyword-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--vp-c-bg-soft);
  border-radius: 20px;
  font-size: 14px;
}

.btn-primary {
  padding: 0.5rem 1rem;
  background: var(--vp-c-brand);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary:hover {
  background: var(--vp-c-brand-dark);
}

.btn-success {
  padding: 0.5rem 1rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-success:hover {
  background: #059669;
}

.btn-danger {
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-danger:hover {
  background: #dc2626;
}

.btn-danger-small {
  padding: 0.25rem 0.5rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
}

.btn-danger-small:hover {
  background: #dc2626;
}

.help-text {
  margin-top: 0.5rem;
  font-size: 14px;
  color: var(--vp-c-text-2);
}
</style>
