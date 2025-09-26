import tkinter as tk
import random
import math

root = tk.Tk()
root.title("动画小人生成器")
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# =================== 小人参数 ===================
class Character:
    def __init__(self):
        self.reset()

    def reset(self):
        # 头部
        self.head_width = random.randint(50, 80)
        self.head_height = random.randint(60, 90)
        self.head_x = 200
        self.head_y = 100
        # 眼睛
        self.eye_spacing = random.randint(20, 35)
        self.eye_size = random.randint(5, 12)
        # 鼻子
        self.nose_width = 8
        self.nose_height = 10
        # 嘴巴
        self.mouth_width = random.randint(20, 40)
        # 身体
        self.body_width = random.randint(40, 60)
        self.body_height = random.randint(60, 100)
        # 四肢
        self.arm_length = random.randint(30, 50)
        self.leg_length = random.randint(40, 60)
        # 颜色
        self.body_color = random.choice(["blue","green","purple","orange"])
        # 运动偏移量
        self.offsets = {"head":0, "arm":0, "leg":0}

    def update_offsets(self):
        # 头部微动
        self.offsets["head"] = random.randint(-3,3)
        # 手臂轻微摆动
        self.offsets["arm"] = random.randint(-5,5)
        # 腿微动
        self.offsets["leg"] = random.randint(-3,3)

# 创建小人对象
char = Character()

# =================== 绘制小人 ===================
def draw_character():
    canvas.delete("all")
    char.update_offsets()
    off_h = char.offsets["head"]
    off_a = char.offsets["arm"]
    off_l = char.offsets["leg"]

    hx = char.head_x + off_h
    hy = char.head_y + off_h
    hw = char.head_width
    hh = char.head_height

    # 头部
    canvas.create_oval(hx - hw//2, hy - hh//2,
                       hx + hw//2, hy + hh//2,
                       fill="#f5c1a0", outline="black")

    # 眼睛
    eye_y = hy - hh//8
    # 左眼
    canvas.create_oval(hx - char.eye_spacing - char.eye_size + off_h, eye_y - char.eye_size,
                       hx - char.eye_spacing + char.eye_size + off_h, eye_y + char.eye_size,
                       fill="white", outline="black")
    # 右眼
    canvas.create_oval(hx + char.eye_spacing - char.eye_size + off_h, eye_y - char.eye_size,
                       hx + char.eye_spacing + char.eye_size + off_h, eye_y + char.eye_size,
                       fill="white", outline="black")
    # 瞳孔
    pupil_size = char.eye_size // 2
    canvas.create_oval(hx - char.eye_spacing - pupil_size + off_h, eye_y - pupil_size,
                       hx - char.eye_spacing + pupil_size + off_h, eye_y + pupil_size,
                       fill="black")
    canvas.create_oval(hx + char.eye_spacing - pupil_size + off_h, eye_y - pupil_size,
                       hx + char.eye_spacing + pupil_size + off_h, eye_y + pupil_size,
                       fill="black")

    # 鼻子
    nose_y = hy
    canvas.create_polygon(hx, nose_y - char.nose_height//2,
                          hx - char.nose_width//2, nose_y + char.nose_height//2,
                          hx + char.nose_width//2, nose_y + char.nose_height//2,
                          fill="#f5a07a", outline="black")

    # 嘴巴
    mouth_y = hy + hh//4
    canvas.create_line(hx - char.mouth_width//2, mouth_y,
                       hx + char.mouth_width//2, mouth_y,
                       fill="red", width=2, smooth=True)

    # 身体
    body_top = hy + hh//2
    canvas.create_rectangle(hx - char.body_width//2, body_top,
                            hx + char.body_width//2, body_top + char.body_height,
                            fill=char.body_color, outline="black")

    # 手臂
    canvas.create_line(hx - char.body_width//2, body_top + 20,
                       hx - char.body_width//2 - char.arm_length + off_a, body_top + 20 + random.randint(-10,10),
                       width=3)
    canvas.create_line(hx + char.body_width//2, body_top + 20,
                       hx + char.body_width//2 + char.arm_length + off_a, body_top + 20 + random.randint(-10,10),
                       width=3)

    # 腿
    canvas.create_line(hx - char.body_width//4, body_top + char.body_height,
                       hx - char.body_width//4 + off_l, body_top + char.body_height + char.leg_length,
                       width=3)
    canvas.create_line(hx + char.body_width//4, body_top + char.body_height,
                       hx + char.body_width//4 + off_l, body_top + char.body_height + char.leg_length,
                       width=3)

# =================== 动画循环 ===================
def animate():
    draw_character()
    root.after(200, animate)  # 每200ms刷新一次，控制动画速度

# =================== 重新生成小人 ===================
def regenerate():
    char.reset()

# 按钮
tk.Button(root, text="重新生成小人", command=regenerate).pack()

# 启动动画
animate()
root.mainloop()
