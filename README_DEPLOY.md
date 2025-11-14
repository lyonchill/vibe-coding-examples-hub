# 🚀 部署指南

## 快速開始

### 方案 1：Render（推薦，最簡單）

1. **推送到 GitHub**
   ```bash
   git add .
   git commit -m "準備部署"
   git push origin main
   ```

2. **在 Render 部署**
   - 訪問 https://render.com
   - 登入（使用 GitHub）
   - New + → Web Service
   - 連接你的 GitHub repository
   - 設置：
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - Plan: Free
   - 點擊 Create Web Service
   - 等待 3-5 分鐘完成部署

3. **完成！**
   - 獲得 URL：`https://your-app-name.onrender.com`
   - 網站已上線！

### 方案 2：Railway（備選）

1. 訪問 https://railway.app
2. New Project → Deploy from GitHub repo
3. 選擇你的 repository
4. Railway 會自動檢測並部署
5. 完成！

### 方案 3：Fly.io（備選）

```bash
# 安裝 Fly CLI
curl -L https://fly.io/install.sh | sh

# 登入
fly auth login

# 初始化並部署
fly launch
fly deploy
```

## 文件說明

- `requirements.txt` - Python 依賴
- `Procfile` - 告訴 Render 如何啟動應用
- `runtime.txt` - Python 版本
- `app.py` - Flask 應用主文件
- `found_examples_latest.json` - 數據文件（會隨代碼一起部署）

## 可選：使用 Supabase

如果需要動態更新數據：

1. 創建 Supabase 項目：https://supabase.com
2. 運行 SQL：`supabase_schema.sql`
3. 運行遷移：`python supabase_migration.py`
4. 在 Render 添加環境變量：
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
5. 將 `app_supabase.py` 重命名為 `app.py`

## 免費層限制

- **Render**: 15 分鐘無活動後休眠，首次訪問需 30-60 秒喚醒
- **Railway**: 每月 $5 免費額度
- **Fly.io**: 3 個共享 CPU，160GB 流量

## 需要幫助？

查看詳細文檔：
- `DEPLOYMENT.md` - 完整部署指南
- `RENDER_SETUP.md` - Render 詳細設置步驟

