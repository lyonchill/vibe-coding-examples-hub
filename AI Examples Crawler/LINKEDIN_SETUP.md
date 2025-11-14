# LinkedIn Search Setup Guide

This guide explains how to set up LinkedIn search functionality for the AI Examples Crawler.

## Option 1: Using SerpAPI (Recommended - Easier Setup)

SerpAPI provides a simple way to search LinkedIn without OAuth complexity.
**Note:** SerpAPI doesn't have a direct LinkedIn engine, so we use Google search with `site:linkedin.com/posts` filter to find LinkedIn posts.

### Steps:

1. **Sign up for SerpAPI**
   - Go to https://serpapi.com/
   - Create a free account (100 searches/month free)
   - Get your API key from the dashboard

2. **Add to .env file**
   ```
   SERPAPI_KEY=your_serpapi_key_here
   ```

3. **That's it!** The crawler will automatically use SerpAPI Google search to find LinkedIn posts.

## Option 2: Using LinkedIn API v2 (More Complex)

LinkedIn API requires OAuth 2.0 authentication and has stricter requirements.

### Steps:

1. **Create a LinkedIn App**
   - Go to https://www.linkedin.com/developers/apps
   - Click "Create app"
   - Fill in app details
   - Request access to "Marketing Developer Platform" or "Sign In with LinkedIn"

2. **Get OAuth Credentials**
   - In your app settings, go to "Auth" tab
   - Copy Client ID and Client Secret

3. **Get Access Token**
   - Use LinkedIn OAuth flow to get an access token
   - Or use LinkedIn's token generator tool
   - Note: Access tokens expire, you may need to refresh them

4. **Add to .env file**
   ```
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   LINKEDIN_ACCESS_TOKEN=your_access_token
   ```

### Limitations:
- LinkedIn API has strict rate limits
- Requires approval for many endpoints
- Access tokens expire and need refresh
- May require business verification

## Recommendation

**Use SerpAPI (Option 1)** for easier setup and more reliable results. It's simpler and works out of the box with just an API key.

## Testing

After setup, run the crawler:
```bash
python ai_examples_crawler.py
```

You should see LinkedIn search results in the output.

