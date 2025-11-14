"""
AI Examples Hub - Setup Verification Script
確認本地環境與關鍵設定是否準備完成。
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Tuple

import requests
from dotenv import load_dotenv

try:
    import google.generativeai as genai
    from google.generativeai import types as genai_types
except ImportError:  # pragma: no cover - optional dependency check
    genai = None
    genai_types = None


PROJECT_ROOT = Path(__file__).resolve().parent
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
ENV_FILE = PROJECT_ROOT / ".env"
PACKAGE_IMPORT_MAP = {
    "python-dotenv": "dotenv",
    "google-generativeai": "google.generativeai",
}


def print_section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def check_python_environment() -> bool:
    print_section("1. Python 與 pip 環境檢查")
    executable = sys.executable
    version = ".".join(map(str, sys.version_info[:3]))
    print(f"✅ 目前使用的 Python: {executable}")
    print(f"✅ Python 版本: {version}")

    pip_path = shutil.which("pip3") or shutil.which("pip")
    if not pip_path:
        print("❌ 找不到 pip 或 pip3，請先安裝 Python 套件管理工具")
        return False

    print(f"✅ pip 路徑: {pip_path}")

    # 樣式化 requirements 檢查
    missing_packages = []
    if REQUIREMENTS_FILE.exists():
        print(f"🔍 檢查必要套件（來源: {REQUIREMENTS_FILE.name}）")
        with REQUIREMENTS_FILE.open("r", encoding="utf-8") as req_file:
            for line in req_file:
                requirement = line.strip()
                if not requirement or requirement.startswith("#"):
                    continue
                package = requirement.split("==")[0].split(">=")[0]
                import_name = PACKAGE_IMPORT_MAP.get(
                    package, package.replace("-", "_")
                )
                try:
                    __import__(import_name)
                    print(f"   ✅ {package} 已安裝")
                except ImportError:
                    print(f"   ❌ {package} 未安裝")
                    missing_packages.append(requirement)
    else:
        print("⚠️ 找不到 requirements.txt，略過套件檢查")

    if missing_packages:
        print("\n❗ 建議執行以下指令安裝缺少的套件：")
        print("   pip install -r requirements.txt")
        return False

    return True


def check_env_file() -> bool:
    print_section("2. .env 設定檢查")
    if not ENV_FILE.exists():
        print(f"❌ 找不到 {ENV_FILE.name}，請先建立 .env 檔案")
        return False

    load_dotenv(ENV_FILE)

    required_keys = ["YOUTUBE_API_KEY", "GEMINI_API_KEY", "EMAIL_TO"]
    optional_keys = [
        "SENDGRID_API_KEY",
        "EMAIL_FROM",
        "GMAIL_APP_PASSWORD",
        "GOOGLE_SHEET_ID",
        "TWITTER_BEARER_TOKEN",
        "LINKEDIN_ACCESS_TOKEN",
        "GEMINI_MODEL",
    ]

    all_ok = True
    for key in required_keys:
        value = os.getenv(key, "").strip()
        if not value or value.startswith("在此填入") or value.endswith("example.com"):
            print(f"❌ {key} 尚未正確填寫")
            all_ok = False
        else:
            print(f"✅ {key} 已設定")

    for key in optional_keys:
        value = os.getenv(key, "").strip()
        if value and not value.startswith("如使用"):
            print(f"ℹ️  {key} 已設定（可選）")

    return all_ok


def test_youtube_api() -> Tuple[bool, str]:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key.startswith("在此"):
        return False, "YouTube API key 尚未設定"

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": "ai project showcase",
        "type": "video",
        "maxResults": 1,
        "key": api_key,
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        items = len(data.get("items", []))
        return True, f"成功呼叫 API，取得 {items} 筆測試結果"
    except requests.HTTPError as http_err:
        return False, f"HTTP 錯誤：{http_err.response.status_code} {http_err.response.text}"
    except Exception as err:
        return False, f"其他錯誤：{err}"


def test_gemini_api() -> Tuple[bool, str]:
    if genai is None or genai_types is None:
        return False, "尚未安裝 google-generativeai 套件"

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.startswith("在此"):
        return False, "Gemini API key 尚未設定"

    try:
        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=genai_types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=64,
                response_mime_type="text/plain",
            ),
        )
        response = model.generate_content(
            ["請用 4 個字回覆：設定完成"], request_options={"timeout": 15}
        )

        text_parts = []
        for candidate in response.candidates or []:
            if candidate.finish_reason and candidate.finish_reason == 3:
                return False, "Gemini 回覆因安全性被阻擋"
            for part in getattr(candidate.content, "parts", []) or []:
                if getattr(part, "text", None):
                    text_parts.append(part.text)

        text = " ".join(text_parts).strip()
        if not text:
            return False, "Gemini 回傳空白內容"
        return True, f"Gemini 回覆：{text}"
    except Exception as err:
        return False, f"Gemini API 錯誤：{err}"


def test_optional_integrations() -> bool:
    print_section("3. API Key 實測")
    youtube_ok, youtube_msg = test_youtube_api()
    print(("✅" if youtube_ok else "❌") + f" YouTube API：{youtube_msg}")

    gemini_ok, gemini_msg = test_gemini_api()
    print(("✅" if gemini_ok else "❌") + f" Gemini API：{gemini_msg}")

    email_to = os.getenv("EMAIL_TO", "")
    if email_to and "@" in email_to:
        print(f"ℹ️  Email digest 會寄送至：{email_to}")
    else:
        print("⚠️  EMAIL_TO 未設定或格式不正確，Email digest 只會儲存為 HTML。")

    return youtube_ok and gemini_ok


def suggest_next_steps(all_checks_ok: bool) -> None:
    print_section("4. 建議下一步")
    if all_checks_ok:
        print("🎉 所有必要設定完成！可以執行：python ai_examples_crawler.py")
    else:
        print("請依照上述錯誤訊息修正設定後，再重新執行此腳本。")
    print("\n額外建議：")
    print(" - 設定 SendGrid 或 Gmail SMTP 將每日 digest 寄出")
    print(" - 填寫 GOOGLE_SHEET_ID 搭配 google_sheets_integration.py 寫入試算表")
    print(" - 預留 Twitter / LinkedIn 權杖供未來擴充內容來源")


def main() -> None:
    python_ok = check_python_environment()
    env_ok = check_env_file()
    api_ok = test_optional_integrations() if env_ok else False

    all_ok = python_ok and env_ok and api_ok
    suggest_next_steps(all_ok)


if __name__ == "__main__":
    main()

