#!/bin/bash

# ====================================
# 直接复制 PDF 图片到网站
# 无需转换，浏览器原生支持
# ====================================

echo "开始复制 PDF 图片到网站..."
echo ""

# 创建图片目录
mkdir -p docs/assets/images

# 定义源目录
PAPER_DIR="paper/MEnvAgent__Scalable_Polyglot_Environment_Building_and_Test_Execution_for_Software_Engineering__icml2026/pic"

# ====================================
# 1. 架构主图
# ====================================
echo "1️⃣  复制架构主图..."
if [ -f "$PAPER_DIR/MEnvAgent-main.pdf" ]; then
    cp "$PAPER_DIR/MEnvAgent-main.pdf" docs/assets/images/MEnvAgent-main.pdf
    echo "   ✅ 已复制: MEnvAgent-main.pdf (965KB)"
else
    echo "   ❌ 未找到: MEnvAgent-main.pdf"
fi

# ====================================
# 2. 结果对比图
# ====================================
echo "2️⃣  复制结果对比图..."
if [ -f "$PAPER_DIR/mainresult1.pdf" ]; then
    cp "$PAPER_DIR/mainresult1.pdf" docs/assets/images/results-comparison.pdf
    echo "   ✅ 已复制: results-comparison.pdf (44KB)"
elif [ -f "$PAPER_DIR/chart_result_refined.pdf" ]; then
    cp "$PAPER_DIR/chart_result_refined.pdf" docs/assets/images/results-comparison.pdf
    echo "   ✅ 已复制: results-comparison.pdf (使用 chart_result_refined)"
else
    echo "   ❌ 未找到合适的结果图"
fi

# ====================================
# 3. 语言分布图
# ====================================
echo "3️⃣  复制语言分布图..."
if [ -f "$PAPER_DIR/menvbench_radar_suc.pdf" ]; then
    cp "$PAPER_DIR/menvbench_radar_suc.pdf" docs/assets/images/language-distribution.pdf
    echo "   ✅ 已复制: language-distribution.pdf"
elif [ -f "$PAPER_DIR/combined_distribution.pdf" ]; then
    cp "$PAPER_DIR/combined_distribution.pdf" docs/assets/images/language-distribution.pdf
    echo "   ✅ 已复制: language-distribution.pdf (使用 combined)"
else
    echo "   ❌ 未找到合适的分布图"
fi

# ====================================
# 4. 数据集结构图
# ====================================
echo "4️⃣  复制数据集结构图..."
if [ -f "$PAPER_DIR/category_distribution.pdf" ]; then
    cp "$PAPER_DIR/category_distribution.pdf" docs/assets/images/dataset-structure.pdf
    echo "   ✅ 已复制: dataset-structure.pdf (21KB)"
else
    echo "   ❌ 未找到合适的结构图"
fi

echo ""
echo "======================================"
echo "复制完成！"
echo "======================================"
echo ""
echo "📁 已生成的文件："
ls -lh docs/assets/images/*.pdf 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}'
echo ""
echo "✅ 优势："
echo "   • 无需安装转换工具"
echo "   • 保持矢量图形质量"
echo "   • 文件体积更小"
echo "   • 支持所有现代浏览器"
echo ""
echo "📝 浏览器支持："
echo "   ✅ Chrome 94+"
echo "   ✅ Firefox 93+"
echo "   ✅ Safari 14+"
echo "   ✅ Edge 94+"
echo ""
echo "✅ 下一步："
echo "   bash update_html_images_pdf.sh  # 更新 HTML 使用 PDF"
