import tkinter as tk
from tkinter import colorchooser, ttk
from PIL import Image, ImageDraw, ImageTk
import os
import random
from datetime import datetime

# =================== 脸型绘制函数 ===================
def draw_oval_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    outline_w = params.get('outline_width', 4)
    width_ratio = params.get('width_ratio', 1.3)  # 默认宽比高大 30%

    # 允许的最大水平半径
    max_half_width = size * 0.9  # 留一点边距
    half_width = min(size / width_ratio, max_half_width)  # 宽窄控制在合理范围

    # 垂直半径保持 size
    draw.ellipse((x - half_width, y - size, x + half_width, y + size),
                 fill=skin_color, outline=outline_color, width=outline_w)

def draw_round_face(draw, center, size, skin_color, outline_color, params):
    # 圆脸保持宽高相等
    draw.ellipse((center[0]-size, center[1]-size, center[0]+size, center[1]+size),
                 fill=skin_color, outline=outline_color, width=params.get('outline_width', 4))

def draw_square_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    outline_w = params.get('outline_width', 4)
    radius = params.get('chin_round', size//8)
    try:
        draw.rounded_rectangle((x-size, y-size, x+size, y+size), radius=radius,
                               fill=skin_color, outline=outline_color, width=outline_w)
    except Exception:
        draw.rectangle((x-size, y-size, x+size, y+size), fill=skin_color, outline=outline_color, width=outline_w)

def draw_triangle_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    outline_w = params.get('outline_width', 4)
    polygon = [(x, y-size), (x+size, y+size), (x-size, y+size)]
    draw.polygon(polygon, fill=skin_color, outline=outline_color)
    draw.line(polygon+[polygon[0]], fill=outline_color, width=outline_w)

def draw_inverted_triangle_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    outline_w = params.get('outline_width', 4)
    polygon = [(x-size, y-size), (x+size, y-size), (x, y+size)]
    draw.polygon(polygon, fill=skin_color, outline=outline_color)
    draw.line(polygon+[polygon[0]], fill=outline_color, width=outline_w)

def draw_diamond_face(draw, center, size, skin_color, outline_color, params):
    x, y = center
    outline_w = params.get('outline_width', 4)
    polygon = [(x, y-size), (x+size, y), (x, y+size), (x-size, y)]
    draw.polygon(polygon, fill=skin_color, outline=outline_color)
    draw.line(polygon+[polygon[0]], fill=outline_color, width=outline_w)

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
    eye_w = params.get('eye_w', size//6)
    eye_h = params.get('eye_h', size//12)
    eye_offset_x = params.get('eye_offset_x', size//3)
    eye_offset_y = params.get('eye_offset_y', -size//6)
    nose_w = params.get('nose_w', size//12)
    nose_h = params.get('nose_h', size//8)
    mouth_w = params.get('mouth_w', size//2)
    mouth_h = params.get('mouth_h', size//12)

    # 左眼
    draw.ellipse((x-eye_offset_x-eye_w, y+eye_offset_y-eye_h,
                  x-eye_offset_x+eye_w, y+eye_offset_y+eye_h),
                  fill=(255,255,255), outline=outline_color, width=2)
    # 右眼
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
                  size=150, params=None, with_features=False):
    if params is None:
        params = {}
    # 椭圆脸默认宽高比例
    if shape == '椭圆脸' and 'width_ratio' not in params:
        params['width_ratio'] = 1.3
    img = Image.new("RGBA", (size*2, size*2), (255,255,255,0))
    draw = ImageDraw.Draw(img)
    func = FACE_SHAPES.get(shape, draw_oval_face)
    func(draw, (size, size), size, skin_color, outline_color, params)
    if with_features:
        draw_features(draw, (size, size), size, outline_color, params)
    return img

# =================== GUI ===================
class FaceGenerator:
    def __init__(self, root):
        self.root = root
        root.title("脸型生成器")
        self.skin_color = (255,224,189)
        self.outline_color = (0,0,0)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.frame_custom = tk.Frame(self.notebook)
        self.frame_random = tk.Frame(self.notebook)

        self.notebook.add(self.frame_custom, text="自定义脸型")
        self.notebook.add(self.frame_random, text="随机生成脸型")

        self.build_custom_page(self.frame_custom)
        self.build_random_page(self.frame_random)
        self.notebook.select(self.frame_custom)

    # ========== 自定义页面 ==========
    def build_custom_page(self, frame):
        top_frame = tk.Frame(frame)
        top_frame.pack(side='top', fill='x', pady=5)
        ttk.Label(top_frame, text="脸型").pack(side='left')
        self.combo_shape = ttk.Combobox(top_frame, values=list(FACE_SHAPES.keys()), state="readonly", width=15)
        self.combo_shape.set("椭圆脸")
        self.combo_shape.pack(side='left', padx=5)
        tk.Button(top_frame, text="皮肤颜色", command=lambda:self.choose_color('skin')).pack(side='left', padx=5)
        tk.Button(top_frame, text="轮廓颜色", command=lambda:self.choose_color('outline')).pack(side='left', padx=5)

        self.features_var = tk.IntVar(value=0)
        tk.Checkbutton(frame, text="启用五官", variable=self.features_var,
                       command=self.toggle_features).pack()

        # 中间主区域，左画布，右滑块
        main_frame = tk.Frame(frame)
        main_frame.pack(fill='both', expand=True, pady=5)

        # 左侧画布
        self.canvas_custom = tk.Canvas(main_frame, width=300, height=300, bg="white")
        self.canvas_custom.pack(side='left', padx=10)

        # 右侧五官参数（加滚动条）
        feature_container = tk.Frame(main_frame)
        feature_container.pack(side='left', fill='y', padx=10)

        canvas_scroll = tk.Canvas(feature_container, width=200, height=300)
        scrollbar = ttk.Scrollbar(feature_container, orient="vertical", command=canvas_scroll.yview)
        self.feature_frame = tk.Frame(canvas_scroll)

        self.feature_frame.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        )
        canvas_scroll.create_window((0,0), window=self.feature_frame, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)

        canvas_scroll.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")

        # 创建滑块
        self.scale_eye_w = tk.Scale(self.feature_frame, from_=5, to=60, orient="horizontal", label="眼睛宽度")
        self.scale_eye_h = tk.Scale(self.feature_frame, from_=5, to=30, orient="horizontal", label="眼睛高度")
        self.scale_eye_offset = tk.Scale(self.feature_frame, from_=10, to=80, orient="horizontal", label="眼距")
        self.scale_nose_w = tk.Scale(self.feature_frame, from_=5, to=40, orient="horizontal", label="鼻子宽度")
        self.scale_nose_h = tk.Scale(self.feature_frame, from_=5, to=60, orient="horizontal", label="鼻子高度")
        self.scale_mouth_w = tk.Scale(self.feature_frame, from_=20, to=150, orient="horizontal", label="嘴巴宽度")
        self.scale_mouth_h = tk.Scale(self.feature_frame, from_=5, to=50, orient="horizontal", label="嘴巴弧度")

        for w in [self.scale_eye_w, self.scale_eye_h, self.scale_eye_offset,
                  self.scale_nose_w, self.scale_nose_h, self.scale_mouth_w, self.scale_mouth_h]:
            w.pack(fill='x', pady=2)
            w.bind("<B1-Motion>", lambda e:self.update_canvas_custom())
            w.bind("<ButtonRelease-1>", lambda e:self.update_canvas_custom())

        self.feature_frame.pack_forget()  # 初始隐藏

        tk.Button(frame, text="生成并保存", command=self.generate_and_save_custom).pack(pady=5)

        self.combo_shape.bind("<<ComboboxSelected>>", lambda e:self.update_canvas_custom())
        self.update_canvas_custom()

    def toggle_features(self):
        if self.features_var.get():
            self.feature_frame.pack()
        else:
            self.feature_frame.pack_forget()
        self.update_canvas_custom()

    # ========== 随机生成页面 ==========
    def build_random_page(self, frame):
        top_frame = tk.Frame(frame)
        top_frame.pack(side='top', fill='x', pady=5)
        tk.Label(top_frame, text="生成数量").pack(side='left')
        self.random_num_var = tk.IntVar(value=5)
        tk.Spinbox(top_frame, from_=1, to=50, width=5, textvariable=self.random_num_var).pack(side='left', padx=5)
        tk.Button(top_frame, text="生成随机脸型", command=self.generate_random_faces).pack(side='left', padx=5)
        tk.Button(top_frame, text="导出随机脸型", command=self.save_random_faces).pack(side='left', padx=5)

        self.canvas_random = tk.Canvas(frame, width=600, height=600, bg="white")
        self.canvas_random.pack()
        self.random_imgs = []
        self.random_img_objs = []

    # ========== 共用 ==========
    def choose_color(self, target):
        c = colorchooser.askcolor()[0]
        if not c: return
        c = tuple(int(x) for x in c)
        if target=='skin': self.skin_color = c
        else: self.outline_color = c
        self.update_canvas_custom()

    def get_params(self):
        return {
            'eye_w': int(self.scale_eye_w.get()),
            'eye_h': int(self.scale_eye_h.get()),
            'eye_offset_x': int(self.scale_eye_offset.get()),
            'nose_w': int(self.scale_nose_w.get()),
            'nose_h': int(self.scale_nose_h.get()),
            'mouth_w': int(self.scale_mouth_w.get()),
            'mouth_h': int(self.scale_mouth_h.get())
        }

    def update_canvas_custom(self):
        params = self.get_params() if self.features_var.get() else {}
        img = generate_face(shape=self.combo_shape.get(), skin_color=self.skin_color,
                            outline_color=self.outline_color, size=150,
                            params=params, with_features=self.features_var.get())
        self.tk_img_custom = ImageTk.PhotoImage(img)
        self.canvas_custom.delete("all")
        self.canvas_custom.create_image(150,150,image=self.tk_img_custom)

    def generate_and_save_custom(self):
        params = self.get_params() if self.features_var.get() else {}
        img = generate_face(shape=self.combo_shape.get(), skin_color=self.skin_color,
                            outline_color=self.outline_color, size=150,
                            params=params, with_features=self.features_var.get())
        save_dir = os.path.join(os.getcwd(), "face_images")
        os.makedirs(save_dir, exist_ok=True)
        idx = 1
        while os.path.exists(os.path.join(save_dir, f"face_{idx}.png")):
            idx += 1
        filename = os.path.join(save_dir, f"face_{idx}.png")
        img.save(filename)
        print(f"已保存: {filename}")

    # ========== 随机生成优化版 ==========
    def generate_random_faces(self):
        num = self.random_num_var.get()
        self.random_imgs.clear()
        self.random_img_objs.clear()
        self.canvas_random.delete("all")

        canvas_size = 600
        padding = 10
        max_face_size = 150
        cols = min(num, 5)  # 最多5列
        rows = (num + cols - 1) // cols
        face_size = min(max_face_size, (canvas_size - padding*(cols+1)) // cols)
        self.canvas_random.config(width=canvas_size, height=max(canvas_size, face_size*rows + padding*(rows+1)))

        for idx in range(num):
            shape = random.choice(list(FACE_SHAPES.keys()))
            skin_color = tuple(random.randint(180,255) for _ in range(3))
            outline_color = (0,0,0)
            params = {
                'eye_w': random.randint(face_size//12, face_size//6),
                'eye_h': random.randint(face_size//24, face_size//12),
                'eye_offset_x': random.randint(face_size//6, face_size//3),
                'nose_w': random.randint(face_size//24, face_size//12),
                'nose_h': random.randint(face_size//16, face_size//8),
                'mouth_w': random.randint(face_size//4, face_size//2),
                'mouth_h': random.randint(face_size//24, face_size//12)
            }
            # 椭圆脸随机宽高比
            if shape == '椭圆脸':
                params['width_ratio'] = random.uniform(1.2, 1.5)

            with_features = random.choice([True, False])
            img = generate_face(shape, skin_color, outline_color, face_size, params, with_features)
            imgtk = ImageTk.PhotoImage(img)

            col = idx % cols
            row = idx // cols
            x_offset = padding + col * (face_size + padding)
            y_offset = padding + row * (face_size + padding)
            self.canvas_random.create_image(x_offset, y_offset, anchor='nw', image=imgtk)

            self.random_imgs.append(imgtk)
            self.random_img_objs.append(img)

    def save_random_faces(self):
        if not self.random_img_objs:
            print("请先生成随机脸型")
            return
        folder = os.path.join(os.getcwd(), "random_faces_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(folder, exist_ok=True)
        for idx, img in enumerate(self.random_img_objs, start=1):
            img.save(os.path.join(folder, f"face_{idx}.png"))
        print(f"已保存 {len(self.random_img_objs)} 个随机脸型到 {folder}")

if __name__=="__main__":
    root = tk.Tk()
    app = FaceGenerator(root)
    root.mainloop()
