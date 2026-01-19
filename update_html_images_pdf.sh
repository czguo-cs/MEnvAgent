#!/bin/bash

# ====================================
# 更新 HTML 使用 PDF 图片
# ====================================

HTML_FILE="docs/index.html"
BACKUP_FILE="docs/index.html.backup_pdf"

echo "开始更新 HTML 使用 PDF 图片..."
echo ""

# 创建备份
cp "$HTML_FILE" "$BACKUP_FILE"
echo "✅ 已创建备份: $BACKUP_FILE"
echo ""

# 创建临时 HTML 片段文件
mkdir -p /tmp/html_fragments

# ====================================
# 1. 架构主图 - 使用 object 标签（最佳实践）
# ====================================
cat > /tmp/html_fragments/architecture.html << 'EOF'
            <div class="architecture-diagram-container" style="margin: 2rem 0;">
                <object data="assets/images/MEnvAgent-main.pdf" type="application/pdf"
                        style="width: 100%; height: 600px; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p>您的浏览器不支持 PDF 预览。<a href="assets/images/MEnvAgent-main.pdf" target="_blank">点击这里查看 PDF</a></p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Overview of MEnvAgent: (Top) Environment Reuse Mechanism retrieves and adapts historical environments.
                    (Bottom) Planning-Execution-Verification loop with autonomous agents.
                </p>
            </div>
EOF

echo "1️⃣  已准备架构主图 HTML (使用 PDF)"

# ====================================
# 2. 结果对比图
# ====================================
cat > /tmp/html_fragments/results.html << 'EOF'
            <div class="results-image-container" style="margin: 2rem 0;">
                <object data="assets/images/results-comparison.pdf" type="application/pdf"
                        style="width: 100%; max-width: 1000px; height: 400px; margin: 0 auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center;">您的浏览器不支持 PDF 预览。<a href="assets/images/results-comparison.pdf" target="_blank">点击这里查看 PDF</a></p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Performance comparison with state-of-the-art baselines across F2P Rate, Time, and Cost metrics.
                </p>
            </div>
EOF

echo "2️⃣  已准备结果对比图 HTML (使用 PDF)"

# ====================================
# 3. 语言分布图
# ====================================
cat > /tmp/html_fragments/language.html << 'EOF'
            <div class="language-chart-container" style="margin: 2rem 0;">
                <object data="assets/images/language-distribution.pdf" type="application/pdf"
                        style="width: 100%; max-width: 800px; height: 600px; margin: 0 auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center;">您的浏览器不支持 PDF 预览。<a href="assets/images/language-distribution.pdf" target="_blank">点击这里查看 PDF</a></p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Performance distribution across 10 programming languages.
                </p>
            </div>
EOF

echo "3️⃣  已准备语言分布图 HTML (使用 PDF)"

# ====================================
# 4. 数据集结构图
# ====================================
cat > /tmp/html_fragments/dataset.html << 'EOF'
            <div class="dataset-viz-container" style="margin: 2rem 0;">
                <object data="assets/images/dataset-structure.pdf" type="application/pdf"
                        style="width: 100%; max-width: 800px; height: 600px; margin: 0 auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center;">您的浏览器不支持 PDF 预览。<a href="assets/images/dataset-structure.pdf" target="_blank">点击这里查看 PDF</a></p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Structure of MEnvData-SWE-2K dataset showing instance fields and organization.
                </p>
            </div>
EOF

echo "4️⃣  已准备数据集结构图 HTML (使用 PDF)"

echo ""
echo "======================================"
echo "HTML 片段已生成"
echo "======================================"
echo ""
echo "📝 说明："
echo "   • 使用 <object> 标签嵌入 PDF"
echo "   • 包含回退链接（不支持时显示）"
echo "   • 保持响应式设计"
echo "   • 自动适配移动端"
echo ""
echo "🌐 浏览器支持："
echo "   ✅ Chrome/Edge - 完美支持"
echo "   ✅ Firefox - 完美支持"
echo "   ✅ Safari - 完美支持"
echo "   ⚠️  移动端 - 可能需要点击查看"
echo ""
echo "✅ 优点："
echo "   • 矢量图形，无限缩放"
echo "   • 文件更小（相比 PNG）"
echo "   • 不失真，完美清晰"
echo ""
echo "📋 手动替换步骤："
echo "   1. 打开 $HTML_FILE"
echo "   2. 搜索 'image-placeholder'"
echo "   3. 用以上 HTML 片段替换对应占位符"
echo ""
echo "🔄 或者运行自动替换脚本："
echo "   python3 replace_placeholders.py"
echo ""
echo "💾 备份位于: $BACKUP_FILE"
