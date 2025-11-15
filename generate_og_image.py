"""
生成 Open Graph 預覽圖（PNG 格式）
LinkedIn 和其他社交平台不支持 SVG，需要 PNG/JPG
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_og_image():
    """創建 1200x630 的 PNG 預覽圖"""
    # 創建白色背景
    width, height = 1200, 630
    image = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(image)
    
    # 嘗試使用系統字體
    try:
        # macOS 系統字體
        title_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 80)
        subtitle_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 32)
    except:
        try:
            # 備選字體
            title_font = ImageFont.truetype('/System/Library/Fonts/SFProDisplay-Regular.otf', 80)
            subtitle_font = ImageFont.truetype('/System/Library/Fonts/SFProDisplay-Regular.otf', 32)
        except:
            # 如果都找不到，使用默認字體
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    
    # 計算文字位置（居中）
    title_text = "Vibe-Coding Examples Hub"
    subtitle_text = "See how others are using AI to build amazing things"
    
    # 獲取文字尺寸
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    
    # 繪製主標題（黑色）
    title_x = (width - title_width) // 2
    title_y = height // 2 - 60
    
    # 分開繪製 "Vibe-Coding"（黑色）和 "Examples Hub"（紫色）
    vibe_text = "Vibe-Coding "
    hub_text = "Examples Hub"
    
    vibe_bbox = draw.textbbox((0, 0), vibe_text, font=title_font)
    vibe_width = vibe_bbox[2] - vibe_bbox[0]
    
    draw.text((title_x, title_y), vibe_text, fill='#000000', font=title_font)
    draw.text((title_x + vibe_width, title_y), hub_text, fill='#667eea', font=title_font)
    
    # 繪製副標題（灰色）
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + title_height + 30
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill='#666666', font=subtitle_font)
    
    # 保存為 PNG
    output_path = os.path.join(os.path.dirname(__file__), 'static', 'og-image.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path, 'PNG', optimize=True)
    print(f"✅ 預覽圖已創建: {output_path}")
    return output_path

if __name__ == '__main__':
    create_og_image()

