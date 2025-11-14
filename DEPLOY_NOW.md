# 🚀 立即部署步驟

## 步驟 1: 推送到 GitHub

你的代碼已經準備好，現在需要推送到 GitHub：

```bash
# 如果還沒有 GitHub repository，先創建一個：
# 1. 訪問 https://github.com/new
# 2. 創建一個新的 repository（例如：vibe-coding-examples-hub）
# 3. 不要初始化 README、.gitignore 或 license（我們已經有了）

# 然後執行：
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

**或者**，如果你已經有 GitHub repository：

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## 步驟 2: 在 Render 部署

### 2.1 登入 Render
1. 訪問 https://render.com
2. 點擊 "Get Started for Free"
3. 選擇 "Sign up with GitHub"（推薦）

### 2.2 創建 Web Service
1. 登入後，點擊右上角 "New +"
2. 選擇 "Web Service"

### 2.3 連接 GitHub Repository
1. 在 "Connect a repository" 部分
2. 點擊 "Connect account"（如果還沒連接）
3. 授權 Render 訪問你的 GitHub
4. 搜索並選擇你的 repository

### 2.4 配置設置
填寫以下信息：

- **Name**: `vibe-coding-examples-hub`（或你喜歡的名稱）
- **Region**: 選擇離你最近的區域
  - `Singapore`（亞洲）
  - `Oregon`（美國西部）
  - `Frankfurt`（歐洲）
- **Branch**: `main`
- **Root Directory**: 留空（使用根目錄）
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: `Free`

### 2.5 環境變量（可選）
如果需要使用 Supabase 或其他 API：
- 點擊 "Advanced"
- 添加環境變量：
  - `SUPABASE_URL`（如果使用 Supabase）
  - `SUPABASE_KEY`（如果使用 Supabase）

### 2.6 部署
1. 點擊 "Create Web Service"
2. Render 會自動開始構建
3. 等待 3-5 分鐘完成部署
4. 部署完成後，你會看到：
   - ✅ "Live" 狀態
   - 🌐 URL：`https://vibe-coding-examples-hub.onrender.com`

## 步驟 3: 驗證部署

1. 訪問你的網站 URL
2. 檢查網站是否正常顯示
3. 如果首次訪問需要 30-60 秒，這是正常的（免費層休眠後喚醒）

## 故障排除

### 構建失敗
- 檢查 Render 的 "Logs" 標籤
- 確認 `requirements.txt` 包含所有依賴
- 確認 `Procfile` 格式正確

### 應用無法啟動
- 檢查 "Logs" 中的錯誤信息
- 確認 `gunicorn` 已安裝（在 requirements.txt 中）
- 確認端口配置正確（使用環境變量 PORT）

### 數據未顯示
- 確認 `found_examples_latest.json` 在 repository 中
- 檢查文件路徑是否正確
- 查看應用日誌

## 完成後

部署成功後，你的網站將：
- ✅ 自動從 GitHub 部署（每次 push 到 main 分支）
- ✅ 免費託管（Render 免費層）
- ✅ HTTPS 自動配置
- ✅ 全球可訪問

## 更新網站

要更新網站內容：
1. 修改本地代碼
2. 更新 `found_examples_latest.json`（如果需要）
3. 推送到 GitHub：
   ```bash
   git add .
   git commit -m "更新內容"
   git push origin main
   ```
4. Render 會自動重新部署（約 3-5 分鐘）

