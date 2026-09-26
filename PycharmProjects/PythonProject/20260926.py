import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import platform

# ================= 核心修复：中文字体配置 =================
system = platform.system()
if system == 'Windows':
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
elif system == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False


# ========================================================

# ============ 1. 纤锌矿结构 3D 可视化 ============
def plot_wurtzite(ax, a, c, title, A_color, B_color, A_label, B_label):
    ax.set_title(title, fontsize=14)

    # 六方晶胞的顶点（底面和顶面）
    hex_vertices = np.array([
        [0, 0, 0], [a, 0, 0], [a / 2, a * np.sqrt(3) / 2, 0],
        [-a / 2, a * np.sqrt(3) / 2, 0], [-a, 0, 0], [-a / 2, -a * np.sqrt(3) / 2, 0], [a / 2, -a * np.sqrt(3) / 2, 0]
    ])
    # 画底面和顶面的六边形
    ax.plot(hex_vertices[:, 0], hex_vertices[:, 1], hex_vertices[:, 2], 'k-', alpha=0.5)
    ax.plot(hex_vertices[:, 0], hex_vertices[:, 1], hex_vertices[:, 2] + c, 'k-', alpha=0.5)
    # 画垂直的棱
    for i in range(6):
        ax.plot([hex_vertices[i, 0], hex_vertices[i, 0]], [hex_vertices[i, 1], hex_vertices[i, 1]], [0, c], 'k--',
                alpha=0.3)

    # 原子位置 (u≈0.375, 即 3/8)
    u = 0.375
    # A 原子坐标 (2个)
    A_pos = np.array([[0, 0, 0], [a / 2, a * np.sqrt(3) / 6, c / 2]])
    # B 原子坐标 (2个)
    B_pos = np.array([[0, 0, u * c], [a / 2, a * np.sqrt(3) / 6, (0.5 + u) * c]])

    # 画原子（用点表示，设置大一点）
    ax.scatter(A_pos[:, 0], A_pos[:, 1], A_pos[:, 2], color=A_color, s=300, label=A_label, edgecolors='black')
    ax.scatter(B_pos[:, 0], B_pos[:, 1], B_pos[:, 2], color=B_color, s=200, label=B_label, edgecolors='black')

    ax.set_xlim([-a, a])
    ax.set_ylim([-a, a])
    ax.set_zlim([0, c * 1.2])
    ax.set_xlabel('X');
    ax.set_ylabel('Y');
    ax.set_zlabel('Z')
    ax.legend()


# ============ 2. 模拟 XRD 图谱 ============
def simulate_xrd(ax, a, c, title, color):
    # 铜靶 K_alpha 波长 (埃)
    lam = 1.5406
    # 常见纤锌矿衍射面 (h, k, l)
    hkls = [(1, 0, 0), (0, 0, 2), (1, 0, 1), (1, 0, 2), (1, 1, 0), (1, 0, 3), (1, 1, 2), (2, 0, 1), (0, 0, 4)]

    theta_list = []
    for h, k, l in hkls:
        # 六方晶系面间距公式
        d = 1 / np.sqrt((4 / 3) * ((h ** 2 + h * k + k ** 2) / a ** 2) + (l ** 2 / c ** 2))
        # 布拉格定律
        sin_theta = lam / (2 * d)
        if sin_theta <= 1:
            theta = np.degrees(np.arcsin(sin_theta))
            theta_list.append(2 * theta)  # 记录 2theta

    # 生成 X 轴 (2theta 范围)
    x = np.linspace(20, 80, 1000)
    y = np.zeros_like(x)

    # 用高斯峰叠加模拟 XRD
    for pos in theta_list:
        # 设定峰的宽度和高度（为了视觉效果，高度做相对处理）
        y += 100 * np.exp(-((x - pos) ** 2) / (2 * 0.2 ** 2))

    ax.plot(x, y, color=color, linewidth=2, label=title)
    # 标出主要峰位
    for pos in theta_list:
        ax.axvline(x=pos, color=color, linestyle='--', alpha=0.3)
        ax.text(pos, 105, f'{pos:.1f}°', color=color, fontsize=8, rotation=90)


# ============ 主程序 ============
# ============ 主程序 (优化版) ============
fig = plt.figure(figsize=(16, 10))

# 1. 画 ZnS 构型 (a=3.82, c=6.26)
ax1 = fig.add_subplot(221, projection='3d')
plot_wurtzite(ax1, a=3.82, c=6.26, title='ZnS 纤锌矿结构', A_color='gray', B_color='yellow', A_label='Zn', B_label='S')
# 调整一下 3D 视角，让六边形更直观
ax1.view_init(elev=20, azim=30)

# 2. 画 GaN 构型 (a=3.19, c=5.18)
ax2 = fig.add_subplot(222, projection='3d')
plot_wurtzite(ax2, a=3.19, c=5.18, title='GaN 纤锌矿结构', A_color='blue', B_color='green', A_label='Ga', B_label='N')
ax2.view_init(elev=20, azim=30)

# 3. 画 XRD 对比图
ax3 = fig.add_subplot(212)
simulate_xrd(ax3, a=3.82, c=6.26, title='ZnS (纤锌矿)', color='orange')
simulate_xrd(ax3, a=3.19, c=5.18, title='GaN (纤锌矿)', color='teal')
ax3.set_title('ZnS 与 GaN 的模拟 XRD 图谱对比 (Cu Kα)', fontsize=14)
ax3.set_xlabel('2θ (度)', fontsize=12)
ax3.set_ylabel('相对强度 (a.u.)', fontsize=12)
ax3.set_ylim(0, 120) # 【新增】设置 Y 轴上限，防止文字超出边界
ax3.legend()
ax3.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()