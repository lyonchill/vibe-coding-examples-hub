# 🚀 AI Examples Crawler - 快速開始

## 你現在有什麼

✅ **完整的自動化爬蟲系統**，可以：
- 每天自動搜尋 YouTube 上的 AI 專案案例
- 用 Google Gemini 智能分析和分類內容
- 特別關注 no-code/low-code 工具（Cursor, Lovable, v0, Make, n8n）
- 生成漂亮的 HTML email digest
- 匯出結構化 JSON 資料

## 📦 檔案說明

```
├── ai_examples_crawler.py      # 主程式（核心爬蟲）
├── test_setup.py                # API 測試工具
├── google_sheets_integration.py # Google Sheets 整合（選用）
├── requirements.txt             # Python 套件清單
├── README.md                    # 完整文件
└── .github/workflows/
    └── daily-crawl.yml          # GitHub Actions 自動化設定
```

## ⚡ 3 步驟開始使用

### 1️⃣ 安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 2️⃣ 設定 API Keys

建立或編輯 `.env` 檔案，至少包含：
- `YOUTUBE_API_KEY` - 從 [Google Cloud Console](https://console.cloud.google.com/) 取得
- `GEMINI_API_KEY` - 從 [Google AI Studio](https://aistudio.google.com/) 取得  
- `EMAIL_TO` - 你的 email 地址

### 3️⃣ 測試並執行

```bash
# 先測試 API 設定是否正確
python test_setup.py

# 如果測試通過，執行爬蟲
python ai_examples_crawler.py
```

執行後會產生：
- `email_digest_YYYYMMDD.html` - 在瀏覽器打開看結果
- `found_examples_YYYYMMDD.json` - 結構化資料

## 📧 Email 工作流程

目前 script 會**存成 HTML 檔案**而不是真的發 email。

**為什麼？** 讓你先預覽結果，確認品質。

**要實際發 email：** 看 `README.md` 的「發送 Email」章節，有 Gmail SMTP 和 SendGrid 的程式碼範例。

## 🤖 自動化執行

### 選項 A: GitHub Actions（推薦，完全免費）

1. 把這些檔案上傳到你的 GitHub repo
2. 在 repo Settings → Secrets 加入：
   - `YOUTUBE_API_KEY`
   - `GEMINI_API_KEY`
   - `EMAIL_TO`
   - （選用）`GEMINI_MODEL`
3. GitHub 會每天自動執行！

### 選項 B: 本地電腦 Cron Job

Mac/Linux:
```bash
crontab -e
# 加入：每天早上 9 點執行
0 9 * * * cd /path/to/project && python ai_examples_crawler.py
```

Windows Task Scheduler:
- 建立新任務
- 觸發器：每天 9:00
- 動作：執行 `python ai_examples_crawler.py`

## 🎯 客製化關鍵字

編輯 `ai_examples_crawler.py` 的這段：

```python
SEARCH_KEYWORDS = [
    "built with Cursor AI",
    "Lovable AI project",
    "加你自己想搜的關鍵字"
]
```

## 💡 接下來做什麼？

### 階段 1：測試和調整（本週）
1. ✅ 執行幾次，看看找到什麼案例
2. ✅ 調整關鍵字和相關性門檻
3. ✅ 確認 AI 分析的品質

### 階段 2：自動化（下週）
1. ✅ 設定 GitHub Actions 或 Cron Job
2. ✅ 串接 Gmail/SendGrid 真的發 email
3. ✅ （選用）串接 Google Sheets

### 階段 3：整合到網站
1. ✅ 把 JSON 資料整合到你的 HTML 網站
2. ✅ 或設定 Google Sheets 作為資料來源
3. ✅ 網站自動顯示最新案例

## 📊 成本估算

- **YouTube API:** 免費（10,000 quota/天，夠用）
- **Google Gemini API:** Gemini 1.5 Flash 每月有免費額度，超額後依官方價目計費（建議在 AI Studio 設定配額上限）
- **其他:** 全部免費

## ❓ 遇到問題？

1. **先跑 `test_setup.py`** 確認 API 設定正確
2. **看 `README.md`** 有完整的疑難排解
3. **調整參數：**
   - 減少 `SEARCH_KEYWORDS` 數量（省 quota）
   - 提高 `relevance_score` 門檻（省 API 成本）
   - 修改 `max_results` 參數（控制搜尋數量）

## 🎉 就是這樣！

你現在有一個完整的 AI 案例自動搜尋系統了。

執行看看，有問題隨時問我！

---

P.S. 記得把 `.env` 加入 `.gitignore`，不要把 API keys 上傳到 GitHub！
