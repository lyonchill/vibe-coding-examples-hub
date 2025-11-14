# 部署指南 - Vibe-Coding Examples Hub

## 部署到 Render（推薦）

### 前置要求
- GitHub 帳號
- Render 帳號（免費註冊：https://render.com）

### 步驟

#### 1. 準備 GitHub Repository
```bash
# 確保所有文件已提交
git add .
git commit -m "準備部署到 Render"
git push origin main
```

#### 2. 在 Render 創建 Web Service

1. 登入 Render：https://dashboard.render.com
2. 點擊 "New +" → "Web Service"
3. 連接你的 GitHub repository
4. 配置設置：
   - **Name**: `vibe-coding-examples-hub`（或你喜歡的名稱）
   - **Region**: 選擇離你最近的區域
   - **Branch**: `main`（或你的主分支）
   - **Root Directory**: 留空（根目錄）
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

5. 點擊 "Create Web Service"

#### 3. 環境變量（如果需要）
在 Render Dashboard → Environment 中添加：
- `PORT`: Render 會自動設置，無需手動添加
- 其他 API keys（如果需要）：`GEMINI_API_KEY`, `YOUTUBE_API_KEY` 等

#### 4. 部署
- Render 會自動開始構建和部署
- 等待幾分鐘，部署完成後會顯示 URL：`https://your-app-name.onrender.com`

### 注意事項

- **免費層限制**：
  - 服務在 15 分鐘無活動後會休眠
  - 首次訪問可能需要 30-60 秒喚醒
  - 每月 750 小時免費時長

- **數據文件**：
  - `found_examples_latest.json` 會隨代碼一起部署
  - 更新數據需要重新部署（或使用 Supabase）

## 部署到 Railway（備選方案）

### 步驟

1. 登入 Railway：https://railway.app
2. 點擊 "New Project" → "Deploy from GitHub repo"
3. 選擇你的 repository
4. Railway 會自動檢測 Flask 應用並部署
5. 部署完成後會提供 URL

### Railway 免費層
- 每月 $5 免費額度
- 無休眠限制
- 自動 HTTPS

## 部署到 Fly.io（備選方案）

### 步驟

1. 安裝 Fly CLI：`curl -L https://fly.io/install.sh | sh`
2. 登入：`fly auth login`
3. 初始化：`fly launch`
4. 部署：`fly deploy`

### Fly.io 免費層
- 3 個共享 CPU 實例
- 3GB 持久存儲
- 160GB 出站流量

## 可選：使用 Supabase 存儲數據

如果需要動態更新數據而不重新部署：

1. 創建 Supabase 項目：https://supabase.com
2. 創建數據表（見 `supabase_schema.sql`）
3. 運行遷移腳本：`python supabase_migration.py`
4. 更新 `app.py` 從 Supabase 讀取數據

## 故障排除

### 部署失敗
- 檢查 `requirements.txt` 是否正確
- 確認 `Procfile` 格式正確
- 查看 Render/Railway 的構建日誌

### 數據未顯示
- 確認 `found_examples_latest.json` 在 repository 中
- 檢查文件路徑是否正確
- 查看應用日誌

### 端口錯誤
- Render/Railway 會自動設置 `PORT` 環境變量
- 確認 `app.py` 使用 `os.environ.get('PORT')`

