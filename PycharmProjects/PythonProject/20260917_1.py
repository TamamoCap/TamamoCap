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
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题
# ========================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# --- C2v 极平面图 ---
# 修改1：将 \(C_{2v}\) 改为 $C_{2v}$
ax1.set_title(r'$C_{2v}$ 极平面图', fontsize=15)
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.axhline(0, color='black', linewidth=1)
ax1.axvline(0, color='black', linewidth=1)
ax1.add_patch(plt.Circle((0, 0), 1, color='black', fill=False, linewidth=2))
# 对称元素
ax1.plot(0, 0, 'ko', markersize=8) # C2轴
# 修改2：将 \(\sigma_v(xz)\) 改为 $\sigma_v(xz)$
ax1.plot([-1.2, 1.2], [0, 0], 'r--', label=r'$\sigma_v(xz)$') # 镜面
ax1.plot([0, 0], [-1.2, 1.2], 'b--', label=r"$\sigma_v'(yz)$") # 镜面
# 等效点 (设 x=0.5, y=0.5)
x, y = 0.5, 0.5
points = [(x, y), (-x, -y), (x, -y), (-x, y)]
for px, py in points:
    ax1.plot(px, py, 'mo')
    ax1.text(px+0.05, py+0.05, f"({px},{py})", fontsize=10)
ax1.legend()
ax1.set_aspect('equal')
ax1.grid(True, linestyle=':')

# --- C3h 极平面图 ---
# 修改3：将 \(C_{3h}\) 改为 $C_{3h}$
ax2.set_title(r'$C_{3h}$ 极平面图 (xy投影)', fontsize=15)
ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax2.axhline(0, color='black', linewidth=1)
ax2.axvline(0, color='black', linewidth=1)
ax2.add_patch(plt.Circle((0, 0), 1, color='black', fill=False, linewidth=2))
# 对称元素
ax2.plot(0, 0, 'ko', markersize=8) # C3轴
# 等效点 (设 x=0.5, y=0.5)
r = np.sqrt(0.5**2 + 0.5**2)
theta = np.arctan2(0.5, 0.5)
for i in range(3):
    angle = theta + i * 2*np.pi/3
    px, py = r*np.cos(angle), r*np.sin(angle)
    ax2.plot(px, py, 'mo')
    ax2.text(px+0.05, py+0.05, f"({px:.2f},{py:.2f})", fontsize=10)
    # 显示对应下方的点（z变-z）
    ax2.plot(px, py, 'co', markerfacecolor='none') # 空心圆代表下方点
ax2.set_aspect('equal')
ax2.grid(True, linestyle=':')

plt.tight_layout()
plt.show()