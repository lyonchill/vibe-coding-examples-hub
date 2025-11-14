# LinkedIn 貼文截圖獲取指南

## 為什麼 LinkedIn 截圖困難？

LinkedIn 貼文通常需要登入才能查看完整內容，這使得公開的截圖服務無法正常工作。

## 解決方案

### 方法 1: 使用 Open Graph 圖片（當前使用，無需登入）

LinkedIn 會為公開貼文提供 Open Graph 圖片，這是目前最簡單的方法。

**優點：**
- 無需 API key
- 免費
- 自動獲取

**缺點：**
- 可能不是完整的貼文截圖
- 有時只是 LinkedIn logo 或預設圖片

### 方法 2: 使用 LinkedIn API（需要登入和 OAuth）

如果你有 LinkedIn 開發者帳號並完成 OAuth 認證：

1. **創建 LinkedIn App**
   - 前往 https://www.linkedin.com/developers/apps
   - 創建應用並獲取 OAuth credentials

2. **使用 LinkedIn API v2**
   - 需要 `r_basicprofile` 和 `r_liteprofile` 權限
   - 可以獲取貼文的詳細信息，包括圖片

3. **設置環境變數**
   ```
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   LINKEDIN_ACCESS_TOKEN=your_access_token
   ```

### 方法 3: 使用付費截圖服務（推薦，如果預算允許）

以下服務支持 LinkedIn 截圖（需要登入模擬）：

1. **ScreenshotAPI.net**
   - 免費額度：100 張/月
   - 付費：$9/月起
   - 支持 LinkedIn 截圖
   - 設置：在 `.env` 中添加 `SCREENSHOTAPI_KEY`

2. **urlbox.io**
   - 免費額度：1000 張/月
   - 付費：$19/月起
   - 支持 LinkedIn 截圖
   - 設置：在 `.env` 中添加 `URLBOX_API_KEY` 和 `URLBOX_SECRET`

3. **htmlcsstoimage.com**
   - 免費額度：50 張/月
   - 付費：$9/月起
   - 支持 LinkedIn 截圖
   - 設置：在 `.env` 中添加 `HTMLCSSTOIMAGE_API_KEY`

4. **screenshot.one**
   - 免費額度：100 張/月
   - 付費：$9/月起
   - 支持 LinkedIn 截圖
   - 設置：在 `.env` 中添加 `SCREENSHOTONE_KEY`

### 方法 4: 使用瀏覽器自動化（需要服務器）

使用 Puppeteer 或 Playwright 自動登入並截圖：

```python
from playwright.sync_api import sync_playwright

def get_linkedin_screenshot(url, username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # 登入 LinkedIn
        page.goto("https://www.linkedin.com/login")
        page.fill("#username", username)
        page.fill("#password", password)
        page.click("button[type=submit]")
        # 訪問貼文並截圖
        page.goto(url)
        screenshot = page.screenshot()
        browser.close()
        return screenshot
```

**注意：** 這需要：
- 服務器環境
- LinkedIn 帳號憑證（不建議在生產環境使用）
- 可能違反 LinkedIn 服務條款

## 推薦方案

**目前最佳方案：**
1. 使用 Open Graph 圖片（已實現，免費）
2. 如果需要更好的截圖，使用 ScreenshotAPI.net 或 urlbox.io（付費但可靠）

**設置付費服務：**
1. 註冊 ScreenshotAPI.net 或 urlbox.io
2. 獲取 API key
3. 添加到 `.env` 文件
4. 重新運行爬蟲

## 當前狀態

目前使用 Open Graph 圖片方法，所有 LinkedIn 案例都有截圖。如果你需要更完整的截圖，建議使用付費截圖服務。

