# 🎨 散点图布局方案对比

针对您提到的"散点图是两张图怎么放"，这里提供三种布局方案供选择。

---

## 方案 1: 并排显示（当前启用）⭐⭐⭐⭐⭐

### 效果预览
```
┌─────────────────────────────────────────┐
│        Evaluation Results               │
│  Performance comparison with baselines  │
├─────────────────────────────────────────┤
│                                         │
│   ┌──────────┐      ┌──────────┐      │
│   │          │      │          │      │
│   │  Kimi    │      │  Gemini  │      │
│   │  Model   │      │  Model   │      │
│   │          │      │          │      │
│   └──────────┘      └──────────┘      │
│    散点图 1           散点图 2          │
│                                         │
│  Side-by-side comparison of models     │
└─────────────────────────────────────────┘

移动端自动变成：
┌──────────┐
│          │
│  Kimi    │
│  Model   │
│          │
└──────────┘
┌──────────┐
│          │
│  Gemini  │
│  Model   │
│          │
└──────────┘
```

### 需要的图片
```
docs/assets/images/
├── performance-scatter-1.png   (Kimi 模型散点图)
└── performance-scatter-2.png   (Gemini 模型散点图)
```

### 优点
- ✅ 方便直接对比两个模型
- ✅ 充分利用屏幕宽度
- ✅ 移动端自动适配
- ✅ 视觉效果专业

### 适用场景
- 对比不同模型的性能
- 对比不同配置的结果
- 需要强调差异性

---

## 方案 2: 上下堆叠显示 ⭐⭐⭐⭐

### 效果预览
```
┌─────────────────────────┐
│  Evaluation Results     │
├─────────────────────────┤
│                         │
│   ┌───────────────┐    │
│   │               │    │
│   │  Kimi Model   │    │
│   │   散点图 1     │    │
│   │               │    │
│   └───────────────┘    │
│   Model A comparison    │
│                         │
│   ┌───────────────┐    │
│   │               │    │
│   │  Gemini Model │    │
│   │   散点图 2     │    │
│   │               │    │
│   └───────────────┘    │
│   Model B comparison    │
│                         │
└─────────────────────────┘
```

### 需要的图片
```
docs/assets/images/
├── performance-scatter-1.png
└── performance-scatter-2.png
```

### 优点
- ✅ 每张图都可以更大
- ✅ 移动端和桌面端体验一致
- ✅ 更易于逐一阅读
- ✅ 适合图表细节较多的情况

### 适用场景
- 图表细节丰富，需要大尺寸显示
- 希望用户逐一关注每张图
- 移动端优先的设计

---

## 方案 3: 单张散点图 ⭐⭐⭐

### 效果预览
```
┌─────────────────────────┐
│  Evaluation Results     │
├─────────────────────────┤
│                         │
│   ┌───────────────┐    │
│   │               │    │
│   │   综合对比     │    │
│   │   散点图       │    │
│   │               │    │
│   └───────────────┘    │
│                         │
│  Repository analysis    │
│  across repositories    │
│                         │
└─────────────────────────┘
```

### 需要的图片
```
docs/assets/images/
└── performance-scatter.png   (单张综合散点图)
```

### 优点
- ✅ 最简洁
- ✅ 减少认知负担
- ✅ 适合整体趋势展示
- ✅ 图片数量最少

### 适用场景
- 不需要模型对比
- 展示整体性能趋势
- 简化信息呈现

---

## 🎯 推荐选择

### 如果您有两个不同模型的结果
**推荐方案 1（并排显示）** - 最直观的对比效果

转换命令：
```bash
# Kimi 模型
pdftoppm -png -r 300 -singlefile \
  paper/.../pic/repo_analysis_kimi_bubble.pdf \
  docs/assets/images/performance-scatter-1

# Gemini 模型
pdftoppm -png -r 300 -singlefile \
  paper/.../pic/repo_analysis_gemini_bubble.pdf \
  docs/assets/images/performance-scatter-2
```

### 如果只有一张综合散点图
**推荐方案 3（单图）** - 简洁清晰

需要修改 HTML（见下方说明），然后转换：
```bash
pdftoppm -png -r 300 -singlefile \
  paper/.../pic/repo_analysis.pdf \
  docs/assets/images/performance-scatter
```

---

## 🔧 如何切换方案

### 当前 HTML 配置：方案 1（并排显示）

在 `docs/index.html` 中，找到 `📌 图片位置 2: 性能对比散点图` 部分：

#### 切换到方案 3（单图）
1. 注释掉第 271-326 行（并排显示代码）
2. 取消注释第 259-269 行（单图代码）

#### 切换到方案 2（上下堆叠）
1. 注释掉第 271-297 行（并排显示代码）
2. 取消注释第 299-317 行（上下堆叠代码）

---

## 📊 视觉效果对比

| 方案 | 桌面端宽度 | 移动端体验 | 对比效果 | 信息密度 |
|------|-----------|-----------|---------|---------|
| 并排显示 | 各占 50% | 自动堆叠 | ⭐⭐⭐⭐⭐ | 高 |
| 上下堆叠 | 100% | 相同 | ⭐⭐⭐⭐ | 中 |
| 单张图 | 100% | 相同 | ⭐⭐⭐ | 低 |

---

## ✅ 下一步

1. **决定使用哪个方案**
   - 两张图对比 → 方案 1 或 方案 2
   - 单张图展示 → 方案 3

2. **准备对应的图片**
   - 方案 1/2: `performance-scatter-1.png` + `performance-scatter-2.png`
   - 方案 3: `performance-scatter.png`

3. **如需切换方案**
   - 修改 `docs/index.html` 中的注释即可

4. **放置图片到** `docs/assets/images/`

5. **本地预览**
   ```bash
   cd docs && python -m http.server 8000
   ```

---

**提示**: 当前 HTML 已配置为**方案 1（并排显示）**，如果您想用这个方案，直接提供两张图片即可，无需修改 HTML！
