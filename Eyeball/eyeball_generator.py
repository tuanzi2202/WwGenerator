import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageTk
import math
import random

# ===================== 眼珠生成函数 =====================
def generate_eyeball(size=256, iris_radius_ratio=0.45, pupil_radius_ratio=0.3,
                     iris_color=(0,128,255), sclera_color=(255,255,255),
                     pupil_color=(0,0,0), pupil_shape='circle',
                     iris_texture='radial', highlight=True):

    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    center = size//2
    eye_radius = size//2

    # 1. 眼白
    draw.ellipse([(0,0),(size,size)], fill=sclera_color)

    # 2. 虹膜
    iris_r = int(iris_radius_ratio*size)
    iris_bbox = [center-iris_r, center-iris_r, center+iris_r, center+iris_r]
    draw.ellipse(iris_bbox, fill=iris_color)

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
        bbox = [center-pupil_r, center-pupil_r, center+pupil_r, center+pupil_r]
        draw.ellipse(bbox, fill=pupil_color)
    elif pupil_shape=='ellipse':
        bbox = [center-pupil_r, center-pupil_r//2, center+pupil_r, center+pupil_r//2]
        draw.ellipse(bbox, fill=pupil_color)
    elif pupil_shape=='slit':
        bbox = [center-pupil_r//4, center-pupil_r, center+pupil_r//4, center+pupil_r]
        draw.ellipse(bbox, fill=pupil_color)
    elif pupil_shape=='cat':
        draw.rectangle([center- pupil_r//6, center- pupil_r, center+ pupil_r//6, center+ pupil_r], fill=pupil_color)

    # 4. 高光
    if highlight:
        hl_r = int(pupil_r*0.4)
        hl_bbox = [center-pupil_r//2, center-pupil_r//2, center-pupil_r//2+hl_r, center-pupil_r//2+hl_r]
        draw.ellipse(hl_bbox, fill=(255,255,255,180))

    return img

# ===================== GUI =====================
class EyeballGenerator:
    def __init__(self, root):
        self.root = root
        root.title("眼珠生成器")

        # 参数默认值
        self.size = 256
        self.iris_radius_ratio = tk.DoubleVar(value=0.45)
        self.pupil_radius_ratio = tk.DoubleVar(value=0.3)
        self.pupil_shape = tk.StringVar(value='circle')
        self.iris_texture = tk.StringVar(value='radial')
        self.highlight = tk.BooleanVar(value=True)
        self.iris_color = (0,128,255)
        self.sclera_color = (255,255,255)
        self.pupil_color = (0,0,0)

        # 画布
        self.canvas = tk.Canvas(root, width=self.size, height=self.size)
        self.canvas.grid(row=0, column=0, columnspan=4)

        # 控件
        tk.Label(root,text="虹膜比例").grid(row=1,column=0)
        tk.Scale(root, from_=0.1, to=0.9, resolution=0.01, orient=tk.HORIZONTAL, variable=self.iris_radius_ratio, command=lambda e:self.update()).grid(row=1,column=1)

        tk.Label(root,text="瞳孔比例").grid(row=2,column=0)
        tk.Scale(root, from_=0.05, to=0.7, resolution=0.01, orient=tk.HORIZONTAL, variable=self.pupil_radius_ratio, command=lambda e:self.update()).grid(row=2,column=1)

        tk.Label(root,text="瞳孔形状").grid(row=1,column=2)
        tk.OptionMenu(root, self.pupil_shape, 'circle','ellipse','slit','cat', command=lambda e:self.update()).grid(row=1,column=3)

        tk.Label(root,text="虹膜纹理").grid(row=2,column=2)
        tk.OptionMenu(root, self.iris_texture, 'radial','spokes','wavy','rings', command=lambda e:self.update()).grid(row=2,column=3)

        tk.Checkbutton(root,text="高光",variable=self.highlight, command=self.update).grid(row=3,column=0)

        tk.Button(root,text="虹膜颜色",command=self.choose_iris_color).grid(row=3,column=1)
        tk.Button(root,text="巩膜颜色",command=self.choose_sclera_color).grid(row=3,column=2)
        tk.Button(root,text="瞳孔颜色",command=self.choose_pupil_color).grid(row=3,column=3)

        tk.Button(root,text="保存PNG",command=self.save_png).grid(row=4,column=0,columnspan=4,sticky='we')

        self.update()

    def update(self):
        img = generate_eyeball(
            size=self.size,
            iris_radius_ratio=self.iris_radius_ratio.get(),
            pupil_radius_ratio=self.pupil_radius_ratio.get(),
            iris_color=self.iris_color,
            sclera_color=self.sclera_color,
            pupil_color=self.pupil_color,
            pupil_shape=self.pupil_shape.get(),
            iris_texture=self.iris_texture.get(),
            highlight=self.highlight.get()
        )
        self.imgtk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0,0,anchor='nw',image=self.imgtk)

    def choose_iris_color(self):
        c = colorchooser.askcolor()[0]
        if c: self.iris_color = tuple(int(x) for x in c); self.update()

    def choose_sclera_color(self):
        c = colorchooser.askcolor()[0]
        if c: self.sclera_color = tuple(int(x) for x in c); self.update()

    def choose_pupil_color(self):
        c = colorchooser.askcolor()[0]
        if c: self.pupil_color = tuple(int(x) for x in c); self.update()

    def save_png(self):
        img = generate_eyeball(
            size=self.size,
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

# ===================== 运行 =====================
if __name__=="__main__":
    root = tk.Tk()
    app = EyeballGenerator(root)
    root.mainloop()
