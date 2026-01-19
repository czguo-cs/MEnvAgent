#!/bin/bash

# ====================================
# 从 paper 目录复制最佳 PDF 图片
# 使用散点图展示性能
# ====================================

echo "📊 从 paper 目录复制最佳 PDF 图片..."
echo ""

# 创建图片目录
mkdir -p docs/assets/images

# 定义源目录
PAPER_DIR="paper/MEnvAgent__Scalable_Polyglot_Environment_Building_and_Test_Execution_for_Software_Engineering__icml2026/pic"

# ====================================
# 1. 架构主图 - MEnvAgent-main.pdf
# ====================================
echo "1️⃣  架构主图"
if [ -f "$PAPER_DIR/MEnvAgent-main.pdf" ]; then
    cp "$PAPER_DIR/MEnvAgent-main.pdf" docs/assets/images/architecture-main.pdf
    echo "   ✅ architecture-main.pdf (965KB) - 系统架构总览"
else
    echo "   ❌ 未找到 MEnvAgent-main.pdf"
fi

# ====================================
# 2. 性能对比散点图 - bubble chart
# ====================================
echo ""
echo "2️⃣  性能对比散点图"

# 优先使用 repo_analysis.pdf (包含所有数据)
if [ -f "$PAPER_DIR/repo_analysis.pdf" ]; then
    cp "$PAPER_DIR/repo_analysis.pdf" docs/assets/images/performance-scatter.pdf
    echo "   ✅ performance-scatter.pdf (104KB) - 仓库性能分析散点图"
# 备选：gemini 散点图
elif [ -f "$PAPER_DIR/repo_analysis_gemini_bubble.pdf" ]; then
    cp "$PAPER_DIR/repo_analysis_gemini_bubble.pdf" docs/assets/images/performance-scatter.pdf
    echo "   ✅ performance-scatter.pdf (51KB) - Gemini 散点图"
# 备选：kimi 散点图
elif [ -f "$PAPER_DIR/repo_analysis_kimi_bubble.pdf" ]; then
    cp "$PAPER_DIR/repo_analysis_kimi_bubble.pdf" docs/assets/images/performance-scatter.pdf
    echo "   ✅ performance-scatter.pdf (51KB) - Kimi 散点图"
else
    echo "   ⚠️  未找到散点图，使用主结果图"
    if [ -f "$PAPER_DIR/mainresult1.pdf" ]; then
        cp "$PAPER_DIR/mainresult1.pdf" docs/assets/images/performance-scatter.pdf
        echo "   ✅ performance-scatter.pdf (44KB) - 主结果对比"
    fi
fi

# ====================================
# 3. 语言分布雷达图 - radar chart
# ====================================
echo ""
echo "3️⃣  语言性能分布图"

if [ -f "$PAPER_DIR/menvbench_radar_suc.pdf" ]; then
    cp "$PAPER_DIR/menvbench_radar_suc.pdf" docs/assets/images/language-radar.pdf
    echo "   ✅ language-radar.pdf - 10语言成功率雷达图"
elif [ -f "$PAPER_DIR/menvbench_radar_valid.pdf" ]; then
    cp "$PAPER_DIR/menvbench_radar_valid.pdf" docs/assets/images/language-radar.pdf
    echo "   ✅ language-radar.pdf - 10语言有效性雷达图"
elif [ -f "$PAPER_DIR/combined_distribution.pdf" ]; then
    cp "$PAPER_DIR/combined_distribution.pdf" docs/assets/images/language-radar.pdf
    echo "   ✅ language-radar.pdf (组合分布图)"
else
    echo "   ❌ 未找到语言分布图"
fi

# ====================================
# 4. 数据集结构/分类分布图
# ====================================
echo ""
echo "4️⃣  数据集结构图"

if [ -f "$PAPER_DIR/category_distribution.pdf" ]; then
    cp "$PAPER_DIR/category_distribution.pdf" docs/assets/images/dataset-structure.pdf
    echo "   ✅ dataset-structure.pdf (21KB) - 类别分布"
elif [ -f "$PAPER_DIR/domain_stats.pdf" ]; then
    cp "$PAPER_DIR/domain_stats.pdf" docs/assets/images/dataset-structure.pdf
    echo "   ✅ dataset-structure.pdf - 领域统计"
elif [ -f "$PAPER_DIR/scale_stats.pdf" ]; then
    cp "$PAPER_DIR/scale_stats.pdf" docs/assets/images/dataset-structure.pdf
    echo "   ✅ dataset-structure.pdf - 规模统计"
else
    echo "   ❌ 未找到数据集图"
fi

# ====================================
# 额外：成功率-时间对比图（可选）
# ====================================
echo ""
echo "🔹  额外：成功率-时间对比图"

if [ -f "$PAPER_DIR/MEnvBench_results_suc_time.pdf" ]; then
    cp "$PAPER_DIR/MEnvBench_results_suc_time.pdf" docs/assets/images/results-time-comparison.pdf
    echo "   ✅ results-time-comparison.pdf (29KB) - 成功率vs时间"
fi

echo ""
echo "======================================"
echo "✅ 复制完成！"
echo "======================================"
echo ""

# 显示所有复制的文件
echo "📁 已复制的图片文件："
if [ -d "docs/assets/images" ]; then
    ls -lh docs/assets/images/*.pdf 2>/dev/null | awk '{
        size = $5
        name = $9
        gsub(".*/", "", name)
        printf "   %-30s %8s\n", name, size
    }' | sort
else
    echo "   (无文件)"
fi

echo ""
echo "📊 图片用途说明："
echo ""
echo "   architecture-main.pdf       → 系统架构（规划-执行-验证循环）"
echo "   performance-scatter.pdf     → 性能散点图（仓库规模 vs 成功率）"
echo "   language-radar.pdf          → 语言分布雷达图（10种语言）"
echo "   dataset-structure.pdf       → 数据集结构/类别分布"
echo "   results-time-comparison.pdf → 成功率vs时间对比（可选）"
echo ""
echo "✅ 优势："
echo "   • 使用论文原图 - 质量保证"
echo "   • PDF 矢量格式 - 完美清晰"
echo "   • 散点图展示 - 更直观的性能对比"
echo "   • 文件体积小 - 总计约 1.2 MB"
echo ""
echo "🚀 下一步："
echo "   python3 update_html_with_pdfs.py  # 更新 HTML"
echo ""
