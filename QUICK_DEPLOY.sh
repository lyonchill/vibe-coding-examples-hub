#!/bin/bash
# 快速部署腳本 - 推送到 GitHub

echo "🚀 準備推送到 GitHub..."
echo ""

# 檢查是否已經有 remote
if git remote -v | grep -q "origin"; then
    echo "✅ 已配置 GitHub remote"
    echo ""
    echo "📋 當前 remote:"
    git remote -v
    echo ""
    read -p "是否要推送到現有的 remote? (y/N): " confirm
    if [[ $confirm == [yY] ]]; then
        echo "📤 推送到 GitHub..."
        git push -u origin main || git push -u origin master
        echo "✅ 推送完成！"
    fi
else
    echo "⚠️  尚未配置 GitHub remote"
    echo ""
    echo "請先執行以下步驟："
    echo ""
    echo "1. 在 GitHub 創建新 repository："
    echo "   - 訪問 https://github.com/new"
    echo "   - Repository name: vibe-coding-examples-hub（或你喜歡的名稱）"
    echo "   - 選擇 Public 或 Private"
    echo "   - 不要初始化 README、.gitignore 或 license"
    echo "   - 點擊 Create repository"
    echo ""
    echo "2. 然後執行以下命令："
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
    echo "   git push -u origin main"
    echo ""
    echo "或者直接運行此腳本，它會提示你輸入 GitHub URL"
    echo ""
    read -p "輸入你的 GitHub repository URL (例如: https://github.com/username/repo.git): " repo_url
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "📤 推送到 GitHub..."
        git push -u origin main || git push -u origin master
        echo "✅ 推送完成！"
        echo ""
        echo "🎉 現在可以前往 Render 部署了！"
        echo "   訪問: https://render.com"
    else
        echo "❌ 未輸入 URL，跳過推送"
    fi
fi

