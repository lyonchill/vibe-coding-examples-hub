"""
使用 Supabase 的 Flask 應用版本（可選）
如果使用 Supabase 存儲數據，將此文件重命名為 app.py
"""
import os
import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Supabase 配置
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

app = Flask(__name__)

# 如果沒有 Supabase 配置，回退到 JSON 文件
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)

if USE_SUPABASE:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ 使用 Supabase 作為數據源")
else:
    print("⚠️  未配置 Supabase，使用 JSON 文件作為數據源")
    DATA_DIR = Path(__file__).parent
    EXAMPLES_FILE = DATA_DIR / "found_examples_latest.json"


def load_examples():
    """載入案例數據"""
    if USE_SUPABASE:
        try:
            # 從 Supabase 讀取數據
            response = supabase.table('examples')\
                .select('*')\
                .order('view_count', desc=True)\
                .order('relevance_score', desc=True)\
                .limit(40)\
                .execute()
            
            examples = response.data
            
            # 轉換數據格式以匹配模板
            for ex in examples:
                # 確保列表字段是列表類型
                if isinstance(ex.get('ai_tools_used'), str):
                    ex['ai_tools_used'] = json.loads(ex['ai_tools_used']) if ex['ai_tools_used'] else []
                if isinstance(ex.get('category_tags'), str):
                    ex['category_tags'] = json.loads(ex['category_tags']) if ex['category_tags'] else []
            
            # 排序：YouTube 優先
            examples.sort(key=lambda x: (
                0 if x.get('source_platform') == 'YouTube' else 1,
                x.get('view_count', 0) if x.get('source_platform') == 'YouTube' else 0,
                x.get('relevance_score', 0)
            ), reverse=True)
            
            return examples[:40]
        except Exception as e:
            import logging
            logging.error(f"Supabase 載入錯誤: {e}")
            return []
    else:
        # 回退到 JSON 文件
        latest_file = DATA_DIR / "found_examples_latest.json"
        if latest_file.exists():
            try:
                with open(latest_file, 'r', encoding='utf-8') as f:
                    examples = json.load(f)
                    examples.sort(key=lambda x: (
                        0 if x.get('source_platform') == 'YouTube' else 1,
                        x.get('view_count', 0) if x.get('source_platform') == 'YouTube' else 0,
                        x.get('relevance_score', 0)
                    ), reverse=True)
                    return examples[:40]
            except Exception as e:
                import logging
                logging.error(f"載入數據錯誤: {e}")
                return []
        return []


def format_number(num):
    """格式化數字（例如：1000 -> 1K）"""
    try:
        num = int(num)
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)
    except:
        return str(num)


@app.template_filter('format_number')
def format_number_filter(num):
    return format_number(num)


@app.route('/')
def index():
    """首頁"""
    try:
        examples = load_examples()
        
        all_tools = set()
        for example in examples:
            all_tools.update(example.get('ai_tools_used', []))
        all_tools = sorted(list(all_tools))
        
        all_categories = set()
        for example in examples:
            category = example.get('primary_category', 'Development')
            if category:
                all_categories.add(category)
        all_categories = sorted(list(all_categories))
        
        return render_template('index.html', 
                             examples=examples, 
                             format_number=format_number,
                             all_tools=all_tools,
                             all_categories=all_categories)
    except Exception as e:
        import logging
        logging.error(f"首頁載入錯誤: {e}")
        return render_template('index.html', 
                             examples=[], 
                             format_number=format_number,
                             all_tools=[],
                             all_categories=[]), 500


@app.route('/api/examples')
def api_examples():
    """API 端點：獲取所有案例"""
    try:
        examples = load_examples()
        return jsonify({
            'success': True,
            'count': len(examples),
            'examples': examples
        })
    except Exception as e:
        import logging
        logging.error(f"API 錯誤: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/examples/<int:example_id>')
def api_example_detail(example_id):
    """API 端點：獲取單個案例詳情"""
    try:
        examples = load_examples()
        if 0 <= example_id < len(examples):
            return jsonify({
                'success': True,
                'example': examples[example_id]
            })
        return jsonify({
            'success': False,
            'error': 'Example not found'
        }), 404
    except Exception as e:
        import logging
        logging.error(f"API 錯誤: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    template_dir = Path(__file__).parent / 'templates'
    template_dir.mkdir(exist_ok=True)
    
    port = int(os.environ.get('PORT', 5001))
    host = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    debug = 'PORT' not in os.environ
    
    print(f"🚀 啟動 Vibe-Coding Examples Hub...")
    print(f"🌐 訪問 http://localhost:{port} 查看網站")
    
    app.run(debug=debug, host=host, port=port)

