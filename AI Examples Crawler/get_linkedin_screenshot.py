"""
Helper function to get LinkedIn post screenshots
Uses free screenshot APIs
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_linkedin_screenshot_url(linkedin_url: str) -> str:
    """
    Generate screenshot URL for LinkedIn post using free services
    
    Options:
    1. Use htmlcsstoimage.com (free tier: 50/month)
    2. Use screenshotapi.net (free tier available)
    3. Use urlbox.io (has free tier)
    """
    
    # Option 1: Using htmlcsstoimage.com (if you have API key)
    htmlcsstoimage_key = os.getenv("HTMLCSSTOIMAGE_API_KEY", "")
    if htmlcsstoimage_key:
        try:
            # This service requires API key
            api_url = "https://hcti.io/v1/image"
            response = requests.post(
                api_url,
                auth=('', htmlcsstoimage_key),
                data={
                    'url': linkedin_url,
                    'viewport_width': 1200,
                    'viewport_height': 630
                },
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('url', '')
        except:
            pass
    
    # Option 2: Using screenshotapi.net (free tier)
    screenshotapi_key = os.getenv("SCREENSHOTAPI_KEY", "")
    if screenshotapi_key:
        try:
            api_url = f"https://api.screenshotapi.net/screenshot"
            params = {
                'token': screenshotapi_key,
                'url': linkedin_url,
                'width': 1200,
                'height': 630,
                'output': 'image',
                'file_type': 'png'
            }
            # This returns image directly, you might need to upload to storage
            # For now, return empty and use placeholder
        except:
            pass
    
    # Option 3: Return empty - frontend will use placeholder
    return ''

# Alternative: Use a public screenshot service (no API key needed but less reliable)
def get_linkedin_screenshot_public(linkedin_url: str) -> str:
    """
    Use public screenshot services (less reliable, may have rate limits)
    """
    # Option: Use services like:
    # - https://image.thum.io/get/width/1200/crop/630/{linkedin_url}
    # - https://api.microlink.io/data?url={linkedin_url}
    
    try:
        # Using microlink.io (free, no API key needed)
        microlink_url = f"https://api.microlink.io/data?url={linkedin_url}"
        response = requests.get(microlink_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('image', {}).get('url', '')
    except:
        pass
    
    return ''

