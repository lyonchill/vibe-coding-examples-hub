#!/bin/bash

# Vibe-Coding Examples Hub 啟動腳本

echo "🚀 啟動 Vibe-Coding Examples Hub..."
echo ""

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤：未找到 Python 3"
    exit 1
fi

# 檢查依賴是否安裝
echo "📦 檢查依賴..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask 未安裝，正在安裝依賴..."
    pip3 install -r "AI Examples Crawler/requirements.txt"
fi

# 檢查數據文件是否存在
if [ ! -f "found_examples_latest.json" ]; then
    echo "⚠️  未找到數據文件，請先運行爬蟲："
    echo "   python3 \"AI Examples Crawler/ai_examples_crawler.py\""
    echo ""
    read -p "是否現在運行爬蟲？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🕷️  運行爬蟲..."
        python3 "AI Examples Crawler/ai_examples_crawler.py"
    fi
fi

echo ""
echo "🌐 啟動網站服務器..."
echo "   訪問 http://localhost:5000 查看網站"
echo "   按 Ctrl+C 停止服務器"
echo ""

python3 app.py

