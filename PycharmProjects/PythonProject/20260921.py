import matplotlib.pyplot as plt
import numpy as np
import platform

# 字体设置
system = platform.system()
if system == 'Windows':
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
elif system == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
axes = axes.flatten()

points_x, points_y = np.meshgrid(np.arange(0, 6), np.arange(0, 6))

planes = [
    (1, 0, 'red', '(100)面 (x = n)'),
    (2, 1, 'blue', '(210)面 (2x + y = n)'),
    (1, -2, 'green', r'(1\(\overline{2}\)0)面 (x - 2y = n)'),
    (-2, 1, 'purple', r'(\(\overline{2}\)10)面 (-2x + y = n)')
]

for idx, (h, k, color, title) in enumerate(planes):
    ax = axes[idx]
    ax.scatter(points_x, points_y, color='black', s=15)

    ax.arrow(0, 0, 5.5, 0, head_width=0.15, head_length=0.2, fc='black', ec='black')
    ax.arrow(0, 0, 0, 5.5, head_width=0.15, head_length=0.2, fc='black', ec='black')
    ax.text(5.6, -0.2, 'a', fontsize=14)
    ax.text(-0.3, 5.6, 'b', fontsize=14)

    if k != 0 and h != 0:
        y_vals = np.linspace(-1, 6, 100)
        for n in [1, 2, 3]:  # n=1,2,3
            x_vals = (n - k * y_vals) / h
            ax.plot(x_vals, y_vals, color=color, linewidth=1.5, alpha=0.7)
            # 寻找一个合适的点来标注释文字
            try:
                # 尝试与x=0.5或y=0.5的交点作为标签位置
                if abs(h) >= abs(k):
                    y_lbl = 0.5
                    x_lbl = (n - k * y_lbl) / h
                else:
                    x_lbl = 0.5
                    y_lbl = (n - h * x_lbl) / k
                if 0 <= x_lbl <= 6 and 0 <= y_lbl <= 6:
                    ax.text(x_lbl, y_lbl, f'n={n}', color=color, fontsize=10, rotation=np.degrees(np.arctan(-h / k)))
            except Exception:
                pass
    elif k == 0:
        for n in [1, 2, 3]:
            ax.axvline(x=n, color=color, linewidth=1.5, alpha=0.7)
            ax.text(n, 5.2, f'n={n}', color=color, fontsize=10, ha='center')

    ax.set_title(title, fontsize=14)
    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 6)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()