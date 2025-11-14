"""
Quick script to fetch and process LinkedIn examples only
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_examples_crawler import AIExamplesCrawler

def main():
    print("🔍 Fetching LinkedIn examples...")
    print("=" * 50)
    
    crawler = AIExamplesCrawler()
    
    # LinkedIn keywords
    linkedin_keywords = [
        "built with Cursor",
        "Lovable project",
        "v0 by Vercel",
        "AI coding project",
        "no-code AI",
        "vibe coding"
    ]
    
    all_linkedin_content = []
    
    # Search LinkedIn
    for keyword in linkedin_keywords[:3]:  # Limit to 3 keywords
        print(f"\nSearching LinkedIn: {keyword}")
        results = crawler.search_linkedin_via_serpapi(keyword, max_results=5)
        if results:
            print(f"  ✅ Found {len(results)} posts")
            all_linkedin_content.extend(results)
        else:
            print(f"  ⚠️  No results")
    
    if not all_linkedin_content:
        print("\n❌ No LinkedIn content found. Check your SERPAPI_KEY.")
        return
    
    # Remove duplicates
    seen_urls = set()
    unique_content = []
    for content in all_linkedin_content:
        if content['url'] not in seen_urls:
            seen_urls.add(content['url'])
            unique_content.append(content)
    
    print(f"\n📊 Found {len(unique_content)} unique LinkedIn posts")
    
    # Process with AI
    print("\n🤖 Processing with AI...")
    processed_examples = []
    
    for i, content in enumerate(unique_content[:10], 1):  # Limit to 10 for testing
        print(f"\n[{i}/{min(10, len(unique_content))}] Processing: {content['title'][:60]}...")
        processed = crawler.process_content(content)
        
        if processed:
            processed_examples.append(processed)
            print(f"  ✅ Added (score: {processed['relevance_score']})")
        else:
            print(f"  ❌ Skipped (low relevance or not a real project)")
    
    if processed_examples:
        # Load existing data
        parent_dir = Path(__file__).parent.parent
        latest_file = parent_dir / "found_examples_latest.json"
        
        existing_examples = []
        if latest_file.exists():
            with open(latest_file, 'r', encoding='utf-8') as f:
                existing_examples = json.load(f)
        
        # Combine and deduplicate
        all_examples = existing_examples + processed_examples
        seen_urls = set()
        unique_examples = []
        for ex in all_examples:
            if ex['original_url'] not in seen_urls:
                seen_urls.add(ex['original_url'])
                unique_examples.append(ex)
        
        # Sort by view count (LinkedIn posts will have 0, so they'll be at the end)
        # For LinkedIn, we can sort by relevance_score instead
        unique_examples.sort(key=lambda x: (
            x.get('view_count', 0) if x.get('source_platform') == 'YouTube' else 0,
            x.get('relevance_score', 0)
        ), reverse=True)
        
        # Save
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(unique_examples[:30], f, indent=2, ensure_ascii=False)
        
        linkedin_count = len([e for e in unique_examples if e.get('source_platform') == 'LinkedIn'])
        print(f"\n✅ Saved {len(unique_examples)} total examples ({linkedin_count} from LinkedIn)")
        print(f"💾 File: {latest_file}")
    else:
        print("\n❌ No valid LinkedIn examples processed")

if __name__ == "__main__":
    main()

