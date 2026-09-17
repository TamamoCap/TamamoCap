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

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('立方晶格、晶面与晶向', fontsize=15)

vertices = np.array([
    [0,0,0], [1,0,0], [1,1,0], [0,1,0],
    [0,0,1], [1,0,1], [1,1,1], [0,1,1]
])
edges = [
    [0,1],[1,2],[2,3],[3,0],
    [4,5],[5,6],[6,7],[7,4],
    [0,4],[1,5],[2,6],[3,7]
]
for edge in edges:
    ax.plot3D(*zip(vertices[edge[0]], vertices[edge[1]]), color='black', linewidth=1)

face_010 = np.array([[0,1,0], [1,1,0], [1,1,1], [0,1,1]])
ax.add_collection3d(Poly3DCollection([face_010], facecolors='yellow', alpha=0.5, edgecolors='orange'))
ax.text(0.5, 1.1, 0.5, '(010)', color='orange', fontsize=12)

face_111 = np.array([[1,0,0], [0,1,0], [0,0,1]])
ax.add_collection3d(Poly3DCollection([face_111], facecolors='red', alpha=0.5, edgecolors='darkred'))
ax.text(0.3, 0.3, 0.3, '(111)', color='darkred', fontsize=12)

ax.quiver(0, 0, 0, 0, 1, 0, color='blue', arrow_length_ratio=0.1, linewidth=3)
ax.text(0, 1.1, 0, '[010]', color='blue', fontsize=12)

ax.quiver(0, 0, 0, 1, 1, 1, color='green', arrow_length_ratio=0.1, linewidth=3)
ax.text(0.6, 0.6, 0.6, '[111]', color='green', fontsize=12)

ax.set_xlim([0, 1.5]); ax.set_ylim([0, 1.5]); ax.set_zlim([0, 1.5])
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')

plt.show()