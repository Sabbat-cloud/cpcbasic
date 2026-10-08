from PIL import Image

palette_rgb = [
    (0,0,0),       # 0 Black
    (0,0,128),     # 1 Blue
    (255,255,0),   # 2 Yellow
    (255,0,0),     # 3 Red
    (255,255,255), # 4 White
    (128,128,128), # 5 Grey
    (255,0,255),   # 6 Magenta
    (0,255,255),   # 7 Cyan
    (0,255,0),     # 8 Green
    (0,0,255),     # 9 Bright Blue
    (128,0,0),     # 10 Dark Red
    (0,128,0),     # 11 Dark Green
    (128,0,128),   # 12 Purple
    (128,128,0),   # 13 Olive
    (255,128,128), # 14 Pink
    (255,128,0),   # 15 Orange
]

def closest_color(r, g, b, a):
    if a < 128:
        return 0
    min_dist = 999999
    idx = 0
    for i, (cr, cg, cb) in enumerate(palette_rgb):
        dist = (r-cr)**2 + (g-cg)**2 + (b-cb)**2
        if dist < min_dist:
            min_dist = dist
            idx = i
    return idx

def convert(filename, varname):
    img = Image.open(filename).convert("RGBA")
    # Resize to exactly 8x8
    img = img.resize((8, 8), Image.NEAREST)
    out = []
    for y in range(8):
        row = []
        for x in range(8):
            r,g,b,a = img.getpixel((x,y))
            c = closest_color(r,g,b,a)
            row.append(str(c))
        out.append(",".join(row))
    
    print(f"'{varname}")
    for row in out:
        print(f"DATA {row}")

convert("D:/cpcbasic/OhMummy-master/Image/GargouRight.png", "PLAYER_RIGHT")
convert("D:/cpcbasic/OhMummy-master/Image/MummyRight.png", "MUMMY_RIGHT")
convert("D:/cpcbasic/OhMummy-master/Image/GargouLeft.png", "PLAYER_LEFT")
convert("D:/cpcbasic/OhMummy-master/Image/MummyLeft.png", "MUMMY_LEFT")
