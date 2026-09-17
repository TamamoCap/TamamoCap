import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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

def draw_cell(ax, a, b, c, alpha, beta, gamma, title):
    alpha, beta, gamma = np.radians([alpha, beta, gamma])
    v1 = np.array([a, 0, 0])
    v2 = np.array([b * np.cos(gamma), b * np.sin(gamma), 0])
    cx = c * np.cos(beta)
    cy = c * (np.cos(alpha) - np.cos(beta) * np.cos(gamma)) / np.sin(gamma)
    cz = np.sqrt(c ** 2 - cx ** 2 - cy ** 2)
    v3 = np.array([cx, cy, cz])

    verts = [np.array([0, 0, 0]), v1, v1 + v2, v2, v3, v3 + v1, v3 + v1 + v2, v3 + v2]
    faces = [
        [verts[0], verts[1], verts[5], verts[4]],
        [verts[1], verts[2], verts[6], verts[5]],
        [verts[2], verts[3], verts[7], verts[6]],
        [verts[3], verts[0], verts[4], verts[7]],
        [verts[0], verts[1], verts[2], verts[3]],
        [verts[4], verts[5], verts[6], verts[7]]
    ]

    ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='black', alpha=0.3))

    ax.quiver(0, 0, 0, *v1, color='r', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, *v2, color='g', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, *v3, color='b', arrow_length_ratio=0.1)

    ax.set_title(title)
    ax.set_xlim([-0.5, 1.5]);
    ax.set_ylim([-0.5, 1.5]);
    ax.set_zlim([-0.5, 1.5])
    ax.set_xlabel('X');
    ax.set_ylabel('Y');
    ax.set_zlabel('Z')


fig = plt.figure(figsize=(16, 12))
params = [
    (1.0, 1.2, 1.4, 80, 100, 110, '三斜 (Triclinic)'),
    (1.0, 1.2, 1.4, 90, 110, 90, '单斜 (Monoclinic)'),
    (1.0, 1.2, 1.4, 90, 90, 90, '正交 (Orthorhombic)'),
    (1.0, 1.0, 1.4, 90, 90, 90, '四方 (Tetragonal)'),
    (1.0, 1.0, 1.0, 80, 80, 80, '三方/菱方 (Trigonal)'),
    (1.0, 1.0, 1.4, 90, 90, 120, '六方 (Hexagonal)'),
    (1.0, 1.0, 1.0, 90, 90, 90, '立方 (Cubic)')
]

for i, (a, b, c, al, be, ga, title) in enumerate(params):
    ax = fig.add_subplot(3, 3, i + 1, projection='3d')
    draw_cell(ax, a, b, c, al, be, ga, title)

plt.tight_layout()
plt.show()