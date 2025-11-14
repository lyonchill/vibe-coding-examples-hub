"""
使用付費截圖 API 獲取 LinkedIn 貼文截圖
支持多種截圖服務：ScreenshotAPI, urlbox.io, htmlcsstoimage, screenshot.one
"""
import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import sys

# 添加父目錄到路徑
sys.path.insert(0, str(Path(__file__).parent))
from ai_examples_crawler import AIExamplesCrawler

load_dotenv()

def get_screenshot_url(linkedin_url, service='auto'):
    """
    使用截圖 API 獲取 LinkedIn 貼文截圖
    
    Args:
        linkedin_url: LinkedIn 貼文 URL
        service: 使用的服務 ('screenshotapi', 'urlbox', 'htmlcsstoimage', 'screenshotone', 'auto')
    
    Returns:
        截圖 URL 或 None
    """
    screenshot_url = None
    
    # 自動選擇可用的服務
    if service == 'auto':
        if os.getenv("SCREENSHOTAPI_KEY"):
            service = 'screenshotapi'
        elif os.getenv("URLBOX_API_KEY"):
            service = 'urlbox'
        elif os.getenv("HTMLCSSTOIMAGE_API_KEY"):
            service = 'htmlcsstoimage'
        elif os.getenv("SCREENSHOTONE_KEY"):
            service = 'screenshotone'
        else:
            print("  ⚠️  沒有找到任何截圖 API key，使用 Open Graph 圖片")
            return None
    
    # ScreenshotAPI.net
    if service == 'screenshotapi':
        api_key = os.getenv("SCREENSHOTAPI_KEY")
        if api_key:
            try:
                # ScreenshotAPI 支持 LinkedIn 截圖
                params = {
                    'access_key': api_key,
                    'url': linkedin_url,
                    'viewport_width': 1200,
                    'viewport_height': 800,
                    'device_scale_factor': 1,
                    'format': 'png',
                    'image_quality': 90,
                    'block_ads': True,
                    'block_cookie_banners': True,
                    'block_banners': True,
                    'block_trackers': True,
                    'delay': 3,  # 等待頁面載入
                    'wait_until': 'networkidle0'  # 等待網絡請求完成
                }
                screenshot_url = f"https://api.screenshotapi.net/screenshot?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
                print(f"  ✅ 使用 ScreenshotAPI")
            except Exception as e:
                print(f"  ⚠️  ScreenshotAPI 錯誤: {e}")
    
    # urlbox.io
    elif service == 'urlbox':
        api_key = os.getenv("URLBOX_API_KEY")
        api_secret = os.getenv("URLBOX_SECRET", "")
        if api_key:
            try:
                import hashlib
                import hmac
                import time
                import urllib.parse
                
                # urlbox.io 需要簽名
                params = {
                    'url': linkedin_url,
                    'width': 1200,
                    'height': 800,
                    'format': 'png',
                    'quality': 90,
                    'wait': 3000,  # 等待 3 秒
                    'block_ads': 'true',
                    'block_cookies': 'true'
                }
                
                query_string = urllib.parse.urlencode(params)
                if api_secret:
                    # 生成簽名
                    signature = hmac.new(
                        api_secret.encode(),
                        query_string.encode(),
                        hashlib.sha1
                    ).hexdigest()
                    query_string += f"&signature={signature}"
                
                screenshot_url = f"https://api.urlbox.io/v1/{api_key}/png?{query_string}"
                print(f"  ✅ 使用 urlbox.io")
            except Exception as e:
                print(f"  ⚠️  urlbox.io 錯誤: {e}")
    
    # htmlcsstoimage.com
    elif service == 'htmlcsstoimage':
        api_key = os.getenv("HTMLCSSTOIMAGE_API_KEY")
        if api_key:
            try:
                # htmlcsstoimage 需要先獲取截圖 ID，然後再獲取圖片
                response = requests.post(
                    'https://hcti.io/v1/image',
                    auth=(api_key, ''),
                    data={
                        'url': linkedin_url,
                        'viewport_width': 1200,
                        'viewport_height': 800,
                        'device_scale_factor': 1,
                        'delay': 3
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    screenshot_url = result.get('url')
                    print(f"  ✅ 使用 htmlcsstoimage")
            except Exception as e:
                print(f"  ⚠️  htmlcsstoimage 錯誤: {e}")
    
    # screenshot.one
    elif service == 'screenshotone':
        api_key = os.getenv("SCREENSHOTONE_KEY")
        if api_key:
            try:
                params = {
                    'access_key': api_key,
                    'url': linkedin_url,
                    'viewport_width': 1200,
                    'viewport_height': 800,
                    'device_scale_factor': 1,
                    'format': 'png',
                    'image_quality': 90,
                    'block_ads': 'true',
                    'block_cookie_banners': 'true',
                    'block_banners': 'true',
                    'block_trackers': 'true',
                    'delay': 3
                }
                screenshot_url = f"https://api.screenshot.one/take?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
                print(f"  ✅ 使用 screenshot.one")
            except Exception as e:
                print(f"  ⚠️  screenshot.one 錯誤: {e}")
    
    return screenshot_url


def create_linkedin_example_with_api(content, service='auto'):
    """
    創建 LinkedIn 案例，使用付費截圖 API
    """
    linkedin_url = content.get('url', '')
    title = content.get('title', '') or content.get('snippet', '')[:100]
    
    # 獲取截圖
    print(f"\n處理: {title[:60]}...")
    screenshot_url = get_screenshot_url(linkedin_url, service)
    
    # 如果 API 失敗，回退到 Open Graph
    if not screenshot_url:
        print("  ⚠️  使用 Open Graph 圖片作為備選")
        try:
            response = requests.get(linkedin_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            if response.status_code == 200:
                import re
                patterns = [
                    r'<meta\s+property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
                    r'<meta\s+name=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
                ]
                for pattern in patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        screenshot_url = match.group(1)
                        if screenshot_url.startswith('//'):
                            screenshot_url = 'https:' + screenshot_url
                        break
        except:
            pass
    
    example = {
        'title': title,
        'description': content.get('snippet', '')[:200],
        'original_url': linkedin_url,
        'source_platform': 'LinkedIn',
        'thumbnail_url': screenshot_url,
        'complexity': 'Unknown',
        'tools': [],
        'category': 'AI Development',
        'relevance_score': 0.8,
        'published_date': content.get('date', ''),
        'view_count': 0,
        'like_count': 0,
        'comment_count': 0
    }
    
    return example


if __name__ == "__main__":
    print("=" * 60)
    print("LinkedIn 案例爬蟲（使用付費截圖 API）")
    print("=" * 60)
    
    # 檢查 API keys
    services = []
    if os.getenv("SCREENSHOTAPI_KEY"):
        services.append("ScreenshotAPI")
    if os.getenv("URLBOX_API_KEY"):
        services.append("urlbox.io")
    if os.getenv("HTMLCSSTOIMAGE_API_KEY"):
        services.append("htmlcsstoimage")
    if os.getenv("SCREENSHOTONE_KEY"):
        services.append("screenshot.one")
    
    if not services:
        print("\n⚠️  沒有找到任何截圖 API key！")
        print("\n請在 .env 文件中添加以下任一服務的 API key：")
        print("  - SCREENSHOTAPI_KEY (ScreenshotAPI.net)")
        print("  - URLBOX_API_KEY + URLBOX_SECRET (urlbox.io)")
        print("  - HTMLCSSTOIMAGE_API_KEY (htmlcsstoimage.com)")
        print("  - SCREENSHOTONE_KEY (screenshot.one)")
        print("\n將使用 Open Graph 圖片作為備選方案。")
    else:
        print(f"\n✅ 找到 {len(services)} 個截圖服務: {', '.join(services)}")
    
    # 搜尋 LinkedIn 貼文
    crawler = AIExamplesCrawler()
    keywords = [
        "built with Cursor",
        "Lovable project",
        "v0 by Vercel",
        "AI coding assistant",
        "no-code builder"
    ]
    
    all_content = []
    for keyword in keywords:
        print(f"\n搜尋: {keyword}")
        results = crawler.search_linkedin_via_serpapi(keyword, max_results=5)
        all_content.extend(results)
        print(f"  找到 {len(results)} 個結果")
    
    # 去重
    seen_urls = set()
    unique_content = []
    for content in all_content:
        if content['url'] not in seen_urls:
            seen_urls.add(content['url'])
            unique_content.append(content)
    
    print(f"\n總共找到 {len(unique_content)} 個唯一 LinkedIn 貼文")
    
    # 處理每個貼文
    examples = []
    for i, content in enumerate(unique_content[:15], 1):
        example = create_linkedin_example_with_api(content, service='auto')
        examples.append(example)
        print(f"  [{i}/{len(unique_content[:15])}] ✅ {example['title'][:50]}...")
        print(f"      截圖: {'✅' if example.get('thumbnail_url') else '❌'}")
    
    # 載入現有數據
    data_file = Path(__file__).parent.parent / "found_examples_latest.json"
    existing_examples = []
    if data_file.exists():
        existing_examples = json.load(open(data_file, 'r', encoding='utf-8'))
        # 移除舊的 LinkedIn 案例
        existing_examples = [x for x in existing_examples if x.get('source_platform') != 'LinkedIn']
    
    # 合併數據
    all_examples = existing_examples + examples
    
    # 去重
    seen_urls = set()
    unique_examples = []
    for ex in all_examples:
        if ex['original_url'] not in seen_urls:
            seen_urls.add(ex['original_url'])
            unique_examples.append(ex)
    
    # 排序
    unique_examples.sort(key=lambda x: (
        0 if x.get('source_platform') == 'YouTube' else 1,
        x.get('view_count', 0) if x.get('source_platform') == 'YouTube' else 0,
        x.get('relevance_score', 0)
    ), reverse=True)
    
    # 保存
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(unique_examples[:40], f, indent=2, ensure_ascii=False)
    
    youtube_count = len([x for x in unique_examples if x.get('source_platform') == 'YouTube'])
    linkedin_count = len([x for x in unique_examples if x.get('source_platform') == 'LinkedIn'])
    linkedin_with_img = len([x for x in unique_examples if x.get('source_platform') == 'LinkedIn' and x.get('thumbnail_url')])
    
    print(f"\n{'='*60}")
    print("✅ 完成！")
    print(f"{'='*60}")
    print(f"  📺 YouTube: {youtube_count}")
    print(f"  💼 LinkedIn: {linkedin_count} (其中 {linkedin_with_img} 個有截圖)")
    print(f"  總計: {len(unique_examples)}")
    print(f"\n數據已保存到: {data_file}")

