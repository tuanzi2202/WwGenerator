import tkinter as tk
from tkinter import colorchooser, ttk
from PIL import Image, ImageDraw, ImageTk
import os
import random
from datetime import datetime

# =================== 脸型绘制函数 ===================
def draw_oval_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    width_ratio = params.get('oval_ratio', 0.8)  # 椭圆长宽比例
    half_w = int(size * width_ratio / 2)
    half_h = size // 2
    outline_w = params.get('outline_width', 2)
    draw.ellipse((x-half_w, y-half_h, x+half_w, y+half_h), fill=skin_color, outline=outline_color, width=outline_w)

def draw_round_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    r = size // 2
    outline_w = params.get('outline_width', 2)
    draw.ellipse((x-r, y-r, x+r, y+r), fill=skin_color, outline=outline_color, width=outline_w)

def draw_square_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    half = size // 2
    radius = params.get('chin_round', 0)
    outline_w = params.get('outline_width', 2)
    draw.rounded_rectangle((x-half, y-half, x+half, y+half), radius=radius,
                           fill=skin_color, outline=outline_color, width=outline_w)

def draw_triangle_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    half = size // 2
    outline_w = params.get('outline_width', 2)
    polygon = [(x, y-half), (x+half, y+half), (x-half, y+half)]
    draw.polygon(polygon, fill=skin_color, outline=outline_color)
    draw.line(polygon + [polygon[0]], fill=outline_color, width=outline_w)

def draw_inverted_triangle_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    half = size // 2
    outline_w = params.get('outline_width', 2)
    polygon = [(x-half, y-half), (x+half, y-half), (x, y+half)]
    draw.polygon(polygon, fill=skin_color, outline=outline_color)
    draw.line(polygon + [polygon[0]], fill=outline_color, width=outline_w)

def draw_diamond_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    half = size // 2
    outline_w = params.get('outline_width', 2)
    polygon = [(x, y-half), (x+half, y), (x, y+half), (x-half, y)]
    draw.polygon(polygon, fill=skin_color, outline=outline_color)
    draw.line(polygon + [polygon[0]], fill=outline_color, width=outline_w)

FACE_SHAPES = {
    '椭圆脸': draw_oval_face,
    '圆脸': draw_round_face,
    '方脸': draw_square_face,
    '三角脸': draw_triangle_face,
    '倒三角脸': draw_inverted_triangle_face,
    '菱形脸': draw_diamond_face
}

# =================== 五官绘制函数 ===================
def draw_features(draw, center, size, outline_color, params):
    x, y = center
    eye_w = params.get('eye_w', size//8)
    eye_h = params.get('eye_h', size//12)
    eye_offset_x = params.get('eye_offset_x', size//4)
    eye_offset_y = params.get('eye_offset_y', -size//8)
    nose_w = params.get('nose_w', size//16)
    nose_h = params.get('nose_h', size//10)
    mouth_w = params.get('mouth_w', size//3)
    mouth_h = params.get('mouth_h', size//12)

    # 眼睛
    draw.ellipse((x-eye_offset_x-eye_w, y+eye_offset_y-eye_h,
                  x-eye_offset_x+eye_w, y+eye_offset_y+eye_h),
                  fill=(255,255,255), outline=outline_color, width=2)
    draw.ellipse((x+eye_offset_x-eye_w, y+eye_offset_y-eye_h,
                  x+eye_offset_x+eye_w, y+eye_offset_y+eye_h),
                  fill=(255,255,255), outline=outline_color, width=2)
    # 鼻子
    draw.polygon([(x, y), (x-nose_w, y+nose_h), (x+nose_w, y+nose_h)], fill=outline_color)
    # 嘴巴
    draw.arc((x-mouth_w, y+size//4, x+mouth_w, y+size//4+mouth_h),
             start=0, end=180, fill=outline_color, width=2)

# =================== 脸型生成函数 ===================
def generate_face(shape='椭圆脸', skin_color=(255,224,189), outline_color=(0,0,0),
                  size=300, params=None, with_features=False):
    if params is None:
        params = {}
    padding = 10
    img = Image.new("RGBA", (size, size), (255,255,255,0))
    draw = ImageDraw.Draw(img)
    func = FACE_SHAPES.get(shape, draw_oval_face)
    func(draw, (size//2, size//2), size-2*padding, skin_color, outline_color, params)
    if with_features:
        draw_features(draw, (size//2, size//2), size-2*padding, outline_color, params)
    return img

# =================== GUI ===================
class FaceGenerator:
    def __init__(self, root):
        self.root = root
        root.title("脸型生成器")
        self.skin_color = (255,224,189)
        self.outline_color = (0,0,0)

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        self.frame_custom = tk.Frame(notebook)
        notebook.add(self.frame_custom, text="自定义脸型")
        self.build_custom_page(self.frame_custom)

        self.frame_random = tk.Frame(notebook)
        notebook.add(self.frame_random, text="随机生成脸型")
        self.build_random_page(self.frame_random)

        notebook.select(self.frame_custom)  # 默认打开自定义页

    def build_custom_page(self, frame):
        control_frame = tk.Frame(frame)
        control_frame.pack(side='left', fill='y', padx=10, pady=10)
        canvas_frame = tk.Frame(frame)
        canvas_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        ttk.Label(control_frame, text="脸型").pack()
        self.combo_shape = ttk.Combobox(control_frame, values=list(FACE_SHAPES.keys()), state="readonly")
        self.combo_shape.set("椭圆脸")
        self.combo_shape.pack(pady=2)

        tk.Button(control_frame, text="皮肤颜色", command=lambda:self.choose_color('skin')).pack(pady=2)
        tk.Button(control_frame, text="轮廓颜色", command=lambda:self.choose_color('outline')).pack(pady=2)

        self.features_var = tk.IntVar(value=0)
        tk.Checkbutton(control_frame, text="启用五官", variable=self.features_var,
                       command=self.toggle_features).pack(pady=5)

        # 五官滑条
        self.scales_frame = tk.Frame(control_frame)
        self.scales_frame.pack()
        self.scales = {}
        for label, default, mn, mx in [
            ('眼睛宽度',20,5,50), ('眼睛高度',10,5,30), ('眼距',60,10,100),
            ('鼻子宽度',10,2,30), ('鼻子高度',20,10,80), ('嘴巴宽度',80,20,150), ('嘴巴弧度',10,5,50)
        ]:
            scale = tk.Scale(self.scales_frame, from_=mn, to=mx, orient='horizontal', label=label)
            scale.set(default)
            scale.pack(pady=2)
            scale.bind("<Motion>", lambda e: self.update_canvas_custom())
            scale.bind("<ButtonRelease-1>", lambda e: self.update_canvas_custom())
            self.scales[label] = scale

        self.scales_frame.pack_forget()  # 默认隐藏

        tk.Button(control_frame, text="生成并保存", command=self.generate_and_save_custom).pack(pady=5)

        self.canvas_custom = tk.Canvas(canvas_frame, width=340, height=340, bg="white")
        self.canvas_custom.pack(expand=True)

        self.combo_shape.bind("<<ComboboxSelected>>", lambda e:self.update_canvas_custom())
        self.update_canvas_custom()

    def toggle_features(self):
        if self.features_var.get() == 1:
            self.scales_frame.pack()
        else:
            self.scales_frame.pack_forget()
        self.update_canvas_custom()

    def build_random_page(self, frame):
        tk.Label(frame, text="生成数量").grid(row=0,column=0)
        self.random_num_var = tk.IntVar(value=5)
        tk.Spinbox(frame, from_=1, to=50, width=5, textvariable=self.random_num_var).grid(row=0,column=1)
        tk.Button(frame, text="生成随机脸型", command=self.generate_random_faces).grid(row=0,column=2)
        tk.Button(frame, text="导出随机脸型", command=self.save_random_faces).grid(row=0,column=3)
        self.canvas_random = tk.Canvas(frame, width=600, height=600, bg="white")
        self.canvas_random.grid(row=1,column=0,columnspan=4)
        self.random_imgs = []
        self.random_img_objs = []

    def choose_color(self, target):
        c = colorchooser.askcolor()[0]
        if not c: return
        c = tuple(int(x) for x in c)
        if target=='skin': self.skin_color=c
        else: self.outline_color=c
        self.update_canvas_custom()

    def update_canvas_custom(self):
        params = {}
        if self.features_var.get()==1:
            params = {k:self.scales[k].get() for k in self.scales}
        img = generate_face(self.combo_shape.get(), self.skin_color, self.outline_color,
                            300, params, with_features=self.features_var.get()==1)
        self.tk_img_custom = ImageTk.PhotoImage(img)
        self.canvas_custom.delete("all")
        self.canvas_custom.create_image(170,170,image=self.tk_img_custom)

    def generate_and_save_custom(self):
        params = {k:self.scales[k].get() for k in self.scales} if self.features_var.get()==1 else {}
        img = generate_face(self.combo_shape.get(), self.skin_color, self.outline_color,
                            300, params, with_features=self.features_var.get()==1)
        save_dir = os.path.join(os.getcwd(),"face_images")
        os.makedirs(save_dir, exist_ok=True)
        idx=1
        while os.path.exists(os.path.join(save_dir,f"face_{idx}.png")):
            idx+=1
        filename=os.path.join(save_dir,f"face_{idx}.png")
        img.save(filename)
        print(f"已保存: {filename}")

    def generate_random_faces(self):
        num = self.random_num_var.get()
        self.random_imgs.clear()
        self.random_img_objs.clear()
        self.canvas_random.delete("all")
        cols=3
        size=200
        for idx in range(num):
            shape = random.choice(list(FACE_SHAPES.keys()))
            skin_color = tuple(random.randint(180,255) for _ in range(3))
            outline_color = (0,0,0)
            params = { 'eye_w':random.randint(10,40),'eye_h':random.randint(5,20),
                       'eye_offset_x':random.randint(20,80),'nose_w':random.randint(5,20),
                       'nose_h':random.randint(10,50),
                       'mouth_w':random.randint(40,120),'mouth_h':random.randint(10,40) }
            with_features=random.choice([True,False])
            img=generate_face(shape, skin_color, outline_color, size, params, with_features)
            imgtk=ImageTk.PhotoImage(img)
            x_offset=(idx%cols)*size
            y_offset=(idx//cols)*size
            self.canvas_random.create_image(x_offset,y_offset,anchor='nw',image=imgtk)
            self.random_imgs.append(imgtk)
            self.random_img_objs.append(img)

    def save_random_faces(self):
        if not self.random_img_objs:
            print("请先生成随机脸型")
            return
        folder=os.path.join(os.getcwd(),"random_faces_"+datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(folder, exist_ok=True)
        for idx,img in enumerate(self.random_img_objs,start=1):
            img.save(os.path.join(folder,f"face_{idx}.png"))
        print(f"已保存 {len(self.random_img_objs)} 个随机脸型到 {folder}")

if __name__=="__main__":
    root=tk.Tk()
    app=FaceGenerator(root)
    root.mainloop()
