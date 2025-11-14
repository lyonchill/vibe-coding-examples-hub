"""
AI Examples Hub - Automated Content Crawler
Searches for AI project examples and sends daily email digest
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List
from dotenv import load_dotenv

import google.generativeai as genai
from google.generativeai import types as genai_types

# Load environment variables from .env file
load_dotenv()

# Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_KEY_HERE")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_KEY_HERE")
EMAIL_TO = os.getenv("EMAIL_TO", "your-email@example.com")
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")

if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_KEY_HERE":
    genai.configure(api_key=GEMINI_API_KEY)

# Search keywords targeting no-code/low-code AI projects
SEARCH_KEYWORDS = [
    "built with Cursor AI",
    "Lovable AI project",
    "v0 by Vercel project",
    "built with Claude",
    "made with ChatGPT",
    "made with Gemini",
    "n8n AI automation",
    "Make.com AI workflow",
    "Replit AI app",
    "Bolt.new project",
    "no-code AI project",
    "AI project showcase",
    "built AI product weekend"
]

# Target tools to detect
TARGET_TOOLS = [
    "Cursor", "Claude", "ChatGPT", "Gemini", "GitHub Copilot", "v0", "Lovable",
    "Replit", "Bolt.new", "Make.com", "n8n", "Zapier", "Bubble",
    "Figma", "Framer", "Webflow", "Airtable", "Notion AI",
    "Midjourney", "DALL-E", "Stable Diffusion", "RunwayML",
    "ElevenLabs", "Suno", "Udio"
]

CATEGORY_TAGS = [
    "Computer Vision", "NLP", "Generative AI", "Machine Learning",
    "Automation", "Content Creation", "Code Generation", "Design",
    "Audio/Music", "Video", "Data Analysis", "Chatbot", "Agent"
]


class AIExamplesCrawler:
    def __init__(self):
        self.found_examples = []
        self.model = None
        if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_KEY_HERE":
            # 嘗試使用可用的模型，優先使用 gemini-2.0-flash-exp
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
            
            # 如果指定的模型不可用，嘗試其他模型
            try:
                self.model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config=genai_types.GenerationConfig(
                        temperature=0.2,
                        top_p=0.8,
                        top_k=40,
                        response_mime_type="application/json",
                    ),
                )
                # 測試模型是否可用
                test_response = self.model.generate_content("test")
            except Exception as e:
                # 如果失敗，嘗試使用 gemini-1.5-flash
                print(f"⚠️  模型 {model_name} 不可用，嘗試使用 gemini-1.5-flash")
                try:
                    self.model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        generation_config=genai_types.GenerationConfig(
                            temperature=0.2,
                            top_p=0.8,
                            top_k=40,
                            response_mime_type="application/json",
                        ),
                    )
                except Exception as e2:
                    print(f"❌ 無法初始化 Gemini 模型: {e2}")
                    self.model = None

    def search_youtube(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search YouTube for AI project videos"""
        url = "https://www.googleapis.com/youtube/v3/search"
        
        # Get videos from the last 30 days
        published_after = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
        
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'order': 'viewCount',  # 改為按觀看數排序
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
            
            # 獲取視頻統計信息（包括觀看數）
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
                
                # 建立 video_id 到統計信息的映射
                stats_map = {}
                for video_item in stats_data.get('items', []):
                    vid = video_item['id']
                    stats_map[vid] = {
                        'view_count': int(video_item['statistics'].get('viewCount', 0)),
                        'like_count': int(video_item['statistics'].get('likeCount', 0)),
                        'comment_count': int(video_item['statistics'].get('commentCount', 0))
                    }
            
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                stats = stats_map.get(video_id, {'view_count': 0, 'like_count': 0, 'comment_count': 0})
                
                results.append({
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail': snippet['thumbnails']['high']['url'],
                    'creator': snippet['channelTitle'],
                    'creator_url': f"https://www.youtube.com/channel/{snippet['channelId']}",
                    'platform': 'YouTube',
                    'published_at': snippet['publishedAt'],
                    'view_count': stats['view_count'],
                    'like_count': stats['like_count'],
                    'comment_count': stats['comment_count']
                })
            
            # 按觀看數排序
            results.sort(key=lambda x: x.get('view_count', 0), reverse=True)
            
            return results
        except Exception as e:
            print(f"YouTube search error: {e}")
            return []

    def search_twitter(self, query: str) -> List[Dict]:
        """
        Search Twitter/X for AI projects
        Note: Requires Twitter API v2 access (paid)
        For free alternative, you could use nitter.net or manual scraping
        """
        # Placeholder - implement if you have Twitter API access
        # For now, returning empty to keep script functional
        print(f"Twitter search for '{query}' - skipped (requires API setup)")
        return []

    def search_linkedin(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search LinkedIn posts for AI project examples
        
        Note: LinkedIn API requires OAuth authentication.
        Options:
        1. Use LinkedIn API v2 with OAuth (recommended)
        2. Use SerpAPI or similar service for LinkedIn search
        3. Manual URL input
        
        This implementation uses LinkedIn API v2.
        """
        if not LINKEDIN_ACCESS_TOKEN or LINKEDIN_ACCESS_TOKEN == "":
            print(f"LinkedIn search for '{query}' - skipped (requires ACCESS_TOKEN)")
            return []
        
        url = "https://api.linkedin.com/v2/search"
        
        headers = {
            'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # LinkedIn search parameters
        params = {
            'keywords': query,
            'q': 'all',
            'count': max_results,
            'start': 0
        }
        
        try:
            # Note: LinkedIn API v2 search endpoint may require different parameters
            # This is a basic implementation - you may need to adjust based on your API access level
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 401:
                print(f"LinkedIn API authentication failed - check your access token")
                return []
            elif response.status_code == 403:
                print(f"LinkedIn API access denied - check your API permissions")
                return []
            
            response.raise_for_status()
            data = response.json()
            
            results = []
            elements = data.get('elements', [])
            
            for element in elements:
                # Extract post information
                # Note: Structure depends on LinkedIn API response format
                target = element.get('target', {})
                if not target:
                    continue
                
                # Get post content
                text = target.get('text', {}).get('text', '')
                if not text:
                    continue
                
                # Get author info
                author = target.get('author', '')
                author_name = 'Unknown'
                author_url = ''
                if isinstance(author, str):
                    author_name = author
                elif isinstance(author, dict):
                    author_name = author.get('name', 'Unknown')
                    author_url = author.get('url', '')
                
                # Get post URL
                post_url = target.get('url', '')
                if not post_url and target.get('id'):
                    post_url = f"https://www.linkedin.com/feed/update/{target.get('id')}"
                
                # Get engagement metrics
                engagement = target.get('socialMetadata', {}).get('engagement', {})
                view_count = engagement.get('viewCount', 0)
                like_count = engagement.get('likeCount', 0)
                comment_count = engagement.get('commentCount', 0)
                
                # Get thumbnail if available
                thumbnail_url = ''
                if target.get('images'):
                    thumbnail_url = target['images'][0].get('url', '')
                
                results.append({
                    'title': text[:100] + '...' if len(text) > 100 else text,
                    'description': text,
                    'url': post_url,
                    'thumbnail': thumbnail_url,
                    'creator': author_name,
                    'creator_url': author_url,
                    'platform': 'LinkedIn',
                    'published_at': target.get('created', {}).get('time', datetime.now().isoformat()),
                    'view_count': view_count,
                    'like_count': like_count,
                    'comment_count': comment_count
                })
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"LinkedIn search error: {e}")
            return []
        except Exception as e:
            print(f"LinkedIn search error: {e}")
            return []

    def search_linkedin_via_serpapi(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search LinkedIn posts using SerpAPI Google search
        Since SerpAPI doesn't have a direct LinkedIn engine, we use Google search
        to find LinkedIn posts with site:linkedin.com filter
        """
        serpapi_key = os.getenv("SERPAPI_KEY", "")
        if not serpapi_key or serpapi_key == "":
            print(f"LinkedIn search via SerpAPI for '{query}' - skipped (requires SERPAPI_KEY)")
            return []
        
        url = "https://serpapi.com/search"
        
        # Use Google search with site:linkedin.com filter
        search_query = f"site:linkedin.com/posts {query}"
        
        params = {
            'engine': 'google',
            'q': search_query,
            'api_key': serpapi_key,
            'num': max_results
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            results = []
            organic_results = data.get('organic_results', [])
            
            for result in organic_results:
                link = result.get('link', '')
                # Only process LinkedIn post URLs
                if 'linkedin.com/posts' not in link and 'linkedin.com/feed' not in link:
                    continue
                
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                
                # Extract author from link or title if possible
                creator_name = 'Unknown'
                creator_url = ''
                
                # Try to extract from link structure
                if '/posts/' in link:
                    # LinkedIn post URL format: linkedin.com/posts/username_activity-id
                    parts = link.split('/posts/')
                    if len(parts) > 1:
                        username = parts[1].split('_')[0] if '_' in parts[1] else parts[1].split('-')[0]
                        creator_name = username.replace('-', ' ').title()
                        creator_url = f"https://www.linkedin.com/in/{username}/"
                
                # Try to fetch engagement metrics from LinkedIn post page
                view_count, like_count, comment_count = self._fetch_linkedin_engagement(link)
                
                results.append({
                    'title': title or snippet[:100],
                    'description': snippet or title,
                    'url': link,
                    'thumbnail': result.get('thumbnail', ''),
                    'creator': creator_name,
                    'creator_url': creator_url,
                    'platform': 'LinkedIn',
                    'published_at': result.get('date', datetime.now().isoformat()),
                    'view_count': view_count,
                    'like_count': like_count,
                    'comment_count': comment_count
                })
            
            return results
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_data = e.response.json() if hasattr(e.response, 'json') else {}
                error_msg = error_data.get('error', str(e))
                print(f"LinkedIn SerpAPI search error: {error_msg}")
            else:
                print(f"LinkedIn SerpAPI search HTTP error: {e}")
            return []
        except Exception as e:
            print(f"LinkedIn SerpAPI search error: {e}")
            return []
    
    def _fetch_linkedin_engagement(self, linkedin_url: str) -> tuple:
        """
        從 LinkedIn 貼文頁面獲取實際的 likes、comments 和 views 數據
        返回: (view_count, like_count, comment_count)
        """
        view_count, like_count, comment_count = 0, 0, 0
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = requests.get(linkedin_url, headers=headers, timeout=10, allow_redirects=True)
            
            if response.status_code != 200:
                return (0, 0, 0)
            
            html = response.text
            
            # LinkedIn 在頁面中嵌入 JSON-LD 結構化數據
            # 嘗試多種方法來提取 engagement metrics
            
            import re
            
            # Method 1: 查找 JSON-LD 中的 engagement metrics
            json_ld_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
            json_ld_matches = re.findall(json_ld_pattern, html, re.DOTALL | re.IGNORECASE)
            
            for json_str in json_ld_matches:
                try:
                    import json
                    data = json.loads(json_str)
                    # 遞歸搜索 engagement 數據
                    if isinstance(data, dict):
                        engagement = self._extract_engagement_from_dict(data)
                        if engagement[1] > 0 or engagement[2] > 0:  # 如果有找到 likes 或 comments
                            return engagement
                except:
                    continue
            
            # Method 2: 查找頁面中的數字模式（likes, comments, views）
            # LinkedIn 顯示格式: "123 reactions", "45 comments", "1,234 views"
            
            # 查找 reactions/likes
            like_patterns = [
                r'(\d+(?:,\d+)*)\s*(?:reactions?|likes?)',  # "568 reactions"
                r'"reactionCount":\s*(\d+)',  # JSON format
                r'"likeCount":\s*(\d+)',  # JSON format
                r'data-reaction-count=["\'](\d+)["\']',  # data attribute
                r'interactionCount["\']?\s*:\s*(\d+)',  # interactionCount: 568
                r'reactions["\']?\s*[:\-]?\s*(\d+)',  # reactions: 568
                r'(\d+)\s*reactions?',  # 568 reactions (simpler)
            ]
            
            like_count = 0
            all_like_numbers = []
            for pattern in like_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    try:
                        numbers = [int(str(m).replace(',', '')) for m in matches]
                        all_like_numbers.extend(numbers)
                    except Exception as e:
                        continue
            
            # 取最大的數字（通常是貼文的主要 engagement）
            if all_like_numbers:
                # 過濾掉異常大的數字（可能是 ID 或其他數據）
                # 通常 LinkedIn reactions 不會超過 100,000
                reasonable_numbers = [n for n in all_like_numbers if 10 <= n <= 100000]
                if reasonable_numbers:
                    like_count = max(reasonable_numbers)
                elif all_like_numbers:
                    # 如果沒有合理的數字，至少取一個
                    like_count = max(all_like_numbers)
            
            # 查找 comments
            comment_patterns = [
                r'(\d+(?:,\d+)*)\s*comments?',
                r'"commentCount":\s*(\d+)',
                r'data-comment-count=["\'](\d+)["\']',
                r'comments["\']?\s*[:\-]?\s*(\d+)',
            ]
            
            comment_count = 0
            for pattern in comment_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    try:
                        numbers = [int(m.replace(',', '')) for m in matches]
                        comment_count = max(numbers) if numbers else 0
                        if comment_count > 0:
                            break
                    except:
                        continue
            
            # 查找 views
            view_patterns = [
                r'(\d+(?:,\d+)*)\s*views?',  # "1,234 views"
                r'"viewCount":\s*(\d+)',  # JSON format
                r'data-view-count=["\'](\d+)["\']',  # data attribute
                r'views["\']?\s*[:\-]?\s*(\d+)',  # views: 1234
                r'(\d+)\s*views?',  # 1234 views (simpler)
                r'viewCount["\']?\s*:\s*(\d+)',  # viewCount: 1234
            ]
            
            view_count = 0
            all_view_numbers = []
            for pattern in view_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    try:
                        numbers = [int(m.replace(',', '')) for m in matches]
                        all_view_numbers.extend(numbers)
                    except:
                        continue
            
            # 取最大的數字
            if all_view_numbers:
                # 過濾掉太小的數字
                filtered_numbers = [n for n in all_view_numbers if n >= 100]
                if filtered_numbers:
                    view_count = max(filtered_numbers)
                elif all_view_numbers:
                    view_count = max(all_view_numbers)
            
            return (view_count, like_count, comment_count)
            
        except Exception as e:
            # 如果獲取失敗，返回當前已提取的數據（可能部分成功）
            # 這樣即使部分提取失敗，也能保留已獲取的數據
            return (view_count, like_count, comment_count)
    
    def _extract_engagement_from_dict(self, data: dict, depth: int = 0) -> tuple:
        """
        遞歸搜索字典中的 engagement metrics
        返回: (view_count, like_count, comment_count)
        """
        if depth > 5:  # 防止無限遞歸
            return (0, 0, 0)
        
        view_count = 0
        like_count = 0
        comment_count = 0
        
        for key, value in data.items():
            key_lower = str(key).lower()
            
            if isinstance(value, dict):
                sub_result = self._extract_engagement_from_dict(value, depth + 1)
                view_count = max(view_count, sub_result[0])
                like_count = max(like_count, sub_result[1])
                comment_count = max(comment_count, sub_result[2])
            elif isinstance(value, (int, float)):
                if 'view' in key_lower and value > view_count:
                    view_count = int(value)
                elif ('like' in key_lower or 'reaction' in key_lower) and value > like_count:
                    like_count = int(value)
                elif 'comment' in key_lower and value > comment_count:
                    comment_count = int(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        sub_result = self._extract_engagement_from_dict(item, depth + 1)
                        view_count = max(view_count, sub_result[0])
                        like_count = max(like_count, sub_result[1])
                        comment_count = max(comment_count, sub_result[2])
        
        return (view_count, like_count, comment_count)

    def search_medium(self, tag: str = "artificial-intelligence") -> List[Dict]:
        """Search Medium via RSS feed"""
        try:
            # Medium's RSS feed for tags
            rss_url = f"https://medium.com/feed/tag/{tag}"
            response = requests.get(rss_url)
            
            # Simple RSS parsing (you might want to use feedparser library)
            # For now, returning placeholder
            print(f"Medium search for tag '{tag}' - implement RSS parsing")
            return []
        except Exception as e:
            print(f"Medium search error: {e}")
            return []

    def analyze_with_ai(self, content: Dict) -> Dict:
        """Use Gemini to analyze and extract structured information"""
        
        if not self.model:
            print("⚠️ Gemini API key not configured - skipping AI analysis")
            return {
                "relevance_score": 0,
                "ai_tools_used": [],
                "category_tags": [],
                "is_no_code_low_code": False,
                "enhanced_description": content["description"][:200],
                "build_complexity": "Unknown",
            }

        prompt = {
            "system_instruction": (
                "You are an analyst helping a research team curate daily AI project showcases. "
                "You must return concise, factual JSON following the provided schema. "
                "Never fabricate tool names, and only include categories that are clearly supported "
                "by the description. Prioritize no-code/low-code relevance. "
                "IMPORTANT: Only mark as a real project if it shows ACTUAL BUILDING/CREATION of a product/app/system. "
                "Exclude posts that only showcase new features, announce updates, or demonstrate capabilities without building something concrete. "
                "The project_evidence must clearly state what was BUILT (e.g. 'built a design system plugin', 'created an icon library', 'made a UI component generator'). "
                "If the content only shows 'how to use' or 'new feature announcement' without actual building, set is_real_project to false. "
                "Also exclude posts about 'cursor' (mouse cursor) unless it clearly refers to 'Cursor AI' tool. "
                "Always capture what digital artifact was created (name, purpose, audience)."
            ),
            "user": {
                "title": content["title"],
                "description": content["description"],
                "url": content["url"],
                "platform": content["platform"],
                "target_tools": TARGET_TOOLS,
                "category_tags": CATEGORY_TAGS,
            },
        }

        try:
            response = self.model.generate_content(
                [
                    "Analyze the following AI project content and respond with JSON only.",
                    json.dumps(prompt),
                    json.dumps(
                        {
                            "expected_schema": {
                                "relevance_score": "integer 0-10",
                                "ai_tools_used": "array of strings",
                                "category_tags": "array of strings chosen from provided list",
                                "is_no_code_low_code": "boolean",
                                "is_real_project": "boolean — True only if a concrete project/app/automation was built and shown",
                                "project_name": "string — concise name of the artifact built or showcased (e.g. 'AI-powered travel itinerary app')",
                                "project_summary": "string — 1 sentence summarizing what the artifact does and for whom",
                                "project_evidence": "string — brief justification citing the specific demo or artifact that was built or showcased",
                                "enhanced_description": "string (2-3 sentences)",
                                "build_complexity": "string enum: No-code | Low-code | Full Build",
                            }
                        }
                    ),
                ]
            )

            response_text = ""
            for candidate in response.candidates or []:
                if candidate.finish_reason and candidate.finish_reason == 3:
                    # Safety blocked
                    raise ValueError("Gemini response blocked by safety filters")
                for part in getattr(candidate.content, "parts", []) or []:
                    text = getattr(part, "text", None)
                    if text:
                        response_text += text
                response_text = response_text.strip()
            
            if not response_text:
                raise ValueError("Gemini 回傳空白內容")

            # Clean up potential formatting issues
            if response_text.startswith("```"):
                response_text = response_text.strip("`")
                if response_text.lower().startswith("json"):
                    response_text = response_text[4:].strip()

            analysis = json.loads(response_text)

            # Basic validation
            analysis.setdefault("ai_tools_used", [])
            analysis.setdefault("category_tags", [])
            analysis.setdefault("is_no_code_low_code", False)
            analysis.setdefault("is_real_project", False)
            analysis.setdefault("project_evidence", "")
            analysis.setdefault("project_name", "")
            analysis.setdefault("project_summary", "")
            analysis.setdefault("enhanced_description", content["description"][:200])
            analysis.setdefault("build_complexity", "Unknown")
            analysis.setdefault("relevance_score", 0)

            return analysis
            
        except Exception as e:
            print(f"AI analysis error: {e}")
            return {
                "relevance_score": 0,
                "ai_tools_used": [],
                "category_tags": [],
                "is_no_code_low_code": False,
                "enhanced_description": content["description"][:200],
                "build_complexity": "Unknown",
            }

    def process_content(self, raw_content: Dict) -> Dict:
        """Process raw content into structured format"""
        
        # Use AI to analyze
        analysis = self.analyze_with_ai(raw_content)
        
        # Skip if not relevant enough
        if analysis['relevance_score'] < 6:
            return None

        if not analysis.get("is_real_project", False):
            return None

        project_name = analysis.get("project_name", "").strip()
        project_summary = analysis.get("project_summary", "").strip()
        if not project_name or project_name.lower() in {"unknown", "unspecified"}:
            return None
        if not project_summary or project_summary.lower() in {"unknown", "unspecified"}:
            return None
        
        # Create structured example
        example = {
            'title': raw_content['title'],
            'description': analysis['enhanced_description'],
            'ai_tools_used': analysis['ai_tools_used'],
            'category_tags': analysis['category_tags'],
            'source_platform': raw_content['platform'],
            'original_url': raw_content['url'],
            'creator_name': raw_content.get('creator', 'Unknown'),
            'creator_link': raw_content.get('creator_url', ''),
            'thumbnail_url': raw_content.get('thumbnail', ''),
            'date_added': datetime.now().isoformat(),
            'relevance_score': analysis['relevance_score'],
            'build_complexity': analysis['build_complexity'],
            'is_no_code_low_code': analysis['is_no_code_low_code'],
            'project_name': project_name,
            'project_summary': project_summary,
            'project_evidence': analysis.get('project_evidence', '')
        }
        
        return example

    def crawl_all_sources(self, target_count: int = 30):
        """Crawl all configured sources and get top videos"""
        print("🔍 Starting crawl...")
        
        all_raw_content = []
        
        # Search YouTube for each keyword, 獲取更多結果以確保有足夠的候選
        for keyword in SEARCH_KEYWORDS:
            print(f"Searching YouTube: {keyword}")
            results = self.search_youtube(keyword, max_results=10)
            all_raw_content.extend(results)
        
        # Search LinkedIn for vibe-coding examples
        linkedin_keywords = [
            "built with Cursor",
            "Lovable project",
            "v0 by Vercel",
            "AI coding project",
            "no-code AI",
            "vibe coding"
        ]
        
        for keyword in linkedin_keywords[:3]:  # Limit to 3 to save API quota
            print(f"Searching LinkedIn: {keyword}")
            # Try SerpAPI first (easier setup), fallback to LinkedIn API
            results = self.search_linkedin_via_serpapi(keyword, max_results=5)
            if not results:
                results = self.search_linkedin(keyword, max_results=5)
            all_raw_content.extend(results)
        
        # 去重（基於 URL）
        seen_urls = set()
        unique_content = []
        for content in all_raw_content:
            if content['url'] not in seen_urls:
                seen_urls.add(content['url'])
                unique_content.append(content)
        
        # 按觀看數排序
        unique_content.sort(key=lambda x: x.get('view_count', 0), reverse=True)
        
        print(f"Found {len(unique_content)} unique raw items")
        
        # Process each item with AI
        for content in unique_content:
            if len(self.found_examples) >= target_count:
                break
            print(f"Analyzing: {content['title'][:50]}...")
            processed = self.process_content(content)
            
            if processed:
                # 添加觀看數等統計信息
                processed['view_count'] = content.get('view_count', 0)
                processed['like_count'] = content.get('like_count', 0)
                processed['comment_count'] = content.get('comment_count', 0)
                self.found_examples.append(processed)
                print(f"✅ Added (score: {processed['relevance_score']}, views: {processed['view_count']})")
            else:
                print(f"❌ Skipped (low relevance)")
        
        # Sort by view count first, then by relevance score
        self.found_examples.sort(key=lambda x: (x.get('view_count', 0), x['relevance_score']), reverse=True)
        
        print(f"\n✨ Found {len(self.found_examples)} relevant examples")
        return self.found_examples

    def generate_email_html(self, examples: List[Dict]) -> str:
        """Generate HTML email with found examples"""
        
        if not examples:
            return "<p>No new AI examples found today.</p>"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #003c72; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .example {{ border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
                .example img {{ max-width: 100%; border-radius: 4px; border: 1px solid #cdd7f3; }}
                .score {{ background: #4CAF50; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; }}
                .tools {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }}
                .tool-tag {{ background: #ebf1ff; color: #003c72; padding: 4px 12px; border-radius: 12px; font-size: 12px; }}
                .buttons {{ margin-top: 15px; }}
                .btn {{ display: inline-block; padding: 10px 20px; margin-right: 10px; text-decoration: none; border-radius: 4px; }}
                .btn-approve {{ background: #4CAF50; color: white; }}
                .btn-reject {{ background: #f44336; color: white; }}
                .evidence {{ background: #f7fbff; border-left: 4px solid #2563eb; padding: 12px 16px; margin: 15px 0; line-height: 1.6; }}
                .artifact {{ margin: 15px 0; }}
                .artifact-label {{ font-weight: bold; color: #0f172a; display: block; margin-bottom: 8px; }}
                .artifact-warning {{ font-size: 12px; color: #6b7280; margin-top: 6px; }}
                .artifact-meta {{ margin: 12px 0; padding: 10px 14px; background: #eef2ff; border-radius: 8px; }}
                .artifact-meta strong {{ color: #1e3a8a; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🤖 Daily AI Examples Digest</h1>
                <p>Found {len(examples)} new projects from {datetime.now().strftime('%Y-%m-%d')}</p>
            </div>
        """
        
        for i, example in enumerate(examples):
            html += f"""
            <div class="example">
                <h2>{example['title']}</h2>
                <span class="score">Relevance: {example['relevance_score']}/10</span>
                <span class="score">{example['build_complexity']}</span>
                
                <div class="artifact-meta">
                    <p><strong>🎯 Artifact:</strong> {example.get('project_name', '未命名專案')}</p>
                    <p><strong>用途說明:</strong> {example.get('project_summary', '尚未摘要用途')}</p>
                </div>
                
                {f'<div class="artifact"><span class="artifact-label">📸 專案截圖（須為實際成果）</span><img src="{example["thumbnail_url"]}" alt="artifact thumbnail"><div class="artifact-warning">請確認縮圖對應影片中的實際產出或 Demo 畫面。</div></div>' if example['thumbnail_url'] else '<p><em>未提供專案截圖，請人工補上成果畫面。</em></p>'}
                
                <p>{example['description']}</p>

                {f'<div class="evidence"><strong>專案成果亮點：</strong> {example["project_evidence"]}</div>' if example.get("project_evidence") else ''}
                
                <div class="tools">
                    <strong>AI Tools:</strong>
                    {' '.join([f'<span class="tool-tag">{tool}</span>' for tool in example['ai_tools_used']])}
                </div>
                
                <div class="tools">
                    <strong>Categories:</strong>
                    {' '.join([f'<span class="tool-tag">{tag}</span>' for tag in example['category_tags']])}
                </div>
                
                <p><strong>Creator:</strong> <a href="{example['creator_link']}">{example['creator_name']}</a></p>
                <p><strong>Platform:</strong> {example['source_platform']}</p>
                <p><strong>URL:</strong> <a href="{example['original_url']}">{example['original_url']}</a></p>
                
                <div class="buttons">
                    <a href="mailto:{EMAIL_TO}?subject=APPROVE:{i}&body=Approved" class="btn btn-approve">✅ Approve & Add</a>
                    <a href="mailto:{EMAIL_TO}?subject=REJECT:{i}&body=Rejected" class="btn btn-reject">❌ Skip</a>
                </div>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html

    def send_email(self, html_content: str):
        """Send email using a service (implement based on your preference)"""
        
        # Option 1: Using Gmail SMTP
        # Option 2: Using SendGrid
        # Option 3: Using Mailgun
        # For now, just save to file for testing
        
        output_file = f"email_digest_{datetime.now().strftime('%Y%m%d')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n📧 Email digest saved to: {output_file}")
        print("Open this file in your browser to preview the email")

    def save_to_json(self, examples: List[Dict]):
        """Save found examples to JSON file"""
        # 保存帶日期的版本
        dated_filename = f"found_examples_{datetime.now().strftime('%Y%m%d')}.json"
        with open(dated_filename, 'w', encoding='utf-8') as f:
            json.dump(examples, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved to: {dated_filename}")
        
        # 同時保存為 latest.json（網站會讀取這個）
        # 保存到父目錄，這樣網站可以直接讀取
        import os
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        latest_filename = os.path.join(parent_dir, "found_examples_latest.json")
        with open(latest_filename, 'w', encoding='utf-8') as f:
            json.dump(examples, f, indent=2, ensure_ascii=False)
        print(f"💾 Also saved to: {latest_filename}")


def main():
    """Main execution"""
    print("🚀 AI Examples Hub Crawler Starting...")
    print("=" * 50)
    
    crawler = AIExamplesCrawler()
    
    # Crawl all sources - 獲取 30 個最熱門的案例
    examples = crawler.crawl_all_sources(target_count=30)
    
    if examples:
        # Save to JSON (網站會讀取這個文件)
        crawler.save_to_json(examples)
        print(f"\n✅ 已保存 {len(examples)} 個案例到 JSON 文件")
    else:
        print("No examples found today")
    
    print("\n✅ Crawl complete!")


if __name__ == "__main__":
    main()
