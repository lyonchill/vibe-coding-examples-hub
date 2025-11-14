# Vibe-Coding Examples Hub - 網站使用說明

這是一個展示 YouTube 上最熱門 AI 編程案例的網站。

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r "AI Examples Crawler/requirements.txt"
```

### 2. 配置環境變數

確保 `.env` 文件已正確配置（在 `AI Examples Crawler` 目錄中）：

```
YOUTUBE_API_KEY=你的YouTube_API_Key
GEMINI_API_KEY=你的Gemini_API_Key
```

### 3. 運行爬蟲獲取數據

```bash
python "AI Examples Crawler/ai_examples_crawler.py"
```

這會：
- 從 YouTube 搜索最熱門的 AI 編程案例
- 使用 Gemini AI 分析每個案例
- 保存 30 個最熱門的案例到 `found_examples_latest.json`

### 4. 啟動網站

```bash
python app.py
```

然後在瀏覽器中打開：http://localhost:5000

## 📁 文件結構

```
.
├── app.py                          # Flask 網站主文件
├── templates/
│   └── index.html                  # 網站首頁模板
├── AI Examples Crawler/
│   ├── ai_examples_crawler.py      # 爬蟲腳本
│   ├── requirements.txt            # Python 依賴
│   └── .env                        # 環境變數配置
├── found_examples_latest.json      # 最新的案例數據（網站讀取此文件）
└── found_examples_YYYYMMDD.json    # 帶日期的歷史數據備份
```

## 🎨 網站功能

- **展示 30 個最熱門案例**：按 YouTube 觀看數排序
- **篩選功能**：可按 No-Code、Low-Code、Full Build 篩選
- **詳細信息**：每個案例顯示：
  - 專案名稱和摘要
  - AI 工具標籤
  - 分類標籤
  - 觀看數、讚數、留言數
  - 創作者信息
  - 直接連結到 YouTube 影片

## 🔄 更新數據

定期運行爬蟲腳本來更新網站數據：

```bash
python "AI Examples Crawler/ai_examples_crawler.py"
```

網站會自動讀取最新的 `found_examples_latest.json` 文件。

## 🌐 部署

### 本地部署

直接運行 `python app.py` 即可。

### 生產環境部署

可以使用以下方式部署：

1. **使用 Gunicorn**：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **使用 Docker**（可選）：
創建 `Dockerfile` 和 `docker-compose.yml` 進行容器化部署

3. **部署到雲端**：
- Heroku
- Railway
- Render
- Vercel (需要適配)

## 📝 注意事項

- 確保 YouTube API 配額充足（每天有足夠的請求次數）
- Gemini API 用於分析內容，確保 API Key 有效
- 網站會自動讀取最新的 JSON 數據文件
- 建議定期運行爬蟲更新數據（例如每天一次）

## 🐛 故障排除

1. **網站顯示「目前沒有案例」**：
   - 確認已運行爬蟲腳本
   - 檢查 `found_examples_latest.json` 是否存在
   - 查看爬蟲腳本的輸出日誌

2. **API 錯誤**：
   - 檢查 `.env` 文件中的 API Key 是否正確
   - 確認 API 配額是否充足

3. **端口被占用**：
   - 修改 `app.py` 中的端口號（默認 5000）

