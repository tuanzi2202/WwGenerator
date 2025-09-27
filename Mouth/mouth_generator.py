import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import random
import os
from datetime import datetime

# ===================== 嘴巴生成函数 =====================
def generate_mouth(size=128,
                   mouth_width_ratio=0.6,
                   mouth_height_ratio=0.2,
                   mouth_shape='line'):
    """
    生成简化嘴巴图像，仅保留轮廓分类
    mouth_shape: 'line', 'circle', 'half_ellipse'
    """
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    center_x, center_y = size // 2, size // 2

    mouth_w = int(size * mouth_width_ratio)
    mouth_h = int(size * mouth_height_ratio)

    if mouth_shape == 'line':
        draw.line([(center_x - mouth_w//2, center_y),
                   (center_x + mouth_w//2, center_y)],
                  fill=(0,0,0), width=2)
    elif mouth_shape == 'circle':
        draw.ellipse([center_x - mouth_w//2, center_y - mouth_w//2,
                      center_x + mouth_w//2, center_y + mouth_w//2],
                     outline=(0,0,0), width=2)
    elif mouth_shape == 'half_ellipse':
        draw.arc([center_x - mouth_w//2, center_y - mouth_h//2,
                  center_x + mouth_w//2, center_y + mouth_h//2],
                 start=0, end=180, fill=(0,0,0), width=2)
    else:
        raise ValueError("mouth_shape must be 'line', 'circle', or 'half_ellipse'")

    return img

# ===================== GUI =====================
class MouthGenerator:
    def __init__(self, root):
        self.root = root
        root.title("嘴巴生成器")

        self.size = 128
        self.mouth_width_ratio = tk.DoubleVar(value=0.6)
        self.mouth_height_ratio = tk.DoubleVar(value=0.2)
        self.mouth_shape = tk.StringVar(value='line')
        self.num_var = tk.IntVar(value=1)

        # 保存文件夹：绝对路径到当前项目目录
        self.save_folder = os.path.join(os.getcwd(), "mouths")
        os.makedirs(self.save_folder, exist_ok=True)

        # 创建分页
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        self.frame_custom = tk.Frame(notebook)
        self.frame_random = tk.Frame(notebook)
        notebook.add(self.frame_custom, text="自定义嘴巴")
        notebook.add(self.frame_random, text="随机生成嘴巴")

        # ========== 自定义页面 ==========
        self.canvas_custom = tk.Canvas(self.frame_custom, width=256, height=256)
        self.canvas_custom.grid(row=0, column=0, columnspan=3, pady=10)

        tk.Label(self.frame_custom,text="嘴巴宽度").grid(row=1,column=0)
        tk.Scale(self.frame_custom, from_=0.1, to=1.0, resolution=0.01, orient=tk.HORIZONTAL,
                 variable=self.mouth_width_ratio, command=lambda e:self.update_custom()).grid(row=1,column=1)
        tk.Label(self.frame_custom,text="嘴巴高度").grid(row=2,column=0)
        tk.Scale(self.frame_custom, from_=0.05, to=0.5, resolution=0.01, orient=tk.HORIZONTAL,
                 variable=self.mouth_height_ratio, command=lambda e:self.update_custom()).grid(row=2,column=1)
        tk.Label(self.frame_custom,text="嘴型").grid(row=1,column=2)
        tk.OptionMenu(self.frame_custom, self.mouth_shape, 'line','circle','half_ellipse', command=lambda e:self.update_custom()).grid(row=1,column=3)
        tk.Button(self.frame_custom, text="保存嘴巴PNG", command=self.save_png).grid(row=3,column=0,columnspan=3,sticky='we', pady=10)

        self.update_custom()

        # ========== 随机生成页面 ==========
        self.canvas_random = tk.Canvas(self.frame_random, width=512, height=512)
        self.canvas_random.grid(row=0, column=0, columnspan=5)

        tk.Label(self.frame_random,text="随机生成数量").grid(row=1,column=0)
        tk.Spinbox(self.frame_random, from_=1, to=20, width=5, textvariable=self.num_var).grid(row=1,column=1)
        tk.Button(self.frame_random,text="生成随机嘴巴", command=self.generate_random_mouths).grid(row=1,column=2,columnspan=2)
        tk.Button(self.frame_random,text="保存随机嘴巴到文件夹", command=self.save_random_mouths_to_folder).grid(row=1,column=4)

    # ========== 自定义页面功能 ==========
    def update_custom(self):
        img = generate_mouth(
            size=256,
            mouth_width_ratio=self.mouth_width_ratio.get(),
            mouth_height_ratio=self.mouth_height_ratio.get(),
            mouth_shape=self.mouth_shape.get()
        )
        self.imgtk_custom = ImageTk.PhotoImage(img)
        self.canvas_custom.create_image(0,0,anchor='nw',image=self.imgtk_custom)

    def save_png(self):
        img = generate_mouth(
            size=256,
            mouth_width_ratio=self.mouth_width_ratio.get(),
            mouth_height_ratio=self.mouth_height_ratio.get(),
            mouth_shape=self.mouth_shape.get()
        )
        filename = f"mouth_{self.mouth_shape.get()}_{datetime.now().strftime('%H%M%S')}.png"
        full_path = os.path.join(self.save_folder, filename)
        img.save(full_path)
        print(f"已保存 {full_path}")

    # ========== 随机生成页面功能 ==========
    def generate_random_mouths(self):
        num = self.num_var.get()
        cols = int(512 / self.size)
        self.canvas_random.delete("all")
        self.random_imgs = []
        self.random_img_objs = []

        for idx in range(num):
            x_offset = (idx % cols) * self.size
            y_offset = (idx // cols) * self.size
            mouth_width = random.uniform(0.2, 0.8)
            mouth_height = random.uniform(0.05, 0.4)
            mouth_shape = random.choice(['line','circle','half_ellipse'])
            img = generate_mouth(
                size=self.size,
                mouth_width_ratio=mouth_width,
                mouth_height_ratio=mouth_height,
                mouth_shape=mouth_shape
            )
            imgtk = ImageTk.PhotoImage(img)
            self.canvas_random.create_image(x_offset, y_offset, anchor='nw', image=imgtk)
            self.random_imgs.append(imgtk)
            self.random_img_objs.append(img)

    def save_random_mouths_to_folder(self):
        if not hasattr(self, 'random_img_objs') or not self.random_img_objs:
            print("没有随机嘴巴可保存，请先生成。")
            return
        timestamp_folder = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = os.path.join(self.save_folder, f"random_mouths_{timestamp_folder}")
        os.makedirs(folder_name, exist_ok=True)
        for idx, img in enumerate(self.random_img_objs, start=1):
            img.save(os.path.join(folder_name, f"mouth_{idx}.png"))
        print(f"已保存 {len(self.random_img_objs)} 个随机嘴巴到文件夹 {folder_name}")

# ===================== 运行 =====================
if __name__=="__main__":
    root = tk.Tk()
    app = MouthGenerator(root)
    root.mainloop()
