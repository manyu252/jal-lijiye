from pathlib import Path
from PIL import Image, ImageDraw

def ensure_assets_dir():
    Path("assets").mkdir(exist_ok=True)

def create_water_icon():
    # 64x64 pixel art half-filled glass of water icon
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    glass_outline = (235, 245, 251, 240)
    water_color = (52, 152, 219, 255)
    water_surface = (174, 214, 241, 255)
    
    water_polygon = [(17, 33), (47, 33), (43, 55), (21, 55)]
    draw.polygon(water_polygon, fill=water_color)
    draw.ellipse([17, 30, 47, 36], fill=water_surface)
    
    glass_outline_poly = [(14, 10), (50, 10), (44, 56), (20, 56)]
    draw.polygon(glass_outline_poly, fill=None, outline=glass_outline, width=3)
    draw.ellipse([14, 7, 50, 13], outline=glass_outline, width=2, fill=(255, 255, 255, 40))
    draw.line([(18, 14), (22, 48)], fill=(255, 255, 255, 160), width=2)
    
    img.save("assets/icon.png")
    img.save("assets/icon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("Created assets/icon.png and assets/icon.ico (half-filled glass)")

def create_pixel_character_frame(frame_type, frame_idx):
    # 96x96 transparent canvas for high-DPI scaling
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Base character colors (Cute Cyan Water Buddy)
    body_color = (41, 128, 185, 255)       # Deep blue
    face_color = (133, 193, 233, 255)      # Light blue
    eye_color = (44, 62, 80, 255)          # Dark navy
    glass_color = (235, 245, 251, 240)    # Glass
    water_fill = (52, 152, 219, 255)       # Water inside glass
    cheek_color = (241, 148, 138, 255)     # Cute pink cheeks
    
    # Animation offsets based on frame_idx
    y_bounce = (frame_idx % 2) * 4
    leg_offset = (frame_idx % 2) * 6
    
    if frame_type == "walk":
        # Body blob
        draw.rounded_rectangle([28, 28 + y_bounce, 68, 68 + y_bounce], radius=16, fill=body_color, outline=(255, 255, 255, 200), width=2)
        draw.rounded_rectangle([34, 34 + y_bounce, 62, 58 + y_bounce], radius=10, fill=face_color)
        
        # Eyes
        draw.rectangle([40, 42 + y_bounce, 44, 48 + y_bounce], fill=eye_color)
        draw.rectangle([52, 42 + y_bounce, 56, 48 + y_bounce], fill=eye_color)
        draw.rectangle([38, 48 + y_bounce, 41, 51 + y_bounce], fill=cheek_color)
        draw.rectangle([55, 48 + y_bounce, 58, 51 + y_bounce], fill=cheek_color)
        
        # Legs walking
        draw.rectangle([34 - leg_offset, 68 + y_bounce, 42 - leg_offset, 80], fill=body_color)
        draw.rectangle([54 + leg_offset, 68 + y_bounce, 62 + leg_offset, 80], fill=body_color)
        
        # Holding water glass on right arm
        draw.rectangle([66, 46 + y_bounce, 78, 64 + y_bounce], fill=water_fill, outline=glass_color, width=2)
        
    elif frame_type == "exit":
        # Walking away (facing left) with glass
        draw.rounded_rectangle([28, 28 + y_bounce, 68, 68 + y_bounce], radius=16, fill=body_color, outline=(255, 255, 255, 200), width=2)
        draw.rounded_rectangle([34, 34 + y_bounce, 62, 58 + y_bounce], radius=10, fill=face_color)
        
        # Eyes looking left
        draw.rectangle([36, 42 + y_bounce, 40, 48 + y_bounce], fill=eye_color)
        draw.rectangle([48, 42 + y_bounce, 52, 48 + y_bounce], fill=eye_color)
        
        # Legs walking left
        draw.rectangle([34 + leg_offset, 68 + y_bounce, 42 + leg_offset, 80], fill=body_color)
        draw.rectangle([54 - leg_offset, 68 + y_bounce, 62 - leg_offset, 80], fill=body_color)
        
        # Waving goodbye arm
        draw.rectangle([16, 36 + y_bounce, 26, 46 + y_bounce], fill=water_fill, outline=glass_color, width=2)

    return img

def generate_gif(frame_type, filename):
    frames = [create_pixel_character_frame(frame_type, i) for i in range(4)]
    # Save as animated GIF with transparency
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=200,
        loop=0,
        disposal=2
    )
    print(f"Created {filename}")

if __name__ == "__main__":
    ensure_assets_dir()
    create_water_icon()
    generate_gif("walk", "assets/walk.gif")
    generate_gif("exit", "assets/exit.gif")
    print("All default assets generated successfully!")
