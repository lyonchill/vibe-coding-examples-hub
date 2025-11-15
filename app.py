"""
Flask Web Application for Vibe-Coding Examples Hub
展示 YouTube 上最熱門的 AI 編程案例
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from pathlib import Path

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 確保模板目錄路徑正確
BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / 'templates'

# 確保模板目錄存在
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

# 初始化 Flask 應用，明確指定模板目錄
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

# 數據文件路徑
DATA_DIR = BASE_DIR
EXAMPLES_FILE = DATA_DIR / "found_examples_latest.json"

logger.info(f"應用啟動 - 模板目錄: {TEMPLATE_DIR}")
logger.info(f"數據目錄: {DATA_DIR}")
logger.info(f"模板文件存在: {(TEMPLATE_DIR / 'index.html').exists()}")
logger.info(f"數據文件存在: {EXAMPLES_FILE.exists()}")


def load_examples():
    """載入案例數據"""
    try:
        # 優先載入 latest.json
        latest_file = DATA_DIR / "found_examples_latest.json"
        
        if latest_file.exists():
            try:
                logger.info(f"載入數據文件: {latest_file}")
                with open(latest_file, 'r', encoding='utf-8') as f:
                    examples = json.load(f)
                    logger.info(f"成功載入 {len(examples)} 個案例")
                    # 排序：YouTube 按觀看數，LinkedIn 按相關性分數
                    # 確保 YouTube 在前面，LinkedIn 在後面
                    examples.sort(key=lambda x: (
                        0 if x.get('source_platform') == 'YouTube' else 1,  # YouTube 優先
                        x.get('view_count', 0) if x.get('source_platform') == 'YouTube' else 0,
                        x.get('relevance_score', 0)
                    ), reverse=True)
                    return examples[:40]  # 返回前 40 個（30 YouTube + 10 LinkedIn）
            except Exception as e:
                logger.error(f"載入數據錯誤: {e}", exc_info=True)
                return []
        
        # 如果沒有 latest.json，嘗試載入最新的帶日期的文件
        json_files = list(DATA_DIR.glob("found_examples_*.json"))
        
        if json_files:
            # 找到最新的文件
            latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
            try:
                logger.info(f"載入數據文件: {latest_file}")
                with open(latest_file, 'r', encoding='utf-8') as f:
                    examples = json.load(f)
                    logger.info(f"成功載入 {len(examples)} 個案例")
                    # 排序：YouTube 按觀看數，LinkedIn 按相關性分數
                    examples.sort(key=lambda x: (
                        0 if x.get('source_platform') == 'YouTube' else 1,
                        x.get('view_count', 0) if x.get('source_platform') == 'YouTube' else 0,
                        x.get('relevance_score', 0)
                    ), reverse=True)
                    return examples[:40]  # 返回前 40 個
            except Exception as e:
                logger.error(f"載入數據錯誤: {e}", exc_info=True)
                return []
        
        logger.warning("未找到數據文件，返回空列表")
        return []
    except Exception as e:
        logger.error(f"load_examples 發生未預期錯誤: {e}", exc_info=True)
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


# 將 format_number 註冊為 Jinja2 過濾器
@app.template_filter('format_number')
def format_number_filter(num):
    return format_number(num)


@app.route('/')
def index():
    """首頁"""
    try:
        logger.info("處理首頁請求")
        examples = load_examples()
        logger.info(f"載入了 {len(examples)} 個案例")
        
        # 提取所有可用的工具
        all_tools = set()
        for example in examples:
            all_tools.update(example.get('ai_tools_used', []))
        all_tools = sorted(list(all_tools))
        
        # 提取所有可用的分類（根據現有數據自動生成）
        all_categories = set()
        for example in examples:
            category = example.get('primary_category', 'Development')
            if category:  # 排除空值和 Management
                all_categories.add(category)
        all_categories = sorted(list(all_categories))
        
        logger.info(f"渲染模板，工具數: {len(all_tools)}, 分類數: {len(all_categories)}")
        return render_template('index.html', 
                             examples=examples, 
                             format_number=format_number,
                             all_tools=all_tools,
                             all_categories=all_categories)
    except Exception as e:
        logger.error(f"首頁載入錯誤: {e}", exc_info=True)
        try:
            return render_template('index.html', 
                                 examples=[], 
                                 format_number=format_number,
                                 all_tools=[],
                                 all_categories=[]), 500
        except Exception as template_error:
            logger.error(f"渲染錯誤模板也失敗: {template_error}", exc_info=True)
            return f"<h1>錯誤</h1><p>無法載入頁面: {str(e)}</p>", 500


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


@app.route('/refresh')
def refresh():
    """手動刷新數據（觸發爬蟲）"""
    try:
        # 導入並運行爬蟲
        import sys
        crawler_path = DATA_DIR / "AI Examples Crawler" / "ai_examples_crawler.py"
        if crawler_path.exists():
            # 這裡可以調用爬蟲腳本
            # 為了簡化，我們直接返回提示
            return jsonify({
                'success': True,
                'message': '請手動運行 python "AI Examples Crawler/ai_examples_crawler.py" 來更新數據'
            })
        return jsonify({
            'success': False,
            'error': 'Crawler script not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # 開發環境啟動
    logger.info("🚀 啟動 Vibe-Coding Examples Hub（開發模式）...")
    logger.info(f"📁 數據目錄: {DATA_DIR}")
    logger.info(f"📁 模板目錄: {TEMPLATE_DIR}")
    
    # 生產環境：使用環境變量 PORT（Render 等託管服務會設置）
    # 開發環境：嘗試使用端口 5001，如果被占用則使用 8080
    port = int(os.environ.get('PORT', 5001))
    
    # 如果是開發環境（沒有 PORT 環境變量），嘗試找到可用端口
    if 'PORT' not in os.environ:
        import socket
        for test_port in [5001, 8080, 5002]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', test_port))
            sock.close()
            if result != 0:  # 端口可用
                port = test_port
                break
    
    # 生產環境使用 0.0.0.0，開發環境使用 127.0.0.1
    host = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    debug = 'PORT' not in os.environ  # 只在開發環境啟用 debug
    
    logger.info(f"🌐 訪問 http://localhost:{port} 查看網站")
    
    app.run(debug=debug, host=host, port=port)

