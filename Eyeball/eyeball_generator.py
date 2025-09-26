import tkinter as tk
from tkinter import colorchooser, ttk
from PIL import Image, ImageDraw, ImageTk
import math
import random
import os
from datetime import datetime

# ===================== 眼珠生成函数 =====================
def generate_eyeball(size=128, iris_radius_ratio=0.45, pupil_radius_ratio=0.3,
                     iris_color=(0,128,255), sclera_color=(255,255,255),
                     pupil_color=(0,0,0), pupil_shape='circle',
                     iris_texture='radial', highlight=True):

    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    center = size//2

    # 1. 眼白
    draw.ellipse([(0,0),(size,size)], fill=sclera_color)

    # 2. 虹膜
    iris_r = int(iris_radius_ratio*size)
    draw.ellipse([center-iris_r, center-iris_r, center+iris_r, center+iris_r], fill=iris_color)

    # 虹膜纹理
    for i in range(iris_r):
        if iris_texture=='radial':
            c = tuple(min(255,int(iris_color[j]*(1-i/iris_r))) for j in range(3))
            draw.ellipse([center-i, center-i, center+i, center+i], outline=c)
        elif iris_texture=='spokes':
            for angle in range(0,360,10):
                x = int(center + i*math.cos(math.radians(angle)))
                y = int(center + i*math.sin(math.radians(angle)))
                draw.point((x,y), fill=iris_color)
        elif iris_texture=='wavy':
            offset = int(5 * math.sin(i/5))
            bbox = [center-i+offset, center-i, center+i+offset, center+i]
            color = tuple(min(255, int(iris_color[j]*(1-i/iris_r))) for j in range(3))
            draw.ellipse(bbox, outline=color)
        elif iris_texture=='rings':
            if i % 5 == 0:
                color = tuple(min(255, int(iris_color[j]*(1-i/iris_r))) for j in range(3))
                draw.ellipse([center-i, center-i, center+i, center+i], outline=color)

    # 3. 瞳孔
    pupil_r = int(pupil_radius_ratio*iris_r)
    if pupil_shape=='circle':
        draw.ellipse([center-pupil_r, center-pupil_r, center+pupil_r, center+pupil_r], fill=pupil_color)
    elif pupil_shape=='ellipse':
        draw.ellipse([center-pupil_r, center-pupil_r//2, center+pupil_r, center+pupil_r//2], fill=pupil_color)
    elif pupil_shape=='slit':
        draw.ellipse([center-pupil_r//4, center-pupil_r, center+pupil_r//4, center+pupil_r], fill=pupil_color)
    elif pupil_shape=='cat':
        draw.rectangle([center- pupil_r//6, center- pupil_r, center+ pupil_r//6, center+ pupil_r], fill=pupil_color)

    # 4. 高光
    if highlight:
        hl_r = int(pupil_r*0.4)
        draw.ellipse([center-pupil_r//2, center-pupil_r//2, center-pupil_r//2+hl_r, center-pupil_r//2+hl_r],
                     fill=(255,255,255,180))

    return img

# ===================== GUI =====================
class EyeballGenerator:
    def __init__(self, root):
        self.root = root
        root.title("眼珠生成器")

        # 通用参数
        self.size = 128
        self.iris_radius_ratio = tk.DoubleVar(value=0.45)
        self.pupil_radius_ratio = tk.DoubleVar(value=0.3)
        self.pupil_shape = tk.StringVar(value='circle')
        self.iris_texture = tk.StringVar(value='radial')
        self.highlight = tk.BooleanVar(value=True)
        self.iris_color = (0,128,255)
        self.sclera_color = (255,255,255)
        self.pupil_color = (0,0,0)

        # 创建分页
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        self.frame_custom = tk.Frame(notebook)
        self.frame_random = tk.Frame(notebook)
        notebook.add(self.frame_custom, text="自定义眼珠")
        notebook.add(self.frame_random, text="随机生成眼珠")

        # ========== 自定义页面 ==========
        self.canvas_custom = tk.Canvas(self.frame_custom, width=256, height=256)
        self.canvas_custom.grid(row=0, column=0, columnspan=4)

        tk.Label(self.frame_custom,text="虹膜比例").grid(row=1,column=0)
        tk.Scale(self.frame_custom, from_=0.1, to=0.9, resolution=0.01, orient=tk.HORIZONTAL,
                 variable=self.iris_radius_ratio, command=lambda e:self.update_custom()).grid(row=1,column=1)

        tk.Label(self.frame_custom,text="瞳孔比例").grid(row=2,column=0)
        tk.Scale(self.frame_custom, from_=0.05, to=0.7, resolution=0.01, orient=tk.HORIZONTAL,
                 variable=self.pupil_radius_ratio, command=lambda e:self.update_custom()).grid(row=2,column=1)

        tk.Label(self.frame_custom,text="瞳孔形状").grid(row=1,column=2)
        tk.OptionMenu(self.frame_custom, self.pupil_shape, 'circle','ellipse','slit','cat', command=lambda e:self.update_custom()).grid(row=1,column=3)

        tk.Label(self.frame_custom,text="虹膜纹理").grid(row=2,column=2)
        tk.OptionMenu(self.frame_custom, self.iris_texture, 'radial','spokes','wavy','rings', command=lambda e:self.update_custom()).grid(row=2,column=3)

        tk.Checkbutton(self.frame_custom,text="高光",variable=self.highlight, command=self.update_custom).grid(row=3,column=0)
        tk.Button(self.frame_custom,text="虹膜颜色",command=self.choose_iris_color).grid(row=3,column=1)
        tk.Button(self.frame_custom,text="巩膜颜色",command=self.choose_sclera_color).grid(row=3,column=2)
        tk.Button(self.frame_custom,text="瞳孔颜色",command=self.choose_pupil_color).grid(row=3,column=3)

        tk.Button(self.frame_custom, text="保存自定义眼珠PNG", command=self.save_png).grid(row=4,column=0,columnspan=4,sticky='we')

        self.update_custom()

        # ========== 随机生成页面 ==========
        self.canvas_random = tk.Canvas(self.frame_random, width=512, height=512)
        self.canvas_random.grid(row=0, column=0, columnspan=5)

        tk.Label(self.frame_random,text="随机生成数量").grid(row=1,column=0)
        self.num_var = tk.IntVar(value=1)
        tk.Spinbox(self.frame_random, from_=1, to=20, width=5, textvariable=self.num_var).grid(row=1,column=1)
        tk.Button(self.frame_random,text="生成随机眼珠", command=self.generate_random_eyes).grid(row=1,column=2,columnspan=2)
        tk.Button(self.frame_random,text="保存随机眼珠到文件夹", command=self.save_random_eyes_to_folder).grid(row=1,column=4)

    # ========== 自定义页面功能 ==========
    def update_custom(self):
        img = generate_eyeball(
            size=256,
            iris_radius_ratio=self.iris_radius_ratio.get(),
            pupil_radius_ratio=self.pupil_radius_ratio.get(),
            iris_color=self.iris_color,
            sclera_color=self.sclera_color,
            pupil_color=self.pupil_color,
            pupil_shape=self.pupil_shape.get(),
            iris_texture=self.iris_texture.get(),
            highlight=self.highlight.get()
        )
        self.imgtk_custom = ImageTk.PhotoImage(img)
        self.canvas_custom.create_image(0,0,anchor='nw',image=self.imgtk_custom)

    def choose_iris_color(self):
        c = colorchooser.askcolor()[0]
        if c: self.iris_color = tuple(int(x) for x in c); self.update_custom()

    def choose_sclera_color(self):
        c = colorchooser.askcolor()[0]
        if c: self.sclera_color = tuple(int(x) for x in c); self.update_custom()

    def choose_pupil_color(self):
        c = colorchooser.askcolor()[0]
        if c: self.pupil_color = tuple(int(x) for x in c); self.update_custom()

    def save_png(self):
        img = generate_eyeball(
            size=256,
            iris_radius_ratio=self.iris_radius_ratio.get(),
            pupil_radius_ratio=self.pupil_radius_ratio.get(),
            iris_color=self.iris_color,
            sclera_color=self.sclera_color,
            pupil_color=self.pupil_color,
            pupil_shape=self.pupil_shape.get(),
            iris_texture=self.iris_texture.get(),
            highlight=self.highlight.get()
        )
        img.save("eyeball_custom.png")
        print("已保存 eyeball_custom.png")

    # ========== 随机生成页面功能 ==========
    def generate_random_eyes(self):
        num = self.num_var.get()
        cols = int(512 / self.size)
        self.canvas_random.delete("all")
        self.random_imgs = []
        self.random_img_objs = []

        for idx in range(num):
            x_offset = (idx % cols) * self.size
            y_offset = (idx // cols) * self.size
            iris_color = tuple(random.randint(0,255) for _ in range(3))
            sclera_color = tuple(random.randint(200,255) for _ in range(3))
            pupil_color = tuple(random.randint(0,50) for _ in range(3))
            iris_texture = random.choice(['radial','spokes','wavy','rings'])
            pupil_shape = random.choice(['circle','ellipse','slit','cat'])
            img = generate_eyeball(
                size=self.size,
                iris_radius_ratio=random.uniform(0.3,0.6),
                pupil_radius_ratio=random.uniform(0.2,0.5),
                iris_color=iris_color,
                sclera_color=sclera_color,
                pupil_color=pupil_color,
                pupil_shape=pupil_shape,
                iris_texture=iris_texture,
                highlight=random.choice([True,False])
            )
            imgtk = ImageTk.PhotoImage(img)
            self.canvas_random.create_image(x_offset, y_offset, anchor='nw', image=imgtk)
            self.random_imgs.append(imgtk)
            self.random_img_objs.append(img)

    def save_random_eyes_to_folder(self):
        if not hasattr(self, 'random_img_objs') or not self.random_img_objs:
            print("没有随机眼珠可保存，请先生成。")
            return
        folder_name = datetime.now().strftime("random_eyes_%Y%m%d_%H%M%S")
        os.makedirs(folder_name, exist_ok=True)
        for idx, img in enumerate(self.random_img_objs, start=1):
            img.save(os.path.join(folder_name, f"eye_{idx}.png"))
        print(f"已保存 {len(self.random_img_objs)} 个随机眼珠到文件夹 {folder_name}")

# ===================== 运行 =====================
if __name__=="__main__":
    root = tk.Tk()
    app = EyeballGenerator(root)
    root.mainloop()
