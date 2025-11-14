"""
專門爬取 YouTube 上 15 個最受歡迎的設計相關 vibe-coding 案例
專注在透過 Cursor, Figma Make/MCP 等工具實際構建 UI/UX design, design system, web design
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
from ai_examples_crawler import AIExamplesCrawler

load_dotenv()

# 優化後的關鍵字：簡化以避免 API 限制，同時保持精確性
# 重點：使用較短的關鍵字，避免過於複雜的查詢
DESIGN_YOUTUBE_KEYWORDS = [
    # Cursor + Design（簡化版）
    "cursor design system",
    "cursor UI components",
    "cursor build UI",
    "cursor web design",
    "cursor figma plugin",
    
    # Figma Make/MCP + Design（簡化版）
    "figma make design",
    "figma mcp plugin",
    "figma make icon",
    
    # Vibe Coding + Design（簡化版）
    "vibe coding design",
    "vibe coding UI",
    
    # 更具體的構建案例（保留最重要的）
    "built with cursor design",
    "cursor build website",
    "cursor create design",
]

def crawl_youtube_design_examples():
    """爬取 YouTube 上 15 個最受歡迎的設計相關案例"""
    print("=" * 70)
    print("爬取 YouTube 上設計相關的 vibe-coding 案例")
    print("=" * 70)
    print(f"目標: 15 個最受歡迎的案例")
    print(f"專注: UI/UX Design, Design System, Web Design")
    print(f"要求: 必須確實使用 vibe-coding 工具（Cursor, Figma Make/MCP 等）")
    print()
    
    crawler = AIExamplesCrawler()
    
    # 修改 YouTube 搜索時間範圍為更長（獲取更多候選）
    original_search_youtube = crawler.search_youtube
    
    def search_youtube_extended(self, query: str, max_results: int = 10):
        """搜索 YouTube 影片（擴展時間範圍以獲取更多候選）"""
        import os
        import requests
        import time
        
        url = "https://www.googleapis.com/youtube/v3/search"
        
        # 過去 6 個月（獲取更多候選，然後按觀看數排序）
        published_after = (datetime.now() - timedelta(days=180)).isoformat() + "Z"
        
        YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
        
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'order': 'viewCount',  # 按觀看數排序
            'maxResults': max_results,
            'publishedAfter': published_after,
            'key': YOUTUBE_API_KEY
        }
        
        # 添加重試機制
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=params, timeout=15)
                
                # 處理 403 錯誤
                if response.status_code == 403:
                    error_data = response.json()
                    error_reason = error_data.get('error', {}).get('errors', [{}])[0].get('reason', '')
                    
                    if 'quotaExceeded' in error_reason or 'quota' in str(error_data).lower():
                        print(f"    ⚠️  API 配額已用完，跳過此關鍵字")
                        return []
                    elif attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)
                        print(f"    ⏳ API 403 錯誤，等待 {wait_time} 秒後重試...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"    ⚠️  API 403 錯誤（可能是權限問題），跳過此關鍵字")
                        return []
                
                response.raise_for_status()
                data = response.json()
                
                # 處理成功的情況
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
                    stats_response.raise_for_status()
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
                
                # 按觀看數排序
                results.sort(key=lambda x: x.get('view_count', 0), reverse=True)
                
                return results
                
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    print(f"    ⏳ 請求錯誤，等待 {wait_time} 秒後重試...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"    ⚠️  YouTube search error after {max_retries} attempts: {e}")
                    return []
            except Exception as e:
                print(f"    ⚠️  YouTube search error: {e}")
                return []
        
        return []  # 如果所有重試都失敗
    
    import types
    crawler.search_youtube = types.MethodType(search_youtube_extended, crawler)
    
    # 搜尋 YouTube（添加延遲以避免 API 限制）
    print("🔍 搜尋 YouTube...")
    print("   注意: 每個關鍵字之間會等待 2 秒，避免觸發 API 限制")
    all_youtube_results = []
    
    import time
    
    for i, keyword in enumerate(DESIGN_YOUTUBE_KEYWORDS):
        print(f"  [{i+1}/{len(DESIGN_YOUTUBE_KEYWORDS)}] 關鍵字: {keyword}")
        
        # 添加延遲（第一個關鍵字不需要）
        if i > 0:
            time.sleep(2)
        
        results = crawler.search_youtube(keyword, max_results=10)
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
    print(f"   前 5 個觀看數: {[x.get('view_count', 0) for x in unique_youtube[:5]]}")
    
    # 使用 AI 分析（專注於設計相關且必須使用 vibe-coding 工具）
    print("\n🤖 AI 分析中...")
    print("   專注於: UI/UX Design, Design System, Web Design")
    print("   要求: 必須確實使用 vibe-coding tools（如 Cursor, Figma Make/MCP）")
    print("   要求: 必須是實際構建的項目，不是單純討論")
    
    design_examples = []
    
    # 分析 YouTube（取前 50 個候選，然後篩選出符合條件的 15 個）
    candidates = unique_youtube[:50]  # 取前 50 個作為候選
    
    import time
    
    for i, result in enumerate(candidates, 1):
        print(f"\n[{i}/{len(candidates)}] YouTube: {result['title'][:60]}...")
        print(f"    觀看數: {result.get('view_count', 0):,}")
        
        # 添加延遲以避免超過 API 配額（每分鐘 10 次 = 每 6 秒一次）
        if i > 1:
            time.sleep(7)  # 等待 7 秒，確保不會超過配額
        
        try:
            # 使用正確的方法名稱
            analysis = crawler.analyze_with_ai(result)
            
            # 檢查是否與設計相關
            category_tags = analysis.get('category_tags', [])
            is_design_related = any(tag in ['Design', 'Design System', 'UI/UX', 'Web Design', 'UI', 'UX'] 
                                   for tag in category_tags)
            
            # 檢查是否使用了設計相關的 vibe-coding 工具
            tools = analysis.get('ai_tools_used', [])
            has_design_tool = any(tool in ['Cursor', 'Figma', 'Figma Make', 'Figma MCP', 'Claude', 'ChatGPT', 'Lovable', 'v0'] 
                                for tool in tools)
            
            # 檢查是否確實構建了項目（不是單純討論）
            is_real_project = analysis.get('is_real_project', False)
            project_evidence = analysis.get('project_evidence', '').lower()
            has_build_evidence = any(keyword in project_evidence for keyword in [
                'build', 'create', 'made', 'generated', 'developed', 'constructed',
                'built a', 'built an', 'built the', 'created a', 'created an',
                'made a', 'made an', 'developed a', 'developed an'
            ])
            
            # 檢查標題和描述中是否有構建證據
            title_desc = (result.get('title', '') + ' ' + result.get('description', '')).lower()
            title_has_build = any(keyword in title_desc for keyword in [
                'build', 'create', 'made', 'built with', 'built a', 'built an',
                'created', 'made with', 'using cursor', 'using figma',
                'cursor build', 'figma make', 'figma mcp'
            ])
            
            # 必須滿足所有條件：
            # 1. 設計相關 OR 使用了設計工具
            # 2. 使用了 vibe-coding 工具
            # 3. 是實際項目（有構建證據）
            meets_criteria = (
                (is_design_related or has_design_tool) and
                has_design_tool and
                (is_real_project or has_build_evidence or title_has_build)
            )
            
            if meets_criteria:
                # 使用 process_content 方法創建示例
                example = crawler.process_content(result)
                
                # 檢查 process_content 是否返回 None（可能因為 relevance_score 太低）
                if example is None:
                    print(f"  ⚠️  process_content 返回 None（可能 relevance_score < 6 或不是真實項目）")
                    # 手動創建示例（因為我們已經通過了篩選條件）
                    example = {
                        'title': result['title'],
                        'description': analysis.get('enhanced_description', result.get('description', '')),
                        'ai_tools_used': tools,
                        'category_tags': category_tags,
                        'source_platform': 'YouTube',
                        'original_url': result['url'],
                        'creator_name': result.get('creator', 'Unknown'),
                        'creator_link': result.get('creator_url', ''),
                        'thumbnail_url': result.get('thumbnail', ''),
                        'date_added': datetime.now().isoformat(),
                        'relevance_score': analysis.get('relevance_score', 7),
                        'build_complexity': analysis.get('build_complexity', 'Low-code'),
                        'is_no_code_low_code': analysis.get('is_no_code_low_code', False),
                        'project_name': analysis.get('project_name', result['title'][:50]),
                        'project_summary': analysis.get('project_summary', ''),
                        'project_evidence': analysis.get('project_evidence', ''),
                        'view_count': result.get('view_count', 0),
                        'like_count': result.get('like_count', 0),
                        'comment_count': result.get('comment_count', 0),
                        'primary_category': 'Design'
                    }
                
                example['source_platform'] = 'YouTube'
                example['view_count'] = result.get('view_count', 0)
                example['like_count'] = result.get('like_count', 0)
                example['comment_count'] = result.get('comment_count', 0)
                example['primary_category'] = 'Design'
                design_examples.append(example)
                print(f"  ✅ 符合條件，已加入（工具: {tools}, 分類: {category_tags}）")
                
                # 如果已經有 15 個符合條件的案例，就停止
                if len(design_examples) >= 15:
                    print(f"\n✅ 已找到 15 個符合條件的案例，停止分析")
                    break
            else:
                reasons = []
                if not is_design_related and not has_design_tool:
                    reasons.append("非設計相關或未使用設計工具")
                if not has_design_tool:
                    reasons.append("未使用 vibe-coding 工具")
                if not is_real_project and not has_build_evidence and not title_has_build:
                    reasons.append("無構建證據")
                print(f"  ⚠️  不符合條件: {', '.join(reasons) if reasons else '未知'}")
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                # 提取重試時間
                import re
                retry_match = re.search(r'retry in (\d+\.?\d*)s', error_msg)
                if retry_match:
                    retry_seconds = float(retry_match.group(1))
                    print(f"  ⏳ API 配額限制，等待 {int(retry_seconds)} 秒後重試...")
                    import time
                    time.sleep(min(retry_seconds + 2, 60))  # 最多等待 60 秒
                    # 重試一次
                    try:
                        analysis = crawler.analyze_with_ai(result)
                        # 繼續處理...
                        category_tags = analysis.get('category_tags', [])
                        is_design_related = any(tag in ['Design', 'Design System', 'UI/UX', 'Web Design', 'UI', 'UX'] 
                                               for tag in category_tags)
                        tools = analysis.get('ai_tools_used', [])
                        has_design_tool = any(tool in ['Cursor', 'Figma', 'Figma Make', 'Figma MCP', 'Claude', 'ChatGPT', 'Lovable', 'v0'] 
                                            for tool in tools)
                        is_real_project = analysis.get('is_real_project', False)
                        project_evidence = analysis.get('project_evidence', '').lower()
                        has_build_evidence = any(keyword in project_evidence for keyword in [
                            'build', 'create', 'made', 'generated', 'developed', 'constructed',
                            'built a', 'built an', 'built the', 'created a', 'created an',
                            'made a', 'made an', 'developed a', 'developed an'
                        ])
                        title_desc = (result.get('title', '') + ' ' + result.get('description', '')).lower()
                        title_has_build = any(keyword in title_desc for keyword in [
                            'build', 'create', 'made', 'built with', 'built a', 'built an',
                            'created', 'made with', 'using cursor', 'using figma',
                            'cursor build', 'figma make', 'figma mcp'
                        ])
                        meets_criteria = (
                            (is_design_related or has_design_tool) and
                            has_design_tool and
                            (is_real_project or has_build_evidence or title_has_build)
                        )
                        if meets_criteria:
                            example = crawler.process_content(result)
                            if example is None:
                                example = {
                                    'title': result['title'],
                                    'description': analysis.get('enhanced_description', result.get('description', '')),
                                    'ai_tools_used': tools,
                                    'category_tags': category_tags,
                                    'source_platform': 'YouTube',
                                    'original_url': result['url'],
                                    'creator_name': result.get('creator', 'Unknown'),
                                    'creator_link': result.get('creator_url', ''),
                                    'thumbnail_url': result.get('thumbnail', ''),
                                    'date_added': datetime.now().isoformat(),
                                    'relevance_score': analysis.get('relevance_score', 7),
                                    'build_complexity': analysis.get('build_complexity', 'Low-code'),
                                    'is_no_code_low_code': analysis.get('is_no_code_low_code', False),
                                    'project_name': analysis.get('project_name', result['title'][:50]),
                                    'project_summary': analysis.get('project_summary', ''),
                                    'project_evidence': analysis.get('project_evidence', ''),
                                    'view_count': result.get('view_count', 0),
                                    'like_count': result.get('like_count', 0),
                                    'comment_count': result.get('comment_count', 0),
                                    'primary_category': 'Design'
                                }
                            example['source_platform'] = 'YouTube'
                            example['view_count'] = result.get('view_count', 0)
                            example['like_count'] = result.get('like_count', 0)
                            example['comment_count'] = result.get('comment_count', 0)
                            example['primary_category'] = 'Design'
                            design_examples.append(example)
                            print(f"  ✅ 符合條件，已加入（工具: {tools}, 分類: {category_tags}）")
                            if len(design_examples) >= 15:
                                print(f"\n✅ 已找到 15 個符合條件的案例，停止分析")
                                break
                        else:
                            print(f"  ⚠️  重試後仍不符合條件")
                    except Exception as retry_e:
                        print(f"  ❌ 重試後仍失敗: {retry_e}")
                else:
                    print(f"  ⏳ API 配額限制，跳過此案例")
            else:
                print(f"  ❌ 分析錯誤: {e}")
                import traceback
                traceback.print_exc()
    
    print(f"\n✅ 找到 {len(design_examples)} 個符合條件的設計案例")
    
    # 載入現有數據
    data_file = Path(__file__).parent.parent / "found_examples_latest.json"
    existing_examples = []
    if data_file.exists():
        with open(data_file, 'r', encoding='utf-8') as f:
            existing_examples = json.load(f)
        print(f"📂 載入現有數據: {len(existing_examples)} 個案例")
    
    # 合併數據（保留現有 + 新增設計相關）
    all_examples = existing_examples + design_examples
    
    # 去重（根據 URL）
    seen_urls = set()
    unique_all = []
    for ex in all_examples:
        url = ex.get('original_url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_all.append(ex)
    
    # 為新案例添加分類
    for ex in design_examples:
        if 'primary_category' not in ex:
            ex['primary_category'] = 'Design'
    
    # 排序（YouTube 優先，然後按觀看數）
    unique_all.sort(key=lambda x: (
        0 if x.get('source_platform') == 'YouTube' else 1,
        -x.get('view_count', 0) if x.get('source_platform') == 'YouTube' else 0,
        -x.get('relevance_score', 0)
    ))
    
    # 保存
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(unique_all, f, indent=2, ensure_ascii=False)
    
    youtube_count = len([x for x in design_examples if x.get('source_platform') == 'YouTube'])
    
    print(f"\n{'='*70}")
    print("✅ 完成！")
    print(f"{'='*70}")
    print(f"  新增 YouTube 設計案例: {youtube_count}")
    print(f"  總案例數: {len(unique_all)}")
    print(f"\n數據已保存到: {data_file}")
    
    if youtube_count < 15:
        print(f"\n⚠️  只找到 {youtube_count} 個符合條件的案例（目標: 15 個）")
        print(f"   可能原因:")
        print(f"   - API 配額限制")
        print(f"   - 符合條件的案例較少")
        print(f"   - 關鍵字需要調整")

if __name__ == "__main__":
    crawl_youtube_design_examples()

