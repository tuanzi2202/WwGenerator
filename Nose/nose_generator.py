import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import os

# =================== 鼻子绘制函数 ===================
def draw_circle(draw, center, size, fill_color, outline_color):
    x, y = center
    r = size // 2
    draw.ellipse((x-r, y-r, x+r, y+r), fill=fill_color, outline=outline_color)

def draw_triangle(draw, center, size, fill_color, outline_color):
    x, y = center
    half = size // 2
    draw.polygon(
        [(x, y-half), (x-half, y+half), (x+half, y+half)],
        fill=fill_color, outline=outline_color
    )

def draw_square(draw, center, size, fill_color, outline_color):
    x, y = center
    half = size // 2
    draw.rectangle((x-half, y-half, x+half, y+half), fill=fill_color, outline=outline_color)

def draw_trapezoid(draw, center, size, fill_color, outline_color):
    x, y = center
    half = size // 2
    h = size // 2
    draw.polygon(
        [(x-half, y+h), (x+half, y+h), (x+half//2, y-h), (x-half//2, y-h)],
        fill=fill_color, outline=outline_color
    )

NOSE_SHAPES = {
    "圆鼻": draw_circle,
    "三角鼻": draw_triangle,
    "方鼻": draw_square,
    "梯形鼻": draw_trapezoid,
}

# =================== 鼻孔绘制函数 ===================
def draw_hole(draw, center, size, shape="圆形"):
    x, y = center
    r = size // 2
    if shape == "圆形":
        draw.ellipse((x-r, y-r, x+r, y+r), fill="black")
    elif shape == "方形":
        draw.rectangle((x-r, y-r, x+r, y+r), fill="black")
    elif shape == "三角形":
        draw.polygon([(x, y-r), (x-r, y+r), (x+r, y+r)], fill="black")
    elif shape == "八字点状":
        # 左右各两个小圆点形成八字
        offset_x = r
        offset_y = r
        draw.ellipse((x-offset_x-2, y-offset_y-2, x-offset_x+2, y-offset_y+2), fill="black")
        draw.ellipse((x+offset_x-2, y-offset_y-2, x+offset_x+2, y-offset_y+2), fill="black")
        draw.ellipse((x-offset_x-2, y+offset_y-2, x-offset_x+2, y+offset_y+2), fill="black")
        draw.ellipse((x+offset_x-2, y+offset_y-2, x+offset_x+2, y+offset_y+2), fill="black")

# =================== 核心生成 ===================
def generate_nose(
    shape="圆鼻",
    fill_color="lightpink",
    outline_color="black",
    has_holes=True,
    hole_shape="圆形",
    hole_size=20,
    hole_offset=40,
    hole_vertical_offset=0
):
    size = 300  # 固定鼻子大小
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 鼻子主体
    func = NOSE_SHAPES.get(shape, draw_circle)
    func(draw, (size // 2, size // 2), size // 2, fill_color, outline_color)

    # 鼻孔
    if has_holes:
        y = size // 2 + hole_vertical_offset
        x = size // 2
        draw_hole(draw, (x - hole_offset, y), hole_size, hole_shape)
        draw_hole(draw, (x + hole_offset, y), hole_size, hole_shape)

    return img

# =================== GUI ===================
def update_canvas(*args):
    shape = combo_shape.get()
    hole_size = int(scale_hole_size.get())
    hole_offset = int(scale_hole_offset.get())
    hole_vertical_offset = int(scale_hole_vertical.get())
    has_holes = hole_var.get() == 1
    hole_shape = combo_hole_shape.get()

    img = generate_nose(
        shape=shape,
        fill_color="lightpink",
        outline_color="black",
        has_holes=has_holes,
        hole_shape=hole_shape,
        hole_size=hole_size,
        hole_offset=hole_offset,
        hole_vertical_offset=hole_vertical_offset
    )
    tk_img = ImageTk.PhotoImage(img)
    canvas.img = tk_img
    canvas.create_image(150, 150, image=tk_img)
    return img

def generate_and_save():
    img = update_canvas()

    # 使用脚本所在目录作为基础路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(script_dir, "nose_images")
    os.makedirs(save_dir, exist_ok=True)

    # 自动递增文件名
    idx = 1
    while os.path.exists(os.path.join(save_dir, f"nose_{idx}.png")):
        idx += 1
    filename = os.path.join(save_dir, f"nose_{idx}.png")
    img.save(filename)
    print(f"已保存: {filename}")

# =================== 窗口 ===================
root = tk.Tk()
root.title("鼻子生成器（八字鼻孔 + 实时预览）")

frame = ttk.Frame(root, padding=10)
frame.pack()

# 鼻子形状
ttk.Label(frame, text="鼻子形状").pack()
combo_shape = ttk.Combobox(frame, values=list(NOSE_SHAPES.keys()), state="readonly")
combo_shape.set("圆鼻")
combo_shape.pack()
combo_shape.bind("<<ComboboxSelected>>", update_canvas)

# 鼻孔开关
hole_var = tk.IntVar(value=1)
chk_hole = ttk.Checkbutton(frame, text="显示鼻孔", variable=hole_var, command=update_canvas)
chk_hole.pack()

# 鼻孔形状
ttk.Label(frame, text="鼻孔形状").pack()
combo_hole_shape = ttk.Combobox(frame, values=["圆形", "方形", "三角形", "八字点状"], state="readonly")
combo_hole_shape.set("圆形")
combo_hole_shape.pack()
combo_hole_shape.bind("<<ComboboxSelected>>", update_canvas)

# 鼻孔参数
scale_hole_size = tk.Scale(frame, from_=5, to=50, orient="horizontal", label="鼻孔大小", command=update_canvas)
scale_hole_size.set(15)
scale_hole_size.pack()

scale_hole_offset = tk.Scale(frame, from_=5, to=80, orient="horizontal", label="鼻孔间距", command=update_canvas)
scale_hole_offset.set(25)
scale_hole_offset.pack()

scale_hole_vertical = tk.Scale(frame, from_=-50, to=50, orient="horizontal", label="鼻孔上下位置", command=update_canvas)
scale_hole_vertical.set(0)
scale_hole_vertical.pack()

# 保存按钮
btn_save = ttk.Button(frame, text="生成并保存", command=generate_and_save)
btn_save.pack(pady=5)

# 画布
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack()

update_canvas()
root.mainloop()
