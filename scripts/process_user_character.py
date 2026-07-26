import os
from PIL import Image, ImageDraw, ImageOps

def process_character():
    input_path = "my_character.png"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        return

    orig_img = Image.open(input_path).convert("RGBA")
    width, height = orig_img.size

    # Remove white background if present (make white pixels transparent)
    datas = orig_img.getdata()
    new_data = []
    for item in datas:
        # If pixel is close to pure white (R, G, B > 240 and A > 200), make it transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    
    clean_img = Image.new("RGBA", orig_img.size)
    clean_img.putdata(new_data)

    # Crop tightly to non-transparent bounding box
    bbox = clean_img.getbbox()
    if bbox:
        char_crop = clean_img.crop(bbox)
    else:
        char_crop = clean_img

    # Target square size for overlay (e.g., 140x140)
    target_canvas_size = 140
    char_w, char_h = char_crop.size
    
    # Scale character preserving aspect ratio so height is ~110px
    scale_factor = 110.0 / char_h
    new_char_w = max(1, int(char_w * scale_factor))
    new_char_h = max(1, int(char_h * scale_factor))
    
    char_scaled = char_crop.resize((new_char_w, new_char_h), Image.Resampling.NEAREST)

    os.makedirs("assets", exist_ok=True)

    # Function to create pixel water glass overlay
    def draw_glass(draw_obj, glass_x, glass_y):
        # Pixel glass outline and water
        water_color = (52, 152, 219, 255)
        glass_border = (235, 245, 251, 240)
        highlight = (174, 214, 241, 255)
        
        # Outer glass
        draw_obj.polygon([
            (glass_x, glass_y), 
            (glass_x + 14, glass_y), 
            (glass_x + 12, glass_y + 18), 
            (glass_x + 2, glass_y + 18)
        ], fill=water_color, outline=glass_border, width=2)
        
        # Glass top rim highlight
        draw_obj.line([(glass_x + 1, glass_y), (glass_x + 13, glass_y)], fill=highlight, width=2)

    # Helper to paste character onto canvas
    def make_canvas():
        return Image.new("RGBA", (target_canvas_size, target_canvas_size), (0, 0, 0, 0))

    # -------------------------------------------------------------
    # 1. WALK.GIF (4 frames walking with subtle bounce & glass)
    # -------------------------------------------------------------
    walk_frames = []
    base_x = (target_canvas_size - new_char_w) // 2
    base_y = target_canvas_size - new_char_h - 10
    
    for i in range(4):
        canvas = make_canvas()
        y_bounce = -4 if (i % 2 == 1) else 0
        
        # Paste character
        canvas.paste(char_scaled, (base_x, base_y + y_bounce), char_scaled)
        
        # Draw water glass in right hand area
        draw = ImageDraw.Draw(canvas)
        glass_x = base_x + new_char_w - 6
        glass_y = base_y + y_bounce + int(new_char_h * 0.45)
        draw_glass(draw, glass_x, glass_y)
        
        walk_frames.append(canvas)

    walk_frames[0].save(
        "assets/walk.gif",
        save_all=True,
        append_images=walk_frames[1:],
        duration=180,
        loop=0,
        disposal=2
    )
    print("Generated assets/walk.gif")

    # -------------------------------------------------------------
    # 2. ASK.GIF (Standing holding glass, question mark / sparkles)
    # -------------------------------------------------------------
    ask_frames = []
    for i in range(4):
        canvas = make_canvas()
        y_bounce = -2 if (i % 2 == 1) else 0
        
        canvas.paste(char_scaled, (base_x, base_y + y_bounce), char_scaled)
        draw = ImageDraw.Draw(canvas)
        
        # Glass held up slightly higher
        glass_x = base_x + new_char_w - 4
        glass_y = base_y + y_bounce + int(new_char_h * 0.38)
        draw_glass(draw, glass_x, glass_y)
        
        # Animated Question Mark / Water Sparkle above head
        qm_y = 6 + (i % 2) * 3
        qm_x = target_canvas_size // 2 - 4
        
        # Yellow sparkle block
        draw.rectangle([qm_x, qm_y, qm_x + 8, qm_y + 3], fill=(241, 196, 15, 255))
        draw.rectangle([qm_x + 4, qm_y + 3, qm_x + 8, qm_y + 8], fill=(241, 196, 15, 255))
        draw.rectangle([qm_x + 4, qm_y + 11, qm_x + 8, qm_y + 14], fill=(241, 196, 15, 255))
        
        ask_frames.append(canvas)

    ask_frames[0].save(
        "assets/ask.gif",
        save_all=True,
        append_images=ask_frames[1:],
        duration=220,
        loop=0,
        disposal=2
    )
    print("Generated assets/ask.gif")

    # -------------------------------------------------------------
    # 3. HAPPY.GIF (Celebration jump with hearts & stars)
    # -------------------------------------------------------------
    happy_frames = []
    for i in range(4):
        canvas = make_canvas()
        jump_y = -12 if (i % 2 == 1) else 0
        
        canvas.paste(char_scaled, (base_x, base_y + jump_y), char_scaled)
        draw = ImageDraw.Draw(canvas)
        
        # Glass
        glass_x = base_x + new_char_w - 4
        glass_y = base_y + jump_y + int(new_char_h * 0.38)
        draw_glass(draw, glass_x, glass_y)
        
        # Floating hearts / stars
        star_y = 12 + jump_y
        draw.polygon([(16, star_y + 6), (22, star_y), (28, star_y + 6), (22, star_y + 12)], fill=(231, 76, 60, 255))
        draw.polygon([(target_canvas_size - 28, star_y + 6), (target_canvas_size - 22, star_y), (target_canvas_size - 16, star_y + 6), (target_canvas_size - 22, star_y + 12)], fill=(241, 196, 15, 255))
        
        happy_frames.append(canvas)

    happy_frames[0].save(
        "assets/happy.gif",
        save_all=True,
        append_images=happy_frames[1:],
        duration=180,
        loop=0,
        disposal=2
    )
    print("Generated assets/happy.gif")

    # -------------------------------------------------------------
    # 4. EXIT.GIF (Flipped left walking away)
    # -------------------------------------------------------------
    char_flipped = ImageOps.mirror(char_scaled)
    exit_frames = []
    for i in range(4):
        canvas = make_canvas()
        y_bounce = -4 if (i % 2 == 1) else 0
        
        canvas.paste(char_flipped, (base_x, base_y + y_bounce), char_flipped)
        draw = ImageDraw.Draw(canvas)
        
        # Glass in left hand (since flipped)
        glass_x = base_x - 10
        glass_y = base_y + y_bounce + int(new_char_h * 0.45)
        draw_glass(draw, glass_x, glass_y)
        
        exit_frames.append(canvas)

    exit_frames[0].save(
        "assets/exit.gif",
        save_all=True,
        append_images=exit_frames[1:],
        duration=180,
        loop=0,
        disposal=2
    )
    print("Generated assets/exit.gif")

    # 5. ICON.PNG (Icon of the character face)
    head_h = int(new_char_h * 0.4)
    head_crop = char_scaled.crop((0, 0, new_char_w, head_h))
    icon_canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    head_scaled = head_crop.resize((48, int(48 * (head_h / new_char_w))), Image.Resampling.NEAREST)
    icon_canvas.paste(head_scaled, ((64 - 48) // 2, (64 - head_scaled.height) // 2), head_scaled)
    icon_canvas.save("assets/icon.png")
    print("Generated assets/icon.png")

if __name__ == "__main__":
    process_character()
