# Render 部署步驟指南

## 快速部署步驟

### 1. 準備 GitHub Repository

確保你的代碼已經推送到 GitHub：

```bash
cd "/Users/Liyuan/Desktop/作品集網站用圖/Vibe-coding examples"
git init  # 如果還沒有初始化
git add .
git commit -m "準備部署到 Render"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 2. 在 Render 創建 Web Service

1. **登入 Render**
   - 訪問 https://render.com
   - 使用 GitHub 帳號登入（推薦）

2. **創建新 Web Service**
   - 點擊 "New +" 按鈕
   - 選擇 "Web Service"

3. **連接 GitHub Repository**
   - 選擇 "Connect GitHub"
   - 授權 Render 訪問你的 repository
   - 選擇你的 repository

4. **配置設置**
   - **Name**: `vibe-coding-examples-hub`（或你喜歡的名稱）
   - **Region**: 選擇離你最近的區域（如 `Singapore` 或 `Oregon`）
   - **Branch**: `main`
   - **Root Directory**: 留空（使用根目錄）
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

5. **環境變量（可選）**
   - 如果需要使用 Supabase，添加：
     - `SUPABASE_URL`: 你的 Supabase 項目 URL
     - `SUPABASE_KEY`: 你的 Supabase API Key
   - 其他 API keys（如果需要）

6. **創建並部署**
   - 點擊 "Create Web Service"
   - Render 會自動開始構建和部署
   - 等待 3-5 分鐘完成部署

### 3. 訪問網站

部署完成後，你會獲得一個 URL：
- `https://vibe-coding-examples-hub.onrender.com`（或你設置的名稱）

### 4. 更新數據

如果需要更新數據：

**方法 1：重新部署**
- 更新 `found_examples_latest.json`
- 推送到 GitHub
- Render 會自動重新部署

**方法 2：使用 Supabase（推薦）**
- 設置 Supabase
- 運行 `python supabase_migration.py`
- 更新環境變量使用 Supabase

## 免費層限制

- **休眠**：15 分鐘無活動後會休眠
- **喚醒時間**：首次訪問需要 30-60 秒
- **時長**：每月 750 小時免費
- **足夠**：對於個人項目完全足夠

## 故障排除

### 構建失敗
- 檢查 `requirements.txt` 是否包含所有依賴
- 確認 Python 版本（`runtime.txt`）
- 查看 Render 的構建日誌

### 應用無法啟動
- 確認 `Procfile` 格式正確：`web: gunicorn app:app`
- 檢查端口配置（應使用環境變量 `PORT`）
- 查看應用日誌

### 數據未顯示
- 確認 `found_examples_latest.json` 在 repository 中
- 檢查文件路徑
- 查看應用日誌中的錯誤信息

## 下一步

部署成功後，你可以：
- 設置自定義域名（在 Render Dashboard）
- 配置自動部署（每次 push 到 main 分支自動部署）
- 設置 Supabase 實現動態數據更新

