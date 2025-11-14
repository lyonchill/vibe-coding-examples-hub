"""
為案例添加分類標籤（design/productivity/innovation/management等）
"""
import json
from pathlib import Path
import re

def categorize_example(example):
    """根據案例內容自動分類"""
    title_desc = (example.get('title', '') + ' ' + example.get('description', '')).lower()
    tools = ' '.join(example.get('ai_tools_used', [])).lower()
    categories = example.get('category_tags', [])
    
    primary_category = 'Innovation'  # 默認分類
    
    # Design 相關
    if any(keyword in title_desc or keyword in tools for keyword in [
        'design system', 'ui', 'ux', 'web design', 'figma', 'icon library',
        'component', 'plugin', 'design tool', 'prototype', 'interface'
    ]):
        primary_category = 'Design'
    
    # Productivity 相關
    elif any(keyword in title_desc for keyword in [
        'automation', 'workflow', 'productivity', 'efficiency', 'time-saving',
        'streamline', 'optimize', 'speed up', 'faster', 'quick'
    ]):
        primary_category = 'Productivity'
    
    # Management 相關
    elif any(keyword in title_desc for keyword in [
        'management', 'project management', 'team', 'collaboration',
        'organization', 'planning', 'strategy', 'leadership'
    ]):
        primary_category = 'Management'
    
    # Innovation 相關（默認，或明確提到創新）
    elif any(keyword in title_desc for keyword in [
        'innovation', 'revolutionary', 'breakthrough', 'game-changer',
        'cutting-edge', 'next-gen', 'future', 'transform'
    ]):
        primary_category = 'Innovation'
    
    # 根據現有 category_tags 調整
    if 'Design' in categories or 'Design System' in categories:
        primary_category = 'Design'
    elif 'Automation' in categories:
        primary_category = 'Productivity'
    
    return primary_category

def add_categories_to_examples():
    """為所有案例添加分類"""
    data_file = Path(__file__).parent.parent / "found_examples_latest.json"
    
    if not data_file.exists():
        print("❌ 找不到數據文件")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        examples = json.load(f)
    
    print(f"處理 {len(examples)} 個案例...\n")
    
    category_counts = {}
    
    for ex in examples:
        # 添加 primary_category
        primary_category = categorize_example(ex)
        ex['primary_category'] = primary_category
        
        # 統計
        category_counts[primary_category] = category_counts.get(primary_category, 0) + 1
    
    # 保存
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
    
    print("✅ 分類完成！")
    print("\n分類統計:")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} 個案例")

if __name__ == "__main__":
    add_categories_to_examples()

