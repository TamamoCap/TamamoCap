import matplotlib.pyplot as plt
import numpy as np
import platform

# ================= 核心修复：中文字体配置 =================
system = platform.system()
if system == 'Windows':
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
elif system == 'Darwin':  # macOS
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC']
else:  # Linux
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False
# ========================================================

fig = plt.figure(figsize=(14, 6))

# --- H2O 结构 (修正：C2轴设为z轴，分子位于xz平面) ---
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_title('H2O 分子结构及对称元素 (C2v)', fontsize=14)
O = [0, 0, 0]
H1 = [0.757, 0, 0.586]   # 放在xz平面
H2 = [-0.757, 0, 0.586]  # 放在xz平面
ax1.scatter(*O, color='red', s=200, label='O')
ax1.scatter(*H1, color='gray', s=100, label='H')
ax1.scatter(*H2, color='gray', s=100)
ax1.plot([O[0], H1[0]], [O[1], H1[1]], [O[2], H1[2]], color='black', linewidth=2)
ax1.plot([O[0], H2[0]], [O[1], H2[1]], [O[2], H2[2]], color='black', linewidth=2)

# 对称元素
ax1.plot([0, 0], [0, 0], [-1, 1], 'b--', linewidth=2, label='C2轴 (z轴)')
# σv(分子平面, y=0)
xx, zz = np.meshgrid([-1.5, 1.5], [-1, 1])
ax1.plot_surface(xx, np.zeros_like(xx), zz, alpha=0.2, color='green', label='σv (分子平面)')
# σv'(垂直平面, x=0)
yy, zz2 = np.meshgrid([-1, 1], [-1, 1])
ax1.plot_surface(np.zeros_like(yy), yy, zz2, alpha=0.2, color='orange', label='σv\' (垂直平面)')

ax1.set_xlim([-1.5, 1.5]); ax1.set_ylim([-1, 1]); ax1.set_zlim([-1, 1])
ax1.set_xlabel('X'); ax1.set_ylabel('Y'); ax1.set_zlabel('Z')
ax1.legend()

# --- NH3 结构 (修正：C3轴为z轴，用平面表示σv镜面) ---
ax2 = fig.add_subplot(122, projection='3d')
ax2.set_title('NH3 分子结构及对称元素 (C3v)', fontsize=14)
N = [0, 0, 0.3]
H1 = [0.94, 0, -0.1]
H2 = [-0.47, 0.81, -0.1]
H3 = [-0.47, -0.81, -0.1]
ax2.scatter(*N, color='blue', s=200, label='N')
ax2.scatter(*H1, color='gray', s=100, label='H')
ax2.scatter(*H2, color='gray', s=100)
ax2.scatter(*H3, color='gray', s=100)
for H in [H1, H2, H3]:
    ax2.plot([N[0], H[0]], [N[1], H[1]], [N[2], H[2]], color='black', linewidth=2)

# 对称元素
ax2.plot([0, 0], [0, 0], [-0.5, 1], 'b--', linewidth=2, label='C3轴 (z轴)')
# 画一个σv镜面（包含N和H1，即y=0平面）
xx2, zz3 = np.meshgrid([-1.5, 1.5], [-1, 1])
ax2.plot_surface(xx2, np.zeros_like(xx2), zz3, color='green', alpha=0.2, label='σv 镜面 (之一)')

ax2.set_xlim([-1.5, 1.5]); ax2.set_ylim([-1.5, 1.5]); ax2.set_zlim([-1, 1])
ax2.set_xlabel('X'); ax2.set_ylabel('Y'); ax2.set_zlabel('Z')
ax2.legend()

plt.tight_layout()
plt.show()