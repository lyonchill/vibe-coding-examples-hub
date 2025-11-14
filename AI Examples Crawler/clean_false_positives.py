"""
清理誤判的案例：移除指鼠標 cursor 的案例和僅功能展示的案例
"""
import json
from pathlib import Path

def clean_false_positives():
    """清理誤判的案例"""
    data_file = Path(__file__).parent.parent / "found_examples_latest.json"
    
    if not data_file.exists():
        print("❌ 找不到數據文件")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"原始案例數: {len(data)}")
    
    cleaned_data = []
    removed = []
    
    for ex in data:
        title_desc = (ex.get('title', '') + ' ' + ex.get('description', '')).lower()
        
        # 檢查是否是指鼠標 cursor 而不是 Cursor AI
        is_mouse_cursor = any(phrase in title_desc for phrase in [
            'custom cursor', 'mouse cursor', 'cursor location', 'cursor position',
            'cursor hover', 'cursor enter', 'cursor image', 'cursor style',
            'change cursor', 'cursor icon', 'cursor design', 'mouse enter',
            'cursor location', 'based on cursor', 'cursor-based', 'cursor trigger'
        ]) and 'cursor ai' not in title_desc and 'built with cursor' not in title_desc and 'using cursor' not in title_desc
        
        # 檢查是否只是功能展示而非實際構建
        is_feature_demo_only = any(phrase in title_desc for phrase in [
            'new feature', 'introducing', 'announcement', 'update',
            'what\'s new', 'check out', 'try this', 'little experiment',
            'here\'s how', 'how to use', 'tutorial', 'guide'
        ]) and not any(keyword in title_desc for keyword in [
            'built', 'build', 'created', 'made', 'generate', 'generated',
            'built with', 'built a', 'made a', 'created a'
        ])
        
        # 檢查是否有實際構建產品的證據
        has_build_evidence = any(keyword in title_desc for keyword in [
            'built', 'build', 'created', 'made', 'generate', 'generated',
            'built with', 'built a', 'made a', 'created a', 'built using',
            'made with', 'created with', 'built this', 'made this'
        ])
        
        # 檢查是否說明構建了什麼產品
        has_product_mention = any(keyword in title_desc for keyword in [
            'app', 'website', 'plugin', 'tool', 'system', 'library',
            'component', 'dashboard', 'interface', 'prototype',
            'case study', 'project', 'product'
        ])
        
        if is_mouse_cursor:
            removed.append({
                'title': ex.get('title', ''),
                'reason': '鼠標 cursor 誤判'
            })
            continue
        
        if is_feature_demo_only or (not has_build_evidence) or (not has_product_mention):
            removed.append({
                'title': ex.get('title', ''),
                'reason': '僅功能展示或無實際構建產品'
            })
            continue
        
        cleaned_data.append(ex)
    
    # 保存清理後的數據
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 清理完成！")
    print(f"  移除案例數: {len(removed)}")
    print(f"  保留案例數: {len(cleaned_data)}")
    
    if removed:
        print(f"\n移除的案例:")
        for i, item in enumerate(removed[:10], 1):
            print(f"  {i}. {item['title'][:60]}...")
            print(f"     原因: {item['reason']}")

if __name__ == "__main__":
    clean_false_positives()

