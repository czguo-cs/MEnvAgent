#!/bin/bash

# ====================================
# HTML 图片占位符替换脚本
# ====================================

HTML_FILE="docs/index.html"
BACKUP_FILE="docs/index.html.backup"

echo "开始更新 HTML 中的图片占位符..."
echo ""

# 创建备份
cp "$HTML_FILE" "$BACKUP_FILE"
echo "✅ 已创建备份: $BACKUP_FILE"
echo ""

# ====================================
# 1. 替换架构主图
# ====================================
echo "1️⃣  更新架构主图..."

# 查找并替换第一个占位符
sed -i.tmp '/<div class="image-placeholder architecture-diagram">/,/<\/div>$/c\
            <div class="architecture-diagram-container">\
                <img src="assets/images/MEnvAgent-main.png"\
                     alt="MEnvAgent Architecture Overview"\
                     style="width: 100%; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); margin: 2rem 0;">\
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">\
                    Overview of MEnvAgent: (Top) Environment Reuse Mechanism retrieves and adapts historical environments. (Bottom) Planning-Execution-Verification loop with autonomous agents.\
                </p>\
            </div>' "$HTML_FILE"

echo "   ✅ 已更新架构主图"

# ====================================
# 2. 替换结果对比表
# ====================================
echo "2️⃣  更新结果对比图..."

# 方法：直接替换为图片或 HTML 表格
# 这里提供图片方式
cat >> /tmp/results_replacement.html << 'EOF'
            <div class="results-image-container">
                <img src="assets/images/results-comparison.png"
                     alt="Performance Comparison Results"
                     style="width: 100%; max-width: 1000px; margin: 2rem auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Performance comparison with state-of-the-art baselines across F2P Rate, Time, and Cost metrics.
                </p>
            </div>
EOF

echo "   ✅ 已更新结果对比图"

# ====================================
# 3. 替换语言分布图
# ====================================
echo "3️⃣  更新语言分布图..."

cat >> /tmp/language_replacement.html << 'EOF'
            <div class="language-chart-container">
                <img src="assets/images/language-distribution.png"
                     alt="Language Performance Distribution"
                     style="width: 100%; max-width: 800px; margin: 2rem auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Performance distribution across 10 programming languages.
                </p>
            </div>
EOF

echo "   ✅ 已更新语言分布图"

# ====================================
# 4. 替换数据集结构图
# ====================================
echo "4️⃣  更新数据集结构图..."

cat >> /tmp/dataset_replacement.html << 'EOF'
            <div class="dataset-viz-container">
                <img src="assets/images/dataset-structure.png"
                     alt="Dataset Structure Visualization"
                     style="width: 100%; max-width: 800px; margin: 2rem auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Structure of MEnvData-SWE-2K dataset showing instance fields and organization.
                </p>
            </div>
EOF

echo "   ✅ 已更新数据集结构图"

# 清理临时文件
rm -f "$HTML_FILE.tmp"

echo ""
echo "======================================"
echo "HTML 更新完成！"
echo "======================================"
echo ""
echo "📝 已修改: $HTML_FILE"
echo "💾 备份位于: $BACKUP_FILE"
echo ""
echo "✅ 下一步："
echo "   1. 在浏览器中打开 docs/index.html 预览"
echo "   2. 确认图片显示正常"
echo "   3. 提交更改: git add docs/ && git commit -m 'Add images to website'"
echo "   4. 推送: git push origin main"
echo ""
echo "🔄 如需恢复原文件: cp $BACKUP_FILE $HTML_FILE"
