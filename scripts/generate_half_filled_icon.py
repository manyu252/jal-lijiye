import os
from PIL import Image, ImageDraw

def create_half_filled_water_glass_icon(output_path="assets/icon.png"):
    # 64x64 pixel art half-filled glass of water icon
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    glass_outline = (235, 245, 251, 240)    # Clean white/ice glass border
    water_color = (52, 152, 219, 255)       # Vibrant water blue
    water_surface = (174, 214, 241, 255)     # Light water reflection
    
    # Glass dimensions: Top rim (14, 10) to (50, 10), Bottom (20, 56) to (44, 56)
    # Glass height is from y=10 to y=56 (total height = 46px)
    # Half-filled level is at y=33 (middle of glass!)
    
    # 1. Fill bottom half with water (y=33 to y=56)
    # At y=33, left x=17, right x=47
    water_polygon = [(17, 33), (47, 33), (43, 55), (21, 55)]
    draw.polygon(water_polygon, fill=water_color)
    
    # Water surface ellipse / line at half level
    draw.ellipse([17, 30, 47, 36], fill=water_surface)
    
    # 2. Draw full glass outline (trapezoid)
    glass_outline_poly = [(14, 10), (50, 10), (44, 56), (20, 56)]
    draw.polygon(glass_outline_poly, fill=None, outline=glass_outline, width=3)
    
    # Top rim of glass
    draw.ellipse([14, 7, 50, 13], outline=glass_outline, width=2, fill=(255, 255, 255, 40))
    
    # Subtle vertical shine/reflection line down the left side
    draw.line([(18, 14), (22, 48)], fill=(255, 255, 255, 160), width=2)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Created half-filled glass icon at {output_path}")

if __name__ == "__main__":
    create_half_filled_water_glass_icon("assets/icon.png")
