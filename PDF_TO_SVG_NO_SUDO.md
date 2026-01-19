# 🔄 PDF 转 SVG - 无需 sudo 权限

三种方案，按推荐程度排序：

---

## 🥇 方案 1: 在线转换（最简单推荐）⭐⭐⭐⭐⭐

### 步骤

1. **访问在线转换网站**
   ```
   https://cloudconvert.com/pdf-to-svg
   ```

2. **上传这 5 个 PDF**
   ```bash
   paper/MEnvAgent_.../pic/
   ├── MEnvAgent-main.pdf                    → MEnvAgent-main.svg
   ├── repo_analysis_kimi_bubble.pdf         → performance-scatter-1.svg
   ├── repo_analysis_gemini_bubble.pdf       → performance-scatter-2.svg
   ├── menvbench_radar_suc.pdf               → language-radar.svg
   └── category_distribution.pdf             → dataset-structure.svg
   ```

3. **批量下载 SVG**

4. **重命名并移动到目标位置**
   ```bash
   mv ~/Downloads/MEnvAgent-main.svg docs/assets/images/
   mv ~/Downloads/repo_analysis_kimi_bubble.svg docs/assets/images/performance-scatter-1.svg
   mv ~/Downloads/repo_analysis_gemini_bubble.svg docs/assets/images/performance-scatter-2.svg
   mv ~/Downloads/menvbench_radar_suc.svg docs/assets/images/language-radar.svg
   mv ~/Downloads/category_distribution.svg docs/assets/images/dataset-structure.svg
   ```

### 其他在线服务

- **Convertio**: https://convertio.co/pdf-svg/
- **Online-Convert**: https://www.online-convert.com/
- **ILovePDF**: https://www.ilovepdf.com/pdf_to_svg

---

## 🥈 方案 2: Python 脚本（本地转换，需联网安装库）⭐⭐⭐⭐

### 安装依赖（用户空间，无需 sudo）

```bash
# 方式 1: 使用 pip (推荐)
pip3 install --user pdf2image pillow pypdf2

# 方式 2: 使用 conda (如果有的话)
conda install -c conda-forge pdf2image pillow
```

### 使用转换脚本

运行准备好的脚本：
```bash
python3 convert_pdf_to_images.py
```

脚本会：
1. 读取 paper/pic/ 中的 5 个 PDF
2. 转换为高质量 PNG (300 DPI)
3. 保存到 docs/assets/images/

**注意**: Python 方式通常转换为 PNG 而非 SVG，因为 PDF→SVG 需要复杂的向量转换。

---

## 🥉 方案 3: 使用预编译工具（无需安装）⭐⭐⭐

### Inkscape 便携版

1. **下载便携版**
   ```bash
   wget https://inkscape.org/gallery/item/44616/Inkscape-1.3.2-x86_64.AppImage
   chmod +x Inkscape-*.AppImage
   ```

2. **转换 PDF**
   ```bash
   ./Inkscape-*.AppImage input.pdf --export-type=svg --export-filename=output.svg
   ```

### pdf2svg 静态编译版

1. **下载静态编译版**
   ```bash
   # 从 GitHub 下载预编译版本
   wget https://github.com/dawbarton/pdf2svg/releases/download/v0.2.3/pdf2svg-linux-x86_64
   chmod +x pdf2svg-linux-x86_64
   ```

2. **转换**
   ```bash
   ./pdf2svg-linux-x86_64 input.pdf output.svg
   ```

---

## 🎯 推荐：方案 1（在线转换）

### 为什么推荐在线转换？

✅ **优点**:
- 无需安装任何东西
- 转换质量最高（专业服务）
- 支持批量处理
- 5 分钟搞定所有转换
- 完全免费（小文件量）

❌ **唯一缺点**:
- 需要手动上传/下载

### 时间对比

| 方案 | 安装时间 | 转换时间 | 总时间 |
|------|---------|---------|--------|
| **在线转换** | 0 分钟 | 5 分钟 | **5 分钟** ✅ |
| Python 脚本 | 10-20 分钟 | 2 分钟 | 12-22 分钟 |
| 便携版工具 | 5-10 分钟 | 2 分钟 | 7-12 分钟 |

---

## 🔄 自动化脚本（如果您有 Python）

如果您已经安装了 `pdf2image`，可以使用这个脚本：

```python
#!/usr/bin/env python3
"""
PDF to PNG Converter (无需 sudo)
需要: pip3 install --user pdf2image pillow
"""

from pdf2image import convert_from_path
from pathlib import Path

PAPER_DIR = Path("paper/MEnvAgent__Scalable_Polyglot_Environment_Building_and_Test_Execution_for_Software_Engineering__icml2026/pic")
OUTPUT_DIR = Path("docs/assets/images")

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 转换配置
conversions = [
    ("MEnvAgent-main.pdf", "MEnvAgent-main.png"),
    ("repo_analysis_kimi_bubble.pdf", "performance-scatter-1.png"),
    ("repo_analysis_gemini_bubble.pdf", "performance-scatter-2.png"),
    ("menvbench_radar_suc.pdf", "language-radar.png"),
    ("category_distribution.pdf", "dataset-structure.png"),
]

print("开始转换 PDF 到 PNG (300 DPI)...")
print()

for pdf_name, png_name in conversions:
    pdf_path = PAPER_DIR / pdf_name

    if not pdf_path.exists():
        print(f"⚠️  跳过: {pdf_name} (文件不存在)")
        continue

    print(f"🔄 转换: {pdf_name} → {png_name}")

    # 转换 PDF 到图片（300 DPI）
    images = convert_from_path(pdf_path, dpi=300)

    # 保存第一页
    output_path = OUTPUT_DIR / png_name
    images[0].save(output_path, 'PNG')

    # 显示文件大小
    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"   ✅ 完成: {size_mb:.2f} MB")
    print()

print("=" * 50)
print("✅ 所有转换完成!")
print(f"📁 图片位置: {OUTPUT_DIR}")
```

保存为 `convert_pdfs.py`，然后运行：
```bash
python3 convert_pdfs.py
```

---

## 📊 PNG vs SVG 的权衡

由于无 sudo 权限限制，我们有两个实际选择：

### 选择 A: 在线转换 → SVG ⭐⭐⭐⭐⭐
```
✅ 矢量图形（完美缩放）
✅ 文件小
✅ 就像 LaTeX 中的效果
❌ 需要手动操作 5 个文件
```

### 选择 B: Python 脚本 → PNG (300 DPI) ⭐⭐⭐⭐
```
✅ 全自动
✅ 质量足够好（网页使用）
❌ 文件较大（约 3-5 MB）
❌ 放大会有轻微模糊
```

---

## 💡 我的建议

### 如果您不急（5分钟手动操作）
→ **使用方案 1（在线转换 → SVG）**
- 访问 https://cloudconvert.com/pdf-to-svg
- 拖拽 5 个 PDF，批量下载 SVG
- 重命名后放到 `docs/assets/images/`
- **效果最好！**

### 如果您想全自动
→ **使用方案 2（Python → PNG）**
- 运行 `pip3 install --user pdf2image pillow`
- 运行转换脚本
- 虽然是 PNG，但 300 DPI 在网页上看起来很好

---

## ✅ 验证清单

转换完成后：

```bash
# 检查文件
ls -lh docs/assets/images/

# 应该看到 5 个文件:
# - MEnvAgent-main.svg (或 .png)
# - performance-scatter-1.svg (或 .png)
# - performance-scatter-2.svg (或 .png)
# - language-radar.svg (或 .png)
# - dataset-structure.svg (或 .png)
```

---

## 🚀 完成后

1. **预览网站**
   ```bash
   cd docs && python -m http.server 8000
   ```

2. **提交推送**
   ```bash
   git add docs/assets/images/
   git commit -m "Add images for GitHub Pages (SVG/PNG)"
   git push origin main
   ```

---

**需要帮助？** 告诉我您选择哪个方案，我可以提供更详细的指导！
