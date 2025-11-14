"""
更新現有 LinkedIn 案例的 engagement metrics（likes, comments, views）
"""
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
from ai_examples_crawler import AIExamplesCrawler

load_dotenv()

def update_linkedin_engagement():
    """更新所有 LinkedIn 案例的 engagement metrics"""
    
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
    
    print(f"找到 {len(linkedin_examples)} 個 LinkedIn 案例")
    print("開始更新 engagement metrics...\n")
    
    crawler = AIExamplesCrawler()
    updated_count = 0
    
    for i, example in enumerate(linkedin_examples, 1):
        url = example.get('original_url', '')
        if not url:
            continue
        
        print(f"[{i}/{len(linkedin_examples)}] 處理: {example['title'][:50]}...")
        
        # 獲取實際的 engagement metrics
        view_count, like_count, comment_count = crawler._fetch_linkedin_engagement(url)
        
        # 更新數據
        old_likes = example.get('like_count', 0)
        old_comments = example.get('comment_count', 0)
        old_views = example.get('view_count', 0)
        
        example['view_count'] = view_count
        example['like_count'] = like_count
        example['comment_count'] = comment_count
        
        # 顯示詳細信息以便調試
        if like_count > 0 or view_count > 0:
            print(f"  ✅ 更新: Views={view_count}, Likes={like_count}, Comments={comment_count}")
            updated_count += 1
        elif comment_count > 0:
            print(f"  ✅ 更新: Views={view_count}, Likes={like_count}, Comments={comment_count}")
            updated_count += 1
        else:
            print(f"  ⚠️  無法獲取數據（可能需要登入或貼文已刪除）")
    
    # 保存更新後的數據
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 完成！更新了 {updated_count}/{len(linkedin_examples)} 個案例的數據")
    print(f"數據已保存到: {data_file}")

if __name__ == "__main__":
    update_linkedin_engagement()

