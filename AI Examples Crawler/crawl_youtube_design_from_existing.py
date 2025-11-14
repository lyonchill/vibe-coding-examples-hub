"""
使用現有數據庫中未分析的 YouTube 案例進行 AI 分析
跳過 YouTube API 搜尋，直接分析現有數據
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
from ai_examples_crawler import AIExamplesCrawler

load_dotenv()

def analyze_existing_youtube_cases():
    """分析現有數據庫中的 YouTube 案例，找出設計相關的"""
    print("=" * 70)
    print("分析現有數據庫中的 YouTube 案例")
    print("=" * 70)
    
    crawler = AIExamplesCrawler()
    
    # 載入現有數據
    data_file = Path(__file__).parent.parent / "found_examples_latest.json"
    if not data_file.exists():
        print("❌ 找不到數據文件")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    print(f"\n📂 載入現有數據: {len(existing_data)} 個案例")
    
    # 找出所有 YouTube 案例
    youtube_cases = [x for x in existing_data if x.get('source_platform') == 'YouTube']
    print(f"  YouTube 案例: {len(youtube_cases)} 個")
    
    # 找出還沒有 primary_category 或不是 Design 的案例
    candidates = []
    for case in youtube_cases:
        category = case.get('primary_category', '')
        # 如果沒有分類，或者是 Development/Productivity，但可能是設計相關的
        if not category or category not in ['Design']:
            # 檢查標題和描述是否可能與設計相關
            title_desc = (case.get('title', '') + ' ' + case.get('description', '')).lower()
            has_design_keywords = any(kw in title_desc for kw in [
                'design', 'ui', 'ux', 'figma', 'component', 'icon', 'plugin',
                'cursor', 'web design', 'interface', 'prototype'
            ])
            if has_design_keywords:
                candidates.append(case)
    
    print(f"\n🎯 找到 {len(candidates)} 個可能的設計相關候選案例")
    
    if len(candidates) == 0:
        print("  沒有需要分析的候選案例")
        return
    
    # 按觀看數排序
    candidates.sort(key=lambda x: x.get('view_count', 0), reverse=True)
    
    print(f"\n🤖 開始 AI 分析...")
    print(f"   目標: 找出設計相關且使用 vibe-coding 工具的案例")
    
    design_examples = []
    
    import time
    
    for i, case in enumerate(candidates[:30], 1):  # 分析前 30 個
        print(f"\n[{i}/{min(len(candidates), 30)}] {case.get('title', 'N/A')[:60]}...")
        print(f"    觀看數: {case.get('view_count', 0):,}")
        
        # 添加延遲以避免超過 API 配額（每分鐘 10 次 = 每 7 秒一次）
        if i > 1:
            time.sleep(7)
        
        try:
            # 準備分析用的數據格式
            content = {
                'title': case.get('title', ''),
                'description': case.get('description', ''),
                'url': case.get('original_url', ''),
                'platform': 'YouTube',
                'creator': case.get('creator_name', ''),
                'creator_url': case.get('creator_link', ''),
                'thumbnail': case.get('thumbnail_url', ''),
            }
            
            analysis = crawler.analyze_with_ai(content)
            
            # 檢查是否與設計相關
            category_tags = analysis.get('category_tags', [])
            is_design_related = any(tag in ['Design', 'Design System', 'UI/UX', 'Web Design', 'UI', 'UX'] 
                                   for tag in category_tags)
            
            # 檢查是否使用了設計相關的 vibe-coding 工具
            tools = analysis.get('ai_tools_used', [])
            has_design_tool = any(tool in ['Cursor', 'Figma', 'Figma Make', 'Figma MCP', 'Claude', 'ChatGPT', 'Lovable', 'v0'] 
                                for tool in tools)
            
            # 檢查是否確實構建了項目
            is_real_project = analysis.get('is_real_project', False)
            project_evidence = analysis.get('project_evidence', '').lower()
            has_build_evidence = any(keyword in project_evidence for keyword in [
                'build', 'create', 'made', 'generated', 'developed'
            ])
            
            title_desc = (case.get('title', '') + ' ' + case.get('description', '')).lower()
            title_has_build = any(keyword in title_desc for keyword in [
                'build', 'create', 'made', 'built with', 'using cursor', 'using figma'
            ])
            
            # 必須滿足所有條件
            meets_criteria = (
                (is_design_related or has_design_tool) and
                has_design_tool and
                (is_real_project or has_build_evidence or title_has_build)
            )
            
            if meets_criteria:
                # 更新案例的分類和工具信息
                case['primary_category'] = 'Design'
                case['ai_tools_used'] = tools
                case['category_tags'] = category_tags
                case['relevance_score'] = analysis.get('relevance_score', case.get('relevance_score', 7))
                case['build_complexity'] = analysis.get('build_complexity', case.get('build_complexity', 'Low-code'))
                case['is_real_project'] = is_real_project
                case['project_evidence'] = analysis.get('project_evidence', '')
                
                design_examples.append(case)
                print(f"  ✅ 符合條件，已更新（工具: {tools}, 分類: {category_tags}）")
                
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
            print(f"  ❌ 分析錯誤: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n✅ 找到 {len(design_examples)} 個符合條件的設計案例")
    
    # 更新數據庫
    # 找出需要更新的案例（根據 URL）
    updated_urls = {ex['original_url'] for ex in design_examples}
    
    # 更新現有數據
    for i, item in enumerate(existing_data):
        if item.get('original_url') in updated_urls:
            # 找到對應的更新數據
            updated_item = next((ex for ex in design_examples if ex['original_url'] == item['original_url']), None)
            if updated_item:
                existing_data[i] = updated_item
    
    # 保存
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print("✅ 完成！")
    print(f"{'='*70}")
    print(f"  更新設計案例: {len(design_examples)}")
    print(f"  總案例數: {len(existing_data)}")
    print(f"\n數據已保存到: {data_file}")

if __name__ == "__main__":
    analyze_existing_youtube_cases()

