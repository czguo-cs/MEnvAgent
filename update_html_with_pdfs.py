#!/usr/bin/env python3
"""
更新 HTML 使用 paper 目录中的 PDF 图片
包含性能散点图
"""

import re
import shutil
from pathlib import Path

HTML_FILE = Path("docs/index.html")
BACKUP_FILE = Path("docs/index.html.backup_final")

# HTML 替换内容
REPLACEMENTS = {
    # 1. 架构主图 - MEnvAgent-main.pdf
    "architecture-diagram": '''            <div class="architecture-diagram-container" style="margin: 2rem 0;">
                <object data="assets/images/architecture-main.pdf" type="application/pdf"
                        style="width: 100%; height: 600px; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center; padding: 2rem;">
                        Your browser doesn't support PDF preview.
                        <a href="assets/images/architecture-main.pdf" target="_blank"
                           style="color: #6366f1; text-decoration: underline;">
                            Click here to view the architecture diagram
                        </a>
                    </p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Overview of MEnvAgent: (Top) Environment Reuse Mechanism retrieves and adapts historical environments.
                    (Bottom) Planning-Execution-Verification loop with autonomous agents.
                </p>
            </div>''',

    # 2. 性能散点图 - bubble/scatter plot
    "results-table": '''            <div class="performance-scatter-container" style="margin: 2rem 0;">
                <object data="assets/images/performance-scatter.pdf" type="application/pdf"
                        style="width: 100%; max-width: 1000px; height: 500px; margin: 0 auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center; padding: 2rem;">
                        Your browser doesn't support PDF preview.
                        <a href="assets/images/performance-scatter.pdf" target="_blank"
                           style="color: #6366f1; text-decoration: underline;">
                            Click here to view the performance comparison
                        </a>
                    </p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Repository analysis scatter plot: Performance comparison across different repository sizes and complexities.
                    Bubble size indicates the number of tasks, showing MEnvAgent's effectiveness across diverse repositories.
                </p>
            </div>''',

    # 3. 语言雷达图
    "language-chart": '''            <div class="language-radar-container" style="margin: 2rem 0;">
                <object data="assets/images/language-radar.pdf" type="application/pdf"
                        style="width: 100%; max-width: 800px; height: 600px; margin: 0 auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center; padding: 2rem;">
                        Your browser doesn't support PDF preview.
                        <a href="assets/images/language-radar.pdf" target="_blank"
                           style="color: #6366f1; text-decoration: underline;">
                            Click here to view the language distribution
                        </a>
                    </p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Performance radar chart across 10 programming languages: Python, Java, JavaScript, TypeScript,
                    Rust, Go, C++, Ruby, PHP, and C#. MEnvAgent maintains consistent high performance across all languages.
                </p>
            </div>''',

    # 4. 数据集结构图
    "dataset-viz": '''            <div class="dataset-structure-container" style="margin: 2rem 0;">
                <object data="assets/images/dataset-structure.pdf" type="application/pdf"
                        style="width: 100%; max-width: 800px; height: 600px; margin: 0 auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center; padding: 2rem;">
                        Your browser doesn't support PDF preview.
                        <a href="assets/images/dataset-structure.pdf" target="_blank"
                           style="color: #6366f1; text-decoration: underline;">
                            Click here to view the dataset structure
                        </a>
                    </p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    MEnvData-SWE-2K dataset structure: Distribution of task categories, domains, and complexity levels.
                    Shows the diversity and comprehensive coverage of our benchmark dataset.
                </p>
            </div>'''
}


def main():
    print("=" * 60)
    print("🔄 更新 HTML 使用 paper 目录中的 PDF 图片")
    print("=" * 60)
    print()

    # 检查 HTML 文件是否存在
    if not HTML_FILE.exists():
        print(f"❌ 错误: 未找到 {HTML_FILE}")
        return

    # 创建备份
    shutil.copy(HTML_FILE, BACKUP_FILE)
    print(f"✅ 已创建备份: {BACKUP_FILE}")
    print()

    # 读取 HTML 内容
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 替换每个占位符
    replacements_made = 0

    print("开始替换图片占位符...\n")

    for class_name, replacement in REPLACEMENTS.items():
        # 匹配整个 placeholder div
        pattern = rf'<div class="image-placeholder {class_name}">\s*<div class="placeholder-content">.*?</div>\s*</div>'

        if re.search(pattern, html_content, re.DOTALL):
            html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
            replacements_made += 1

            # 显示友好的名称
            names = {
                "architecture-diagram": "架构主图 (MEnvAgent-main)",
                "results-table": "性能散点图 (Repository Analysis)",
                "language-chart": "语言雷达图 (10 Languages)",
                "dataset-viz": "数据集结构 (Category Distribution)"
            }
            print(f"   ✅ {names.get(class_name, class_name)}")
        else:
            print(f"   ⚠️  未找到占位符: {class_name}")

    # 写回文件
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print()
    print("=" * 60)
    print(f"✅ 完成！共替换 {replacements_made}/4 个占位符")
    print("=" * 60)
    print()

    # 显示图片映射
    print("📊 图片映射关系:")
    print()
    print("   HTML 占位符                 → PDF 文件")
    print("   " + "-" * 55)
    print("   architecture-diagram         → architecture-main.pdf")
    print("   results-table                → performance-scatter.pdf 🎯")
    print("   language-chart               → language-radar.pdf")
    print("   dataset-viz                  → dataset-structure.pdf")
    print()

    print("📝 特色说明:")
    print()
    print("   🎯 性能散点图:")
    print("      • 使用 repo_analysis.pdf 或 bubble chart")
    print("      • X轴: 仓库规模, Y轴: 成功率")
    print("      • 气泡大小表示任务数量")
    print("      • 更直观展示性能分布")
    print()
    print("   📐 矢量 PDF 优势:")
    print("      • 无限缩放不失真")
    print("      • 文件体积小 (~1.2 MB)")
    print("      • 保持论文原图质量")
    print()

    print("🌐 浏览器支持:")
    print("   ✅ Chrome/Edge 94+ - 完美支持")
    print("   ✅ Firefox 93+ - 完美支持")
    print("   ✅ Safari 14+ - 完美支持")
    print("   ✅ 移动端浏览器 - 支持（可能显示下载链接）")
    print()

    print("🔍 验证步骤:")
    print()
    print("   1. 本地预览:")
    print("      cd docs && python -m http.server 8000")
    print("      访问 http://localhost:8000")
    print()
    print("   2. 检查图片:")
    print("      • 架构图显示清晰")
    print("      • 散点图可以缩放")
    print("      • 雷达图完整显示")
    print("      • 所有文字可读")
    print()

    print("📦 提交推送:")
    print()
    print("   git add docs/")
    print("   git commit -m 'Add PDF images from paper (with scatter plot)'")
    print("   git push origin main")
    print()

    print(f"💾 如需恢复: cp {BACKUP_FILE} {HTML_FILE}")
    print()


if __name__ == "__main__":
    main()
