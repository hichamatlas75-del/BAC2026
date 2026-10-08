from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_bac_icon(size):
    # Create image with RGBA
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Rounded rectangle background
    corner_radius = int(size * 0.22)
    
    # Background gradient approximation using multiple rounded rectangles or vertical steps
    for y in range(size):
        ratio = y / size
        # Navy blue to royal indigo gradient
        r = int(16 + ratio * (37 - 16))
        g = int(24 + ratio * (99 - 24))
        b = int(40 + ratio * (235 - 40))
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
        
    # Create mask for rounded corners
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=corner_radius, fill=255)
    
    # Apply mask to background
    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    base.paste(img, (0, 0), mask)
    img = base
    draw = ImageDraw.Draw(img)

    # Subtle inner border
    draw.rounded_rectangle([(2, 2), (size - 3, size - 3)], radius=corner_radius - 2, outline=(255, 255, 255, 45), width=int(max(1, size * 0.015)))

    # Subtle Moroccan star polygon or accent ring in background
    cx, cy = size // 2, int(size * 0.44)
    star_radius = int(size * 0.28)
    
    # Draw soft glowing circle behind icon
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([cx - star_radius, cy - star_radius, cx + star_radius, cy + star_radius], fill=(255, 255, 255, 25))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # Draw Graduation Cap (Mortarboard)
    # Diamond top of mortarboard
    w = int(size * 0.32)
    h = int(size * 0.16)
    diamond = [
        (cx, cy - h),            # Top
        (cx + w, cy),            # Right
        (cx, cy + h),            # Bottom
        (cx - w, cy)             # Left
    ]
    # Draw shadow
    shadow_diamond = [(x, y + int(size * 0.02)) for x, y in diamond]
    draw.polygon(shadow_diamond, fill=(10, 15, 30, 160))
    # Draw top cap surface (Gold/Amber or Pure Crisp White with subtle shading)
    draw.polygon(diamond, fill=(255, 255, 255, 255))
    
    # Lower skull cap / headband
    skull_w = int(w * 0.58)
    skull_top_y = cy + int(h * 0.5)
    skull_bot_y = cy + int(h * 1.35)
    skull_poly = [
        (cx - skull_w, skull_top_y),
        (cx + skull_w, skull_top_y),
        (cx + skull_w, skull_bot_y),
        (cx, skull_bot_y + int(size * 0.04)),
        (cx - skull_w, skull_bot_y)
    ]
    draw.polygon(skull_poly, fill=(230, 235, 248, 255))
    
    # Tassel button
    btn_r = int(size * 0.025)
    draw.ellipse([cx - btn_r, cy - btn_r, cx + btn_r, cy + btn_r], fill=(245, 158, 11, 255)) # Golden button
    
    # Tassel string and ribbon
    tassel_pts = [
        (cx, cy),
        (cx + int(w * 0.75), cy + int(h * 0.3)),
        (cx + int(w * 0.9), cy + int(h * 1.2))
    ]
    for i in range(len(tassel_pts)-1):
        draw.line([tassel_pts[i], tassel_pts[i+1]], fill=(245, 158, 11, 255), width=int(max(2, size * 0.02)))
        
    # Tassel brush
    brush_x = tassel_pts[-1][0]
    brush_y = tassel_pts[-1][1]
    brush_w = int(size * 0.035)
    brush_h = int(size * 0.07)
    draw.polygon([
        (brush_x - brush_w//2, brush_y),
        (brush_x + brush_w//2, brush_y),
        (brush_x + brush_w, brush_y + brush_h),
        (brush_x - brush_w, brush_y + brush_h)
    ], fill=(245, 158, 11, 255))

    # Text Banner: "2BAC 2026"
    # Small badge pill at bottom
    pill_w = int(size * 0.75)
    pill_h = int(size * 0.22)
    pill_x0 = (size - pill_w) // 2
    pill_y0 = int(size * 0.70)
    pill_radius = pill_h // 2
    
    # Pill shadow
    draw.rounded_rectangle([pill_x0, pill_y0 + int(size*0.015), pill_x0 + pill_w, pill_y0 + pill_h + int(size*0.015)],
                           radius=pill_radius, fill=(5, 10, 20, 140))
    # Pill body (Emerald green accent or vibrant blue)
    draw.rounded_rectangle([pill_x0, pill_y0, pill_x0 + pill_w, pill_y0 + pill_h],
                           radius=pill_radius, fill=(16, 185, 129, 255), outline=(255, 255, 255, 180), width=int(max(1, size*0.01)))

    # Try loading a system font or default font
    font = None
    try:
        # Try Windows standard Segoe UI or Arial Bold
        font_path = "C:/Windows/Fonts/segoeuib.ttf"
        if not os.path.exists(font_path):
            font_path = "C:/Windows/Fonts/arialbd.ttf"
        font = ImageFont.truetype(font_path, int(pill_h * 0.55))
    except Exception:
        font = ImageFont.load_default()

    label = "2BAC 2026"
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) // 2
    ty = pill_y0 + (pill_h - th) // 2 - int(bbox[1])
    draw.text((tx, ty), label, fill=(255, 255, 255, 255), font=font)

    return img

cwd = os.getcwd()
icon_512 = create_bac_icon(512)
icon_512.save(os.path.join(cwd, "icon-512.png"), "PNG")

icon_192 = create_bac_icon(192)
icon_192.save(os.path.join(cwd, "icon-192.png"), "PNG")

icon_apple = create_bac_icon(180)
icon_apple.save(os.path.join(cwd, "apple-touch-icon.png"), "PNG")

favicon = create_bac_icon(64)
favicon.save(os.path.join(cwd, "favicon.png"), "PNG")
favicon.save(os.path.join(cwd, "favicon.ico"), format="ICO")

print("All icons generated successfully!")
