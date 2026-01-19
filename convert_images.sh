#!/bin/bash

# ====================================
# 图片转换和替换脚本
# ====================================

echo "开始转换论文图片为网站所需格式..."

# 创建图片目录
mkdir -p docs/assets/images

# 定义源目录
PAPER_DIR="paper/MEnvAgent__Scalable_Polyglot_Environment_Building_and_Test_Execution_for_Software_Engineering__icml2026/pic"

# ====================================
# 1. 架构主图
# ====================================
echo "1️⃣  转换架构主图..."
if [ -f "$PAPER_DIR/MEnvAgent-main.pdf" ]; then
    # 方法1: 使用 ImageMagick (如果已安装)
    if command -v convert &> /dev/null; then
        convert -density 300 "$PAPER_DIR/MEnvAgent-main.pdf" -quality 90 docs/assets/images/MEnvAgent-main.png
        echo "   ✅ 已转换: MEnvAgent-main.png"
    # 方法2: 直接复制 PDF (浏览器支持)
    else
        cp "$PAPER_DIR/MEnvAgent-main.pdf" docs/assets/images/MEnvAgent-main.pdf
        echo "   ⚠️  已复制 PDF 文件，建议转换为 PNG"
    fi
else
    echo "   ❌ 未找到: MEnvAgent-main.pdf"
fi

# ====================================
# 2. 结果对比图
# ====================================
echo "2️⃣  转换结果对比图..."
# 使用 mainresult1 或 chart_result_refined
if [ -f "$PAPER_DIR/mainresult1.pdf" ]; then
    if command -v convert &> /dev/null; then
        convert -density 300 "$PAPER_DIR/mainresult1.pdf" -quality 90 docs/assets/images/results-comparison.png
        echo "   ✅ 已转换: results-comparison.png (使用 mainresult1)"
    else
        cp "$PAPER_DIR/mainresult1.pdf" docs/assets/images/results-comparison.pdf
        echo "   ⚠️  已复制 PDF 文件"
    fi
elif [ -f "$PAPER_DIR/chart_result_refined.pdf" ]; then
    if command -v convert &> /dev/null; then
        convert -density 300 "$PAPER_DIR/chart_result_refined.pdf" -quality 90 docs/assets/images/results-comparison.png
        echo "   ✅ 已转换: results-comparison.png (使用 chart_result_refined)"
    else
        cp "$PAPER_DIR/chart_result_refined.pdf" docs/assets/images/results-comparison.pdf
        echo "   ⚠️  已复制 PDF 文件"
    fi
else
    echo "   ❌ 未找到合适的结果图"
fi

# ====================================
# 3. 语言分布图
# ====================================
echo "3️⃣  转换语言分布图..."
# 使用 menvbench_radar 或 combined_distribution
if [ -f "$PAPER_DIR/menvbench_radar_suc.pdf" ]; then
    if command -v convert &> /dev/null; then
        convert -density 300 "$PAPER_DIR/menvbench_radar_suc.pdf" -quality 90 docs/assets/images/language-distribution.png
        echo "   ✅ 已转换: language-distribution.png (使用 radar)"
    else
        cp "$PAPER_DIR/menvbench_radar_suc.pdf" docs/assets/images/language-distribution.pdf
        echo "   ⚠️  已复制 PDF 文件"
    fi
elif [ -f "$PAPER_DIR/combined_distribution.pdf" ]; then
    if command -v convert &> /dev/null; then
        convert -density 300 "$PAPER_DIR/combined_distribution.pdf" -quality 90 docs/assets/images/language-distribution.png
        echo "   ✅ 已转换: language-distribution.png (使用 combined)"
    else
        cp "$PAPER_DIR/combined_distribution.pdf" docs/assets/images/language-distribution.pdf
        echo "   ⚠️  已复制 PDF 文件"
    fi
else
    echo "   ❌ 未找到合适的分布图"
fi

# ====================================
# 4. 数据集结构图
# ====================================
echo "4️⃣  转换数据集结构图..."
# 使用 category_distribution 或 domain_stats
if [ -f "$PAPER_DIR/category_distribution.pdf" ]; then
    if command -v convert &> /dev/null; then
        convert -density 300 "$PAPER_DIR/category_distribution.pdf" -quality 90 docs/assets/images/dataset-structure.png
        echo "   ✅ 已转换: dataset-structure.png"
    else
        cp "$PAPER_DIR/category_distribution.pdf" docs/assets/images/dataset-structure.pdf
        echo "   ⚠️  已复制 PDF 文件"
    fi
else
    echo "   ❌ 未找到合适的结构图"
fi

echo ""
echo "======================================"
echo "转换完成！"
echo "======================================"
echo ""
echo "📁 已生成的文件："
ls -lh docs/assets/images/ 2>/dev/null || echo "   (无文件)"
echo ""

# 检查是否需要安装 ImageMagick
if ! command -v convert &> /dev/null; then
    echo "⚠️  建议安装 ImageMagick 以转换 PDF 为 PNG："
    echo ""
    echo "   Ubuntu/Debian: sudo apt-get install imagemagick"
    echo "   CentOS/RHEL:   sudo yum install ImageMagick"
    echo "   macOS:         brew install imagemagick"
    echo ""
fi

echo "✅ 下一步："
echo "   1. 检查生成的图片质量"
echo "   2. 运行 update_html_images.sh 更新 HTML"
echo "   3. 提交并推送到 GitHub"
