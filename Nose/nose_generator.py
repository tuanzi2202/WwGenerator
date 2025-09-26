import tkinter as tk
from tkinter import colorchooser, ttk
from PIL import Image, ImageDraw, ImageTk
import os
import random
from datetime import datetime

# =================== 鼻子绘制函数 ===================
def draw_circle(draw, center, size, fill_color, outline_color):
    x, y = center
    r = size // 2
    draw.ellipse((x-r, y-r, x+r, y+r), fill=fill_color, outline=outline_color)

def draw_triangle(draw, center, size, fill_color, outline_color):
    x, y = center
    half = size // 2
    draw.polygon([(x, y-half), (x-half, y+half), (x+half, y+half)], fill=fill_color, outline=outline_color)

def draw_square(draw, center, size, fill_color, outline_color):
    x, y = center
    half = size // 2
    draw.rectangle((x-half, y-half, x+half, y+half), fill=fill_color, outline=outline_color)

def draw_trapezoid(draw, center, size, fill_color, outline_color):
    x, y = center
    half = size // 2
    h = size // 2
    draw.polygon([(x-half, y+h), (x+half, y+h), (x+half//2, y-h), (x-half//2, y-h)], fill=fill_color, outline=outline_color)

NOSE_SHAPES = {"圆鼻": draw_circle, "三角鼻": draw_triangle, "方鼻": draw_square, "梯形鼻": draw_trapezoid}

# =================== 鼻孔绘制函数 ===================
def draw_hole(draw, center, size, shape="圆形", hole_color=(0,0,0)):
    x, y = center
    r = size // 2
    if shape == "圆形":
        draw.ellipse((x-r, y-r, x+r, y+r), fill=hole_color)
    elif shape == "方形":
        draw.rectangle((x-r, y-r, x+r, y+r), fill=hole_color)
    elif shape == "三角形":
        draw.polygon([(x, y-r), (x-r, y+r), (x+r, y+r)], fill=hole_color)

# =================== 核心生成 ===================
def generate_nose(
    shape="圆鼻",
    fill_color=(255,182,193),
    outline_color=(0,0,0),
    has_holes=True,
    hole_shape="圆形",
    hole_size=20,
    hole_offset=40,
    hole_vertical_offset=0,
    hole_color=(0,0,0)
):
    size = 300
    img = Image.new("RGBA", (size, size), (255,255,255,0))
    draw = ImageDraw.Draw(img)
    func = NOSE_SHAPES.get(shape, draw_circle)
    func(draw, (size//2, size//2), size//2, fill_color, outline_color)

    if has_holes:
        y = size//2 + hole_vertical_offset
        x = size//2
        draw_hole(draw, (x - hole_offset, y), hole_size, hole_shape, hole_color)
        draw_hole(draw, (x + hole_offset, y), hole_size, hole_shape, hole_color)
    return img

# =================== GUI ===================
class NoseGenerator:
    def __init__(self, root):
        self.root = root
        root.title("鼻子生成器（颜色+随机生成）")

        self.nose_fill_color = (255,182,193)
        self.nose_outline_color = (0,0,0)
        self.nose_hole_color = (0,0,0)

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        # ===== 自定义页面 =====
        self.frame_custom = tk.Frame(notebook)
        notebook.add(self.frame_custom, text="自定义鼻子")

        self.build_custom_page(self.frame_custom)

        # ===== 随机生成页面 =====
        self.frame_random = tk.Frame(notebook)
        notebook.add(self.frame_random, text="随机生成鼻子")

        self.build_random_page(self.frame_random)

    # ========== 自定义页面 ==========
    def build_custom_page(self, frame):
        ttk.Label(frame, text="鼻子形状").pack()
        self.combo_shape = ttk.Combobox(frame, values=list(NOSE_SHAPES.keys()), state="readonly")
        self.combo_shape.set("圆鼻")
        self.combo_shape.pack()

        tk.Button(frame, text="鼻子颜色", command=lambda:self.choose_color('fill')).pack()
        tk.Button(frame, text="轮廓颜色", command=lambda:self.choose_color('outline')).pack()
        tk.Button(frame, text="鼻孔颜色", command=lambda:self.choose_color('hole')).pack()

        self.hole_var = tk.IntVar(value=1)
        tk.Checkbutton(frame, text="显示鼻孔", variable=self.hole_var).pack()

        ttk.Label(frame, text="鼻孔形状").pack()
        self.combo_hole_shape = ttk.Combobox(frame, values=["圆形","方形","三角形"], state="readonly")
        self.combo_hole_shape.set("圆形")
        self.combo_hole_shape.pack()

        self.scale_hole_size = tk.Scale(frame, from_=5, to=50, orient="horizontal", label="鼻孔大小")
        self.scale_hole_size.set(15)
        self.scale_hole_size.pack()
        self.scale_hole_offset = tk.Scale(frame, from_=5, to=80, orient="horizontal", label="鼻孔间距")
        self.scale_hole_offset.set(25)
        self.scale_hole_offset.pack()
        self.scale_hole_vertical = tk.Scale(frame, from_=-50, to=50, orient="horizontal", label="鼻孔上下位置")
        self.scale_hole_vertical.set(0)
        self.scale_hole_vertical.pack()

        self.canvas_custom = tk.Canvas(frame, width=300, height=300, bg="white")
        self.canvas_custom.pack()
        tk.Button(frame, text="生成并保存", command=self.generate_and_save_custom).pack(pady=5)

        # 绑定事件更新
        self.combo_shape.bind("<<ComboboxSelected>>", lambda e:self.update_canvas_custom())
        self.combo_hole_shape.bind("<<ComboboxSelected>>", lambda e:self.update_canvas_custom())
        self.hole_var.trace("w", lambda *args:self.update_canvas_custom())
        self.scale_hole_size.config(command=lambda e:self.update_canvas_custom())
        self.scale_hole_offset.config(command=lambda e:self.update_canvas_custom())
        self.scale_hole_vertical.config(command=lambda e:self.update_canvas_custom())

        self.update_canvas_custom()

    # ========== 随机生成页面 ==========
    def build_random_page(self, frame):
        tk.Label(frame, text="生成数量").grid(row=0,column=0)
        self.random_num_var = tk.IntVar(value=5)
        tk.Spinbox(frame, from_=1, to=50, width=5, textvariable=self.random_num_var).grid(row=0,column=1)

        tk.Button(frame, text="生成随机鼻子", command=self.generate_random_noses).grid(row=0,column=2)
        tk.Button(frame, text="导出随机鼻子", command=self.save_random_noses).grid(row=0,column=3)

        self.canvas_random = tk.Canvas(frame, width=600, height=600, bg="white")
        self.canvas_random.grid(row=1,column=0,columnspan=4)

        self.random_imgs = []
        self.random_img_objs = []

    # ========== 共用功能 ==========
    def choose_color(self, target):
        c = colorchooser.askcolor()[0]
        if not c: return
        c = tuple(int(x) for x in c)
        if target == 'fill': self.nose_fill_color = c
        elif target == 'outline': self.nose_outline_color = c
        elif target == 'hole': self.nose_hole_color = c
        self.update_canvas_custom()

    # ========== 自定义页面功能 ==========
    def update_canvas_custom(self):
        img = generate_nose(
            shape=self.combo_shape.get(),
            fill_color=self.nose_fill_color,
            outline_color=self.nose_outline_color,
            has_holes=self.hole_var.get()==1,
            hole_shape=self.combo_hole_shape.get(),
            hole_size=int(self.scale_hole_size.get()),
            hole_offset=int(self.scale_hole_offset.get()),
            hole_vertical_offset=int(self.scale_hole_vertical.get()),
            hole_color=self.nose_hole_color
        )
        self.tk_img_custom = ImageTk.PhotoImage(img)
        self.canvas_custom.create_image(150,150,image=self.tk_img_custom)

    def generate_and_save_custom(self):
        img = generate_nose(
            shape=self.combo_shape.get(),
            fill_color=self.nose_fill_color,
            outline_color=self.nose_outline_color,
            has_holes=self.hole_var.get()==1,
            hole_shape=self.combo_hole_shape.get(),
            hole_size=int(self.scale_hole_size.get()),
            hole_offset=int(self.scale_hole_offset.get()),
            hole_vertical_offset=int(self.scale_hole_vertical.get()),
            hole_color=self.nose_hole_color
        )
        save_dir = os.path.join(os.getcwd(), "nose_images")
        os.makedirs(save_dir, exist_ok=True)
        idx = 1
        while os.path.exists(os.path.join(save_dir, f"nose_{idx}.png")):
            idx += 1
        filename = os.path.join(save_dir, f"nose_{idx}.png")
        img.save(filename)
        print(f"已保存: {filename}")

    # ========== 随机生成功能 ==========
    def generate_random_noses(self):
        num = self.random_num_var.get()
        self.random_imgs.clear()
        self.random_img_objs.clear()
        self.canvas_random.delete("all")

        cols = 3
        size = 200
        for idx in range(num):
            shape = random.choice(list(NOSE_SHAPES.keys()))
            fill_color = tuple(random.randint(150,255) for _ in range(3))
            outline_color = tuple(random.randint(0,50) for _ in range(3))
            hole_color = tuple(random.randint(0,50) for _ in range(3))
            hole_shape = random.choice(["圆形","方形","三角形"])
            has_holes = random.choice([True,False])
            hole_size = random.randint(5,50)
            hole_offset = random.randint(10,50)
            hole_vertical_offset = random.randint(-20,20)

            img = generate_nose(shape, fill_color, outline_color, has_holes, hole_shape,
                                hole_size, hole_offset, hole_vertical_offset, hole_color)
            imgtk = ImageTk.PhotoImage(img)
            x_offset = (idx % cols) * size
            y_offset = (idx // cols) * size
            self.canvas_random.create_image(x_offset, y_offset, anchor='nw', image=imgtk)
            self.random_imgs.append(imgtk)
            self.random_img_objs.append(img)

    def save_random_noses(self):
        if not self.random_img_objs:
            print("请先生成随机鼻子")
            return
        folder = os.path.join(os.getcwd(), "random_noses_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(folder, exist_ok=True)
        for idx, img in enumerate(self.random_img_objs, start=1):
            img.save(os.path.join(folder, f"nose_{idx}.png"))
        print(f"已保存 {len(self.random_img_objs)} 个随机鼻子到 {folder}")


# =================== 运行 ===================
if __name__=="__main__":
    root = tk.Tk()
    app = NoseGenerator(root)
    root.mainloop()
