"""
幫助添加 ScreenshotAPI key 到 .env 文件
"""
from pathlib import Path

def add_screenshot_api_key():
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ 找不到 .env 文件")
        print(f"預期位置: {env_file.absolute()}")
        return
    
    # 讀取現有內容
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 檢查是否已經有 SCREENSHOTAPI_KEY
    has_key = False
    for i, line in enumerate(lines):
        if 'SCREENSHOTAPI_KEY' in line.upper() or 'SCREENSHOT_API_KEY' in line.upper():
            has_key = True
            print(f"✅ 找到現有的 API key 在第 {i+1} 行:")
            print(f"   {line.strip()}")
            break
    
    if not has_key:
        print("📝 請在 .env 文件中添加以下行:")
        print("\nSCREENSHOTAPI_KEY=your_api_key_here\n")
        print("添加後，請重新運行 update_linkedin_screenshots.py")
    else:
        print("\n✅ API key 已存在，請確認值是否正確")

if __name__ == "__main__":
    add_screenshot_api_key()

