#include <iostream>
#include <cmath>
#include <fstream>
#include <string>
#include <algorithm>

int main() {
    // 画布尺寸
    const int size = 800;
    // 坐标轴范围 (-15 到 15 玻尔半径)
    const double x_min = -15.0, x_max = 15.0;
    const double z_min = -15.0, z_max = 15.0;

    // 采样精度 (每像素采样一次)
    const int res = 400;
    double step = (x_max - x_min) / res;

    std::ofstream svg("2pz_orbital.svg");
    if (!svg) {
        std::cerr << "无法创建文件！" << std::endl;
        return 1;
    }

    // 1. 写入 SVG 头部
    svg << "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 " << size << " " << size << "\" width=\"" << size << "\" height=\"" << size << "\">\n";

    // 白色背景
    svg << "<rect width=\"100%\" height=\"100%\" fill=\"#ffffff\" />\n";

    // 2. 绘制坐标轴 (黑线、箭头、标签)
    // 中心坐标
    int cx = size / 2;
    int cy = size / 2;
    int axis_len = 320;

    // X 轴
    svg << "<line x1=\"" << cx - axis_len << "\" y1=\"" << cy << "\" x2=\"" << cx + axis_len << "\" y2=\"" << cy << "\" stroke=\"black\" stroke-width=\"2\" />\n";
    svg << "<polygon points=\"" << cx + axis_len - 10 << "," << cy - 5 << " " << cx + axis_len << "," << cy << " " << cx + axis_len - 10 << "," << cy + 5 << "\" fill=\"black\" />\n";
    svg << "<text x=\"" << cx + axis_len + 5 << "\" y=\"" << cy + 5 << "\" font-family=\"Arial\" font-size=\"20\" font-style=\"italic\">x / a₀</text>\n";

    // Z 轴
    svg << "<line x1=\"" << cx << "\" y1=\"" << cy - axis_len << "\" x2=\"" << cx << "\" y2=\"" << cy + axis_len << "\" stroke=\"black\" stroke-width=\"2\" />\n";
    svg << "<polygon points=\"" << cx - 5 << "," << cy - axis_len + 10 << " " << cx << "," << cy - axis_len << " " << cx + 5 << "," << cy - axis_len + 10 << "\" fill=\"black\" />\n";
    svg << "<text x=\"" << cx - 25 << "\" y=\"" << cy - axis_len - 15 << "\" font-family=\"Arial\" font-size=\"20\" font-style=\"italic\">z / a₀</text>\n";

    // 3. 绘制波函数云图 (使用半透明的矩形块拼合)
    for (int i = 0; i < res; ++i) {
        for (int j = 0; j < res; ++j) {
            double x = x_min + i * step;
            double z = z_max - j * step; // 翻转 Z 轴，让正值朝上

            double r = std::sqrt(x * x + z * z);
            // 波函数 ψ_2pz ∝ z * e^(-r/2)
            double psi = z * std::exp(-r / 2.0);

            double intensity = std::abs(psi) * 2.5; // 放大对比度
            if (intensity > 1.0) intensity = 1.0;
            if (intensity < 0.02) continue; // 忽略极低概率区域

            int r_col, g_col, b_col;
            if (psi > 0) {
                // 正相位：红色渐变
                r_col = 255;
                g_col = static_cast<int>(255 * (1.0 - intensity));
                b_col = static_cast<int>(255 * (1.0 - intensity));
            } else {
                // 负相位：蓝色渐变
                r_col = static_cast<int>(255 * (1.0 - intensity));
                g_col = static_cast<int>(255 * (1.0 - intensity));
                b_col = 255;
            }

            // 计算 SVG 坐标
            double svg_x = cx + (x / x_max) * axis_len;
            double svg_z = cy - (z / z_max) * axis_len;
            double svg_size = step * (axis_len / x_max) + 0.5; // 稍微放大矩形防止有缝隙

            svg << "<rect x=\"" << svg_x << "\" y=\"" << svg_z << "\" width=\"" << svg_size << "\" height=\"" << svg_size << "\" fill=\"rgb(" << r_col << "," << g_col << "," << b_col << ")\" opacity=\"0.8\"/>\n";
        }
    }

    // 4. 添加图例和节点面标注
    // 标出节面 (xy平面，即 z=0)
    svg << "<text x=\"" << cx + 20 << "\" y=\"" << cy - 15 << "\" font-family=\"Arial\" font-size=\"16\" fill=\"#333\">节面 (ψ=0)</text>\n";
    // 标出相位
    svg << "<text x=\"" << cx + 40 << "\" y=\"" << cy - 150 << "\" font-family=\"Arial\" font-size=\"18\" fill=\"#cc0000\">ψ &gt; 0 (正相位)</text>\n";
    svg << "<text x=\"" << cx + 40 << "\" y=\"" << cy + 160 << "\" font-family=\"Arial\" font-size=\"18\" fill=\"#0000cc\">ψ &lt; 0 (负相位)</text>\n";

    // 标题
    svg << "<text x=\"" << size/2 - 80 << "\" y=\"40\" font-family=\"Arial\" font-size=\"24\" font-weight=\"bold\">2p_z 轨道角度分布图</text>\n";

    // 5. 结束标签
    svg << "</svg>\n";
    svg.close();

    std::cout << "美化版图像已生成！请找到 2pz_orbital.svg 文件，用浏览器打开，然后截图提交。" << std::endl;
    return 0;
}