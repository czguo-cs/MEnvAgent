# GitHub Pages 配置和命名指南

## 📌 URL 结构说明

### 默认 URL

你的 GitHub Pages 网站 URL 将是：

```
https://你的GitHub用户名.github.io/MEnvAgent/
```

**示例**：
- 用户名：`guochuanzhe`
- 仓库名：`MEnvAgent`
- 完整 URL：`https://guochuanzhe.github.io/MEnvAgent/`

### URL 组成部分

```
https://[username].github.io/[repository-name]/
       ↑             ↑              ↑
    你的用户名   固定域名后缀    仓库名称
```

---

## 🚀 部署步骤

### 1. 推送代码到 GitHub

```bash
git push origin main
```

### 2. 启用 GitHub Pages

1. 访问：`https://github.com/你的用户名/MEnvAgent`
2. 点击 **Settings** 标签页
3. 在左侧菜单找到 **Pages**
4. 在 "Build and deployment" 部分：
   - **Source**: 选择 `Deploy from a branch`
   - **Branch**: 选择 `main`
   - **Folder**: 选择 `/docs`
5. 点击 **Save**

### 3. 等待部署

- GitHub 会自动构建和部署网站
- 通常需要 1-3 分钟
- 完成后，页面顶部会显示：
  ```
  ✓ Your site is live at https://你的用户名.github.io/MEnvAgent/
  ```

### 4. 访问网站

点击显示的 URL 即可查看你的网站！

---

## 🌐 自定义域名配置（可选）

如果你有自己的域名（如 `menvagent.com`），可以配置自定义域名：

### 方法 1: 使用自定义根域名

**1. 在项目中创建 CNAME 文件：**

```bash
echo "menvagent.com" > docs/CNAME
git add docs/CNAME
git commit -m "Add custom domain"
git push origin main
```

**2. 在域名服务商配置 DNS：**

添加以下 DNS 记录：

```
类型: A
名称: @
值: 185.199.108.153

类型: A
名称: @
值: 185.199.109.153

类型: A
名称: @
值: 185.199.110.153

类型: A
名称: @
值: 185.199.111.153
```

**3. 在 GitHub Pages 设置中：**
- 进入 Settings → Pages
- 在 "Custom domain" 输入：`menvagent.com`
- 勾选 "Enforce HTTPS"
- 保存

### 方法 2: 使用子域名

**1. 创建 CNAME 文件：**

```bash
echo "docs.menvagent.com" > docs/CNAME
```

或者：

```bash
echo "www.menvagent.com" > docs/CNAME
```

**2. 在域名服务商配置 DNS：**

```
类型: CNAME
名称: docs (或 www)
值: 你的用户名.github.io
```

**3. 在 GitHub Pages 设置中输入子域名**

---

## 📝 命名规范和建议

### 1. 仓库命名

**当前命名**: `MEnvAgent` ✅ 很好！

**建议**：
- 使用 PascalCase 或 kebab-case
- 保持简洁、有意义
- 避免特殊字符

**示例**：
```
✅ 好的命名：
  - MEnvAgent
  - menv-agent
  - environment-builder

❌ 避免：
  - menv_agent_2024_final
  - test-repo-123
  - my-project
```

### 2. 文件夹命名

**当前结构**：
```
docs/
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
├── index.html
└── README.md
```

✅ **符合标准！**

**规范**：
- 使用小写字母
- 使用连字符 `-` 而非下划线 `_`
- 保持层级清晰

### 3. 文件命名

**HTML 文件**：
```
✅ index.html      # 主页（必须）
✅ about.html      # 其他页面
✅ contact.html
```

**CSS/JS 文件**：
```
✅ style.css
✅ main.css
✅ script.js
✅ app.js
```

**图片文件**：
```
✅ logo.png
✅ hero-background.jpg
✅ architecture-diagram.png
✅ results-chart-2024.png

❌ 避免：
  - 图片1.png
  - IMG_20240101.jpg
  - screenshot (1).png
```

---

## 🔍 验证部署

### 检查部署状态

**方法 1: 在 GitHub 仓库页面**
- 访问 `Actions` 标签页
- 查看 "pages build and deployment" 工作流
- 绿色 ✓ 表示成功

**方法 2: 在 Settings → Pages**
- 查看顶部状态
- 会显示 "Your site is live at..." 和绿色图标

### 测试网站

**1. 检查主页**：
```
https://你的用户名.github.io/MEnvAgent/
```

**2. 检查资源加载**：
- 打开浏览器开发者工具（F12）
- 切换到 Network 标签
- 刷新页面
- 确保没有 404 错误

**3. 检查移动端**：
- 在开发者工具中切换到移动设备视图
- 测试响应式布局

---

## 🐛 常见问题解决

### 问题 1: 404 Not Found

**原因**：
- GitHub Pages 可能还在构建中
- 路径配置错误

**解决**：
1. 等待 2-3 分钟
2. 检查 Settings → Pages 中的配置
3. 确认选择了 `/docs` 文件夹

### 问题 2: CSS/JS 无法加载

**原因**：路径错误

**解决**：确保使用相对路径
```html
<!-- ✅ 正确 -->
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/script.js"></script>

<!-- ❌ 错误 -->
<link rel="stylesheet" href="/assets/css/style.css">
```

### 问题 3: 更新不生效

**解决**：
1. 清除浏览器缓存（Ctrl + Shift + R）
2. 等待几分钟让 GitHub Pages 重新构建
3. 使用无痕模式测试

### 问题 4: 自定义域名不工作

**解决**：
1. 检查 DNS 配置（可能需要 24-48 小时生效）
2. 使用 `dig` 或 `nslookup` 验证 DNS 记录
   ```bash
   dig menvagent.com
   nslookup www.menvagent.com
   ```
3. 在 GitHub Pages 设置中勾选 "Enforce HTTPS"

---

## 📊 URL 示例对照表

| 场景 | URL |
|------|-----|
| **默认项目站点** | `https://username.github.io/MEnvAgent/` |
| **用户站点** | `https://username.github.io/` |
| **自定义根域名** | `https://menvagent.com/` |
| **自定义子域名** | `https://docs.menvagent.com/` |
| **自定义 www 域名** | `https://www.menvagent.com/` |

---

## ✅ 推荐工作流

### 开发 → 部署流程

```bash
# 1. 开发完成后提交
git add docs/
git commit -m "Update website content"

# 2. 推送到 GitHub
git push origin main

# 3. 等待自动部署（1-3分钟）

# 4. 访问网站验证
# https://你的用户名.github.io/MEnvAgent/
```

### 本地预览 → 部署

```bash
# 1. 本地测试
cd docs
python -m http.server 8000
# 访问 http://localhost:8000

# 2. 确认无误后提交推送
git add docs/
git commit -m "Update website"
git push origin main
```

---

## 🎯 快速检查清单

部署前检查：

- [ ] 确认 `docs/index.html` 存在
- [ ] 所有资源使用相对路径
- [ ] 图片文件已添加到 `docs/assets/images/`
- [ ] 测试在本地浏览器中正常显示
- [ ] 代码已推送到 `main` 分支
- [ ] GitHub Pages 设置为 `main` 分支 `/docs` 文件夹

部署后验证：

- [ ] 访问 GitHub Pages URL 可以正常打开
- [ ] 所有 CSS 样式正常加载
- [ ] JavaScript 功能正常工作
- [ ] 图片正常显示
- [ ] 移动端显示正常
- [ ] 所有链接可点击

---

## 📞 需要帮助？

如果遇到问题：

1. 查看 GitHub Pages 官方文档：https://docs.github.com/en/pages
2. 检查 Actions 标签页的构建日志
3. 在仓库中创建 Issue 描述问题

---

**当前项目配置状态**：✅ 已完成
- 路径配置：正确（使用相对路径）
- 文件结构：符合标准
- 命名规范：良好
- 准备部署：是

**下一步**：推送代码并在 GitHub 启用 Pages！
