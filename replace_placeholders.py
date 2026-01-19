#!/usr/bin/env python3
"""
自动替换 HTML 中的图片占位符为 PDF
"""

import re
import shutil
from pathlib import Path

HTML_FILE = Path("docs/index.html")
BACKUP_FILE = Path("docs/index.html.backup_pdf")

# HTML 替换内容
REPLACEMENTS = {
    # 1. 架构主图
    "architecture-diagram": '''            <div class="architecture-diagram-container" style="margin: 2rem 0;">
                <object data="assets/images/MEnvAgent-main.pdf" type="application/pdf"
                        style="width: 100%; height: 600px; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p>Your browser doesn't support PDF preview. <a href="assets/images/MEnvAgent-main.pdf" target="_blank">Click here to view PDF</a></p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Overview of MEnvAgent: (Top) Environment Reuse Mechanism retrieves and adapts historical environments.
                    (Bottom) Planning-Execution-Verification loop with autonomous agents.
                </p>
            </div>''',

    # 2. 结果对比表
    "results-table": '''            <div class="results-image-container" style="margin: 2rem 0;">
                <object data="assets/images/results-comparison.pdf" type="application/pdf"
                        style="width: 100%; max-width: 1000px; height: 400px; margin: 0 auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center;">Your browser doesn't support PDF preview. <a href="assets/images/results-comparison.pdf" target="_blank">Click here to view PDF</a></p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Performance comparison with state-of-the-art baselines across F2P Rate, Time, and Cost metrics.
                </p>
            </div>''',

    # 3. 语言分布图
    "language-chart": '''            <div class="language-chart-container" style="margin: 2rem 0;">
                <object data="assets/images/language-distribution.pdf" type="application/pdf"
                        style="width: 100%; max-width: 800px; height: 600px; margin: 0 auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center;">Your browser doesn't support PDF preview. <a href="assets/images/language-distribution.pdf" target="_blank">Click here to view PDF</a></p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Performance distribution across 10 programming languages.
                </p>
            </div>''',

    # 4. 数据集结构图
    "dataset-viz": '''            <div class="dataset-viz-container" style="margin: 2rem 0;">
                <object data="assets/images/dataset-structure.pdf" type="application/pdf"
                        style="width: 100%; max-width: 800px; height: 600px; margin: 0 auto; display: block; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                    <p style="text-align: center;">Your browser doesn't support PDF preview. <a href="assets/images/dataset-structure.pdf" target="_blank">Click here to view PDF</a></p>
                </object>
                <p style="text-align: center; color: #6b7280; margin-top: 1rem; font-style: italic;">
                    Structure of MEnvData-SWE-2K dataset showing instance fields and organization.
                </p>
            </div>'''
}


def main():
    print("🔄 开始替换 HTML 中的图片占位符...")
    print()

    # 创建备份
    shutil.copy(HTML_FILE, BACKUP_FILE)
    print(f"✅ 已创建备份: {BACKUP_FILE}")
    print()

    # 读取 HTML 内容
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 替换每个占位符
    replacements_made = 0

    for class_name, replacement in REPLACEMENTS.items():
        # 匹配整个 placeholder div
        pattern = rf'<div class="image-placeholder {class_name}">\s*<div class="placeholder-content">.*?</div>\s*</div>'

        if re.search(pattern, html_content, re.DOTALL):
            html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
            replacements_made += 1
            print(f"✅ 已替换: {class_name}")
        else:
            print(f"⚠️  未找到: {class_name}")

    # 写回文件
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print()
    print("=" * 50)
    print(f"✅ 完成！共替换 {replacements_made} 个占位符")
    print("=" * 50)
    print()
    print("📝 说明:")
    print("   • PDF 文件使用 <object> 标签嵌入")
    print("   • 所有现代浏览器都支持")
    print("   • 包含回退链接（不支持时显示）")
    print()
    print("🌐 浏览器支持:")
    print("   ✅ Chrome/Edge - 完美支持")
    print("   ✅ Firefox - 完美支持")
    print("   ✅ Safari - 完美支持")
    print()
    print("📋 下一步:")
    print("   1. 本地预览: cd docs && python -m http.server 8000")
    print("   2. 提交更改: git add docs/ && git commit -m 'Add PDF images'")
    print("   3. 推送代码: git push origin main")
    print()
    print(f"💾 如需恢复: cp {BACKUP_FILE} {HTML_FILE}")


if __name__ == "__main__":
    main()
