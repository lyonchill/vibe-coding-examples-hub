"""
專門爬取 UI/UX Design, Design System, Web Design 相關的 vibe-coding 案例
專注在過去三個月內，使用 Cursor, Figma Make/MCP 等工具實際構建的案例
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
from ai_examples_crawler import AIExamplesCrawler

load_dotenv()

# 專注於設計相關的關鍵字
DESIGN_YOUTUBE_KEYWORDS = [
    "cursor design system",
    "cursor UI design",
    "cursor web design",
    "figma mcp cursor",
    "figma make design system",
    "figma make icon library",
    "vibe coding design system",
    "vibe coding UI UX",
    "no-code design system",
    "cursor build design",
    "AI design system",
    "cursor figma plugin",
    "vibe coding web design",
    "cursor UI components",
    "figma make documentation",
]

DESIGN_LINKEDIN_KEYWORDS = [
    "Figma Make design system",
    "Figma Make icon library",
    "cursor design system",
    "figma mcp cursor",
    "vibe coding UI design",
    "cursor UI UX",
    "no-code design system",
    "figma make plugin",
    "cursor build design",
    "AI design system",
    "vibe coding web design",
    "cursor figma",
    "design system with cursor",
    "figma make documentation",
    "cursor UI components",
]

def crawl_design_examples():
    """爬取設計相關的 vibe-coding 案例"""
    print("=" * 70)
    print("爬取 UI/UX Design, Design System, Web Design 相關案例")
    print("=" * 70)
    print(f"時間範圍: 過去三個月（90天）")
    print(f"目標: 15個 YouTube + 15個 LinkedIn")
    print()
    
    crawler = AIExamplesCrawler()
    
    # 修改 YouTube 搜索時間範圍為90天（使用原始方法但修改時間）
    original_search_youtube = crawler.search_youtube
    
    def search_youtube_90days(query: str, max_results: int = 5):
        """搜索過去90天的 YouTube 影片"""
        # 使用原始方法，但臨時修改時間範圍
        import os
        from datetime import timedelta
        
        # 臨時修改 crawler 的時間範圍
        original_method = crawler.search_youtube.__func__
        
        # 創建一個包裝函數
        def wrapper(self, query: str, max_results: int = 5):
            url = "https://www.googleapis.com/youtube/v3/search"
            
            # 過去90天
            published_after = (datetime.now() - timedelta(days=90)).isoformat() + "Z"
            
            YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
            
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'order': 'viewCount',
                'maxResults': max_results,
                'publishedAfter': published_after,
                'key': YOUTUBE_API_KEY
            }
            
            try:
                import requests
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                results = []
                video_ids = []
                for item in data.get('items', []):
                    video_id = item['id']['videoId']
                    video_ids.append(video_id)
                
                # 獲取視頻統計信息
                if video_ids:
                    stats_url = "https://www.googleapis.com/youtube/v3/videos"
                    stats_params = {
                        'part': 'statistics,snippet',
                        'id': ','.join(video_ids),
                        'key': YOUTUBE_API_KEY
                    }
                    stats_response = requests.get(stats_url, params=stats_params)
                    stats_data = stats_response.json()
                    
                    stats_dict = {}
                    for item in stats_data.get('items', []):
                        stats_dict[item['id']] = item['statistics']
                    
                    for item in data.get('items', []):
                        video_id = item['id']['videoId']
                        snippet = item['snippet']
                        stats = stats_dict.get(video_id, {})
                        
                        results.append({
                            'title': snippet['title'],
                            'description': snippet['description'],
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'thumbnail': snippet['thumbnails'].get('high', {}).get('url', ''),
                            'creator': snippet['channelTitle'],
                            'creator_url': f"https://www.youtube.com/channel/{snippet['channelId']}",
                            'platform': 'YouTube',
                            'published_at': snippet['publishedAt'],
                            'view_count': int(stats.get('viewCount', 0)),
                            'like_count': int(stats.get('likeCount', 0)),
                            'comment_count': int(stats.get('commentCount', 0))
                        })
                
                return results
                
            except Exception as e:
                print(f"YouTube search error for '{query}': {e}")
                return []
        
        return wrapper(crawler, query, max_results)
    
    # 使用原始方法但手動設置時間範圍
    import types
    crawler.search_youtube = types.MethodType(search_youtube_90days, crawler)
    
    # 搜尋 YouTube（使用原始方法，但修改為90天）
    print("🔍 搜尋 YouTube...")
    print("   注意: 使用原始 search_youtube 方法，時間範圍改為90天")
    all_youtube_results = []
    
    # 臨時修改 search_youtube 的時間範圍
    original_method = crawler.search_youtube
    import types
    
    def search_youtube_90days(self, query: str, max_results: int = 5):
        """搜索過去90天的 YouTube 影片"""
        url = "https://www.googleapis.com/youtube/v3/search"
        
        # 過去90天
        published_after = (datetime.now() - timedelta(days=90)).isoformat() + "Z"
        
        import os
        import requests
        YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
        
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'order': 'viewCount',
            'maxResults': max_results,
            'publishedAfter': published_after,
            'key': YOUTUBE_API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            video_ids = []
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                video_ids.append(video_id)
            
            # 獲取視頻統計信息
            if video_ids:
                stats_url = "https://www.googleapis.com/youtube/v3/videos"
                stats_params = {
                    'part': 'statistics,snippet',
                    'id': ','.join(video_ids),
                    'key': YOUTUBE_API_KEY
                }
                stats_response = requests.get(stats_url, params=stats_params)
                stats_data = stats_response.json()
                
                stats_dict = {}
                for item in stats_data.get('items', []):
                    stats_dict[item['id']] = item['statistics']
                
                for item in data.get('items', []):
                    video_id = item['id']['videoId']
                    snippet = item['snippet']
                    stats = stats_dict.get(video_id, {})
                    
                    results.append({
                        'title': snippet['title'],
                        'description': snippet['description'],
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'thumbnail': snippet['thumbnails'].get('high', {}).get('url', ''),
                        'creator': snippet['channelTitle'],
                        'creator_url': f"https://www.youtube.com/channel/{snippet['channelId']}",
                        'platform': 'YouTube',
                        'published_at': snippet['publishedAt'],
                        'view_count': int(stats.get('viewCount', 0)),
                        'like_count': int(stats.get('likeCount', 0)),
                        'comment_count': int(stats.get('commentCount', 0))
                    })
            
            return results
            
        except Exception as e:
            print(f"    ⚠️  YouTube search error: {e}")
            return []
    
    crawler.search_youtube = types.MethodType(search_youtube_90days, crawler)
    
    for keyword in DESIGN_YOUTUBE_KEYWORDS[:10]:  # 限制前10個關鍵字
        print(f"  關鍵字: {keyword}")
        results = crawler.search_youtube(keyword, max_results=3)
        all_youtube_results.extend(results)
        print(f"    找到 {len(results)} 個結果")
    
    # 去重 YouTube
    seen_youtube_urls = set()
    unique_youtube = []
    for result in all_youtube_results:
        if result['url'] not in seen_youtube_urls:
            seen_youtube_urls.add(result['url'])
            unique_youtube.append(result)
    
    # 按觀看數排序
    unique_youtube.sort(key=lambda x: x.get('view_count', 0), reverse=True)
    
    print(f"\n✅ YouTube: 找到 {len(unique_youtube)} 個唯一結果")
    
    # 搜尋 LinkedIn
    print("\n🔍 搜尋 LinkedIn...")
    all_linkedin_results = []
    for keyword in DESIGN_LINKEDIN_KEYWORDS:
        print(f"  關鍵字: {keyword}")
        results = crawler.search_linkedin_via_serpapi(keyword, max_results=3)
        all_linkedin_results.extend(results)
        print(f"    找到 {len(results)} 個結果")
    
    # 去重 LinkedIn
    seen_linkedin_urls = set()
    unique_linkedin = []
    for result in all_linkedin_results:
        if result['url'] not in seen_linkedin_urls:
            seen_linkedin_urls.add(result['url'])
            unique_linkedin.append(result)
    
    print(f"\n✅ LinkedIn: 找到 {len(unique_linkedin)} 個唯一結果")
    
    # 使用 AI 分析（專注於設計相關）
    print("\n🤖 AI 分析中...")
    print("   專注於: UI/UX Design, Design System, Web Design")
    print("   要求: 必須確實使用 vibe-coding tools（如 Cursor, Figma Make）")
    
    design_examples = []
    
    # 分析 YouTube（取前15個）
    for i, result in enumerate(unique_youtube[:15], 1):
        print(f"\n[{i}/15] YouTube: {result['title'][:60]}...")
        try:
            analysis = crawler.analyze_content_with_ai(result)
            
            # 檢查是否與設計相關
            is_design_related = any(tag in ['Design', 'Design System', 'UI/UX', 'Web Design'] 
                                   for tag in analysis.get('category_tags', []))
            
            # 檢查是否使用了設計相關的工具
            tools = analysis.get('ai_tools_used', [])
            has_design_tool = any(tool in ['Cursor', 'Figma', 'Figma Make', 'Figma MCP'] 
                                for tool in tools)
            
            # 檢查是否確實構建了項目（不是單純討論）
            is_real_project = analysis.get('is_real_project', False)
            project_evidence = analysis.get('project_evidence', '')
            has_build_evidence = 'build' in project_evidence.lower() or \
                               'create' in project_evidence.lower() or \
                               'made' in project_evidence.lower() or \
                               'generated' in project_evidence.lower()
            
            if (is_design_related or has_design_tool) and (is_real_project or has_build_evidence):
                example = crawler.create_example_from_content(result, analysis)
                example['source_platform'] = 'YouTube'
                design_examples.append(example)
                print(f"  ✅ 符合條件，已加入")
            else:
                print(f"  ⚠️  不符合條件（設計相關: {is_design_related}, 工具: {has_design_tool}, 實際項目: {is_real_project or has_build_evidence}）")
        except Exception as e:
            print(f"  ❌ 分析錯誤: {e}")
    
    # 分析 LinkedIn（取前15個）
    for i, result in enumerate(unique_linkedin[:15], 1):
        print(f"\n[{i}/15] LinkedIn: {result['title'][:60]}...")
        try:
            # LinkedIn 使用簡化分析（避免 API quota 問題）
            from add_linkedin_simple import create_simple_linkedin_example
            example = create_simple_linkedin_example(result)
            
            # 檢查是否與設計相關
            title_desc = (example.get('title', '') + ' ' + example.get('description', '')).lower()
            
            # 排除誤判：檢查是否是指鼠標 cursor 而不是 Cursor AI 工具
            is_mouse_cursor = any(phrase in title_desc for phrase in [
                'custom cursor', 'mouse cursor', 'cursor location', 'cursor position',
                'cursor hover', 'cursor enter', 'cursor image', 'cursor style',
                'change cursor', 'cursor icon', 'cursor design', 'mouse enter',
                'cursor location', 'based on cursor', 'cursor-based', 'cursor trigger'
            ]) and 'cursor ai' not in title_desc and 'built with cursor' not in title_desc and 'using cursor' not in title_desc
            
            if is_mouse_cursor:
                print(f"  ❌ 排除：指的是鼠標 cursor，不是 Cursor AI 工具")
                continue
            
            # 必須包含設計相關關鍵字
            is_design_related = any(keyword in title_desc for keyword in [
                'design system', 'ui', 'ux', 'web design', 'figma make', 'figma mcp',
                'icon library', 'component library', 'plugin', 'figma plugin',
                'built with cursor', 'cursor ai', 'cursor build', 'cursor created',
                'made with cursor', 'using cursor', 'cursor tool'
            ])
            
            # 必須使用了 vibe-coding 工具
            tools = example.get('ai_tools_used', [])
            has_vibe_tool = any(tool in ['Cursor', 'Figma', 'Figma Make', 'Figma MCP', 'Claude', 'ChatGPT', 'Lovable', 'v0'] for tool in tools)
            
            # 必須有實際構建產品的證據（不是單純功能展示）
            has_build_evidence = any(keyword in title_desc for keyword in [
                'built', 'build', 'created', 'made', 'generate', 'generated',
                'built with', 'built a', 'made a', 'created a', 'built using',
                'made with', 'created with', 'built this', 'made this',
                'created this', 'built an', 'made an', 'created an'
            ])
            
            # 檢查是否只是功能展示而非實際構建
            is_feature_demo_only = any(phrase in title_desc for phrase in [
                'new feature', 'introducing', 'announcement', 'update',
                'what\'s new', 'check out', 'try this', 'little experiment',
                'here\'s how', 'how to use', 'tutorial', 'guide'
            ]) and not has_build_evidence
            
            # 必須說明構建了什麼產品/功能
            has_product_mention = any(keyword in title_desc for keyword in [
                'app', 'website', 'plugin', 'tool', 'system', 'library',
                'component', 'dashboard', 'interface', 'prototype',
                'case study', 'project', 'product'
            ])
            
            # 排除單純討論設計的貼文
            is_just_discussion = any(keyword in title_desc for keyword in [
                'why', 'should', 'think', 'opinion', 'thoughts', 'learn',
                'tips', 'advice', 'guide to', 'how to think', 'mistake'
            ]) and not has_build_evidence
            
            if (is_design_related or has_vibe_tool) and has_build_evidence and has_product_mention and not is_feature_demo_only and not is_just_discussion:
                example['source_platform'] = 'LinkedIn'
                design_examples.append(example)
                print(f"  ✅ 符合條件（設計相關 + 使用工具 + 實際構建產品）")
            else:
                reasons = []
                if is_mouse_cursor:
                    reasons.append("鼠標cursor誤判")
                if not is_design_related and not has_vibe_tool:
                    reasons.append("非設計相關或未使用工具")
                if not has_build_evidence:
                    reasons.append("無構建證據")
                if not has_product_mention:
                    reasons.append("未說明構建了什麼產品")
                if is_feature_demo_only:
                    reasons.append("僅為功能展示")
                if is_just_discussion:
                    reasons.append("僅為討論")
                print(f"  ⚠️  不符合條件: {', '.join(reasons) if reasons else '未知'}")
        except Exception as e:
            print(f"  ❌ 處理錯誤: {e}")
    
    # 載入現有數據
    data_file = Path(__file__).parent.parent / "found_examples_latest.json"
    existing_examples = []
    if data_file.exists():
        existing_examples = json.load(open(data_file, 'r', encoding='utf-8'))
    
    # 合併數據（保留現有 + 新增設計相關）
    all_examples = existing_examples + design_examples
    
    # 去重
    seen_urls = set()
    unique_all = []
    for ex in all_examples:
        if ex['original_url'] not in seen_urls:
            seen_urls.add(ex['original_url'])
            unique_all.append(ex)
    
    # 排序
    unique_all.sort(key=lambda x: (
        0 if x.get('source_platform') == 'YouTube' else 1,
        x.get('view_count', 0) if x.get('source_platform') == 'YouTube' else 0,
        x.get('relevance_score', 0)
    ), reverse=True)
    
    # 保存
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(unique_all[:50], f, indent=2, ensure_ascii=False)
    
    youtube_count = len([x for x in design_examples if x.get('source_platform') == 'YouTube'])
    linkedin_count = len([x for x in design_examples if x.get('source_platform') == 'LinkedIn'])
    
    print(f"\n{'='*70}")
    print("✅ 完成！")
    print(f"{'='*70}")
    print(f"  新增 YouTube 設計案例: {youtube_count}")
    print(f"  新增 LinkedIn 設計案例: {linkedin_count}")
    print(f"  總案例數: {len(unique_all)}")
    print(f"\n數據已保存到: {data_file}")

if __name__ == "__main__":
    crawl_design_examples()

