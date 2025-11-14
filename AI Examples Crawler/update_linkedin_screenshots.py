"""
更新現有 LinkedIn 案例的截圖，使用付費截圖 API
"""
import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import sys

sys.path.insert(0, str(Path(__file__).parent))
from ai_examples_crawler import AIExamplesCrawler

# 載入 .env（從當前目錄或父目錄）
load_dotenv()
load_dotenv(Path(__file__).parent.parent / '.env')

def get_screenshot_url(linkedin_url, service='auto'):
    """使用截圖 API 獲取 LinkedIn 貼文截圖"""
    screenshot_url = None
    
    # 首先嘗試 microlink.io（免費，支持 LinkedIn）
    try:
        # microlink.io 需要調用 API 獲取圖片 URL
        microlink_api = f"https://api.microlink.io?url={linkedin_url}&screenshot=true"
        response = requests.get(microlink_api, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success' and result.get('data', {}).get('image', {}).get('url'):
                screenshot_url = result['data']['image']['url']
                print(f"  ✅ 使用 microlink.io（免費服務）")
                return screenshot_url
    except Exception as e:
        pass
    
    # 自動選擇可用的服務（嘗試多種可能的變數名）
    if service == 'auto':
        screenshotapi_key = (os.getenv("SCREENSHOTAPI_KEY") or 
                           os.getenv("SCREENSHOT_API_KEY") or
                           os.getenv("screenshotapi_key") or
                           os.getenv("ScreenshotAPI_KEY"))
        if screenshotapi_key:
            service = 'screenshotapi'
        elif os.getenv("URLBOX_API_KEY"):
            service = 'urlbox'
        elif os.getenv("HTMLCSSTOIMAGE_API_KEY"):
            service = 'htmlcsstoimage'
        elif os.getenv("SCREENSHOTONE_KEY"):
            service = 'screenshotone'
        else:
            return None
    
    # ScreenshotAPI.net
    if service == 'screenshotapi':
        # 嘗試多種可能的變數名
        api_key = (os.getenv("SCREENSHOTAPI_KEY") or 
                  os.getenv("SCREENSHOT_API_KEY") or
                  os.getenv("screenshotapi_key") or
                  os.getenv("ScreenshotAPI_KEY"))
        if api_key:
            try:
                # ScreenshotAPI 需要實際調用 API 來獲取截圖 URL
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
                    'delay': 3,
                }
                
                # ScreenshotAPI 直接返回圖片，使用 URL 格式
                # 格式: https://api.screenshotapi.net/screenshot?access_key=KEY&url=URL&...
                screenshot_url = f"https://api.screenshotapi.net/screenshot?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
                
                # 驗證 URL 是否可訪問（可選，但會增加時間）
                try:
                    # 只檢查 HEAD 請求，不下載完整圖片
                    verify_response = requests.head(screenshot_url, timeout=5, allow_redirects=True)
                    if verify_response.status_code == 200 and 'image' in verify_response.headers.get('Content-Type', ''):
                        print(f"  ✅ 使用 ScreenshotAPI，截圖 URL 驗證成功")
                    else:
                        print(f"  ⚠️  截圖 URL 可能無效，狀態碼: {verify_response.status_code}")
                except:
                    # 如果驗證失敗，仍然使用 URL（可能只是需要時間生成）
                    print(f"  ✅ 使用 ScreenshotAPI（URL 已生成，可能需要時間載入）")
            except Exception as e:
                print(f"  ⚠️  ScreenshotAPI 錯誤: {e}")
                screenshot_url = None
    
    # urlbox.io
    elif service == 'urlbox':
        api_key = os.getenv("URLBOX_API_KEY")
        api_secret = os.getenv("URLBOX_SECRET", "")
        if api_key:
            try:
                import hashlib
                import hmac
                import urllib.parse
                
                params = {
                    'url': linkedin_url,
                    'width': 1200,
                    'height': 800,
                    'format': 'png',
                    'quality': 90,
                    'wait': 3000,
                    'block_ads': 'true',
                    'block_cookies': 'true'
                }
                
                query_string = urllib.parse.urlencode(params)
                if api_secret:
                    signature = hmac.new(
                        api_secret.encode(),
                        query_string.encode(),
                        hashlib.sha1
                    ).hexdigest()
                    query_string += f"&signature={signature}"
                
                screenshot_url = f"https://api.urlbox.io/v1/{api_key}/png?{query_string}"
            except Exception as e:
                print(f"  ⚠️  urlbox.io 錯誤: {e}")
    
    # htmlcsstoimage.com
    elif service == 'htmlcsstoimage':
        api_key = os.getenv("HTMLCSSTOIMAGE_API_KEY")
        if api_key:
            try:
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
            except Exception as e:
                print(f"  ⚠️  screenshot.one 錯誤: {e}")
    
    return screenshot_url


def update_linkedin_screenshots():
    """更新所有 LinkedIn 案例的截圖"""
    
    # 載入數據
    data_file = Path(__file__).parent.parent / "found_examples_latest.json"
    
    if not data_file.exists():
        print(f"❌ 找不到數據文件: {data_file}")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        examples = json.load(f)
    
    # 找出所有 LinkedIn 案例
    linkedin_examples = [ex for ex in examples if ex.get('source_platform') == 'LinkedIn']
    
    if not linkedin_examples:
        print("❌ 沒有找到 LinkedIn 案例")
        return
    
    # 檢查 API key（嘗試多種可能的變數名）
    services = []
    screenshotapi_key = (os.getenv("SCREENSHOTAPI_KEY") or 
                       os.getenv("SCREENSHOT_API_KEY") or
                       os.getenv("screenshotapi_key") or
                       os.getenv("ScreenshotAPI_KEY"))
    if screenshotapi_key:
        services.append("ScreenshotAPI")
    if os.getenv("URLBOX_API_KEY"):
        services.append("urlbox.io")
    if os.getenv("HTMLCSSTOIMAGE_API_KEY"):
        services.append("htmlcsstoimage")
    if os.getenv("SCREENSHOTONE_KEY"):
        services.append("screenshot.one")
    
    if not services:
        print("❌ 沒有找到任何截圖 API key！")
        print("\n請在 .env 文件中添加以下任一服務的 API key：")
        print("  - SCREENSHOTAPI_KEY (ScreenshotAPI.net)")
        print("  - URLBOX_API_KEY + URLBOX_SECRET (urlbox.io)")
        print("  - HTMLCSSTOIMAGE_API_KEY (htmlcsstoimage.com)")
        print("  - SCREENSHOTONE_KEY (screenshot.one)")
        return
    
    print(f"✅ 找到 {len(services)} 個截圖服務: {', '.join(services)}")
    print(f"\n找到 {len(linkedin_examples)} 個 LinkedIn 案例")
    print("開始更新截圖...\n")
    
    updated_count = 0
    
    for i, example in enumerate(linkedin_examples, 1):
        url = example.get('original_url', '')
        if not url:
            continue
        
        print(f"[{i}/{len(linkedin_examples)}] 處理: {example['title'][:50]}...")
        
        # 獲取新的截圖 URL
        new_screenshot = get_screenshot_url(url, service='auto')
        
        if new_screenshot:
            old_screenshot = example.get('thumbnail_url', '')
            example['thumbnail_url'] = new_screenshot
            updated_count += 1
            print(f"  ✅ 更新截圖")
            if old_screenshot:
                print(f"     舊: {old_screenshot[:60]}...")
            print(f"     新: {new_screenshot[:60]}...")
        else:
            print(f"  ⚠️  無法獲取截圖（API 可能失敗或需要等待）")
    
    # 保存更新後的數據
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 完成！更新了 {updated_count}/{len(linkedin_examples)} 個案例的截圖")
    print(f"數據已保存到: {data_file}")

if __name__ == "__main__":
    update_linkedin_screenshots()

