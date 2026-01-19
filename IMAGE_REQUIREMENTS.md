# 📸 GitHub Pages 需要的图片清单

## 图片保存位置
所有图片放到：`docs/assets/images/`

---

## 需要的 4 张图片

### 📌 图片 1: 系统架构图
- **文件名**: `architecture-main.png`
- **源PDF**: `paper/.../pic/MEnvAgent-main.pdf`
- **用途**: 展示 MEnvAgent 整体架构
- **内容要求**:
  - 顶部：环境复用机制（Environment Reuse Mechanism）
  - 底部：Planning-Execution-Verification 循环
- **建议尺寸**: 宽度 1200-1600px
- **位置**: Architecture Overview 部分

---

### 📌 图片 2: 性能对比散点图

#### 选项 A: 单张散点图
- **文件名**: `performance-scatter.png`
- **源PDF**: `paper/.../pic/repo_analysis.pdf` （散点图/气泡图）
- **用途**: 展示性能对比
- **内容要求**:
  - X轴：仓库规模 (Repository Size/Complexity)
  - Y轴：成功率 (Success Rate)
  - 气泡大小表示任务数量
- **建议尺寸**: 宽度 1000-1200px
- **位置**: Benchmark Results 部分

#### 选项 B: 两张散点图（对比不同模型）⭐
如果想展示两个模型的对比，提供两张图：

- **文件名**:
  - `performance-scatter-1.png` （第一个模型，如 Kimi）
  - `performance-scatter-2.png` （第二个模型，如 Gemini）

- **源PDF**:
  - `repo_analysis_kimi_bubble.pdf` → `performance-scatter-1.png`
  - `repo_analysis_gemini_bubble.pdf` → `performance-scatter-2.png`

- **建议尺寸**: 每张宽度 600-800px（并排显示时会各占一半）

- **显示方式**:
  - 桌面端：左右并排显示
  - 移动端：自动变成上下堆叠

- **说明**: HTML 已配置好并排显示，自动响应式布局

**备选方案**:
- `mainresult1.pdf` - 传统表格（如果不想用散点图）

---

### 📌 图片 3: 语言性能分布雷达图
- **文件名**: `language-radar.png`
- **源PDF**: `paper/.../pic/menvbench_radar_suc.pdf`
- **用途**: 展示 10 种编程语言的性能分布
- **内容要求**:
  - 雷达图显示 10 种语言：Python, Java, JavaScript, TypeScript, Rust, Go, C++, Ruby, PHP, C
  - 显示成功率或有效性指标
- **建议尺寸**: 宽度 800-1000px（正方形或接近正方形）
- **位置**: Benchmark Results 部分

**备选方案**:
- `menvbench_radar_valid.pdf` - 有效性雷达图
- `combined_distribution.pdf` - 组合分布图

---

### 📌 图片 4: 数据集结构分布图
- **文件名**: `dataset-structure.png`
- **源PDF**: `paper/.../pic/category_distribution.pdf`
- **用途**: 展示 MEnvData-SWE-2K 数据集结构
- **内容要求**:
  - 任务类别分布（Task Categories）
  - 领域分布（Domains）
  - 复杂度级别（Complexity Levels）
- **建议尺寸**: 宽度 800-1000px
- **位置**: Dataset 部分

**备选方案**:
- `domain_stats.pdf` - 领域统计
- `scale_stats.pdf` - 规模统计

---

## 图片质量要求

### ✅ 推荐设置
- **格式**: PNG（推荐）或 JPG
- **DPI**: 150-300 DPI
- **背景**: 白色或透明
- **文字**: 清晰可读
- **颜色**: 保持原始颜色（不需要调整）

### 📏 尺寸参考
| 图片 | 建议宽度 | 建议高度 | 宽高比 |
|------|---------|---------|--------|
| 架构图 | 1200-1600px | 700-1000px | ~16:9 或 4:3 |
| 散点图 | 1000-1200px | 600-800px | ~4:3 |
| 雷达图 | 800-1000px | 800-1000px | 1:1 (正方形) |
| 结构图 | 800-1000px | 600-800px | ~4:3 |

---

## 🎨 转换方法

### 方法 1: 使用 pdftoppm (Linux/Mac)
```bash
# 安装工具
sudo apt-get install poppler-utils  # Ubuntu/Debian
brew install poppler                 # macOS

# 转换单个 PDF
pdftoppm -png -r 300 -singlefile input.pdf output
# 会生成 output.png
```

### 方法 2: 使用 ImageMagick
```bash
# 安装
sudo apt-get install imagemagick

# 转换
convert -density 300 input.pdf -quality 90 output.png
```

### 方法 3: 在线转换
- https://www.ilovepdf.com/pdf_to_jpg
- https://smallpdf.com/pdf-to-jpg
- https://convertio.co/pdf-png/

---

## 📋 转换命令示例

假设您的 paper 目录路径是：
`paper/MEnvAgent__Scalable_Polyglot_Environment_Building_and_Test_Execution_for_Software_Engineering__icml2026/pic/`

```bash
# 创建输出目录
mkdir -p docs/assets/images

# 1. 转换架构图
pdftoppm -png -r 300 -singlefile \
  paper/.../pic/MEnvAgent-main.pdf \
  docs/assets/images/architecture-main

# 2. 转换散点图
pdftoppm -png -r 300 -singlefile \
  paper/.../pic/repo_analysis.pdf \
  docs/assets/images/performance-scatter

# 3. 转换雷达图
pdftoppm -png -r 300 -singlefile \
  paper/.../pic/menvbench_radar_suc.pdf \
  docs/assets/images/language-radar

# 4. 转换结构图
pdftoppm -png -r 300 -singlefile \
  paper/.../pic/category_distribution.pdf \
  docs/assets/images/dataset-structure
```

---

## ✅ 验证清单

转换完成后检查：

- [ ] 文件名正确
  - [ ] `architecture-main.png`
  - [ ] `performance-scatter.png`
  - [ ] `language-radar.png`
  - [ ] `dataset-structure.png`

- [ ] 图片质量
  - [ ] 文字清晰可读
  - [ ] 颜色正常
  - [ ] 没有截断
  - [ ] 背景干净

- [ ] 文件大小
  - [ ] 单个文件 < 2MB（推荐）
  - [ ] 总大小 < 5MB（推荐）

---

## 🚀 完成后

将图片放到 `docs/assets/images/` 后：

1. **本地预览**:
```bash
cd docs
python -m http.server 8000
# 访问 http://localhost:8000
```

2. **提交推送**:
```bash
git add docs/assets/images/*.png
git commit -m "Add images for GitHub Pages"
git push origin main
```

3. **访问网站**:
```
https://你的用户名.github.io/MEnvAgent/
```

---

## 🎨 散点图布局切换

HTML 中已经为您准备好了三种布局方案，当前启用的是**并排显示两张图**。

### 当前启用：方案 B - 并排显示两张图 ✅

需要提供：
```
docs/assets/images/
├── performance-scatter-1.png   (如 Kimi 模型)
└── performance-scatter-2.png   (如 Gemini 模型)
```

显示效果：
```
桌面端：  [图1]  [图2]
手机端：  [图1]
          [图2]
```

---

### 如果只想要一张图

打开 `docs/index.html`，找到 `📌 图片位置 2`，然后：

1. **删除或注释掉** 271-326 行（当前的双图代码）
2. **取消注释** 259-269 行（单图代码）

需要提供：
```
docs/assets/images/
└── performance-scatter.png   (单张散点图)
```

---

### 如果想要上下堆叠显示

打开 `docs/index.html`，找到 `📌 图片位置 2`，然后：

1. **注释掉** 271-297 行（当前的并排显示）
2. **取消注释** 299-317 行（上下堆叠显示）

需要提供：
```
docs/assets/images/
├── performance-scatter-1.png
└── performance-scatter-2.png
```

显示效果：
```
[图1]
说明文字

[图2]
说明文字
```

---

## 📞 说明

- 如果图片不显示，检查文件名是否完全匹配
- 如果图片太大，可以降低 DPI (如 `-r 200` 或 `-r 150`)
- PNG 推荐用于图表，JPG 推荐用于照片
- 如果需要调整图片位置或样式，可以修改 `docs/index.html`
- 并排显示会在移动端自动变成上下堆叠（响应式设计）

---

**当前状态**: ✅ HTML 已准备好（默认双图并排），等待图片

**下一步**:
- **如果要双图**: 提供 `performance-scatter-1.png` 和 `performance-scatter-2.png`
- **如果要单图**: 修改 HTML 注释，提供 `performance-scatter.png`
