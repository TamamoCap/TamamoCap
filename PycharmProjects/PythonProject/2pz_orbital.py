import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import matplotlib as mpl

# ==========================================
# 0. 解决中文乱码与字体设置
# ==========================================
# 自动适配不同操作系统的中文字体
system_fonts = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'PingFang SC']
mpl.rcParams['font.sans-serif'] = system_fonts
mpl.rcParams['axes.unicode_minus'] = False  # 正常显示负号
mpl.rcParams['mathtext.fontset'] = 'stix'  # 使用科学界标准的 STIX 字体渲染数学公式

# ==========================================
# 1. 设置网格与计算波函数
# ==========================================
# 空间网格：x-z 平面，范围取 -12 到 12 玻尔半径 (a0)
x = np.linspace(-12, 12, 1000)
z = np.linspace(-12, 12, 1000)
X, Z = np.meshgrid(x, z)

# 2pz 轨道波函数 ψ_2pz ∝ z * e^(-r/2)
R = np.sqrt(X ** 2 + Z ** 2)
Psi = Z * np.exp(-R / 2.0)

# ==========================================
# 2. 绘图与美学设置
# ==========================================
fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

# 严格对称颜色条，保证正负相位绝对对称
max_abs = np.max(np.abs(Psi))
norm = TwoSlopeNorm(vmin=-max_abs, vcenter=0, vmax=max_abs)

# 绘制高密度渐变云图 (RdBu_r: 红色为正，蓝色为负，白色为0)
contour = ax.contourf(X, Z, Psi, levels=100, cmap='RdBu_r', norm=norm, alpha=0.9)

# 叠加精细等高线，体现波函数衰减梯度
ax.contour(X, Z, Psi, levels=np.linspace(-max_abs, max_abs, 15),
           colors='white', linewidths=0.6, alpha=0.4)

# 添加浅色网格
ax.grid(True, linestyle='--', alpha=0.3, color='gray')

# ==========================================
# 3. 坐标轴深度定制 (十字交叉在原点)
# ==========================================
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)

ax.set_xticks([-10, -5, 5, 10])
ax.set_yticks([-10, -5, 5, 10])

# 【修正点】：使用标准的字典 {'key': value} 代替 dict()
text_box_style = {
    'facecolor': 'white',
    'edgecolor': 'none',
    'alpha': 0.8,
    'pad': 2
}

# 将坐标轴标题放置在最远端，并加白色背景防遮挡
ax.text(11.5, -1.5, '\(x / a_0\)', fontsize=16, fontweight='bold', ha='center',
        bbox=text_box_style)

ax.text(-1.5, 11.5, '\(z / a_0\)', fontsize=16, fontweight='bold', va='center',
        bbox=text_box_style)

# 坐标轴末端的箭头
ax.annotate('', xy=(12, 0), xytext=(0, 0),
            arrowprops={'arrowstyle': "->", 'color': 'black', 'lw': 1.5})

ax.annotate('', xy=(0, 12), xytext=(0, 0),
            arrowprops={'arrowstyle': "->", 'color': 'black', 'lw': 1.5})

# ==========================================
# 4. 物理标注与图例
# ==========================================
# 节面标注
ax.axhline(0, color='black', linestyle='--', linewidth=1.5, alpha=0.8)
ax.text(4, -1.5, '节面 (Nodal plane, \(\psi = 0\))', fontsize=12, color='black',
        fontstyle='italic', bbox=text_box_style)

# 相位标注
ax.text(4, 9, '\(\psi > 0\) (正相位)', fontsize=14, color='#67001f', fontweight='bold')
ax.text(4, -10.5, '\(\psi < 0\) (负相位)', fontsize=14, color='#053061', fontweight='bold')

# 标题
ax.set_title('\(2p_z\) 轨道波函数截面图 (\(x-z\) 平面)', fontsize=18, fontweight='bold', pad=20)

# 颜色条
cbar = fig.colorbar(contour, ax=ax, shrink=0.75, pad=0.05)
cbar.set_label('波函数值 \(\psi_{2p_z}\)', fontsize=14, labelpad=10)
cbar.ax.tick_params(labelsize=11)

# ==========================================
# 5. 保存与展示
# ==========================================
plt.tight_layout()

# 保存高分辨率图片
plt.savefig('2pz_orbital_optimized.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ 图像生成成功！文件名为: 2pz_orbital_optimized.png")
plt.show()