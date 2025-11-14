"""
Add LinkedIn posts to data without AI analysis (for when API quota is exceeded)
"""

import json
from pathlib import Path
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_examples_crawler import AIExamplesCrawler

def create_simple_linkedin_example(raw_content):
    """Create a simple example from LinkedIn post without AI analysis"""
    
    # Extract basic info
    title = raw_content.get('title', '')[:100]
    description = raw_content.get('description', '')[:300]
    
    # Try to detect tools from title/description
    tools_mentioned = []
    tool_keywords = {
        'Cursor': ['cursor'],
        'Lovable': ['lovable'],
        'v0': ['v0', 'v0.dev'],
        'Claude': ['claude'],
        'ChatGPT': ['chatgpt', 'gpt'],
        'Replit': ['replit'],
        'Make.com': ['make.com', 'make'],
        'n8n': ['n8n']
    }
    
    text_lower = (title + ' ' + description).lower()
    for tool, keywords in tool_keywords.items():
        if any(kw in text_lower for kw in keywords):
            tools_mentioned.append(tool)
    
    if not tools_mentioned:
        tools_mentioned = ['AI Tools']
    
    # Generate screenshot URL for LinkedIn post
    linkedin_url = raw_content.get('url', '')
    screenshot_url = ''
    
    # Try multiple methods to get LinkedIn post screenshot
    if linkedin_url:
        import requests
        
        # Method 1: Try ScreenshotAPI.net (free tier available)
        screenshotapi_key = os.getenv("SCREENSHOTAPI_KEY", "")
        if screenshotapi_key:
            try:
                api_url = f"https://api.screenshotapi.net/screenshot"
                params = {
                    'token': screenshotapi_key,
                    'url': linkedin_url,
                    'width': 1200,
                    'height': 630,
                    'output': 'image',
                    'file_type': 'png',
                    'wait_for': 'networkidle0'
                }
                # Note: This returns image directly, you'd need to upload to storage
                # For now, we'll use the API URL pattern
                screenshot_url = f"{api_url}?token={screenshotapi_key}&url={linkedin_url}&width=1200&height=630"
            except:
                pass
        
        # Method 2: Try htmlcsstoimage.com (if API key available)
        htmlcsstoimage_key = os.getenv("HTMLCSSTOIMAGE_API_KEY", "")
        if not screenshot_url and htmlcsstoimage_key:
            try:
                api_url = "https://hcti.io/v1/image"
                response = requests.post(
                    api_url,
                    auth=('', htmlcsstoimage_key),
                    data={
                        'url': linkedin_url,
                        'viewport_width': 1200,
                        'viewport_height': 630
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    screenshot_url = data.get('url', '')
            except:
                pass
        
        # Method 3: Try urlbox.io (if API key available)
        urlbox_key = os.getenv("URLBOX_API_KEY", "")
        urlbox_secret = os.getenv("URLBOX_SECRET", "")
        if not screenshot_url and urlbox_key and urlbox_secret:
            try:
                import hashlib
                import hmac
                import base64
                import urllib.parse
                
                query_string = urllib.parse.urlencode({
                    'url': linkedin_url,
                    'width': 1200,
                    'height': 630
                })
                token = hmac.new(
                    urlbox_secret.encode('utf-8'),
                    query_string.encode('utf-8'),
                    hashlib.sha1
                ).hexdigest()
                
                screenshot_url = f"https://api.urlbox.io/v1/{urlbox_key}/{token}/png?{query_string}"
            except:
                pass
        
        # Method 4: Try using Open Graph image from LinkedIn (most reliable for public posts)
        if not screenshot_url:
            try:
                response = requests.get(linkedin_url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5'
                })
                if response.status_code == 200:
                    import re
                    # Look for og:image meta tag (multiple patterns)
                    patterns = [
                        r'<meta\s+property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
                        r'<meta\s+name=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
                        r'"image":"([^"]+)"',  # JSON-LD format
                    ]
                    for pattern in patterns:
                        match = re.search(pattern, response.text)
                        if match:
                            img_url = match.group(1)
                            # Clean up URL
                            if img_url.startswith('//'):
                                img_url = 'https:' + img_url
                            elif img_url.startswith('/'):
                                img_url = 'https://www.linkedin.com' + img_url
                            screenshot_url = img_url
                            break
            except Exception as e:
                print(f"  ⚠️  Error fetching OG image: {e}")
                pass
        
        # Method 5: Try screenshot.one (if API key available)
        screenshotone_key = os.getenv("SCREENSHOTONE_KEY", "")
        if not screenshot_url and screenshotone_key:
            try:
                screenshot_url = f"https://api.screenshotone.com/take?access_key={screenshotone_key}&url={linkedin_url}&viewport_width=1200&viewport_height=630&device_scale_factor=1&format=png&image_quality=80&block_ads=true&block_cookie_banners=true&block_banners=true&block_trackers=true"
            except:
                pass
    
    # Create example
    example = {
        'title': title,
        'description': description or title,
        'ai_tools_used': tools_mentioned,
        'category_tags': ['Code Generation', 'AI Project'],
        'source_platform': 'LinkedIn',
        'original_url': linkedin_url,
        'creator_name': raw_content.get('creator', 'Unknown'),
        'creator_link': raw_content.get('creator_url', ''),
        'thumbnail_url': screenshot_url or raw_content.get('thumbnail', ''),  # Use screenshot if available
        'date_added': datetime.now().isoformat(),
        'relevance_score': 7,  # Default score
        'build_complexity': 'Low-code' if len(tools_mentioned) > 0 else 'Unknown',
        'is_no_code_low_code': True,
        'project_name': title[:50],
        'project_summary': description[:150] if description else 'AI coding project shared on LinkedIn',
        'project_evidence': 'Shared on LinkedIn',
        'view_count': raw_content.get('view_count', 0),
        'like_count': raw_content.get('like_count', 0),
        'comment_count': raw_content.get('comment_count', 0)
    }
    
    return example

def main():
    print("🔍 Adding LinkedIn posts (simple mode, no AI analysis)...")
    print("=" * 50)
    
    crawler = AIExamplesCrawler()
    
    # LinkedIn keywords
    linkedin_keywords = [
        "built with Cursor",
        "Lovable project",
        "v0 by Vercel"
    ]
    
    all_linkedin_content = []
    
    # Search LinkedIn
    for keyword in linkedin_keywords:
        print(f"\nSearching LinkedIn: {keyword}")
        results = crawler.search_linkedin_via_serpapi(keyword, max_results=5)
        if results:
            print(f"  ✅ Found {len(results)} posts")
            all_linkedin_content.extend(results)
    
    if not all_linkedin_content:
        print("\n❌ No LinkedIn content found.")
        return
    
    # Remove duplicates
    seen_urls = set()
    unique_content = []
    for content in all_linkedin_content:
        if content['url'] not in seen_urls:
            seen_urls.add(content['url'])
            unique_content.append(content)
    
    print(f"\n📊 Found {len(unique_content)} unique LinkedIn posts")
    
    # Create simple examples
    print("\n📝 Creating examples (without AI analysis)...")
    linkedin_examples = []
    
    for content in unique_content[:10]:  # Limit to 10
        example = create_simple_linkedin_example(content)
        linkedin_examples.append(example)
        print(f"  ✅ Added: {example['title'][:60]}...")
    
    # Load existing data
    parent_dir = Path(__file__).parent.parent
    latest_file = parent_dir / "found_examples_latest.json"
    
    existing_examples = []
    if latest_file.exists():
        with open(latest_file, 'r', encoding='utf-8') as f:
            existing_examples = json.load(f)
    
    # Combine and deduplicate
    all_examples = existing_examples + linkedin_examples
    seen_urls = set()
    unique_examples = []
    for ex in all_examples:
        if ex['original_url'] not in seen_urls:
            seen_urls.add(ex['original_url'])
            unique_examples.append(ex)
    
    # Sort: YouTube first (by views), then LinkedIn (by relevance)
    unique_examples.sort(key=lambda x: (
        0 if x.get('source_platform') == 'YouTube' else 1,
        x.get('view_count', 0) if x.get('source_platform') == 'YouTube' else 0,
        x.get('relevance_score', 0)
    ))
    
    # Save
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump(unique_examples[:30], f, indent=2, ensure_ascii=False)
    
    linkedin_count = len([e for e in unique_examples if e.get('source_platform') == 'LinkedIn'])
    youtube_count = len([e for e in unique_examples if e.get('source_platform') == 'YouTube'])
    
    print(f"\n✅ Saved {len(unique_examples)} total examples")
    print(f"   📺 YouTube: {youtube_count}")
    print(f"   💼 LinkedIn: {linkedin_count}")
    print(f"💾 File: {latest_file}")

if __name__ == "__main__":
    main()

