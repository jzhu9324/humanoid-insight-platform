---
title: 配置管理
---

<script setup>
import { ref, onMounted } from 'vue'

const REPO_OWNER = 'jzhu9324'
const REPO_NAME = 'humanoid-insight-platform'
const FILE_PATH = 'config/sources.json'

const config = ref({ companies: [], paper_keywords: [], wechat_accounts: [] })
const token = ref('')
const fileSha = ref('')
const loading = ref(false)
const saveMessage = ref('')

const newCompany = ref({ name: '', name_cn: '', website: '', rss_feeds: '', keywords: '' })
const newKeyword = ref('')
const newWechatAccount = ref({ name: '', keywords: '' })
const showAddCompany = ref(false)
const showAddKeyword = ref(false)
const showAddWechat = ref(false)

onMounted(() => {
  const saved = localStorage.getItem('github_token')
  if (saved) {
    token.value = saved
    loadConfig()
  }
})

const saveToken = () => {
  localStorage.setItem('github_token', token.value)
  loadConfig()
}

const loadConfig = async () => {
  if (!token.value) return
  loading.value = true
  saveMessage.value = ''
  try {
    const res = await fetch(
      `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${FILE_PATH}`,
      { headers: { Authorization: `token ${token.value}`, Accept: 'application/vnd.github.v3+json' } }
    )
    if (!res.ok) throw new Error('Token 无效或无权限')
    const data = await res.json()
    fileSha.value = data.sha
    config.value = JSON.parse(atob(data.content.replace(/\n/g, '')))
    saveMessage.value = '✅ 配置加载成功'
    setTimeout(() => saveMessage.value = '', 3000)
  } catch (e) {
    saveMessage.value = `❌ 加载失败: ${e.message}`
  } finally {
    loading.value = false
  }
}

const saveConfig = async () => {
  if (!token.value) { saveMessage.value = '❌ 请先输入 GitHub Token'; return }
  loading.value = true
  saveMessage.value = '正在保存...'
  try {
    const content = btoa(unescape(encodeURIComponent(JSON.stringify(config.value, null, 2))))
    const res = await fetch(
      `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${FILE_PATH}`,
      {
        method: 'PUT',
        headers: { Authorization: `token ${token.value}`, Accept: 'application/vnd.github.v3+json', 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: 'chore: update sources config via web UI', content, sha: fileSha.value })
      }
    )
    if (!res.ok) throw new Error((await res.json()).message)
    const data = await res.json()
    fileSha.value = data.content.sha
    saveMessage.value = '✅ 保存成功，GitHub Actions 将自动触发数据更新'
    setTimeout(() => saveMessage.value = '', 5000)
  } catch (e) {
    saveMessage.value = `❌ 保存失败: ${e.message}`
  } finally {
    loading.value = false
  }
}

const addCompany = () => {
  config.value.companies.push({
    name: newCompany.value.name,
    name_cn: newCompany.value.name_cn,
    website: newCompany.value.website,
    rss_feeds: newCompany.value.rss_feeds ? newCompany.value.rss_feeds.split(',').map(s => s.trim()) : [],
    keywords: newCompany.value.keywords ? newCompany.value.keywords.split(',').map(s => s.trim()) : []
  })
  newCompany.value = { name: '', name_cn: '', website: '', rss_feeds: '', keywords: '' }
  showAddCompany.value = false
  saveConfig()
}

const removeCompany = (index) => { config.value.companies.splice(index, 1); saveConfig() }

const addKeyword = () => {
  if (newKeyword.value.trim()) {
    config.value.paper_keywords.push(newKeyword.value.trim())
    newKeyword.value = ''
    showAddKeyword.value = false
    saveConfig()
  }
}

const removeKeyword = (index) => { config.value.paper_keywords.splice(index, 1); saveConfig() }

const addWechatAccount = () => {
  config.value.wechat_accounts.push({
    name: newWechatAccount.value.name,
    keywords: newWechatAccount.value.keywords ? newWechatAccount.value.keywords.split(',').map(s => s.trim()) : []
  })
  newWechatAccount.value = { name: '', keywords: '' }
  showAddWechat.value = false
  saveConfig()
}

const removeWechatAccount = (index) => { config.value.wechat_accounts.splice(index, 1); saveConfig() }
</script>

# 配置管理

<div v-if="saveMessage" class="save-message" :class="{ success: saveMessage.includes('✅'), error: saveMessage.includes('❌') }">
  {{ saveMessage }}
</div>

## GitHub Token

<div class="config-section">
  <p class="help-text">输入你的 GitHub Personal Access Token（需要 repo 权限），保存在浏览器本地，不会上传。</p>
  <div class="token-row">
    <input v-model="token" type="password" placeholder="ghp_xxxxxxxxxxxx" class="input-field" style="flex:1" />
    <button @click="saveToken" class="btn-primary" :disabled="loading">{{ loading ? '加载中...' : '连接' }}</button>
  </div>
</div>

<div v-if="fileSha">

## 监控公司

<div class="config-section">
  <div class="section-header">
    <h3>当前监控 {{ config.companies.length }} 家公司</h3>
    <button @click="showAddCompany = !showAddCompany" class="btn-primary">{{ showAddCompany ? '取消' : '+ 添加公司' }}</button>
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
    <button @click="showAddKeyword = !showAddKeyword" class="btn-primary">{{ showAddKeyword ? '取消' : '+ 添加关键词' }}</button>
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
    <button @click="showAddWechat = !showAddWechat" class="btn-primary">{{ showAddWechat ? '取消' : '+ 添加公众号' }}</button>
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

</div>

<style scoped>
.save-message { padding: 1rem; margin-bottom: 1.5rem; border-radius: 8px; font-weight: 500; }
.save-message.success { background: #d1fae5; color: #065f46; border: 1px solid #10b981; }
.save-message.error { background: #fee2e2; color: #991b1b; border: 1px solid #ef4444; }
.config-section { margin: 2rem 0; padding: 1.5rem; border: 1px solid var(--vp-c-divider); border-radius: 8px; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.section-header h3 { margin: 0; }
.token-row { display: flex; gap: 0.5rem; align-items: center; }
.add-form { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem; padding: 1rem; background: var(--vp-c-bg-soft); border-radius: 4px; }
.input-field { padding: 0.5rem; border: 1px solid var(--vp-c-divider); border-radius: 4px; font-size: 14px; background: var(--vp-c-bg); color: var(--vp-c-text-1); }
.company-list, .wechat-list { display: flex; flex-direction: column; gap: 1rem; }
.company-item, .wechat-item { display: flex; justify-content: space-between; align-items: flex-start; padding: 1rem; background: var(--vp-c-bg-soft); border-radius: 4px; }
.company-info, .wechat-info { flex: 1; }
.company-info h4, .wechat-info h4 { margin: 0 0 0.5rem 0; }
.company-info p, .wechat-info p { margin: 0.25rem 0; font-size: 14px; color: var(--vp-c-text-2); }
.keyword-list { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.keyword-item { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; background: var(--vp-c-bg-soft); border-radius: 20px; font-size: 14px; }
.btn-primary { padding: 0.5rem 1rem; background: var(--vp-c-brand); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-success { padding: 0.5rem 1rem; background: #10b981; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
.btn-danger { padding: 0.5rem 1rem; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
.btn-danger-small { padding: 0.25rem 0.5rem; background: #ef4444; color: white; border: none; border-radius: 50%; cursor: pointer; font-size: 16px; line-height: 1; }
.help-text { margin: 0 0 0.75rem 0; font-size: 14px; color: var(--vp-c-text-2); }
</style>
