# 🖼️ GitHub Pages 图片替换清单

## 📋 需要替换的 4 张图片

| # | 图片名称 | 推荐源文件 | 输出文件 | 位置 |
|---|---------|----------|---------|------|
| 1️⃣ | 架构主图 | `MEnvAgent-main.pdf` | `MEnvAgent-main.png` | Architecture 部分 |
| 2️⃣ | 结果对比 | `mainresult1.pdf` | `results-comparison.png` | Benchmark 部分 |
| 3️⃣ | 语言分布 | `menvbench_radar_suc.pdf` | `language-distribution.png` | Benchmark 部分 |
| 4️⃣ | 数据集结构 | `category_distribution.pdf` | `dataset-structure.png` | Dataset 部分 |

---

## 🚀 快速替换方法

### 方法 1: 一键自动转换（推荐）

```bash
# 1. 转换图片（PDF → PNG）
bash convert_images.sh

# 2. 更新 HTML 文件
bash update_html_images.sh

# 3. 预览效果
cd docs && python -m http.server 8000
# 访问 http://localhost:8000

# 4. 提交更改
git add docs/
git commit -m "Add images to GitHub Pages"
git push origin main
```

### 方法 2: 手动转换

如果自动脚本不工作，可以手动操作：

#### 步骤 1: 转换图片

```bash
# 创建图片目录
mkdir -p docs/assets/images

# 使用 ImageMagick 转换 PDF 为 PNG
convert -density 300 \
  paper/.../pic/MEnvAgent-main.pdf \
  -quality 90 \
  docs/assets/images/MEnvAgent-main.png

# 重复其他图片...
```

#### 步骤 2: 手动编辑 HTML

打开 `docs/index.html`，搜索 `image-placeholder`，替换为实际图片。

---

## 📊 图片详细说明

### 1️⃣ 架构主图

**源文件位置**：
```
paper/.../pic/MEnvAgent-main.pdf
```

**推荐源文件**：
- `MEnvAgent-main.pdf` (首选)
- `mainfig.pdf` (备选)
- `mainfigure.pdf` (备选)

**输出位置**：
```
docs/assets/images/MEnvAgent-main.png
```

**内容**：
- 上部：环境复用机制
- 下部：规划-执行-验证循环

**尺寸要求**：1200×600 像素

---

### 2️⃣ 结果对比图

**源文件位置**：
```
paper/.../pic/mainresult1.pdf
paper/.../pic/mainresult2.pdf
paper/.../pic/chart_result_refined.pdf
```

**推荐源文件**：
- `mainresult1.pdf` (首选 - 主要结果)
- `chart_result_refined.pdf` (备选 - 精炼版图表)
- `MEnvBench_results_suc_time.pdf` (备选 - 成功率+时间)

**输出位置**：
```
docs/assets/images/results-comparison.png
```

**内容**：
- F2P Rate (%)
- Time (min)
- Cost (USD)
- 对比 MEnvAgent vs Baselines

**尺寸要求**：1000×400 像素

---

### 3️⃣ 语言分布图

**源文件位置**：
```
paper/.../pic/menvbench_radar_suc.pdf
paper/.../pic/combined_distribution.pdf
```

**推荐源文件**：
- `menvbench_radar_suc.pdf` (首选 - 雷达图)
- `menvbench_radar_valid.pdf` (备选)
- `combined_distribution.pdf` (备选 - 组合分布)

**输出位置**：
```
docs/assets/images/language-distribution.png
```

**内容**：
展示 10 种语言的性能分布：
- Python, Java, JavaScript, TypeScript
- Rust, Go, C++, Ruby, PHP, C#

**尺寸要求**：800×600 像素

---

### 4️⃣ 数据集结构图

**源文件位置**：
```
paper/.../pic/category_distribution.pdf
paper/.../pic/domain_stats.pdf
```

**推荐源文件**：
- `category_distribution.pdf` (首选 - 类别分布)
- `domain_stats.pdf` (备选 - 领域统计)
- `scale_stats.pdf` (备选 - 规模统计)

**输出位置**：
```
docs/assets/images/dataset-structure.png
```

**内容**：
- 数据集字段结构
- 实例分布
- 类别统计

**尺寸要求**：800×600 像素

---

## 🛠️ 所需工具

### ImageMagick（推荐）

**安装**：
```bash
# Ubuntu/Debian
sudo apt-get install imagemagick

# CentOS/RHEL
sudo yum install ImageMagick

# macOS
brew install imagemagick
```

**使用**：
```bash
convert -density 300 input.pdf -quality 90 output.png
```

### 在线转换工具（备选）

如果无法安装 ImageMagick：
- https://cloudconvert.com/pdf-to-png
- https://www.ilovepdf.com/pdf_to_jpg
- https://www.zamzar.com/convert/pdf-to-png/

---

## ✅ 检查清单

完成后检查：

- [ ] 4 张图片已转换并放入 `docs/assets/images/`
- [ ] 图片文件名正确：
  - [ ] `MEnvAgent-main.png`
  - [ ] `results-comparison.png`
  - [ ] `language-distribution.png`
  - [ ] `dataset-structure.png`
- [ ] HTML 文件已更新（移除占位符）
- [ ] 本地预览正常显示
- [ ] 图片清晰可读
- [ ] 文件大小合理（< 500KB 每张）
- [ ] 已提交到 Git

---

## 📸 图片优化建议

### 压缩图片

如果图片太大，使用以下工具压缩：

```bash
# 使用 ImageMagick 优化
convert input.png -quality 85 -resize 1200x output.png

# 使用 pngquant (更好的压缩)
pngquant --quality=70-85 input.png -o output.png
```

### 在线压缩工具
- https://tinypng.com/
- https://compressor.io/
- https://squoosh.app/

---

## 🔄 如果出错

### 恢复原始 HTML

```bash
cp docs/index.html.backup docs/index.html
```

### 重新开始

```bash
# 清理生成的文件
rm -rf docs/assets/images/*

# 重新运行脚本
bash convert_images.sh
bash update_html_images.sh
```

---

## 📞 需要帮助？

问题排查：

1. **图片不显示**
   - 检查文件路径是否正确
   - 确认文件名拼写无误
   - 查看浏览器控制台的 404 错误

2. **图片模糊**
   - 提高转换密度：`-density 600`
   - 使用更大的源图片

3. **PDF 转换失败**
   - 确认 ImageMagick 已安装
   - 尝试在线转换工具

4. **文件太大**
   - 降低质量：`-quality 70`
   - 调整尺寸：`-resize 1000x`
   - 使用压缩工具

---

## 🎯 当前可用图片

从 paper 目录找到的可用图片：

| 图片文件 | 用途 | 状态 |
|---------|------|------|
| `MEnvAgent-main.pdf` (965KB) | 架构主图 | ✅ 可用 |
| `mainresult1.pdf` (44KB) | 结果对比1 | ✅ 可用 |
| `mainresult2.pdf` (36KB) | 结果对比2 | ✅ 可用 |
| `menvbench_radar_suc.pdf` | 语言雷达图 | ✅ 可用 |
| `category_distribution.pdf` | 类别分布 | ✅ 可用 |
| `combined_distribution.pdf` | 组合分布 | ✅ 可用 |

所有需要的图片都已存在，只需要转换格式！

---

**下一步**：运行 `bash convert_images.sh` 开始转换！
