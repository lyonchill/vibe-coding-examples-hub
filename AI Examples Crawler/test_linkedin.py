"""
Quick test script for LinkedIn search functionality
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path to import crawler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_examples_crawler import AIExamplesCrawler

def test_linkedin_search():
    """Test LinkedIn search functionality"""
    print("🧪 Testing LinkedIn Search...")
    print("=" * 50)
    
    crawler = AIExamplesCrawler()
    
    # Test SerpAPI search
    print("\n1. Testing SerpAPI LinkedIn search...")
    test_query = "built with Cursor"
    results = crawler.search_linkedin_via_serpapi(test_query, max_results=3)
    
    if results:
        print(f"✅ Found {len(results)} LinkedIn posts!")
        for i, result in enumerate(results[:3], 1):
            print(f"\n  Post {i}:")
            print(f"    Title: {result['title'][:80]}...")
            print(f"    Creator: {result['creator']}")
            print(f"    URL: {result['url']}")
            print(f"    Platform: {result['platform']}")
            print(f"    Likes: {result.get('like_count', 0)}")
    else:
        print("❌ No results found")
        print("   Check your SERPAPI_KEY in .env file")
    
    print("\n" + "=" * 50)
    print("Test complete!")

if __name__ == "__main__":
    test_linkedin_search()

