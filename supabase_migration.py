"""
將 JSON 數據遷移到 Supabase（可選）
"""
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

def migrate_to_supabase():
    """將 found_examples_latest.json 遷移到 Supabase"""
    
    # Supabase 配置
    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_KEY", "")
    
    if not supabase_url or not supabase_key:
        print("❌ 請設置 SUPABASE_URL 和 SUPABASE_KEY 環境變量")
        return
    
    # 連接 Supabase
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # 載入 JSON 數據
    data_file = Path(__file__).parent / "found_examples_latest.json"
    if not data_file.exists():
        print(f"❌ 找不到數據文件: {data_file}")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        examples = json.load(f)
    
    print(f"📊 準備遷移 {len(examples)} 個案例到 Supabase...")
    
    # 清空現有數據（可選）
    response = input("是否清空 Supabase 中的現有數據？(y/N): ")
    if response.lower() == 'y':
        try:
            supabase.table('examples').delete().neq('id', 0).execute()
            print("✅ 已清空現有數據")
        except Exception as e:
            print(f"⚠️  清空數據時出錯（可能表為空）: {e}")
    
    # 批量插入數據
    success_count = 0
    error_count = 0
    
    for i, example in enumerate(examples, 1):
        try:
            # 準備數據
            data = {
                'title': example.get('title', ''),
                'description': example.get('description', ''),
                'project_name': example.get('project_name', ''),
                'project_summary': example.get('project_summary', ''),
                'project_evidence': example.get('project_evidence', ''),
                'ai_tools_used': example.get('ai_tools_used', []),
                'category_tags': example.get('category_tags', []),
                'source_platform': example.get('source_platform', ''),
                'original_url': example.get('original_url', ''),
                'creator_name': example.get('creator_name', ''),
                'creator_link': example.get('creator_link', ''),
                'thumbnail_url': example.get('thumbnail_url', ''),
                'relevance_score': example.get('relevance_score', 0),
                'build_complexity': example.get('build_complexity', ''),
                'is_no_code_low_code': example.get('is_no_code_low_code', False),
                'primary_category': example.get('primary_category', 'Development'),
                'view_count': example.get('view_count', 0),
                'like_count': example.get('like_count', 0),
                'comment_count': example.get('comment_count', 0),
            }
            
            # 插入數據（使用 upsert 避免重複）
            supabase.table('examples').upsert(data, on_conflict='original_url').execute()
            success_count += 1
            
            if i % 10 == 0:
                print(f"  已處理 {i}/{len(examples)} 個案例...")
                
        except Exception as e:
            error_count += 1
            print(f"  ❌ 錯誤 [{i}]: {example.get('title', 'N/A')[:50]}... - {e}")
    
    print(f"\n✅ 遷移完成！")
    print(f"  成功: {success_count} 個")
    print(f"  失敗: {error_count} 個")

if __name__ == "__main__":
    migrate_to_supabase()

