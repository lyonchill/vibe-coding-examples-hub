# AI Examples Hub - Automated Crawler

自動搜尋並整理 AI 專案案例的 Python 工具。

## 🎯 功能

- ✅ 自動搜尋 YouTube 上的 AI 專案影片
- ✅ 使用 Google Gemini 分析內容、提取重點資訊
- ✅ 特別關注 no-code/low-code 工具（Cursor, Lovable, v0, Make.com, n8n 等）
- ✅ 自動分類標籤（Computer Vision, NLP, Generative AI 等）
- ✅ 生成每日 HTML email digest
- ✅ 匯出結構化 JSON 資料

## 📋 提取的資料欄位

每個案例包含：
- Title (標題)
- Description (描述)
- AI Tools Used (使用的 AI 工具)
- Category Tags (分類標籤)
- Source Platform (來源平台)
- Original URL (原始連結)
- Creator Name & Link (創作者資訊)
- Thumbnail URL (縮圖)
- Date Added (加入日期)
- Relevance Score (相關性評分)
- Build Complexity (開發複雜度)

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定 API Keys

建立 `.env` 並填入你的 API keys：

```
YOUTUBE_API_KEY=你的YouTube_API_Key
GEMINI_API_KEY=你的Gemini_API_Key  
EMAIL_TO=你的email地址
```

#### 如何取得 API Keys：

**YouTube Data API v3：**
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 "YouTube Data API v3"
4. 建立 API key (Credentials → Create Credentials → API Key)
5. 免費額度：10,000 quota/天（足夠搜尋約 100 支影片）

**Google Gemini API：**
1. 前往 [Google AI Studio](https://aistudio.google.com/)
2. 建立或選擇專案後，進入右上角「Get API key」
3. 建立 API Key 並複製（格式：`AIza...`），貼到 `.env` 的 `GEMINI_API_KEY`
4. 免費額度：每月 15 次 Gemini 1.5 Flash 免費呼叫（超額依照用量計費）

### 3. 執行 Crawler

```bash
python ai_examples_crawler.py
```

執行後會：
- 搜尋多個關鍵字的 YouTube 影片
- 用 AI 分析每個影片
- 生成 HTML email digest
- 儲存 JSON 資料檔案

## 📊 輸出檔案

執行後會產生兩個檔案：

1. **email_digest_YYYYMMDD.html** - 可在瀏覽器開啟預覽的 email
2. **found_examples_YYYYMMDD.json** - 結構化的案例資料

## ⚙️ 自訂設定

### 修改搜尋關鍵字

編輯 `ai_examples_crawler.py` 的 `SEARCH_KEYWORDS`：

```python
SEARCH_KEYWORDS = [
    "built with Cursor AI",
    "Lovable AI project",
    "你自己的關鍵字"
]
```

### 修改目標工具

編輯 `TARGET_TOOLS` 列表來調整要偵測的 AI 工具。

### 調整相關性門檻

在 `process_content()` 方法中：

```python
if analysis['relevance_score'] < 6:  # 改成你想要的門檻（1-10）
    return None
```

## 🤖 自動化執行

### 方法 1: Cron Job (Mac/Linux)

```bash
# 每天早上 9 點執行
0 9 * * * cd /path/to/project && python ai_examples_crawler.py
```

### 方法 2: GitHub Actions (推薦)

創建 `.github/workflows/daily-crawl.yml`：

```yaml
name: Daily AI Examples Crawl

on:
  schedule:
    - cron: '0 9 * * *'  # 每天 UTC 9:00
  workflow_dispatch:  # 允許手動觸發

jobs:
  crawl:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run crawler
        env:
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
          GEMINI_MODEL: ${{ secrets.GEMINI_MODEL }}
        run: python ai_examples_crawler.py
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: crawl-results
          path: |
            found_examples_*.json
            email_digest_*.html
```

在 GitHub repo 的 Settings → Secrets 中加入你的 API keys。

### 方法 3: 雲端部署

可部署到：
- **Render** (免費方案，支援 Cron Jobs)
- **Railway** (免費 $5 credit/月)
- **Heroku** (有付費 Scheduler add-on)

## 📧 發送 Email

目前 script 會將 email 存成 HTML 檔案。要實際發送 email，有幾個選項：

### 選項 1: Gmail SMTP

在 `send_email()` 方法中加入：

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(self, html_content: str):
    sender = "your-gmail@gmail.com"
    password = "your-app-password"  # 使用 Gmail App Password
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"AI Examples Digest - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = sender
    msg['To'] = EMAIL_TO
    
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, EMAIL_TO, msg.as_string())
```

### 選項 2: SendGrid (推薦)

```bash
pip install sendgrid
```

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(self, html_content: str):
    message = Mail(
        from_email='noreply@yourdomain.com',
        to_emails=EMAIL_TO,
        subject=f"AI Examples Digest - {datetime.now().strftime('%Y-%m-%d')}",
        html_content=html_content
    )
    
    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    response = sg.send(message)
```

## 🔮 未來功能

- [ ] Twitter/X API 整合
- [ ] Medium RSS 解析
- [ ] LinkedIn posts 搜尋
- [ ] 自動去重（避免重複案例）
- [ ] Email 中的 Approve/Reject 連結自動寫入 Google Sheets
- [ ] Slack 通知整合
- [ ] 自動生成案例摘要影片

## 💡 使用建議

1. **先手動執行測試** - 確保 API keys 正確、輸出符合預期
2. **調整搜尋關鍵字** - 根據你的 niche 優化關鍵字
3. **設定每週執行** - 避免 API quota 用完，一週 2-3 次即可
4. **人工審核** - AI 分析不是 100% 準確，建議都過目一遍

## 📝 注意事項

- YouTube API 有每日 quota 限制（10,000 units）
- 每次搜尋約消耗 100 units，每支影片詳細資料約 3-5 units
- Google Gemini API 依用量計費（建議在 Google AI Studio 設定每日/每月用量上限）

## 🤝 整合到網站

找到好案例後，可以：

1. **手動複製** - 從 JSON 檔案複製到你的 `projectsData`
2. **自動同步** - 設定 GitHub Actions 自動 commit JSON 到 repo
3. **Google Sheets** - 寫入 Google Sheets，網站從那裡讀取

## 問題排解

**Q: YouTube API quota 不夠用？**
A: 減少 `SEARCH_KEYWORDS` 數量，或降低 `max_results`

**Q: Gemini 分析太貴？**
A: 調高 `relevance_score` 門檻，或先用簡單的關鍵字過濾，並在 Google AI Studio 設定使用量上限

**Q: 找不到相關案例？**
A: 調整搜尋關鍵字，或降低 `relevance_score` 門檻

---

Made with ❤️ for finding awesome AI projects
