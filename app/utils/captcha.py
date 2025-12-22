import base64
import io
import random
from PIL import Image, ImageDraw, ImageFont


def generate_captcha(
    width=120, height=40, line_count=5, dot_count=30, font_size=28
):
    """
    Generate captcha image
    return: (base64_str, result_str)
    """
    # 1. Random numbers and operator
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(["+", "-", "*"])
    
    # Ensure positive result for subtraction
    if op == "-":
        if a < b:
            a, b = b, a
    
    expr = f"{a}{op}{b}=?"
    
    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    else:
        result = a * b

    # 2. Create image
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 3. Load font
    try:
        # Try common system fonts
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
            "arial.ttf",
            "Arial.ttf"
        ]
        font = None
        for path in font_paths:
            try:
                font = ImageFont.truetype(path, font_size)
                break
            except IOError:
                continue
        
        if font is None:
             font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # 4. Draw text
    # text_bbox is safer than text_size in newer Pillow
    try:
        bbox = draw.textbbox((0, 0), expr, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback for older Pillow
        text_w, text_h = draw.textsize(expr, font=font)
        
    text_x = (width - text_w) // 2
    text_y = (height - text_h) // 2
    
    draw.text((text_x, text_y), expr, font=font, fill=(0, 0, 0))

    # 5. Add interference lines
    for _ in range(line_count):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([start, end], fill=random_color(), width=1)

    # 6. Add interference dots
    for _ in range(dot_count):
        xy = (random.randint(0, width), random.randint(0, height))
        draw.point(xy, fill=random_color())

    # 7. Save to BytesIO
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    
    b64_str = base64.b64encode(img_bytes).decode("ascii")
    return b64_str, str(result)


def random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )

