#!/usr/bin/env python3
"""
PDF to PNG Converter - 无需 sudo 权限
将论文中的 PDF 图表转换为高质量 PNG

需要安装: pip3 install --user pdf2image pillow
"""

from pathlib import Path

# 配置路径
PAPER_DIR = Path("paper/MEnvAgent__Scalable_Polyglot_Environment_Building_and_Test_Execution_for_Software_Engineering__icml2026/pic")
OUTPUT_DIR = Path("docs/assets/images")

# 转换配置：(源PDF, 目标PNG)
CONVERSIONS = [
    ("MEnvAgent-main.pdf", "MEnvAgent-main.png"),
    ("repo_analysis_kimi_bubble.pdf", "performance-scatter-1.png"),
    ("repo_analysis_gemini_bubble.pdf", "performance-scatter-2.png"),
    ("menvbench_radar_suc.pdf", "language-radar.png"),
    ("category_distribution.pdf", "dataset-structure.png"),
]

def main():
    print("=" * 60)
    print("PDF → PNG 转换器 (300 DPI)")
    print("=" * 60)
    print()

    # 检查是否安装了必要的库
    try:
        from pdf2image import convert_from_path
        print("✅ pdf2image 已安装")
    except ImportError:
        print("❌ 错误: 未安装 pdf2image")
        print()
        print("请先安装:")
        print("  pip3 install --user pdf2image pillow")
        print()
        return

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ 输出目录: {OUTPUT_DIR}")
    print()

    # 检查源目录
    if not PAPER_DIR.exists():
        print(f"❌ 错误: 未找到 paper 目录: {PAPER_DIR}")
        return

    # 转换每个 PDF
    success_count = 0
    for pdf_name, png_name in CONVERSIONS:
        pdf_path = PAPER_DIR / pdf_name
        output_path = OUTPUT_DIR / png_name

        if not pdf_path.exists():
            print(f"⚠️  跳过: {pdf_name} (文件不存在)")
            continue

        print(f"🔄 转换: {pdf_name}")
        print(f"   → {png_name}")

        try:
            # 转换 PDF 到图片（300 DPI，高质量）
            images = convert_from_path(
                pdf_path,
                dpi=300,
                fmt='png'
            )

            # 保存第一页
            images[0].save(output_path, 'PNG', optimize=True)

            # 显示文件大小
            size_mb = output_path.stat().st_size / 1024 / 1024
            print(f"   ✅ 完成: {size_mb:.2f} MB")
            success_count += 1

        except Exception as e:
            print(f"   ❌ 失败: {e}")

        print()

    # 总结
    print("=" * 60)
    print(f"✅ 转换完成: {success_count}/{len(CONVERSIONS)} 个文件")
    print("=" * 60)
    print()

    # 显示所有生成的文件
    if success_count > 0:
        print("📁 生成的图片:")
        for png_file in sorted(OUTPUT_DIR.glob("*.png")):
            size_mb = png_file.stat().st_size / 1024 / 1024
            print(f"   {png_file.name:<30} {size_mb:>7.2f} MB")
        print()

    print("🚀 下一步:")
    print("   1. 预览: cd docs && python -m http.server 8000")
    print("   2. 提交: git add docs/assets/images/ && git commit -m 'Add images'")
    print()


if __name__ == "__main__":
    main()
