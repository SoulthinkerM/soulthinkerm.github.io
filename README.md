# 素心客 | Soulthinker Blog

基于 Hexo 框架搭建的个人博客，保留所有自定义功能。

## 快速开始

### 安装依赖

```bash
npm install
```

### 本地开发

```bash
# 启动本地服务器
npm run server

# 或者使用 hexo 命令
hexo clean
hexo generate
python3 scripts/update-pages.py
hexo server
```

访问 http://localhost:4000 预览网站。

### 构建静态文件

```bash
npm run build
python3 scripts/update-pages.py
```

生成的静态文件位于 `public/` 目录。

### 部署到 GitHub Pages

本项目配置了 GitHub Actions 自动部署：

1. 推送到 `main` 分支会自动触发构建
2. GitHub Actions 会运行 `hexo generate` 和自定义脚本
3. 生成的静态文件部署到 `gh-pages` 分支

**重要：** GitHub Pages 设置中需要：
- 选择 "GitHub Actions" 作为部署源
- 或者手动选择 `gh-pages` 分支作为部署源

## 目录结构

```
├── source/              # 源文件目录
│   ├── _posts/          # 文章
│   ├── css/             # 样式文件
│   ├── js/              # JavaScript 文件
│   ├── fonts/           # 字体文件
│   ├── categories/      # 分类页面
│   ├── archives/        # 归档页面
│   └── timeline/        # 时间线页面
├── themes/
│   └── custom-theme/    # 自定义主题
│       ├── layout/      # 布局模板
│       └── source/      # 主题资源
├── scripts/
│   └── update-pages.py  # 自定义更新脚本
├── public/              # 生成的静态文件（构建后）
├── .nojekyll            # 禁用 Jekyll 构建
├── _config.yml          # Hexo 配置文件
└── package.json         # Node.js 依赖配置
```

## 自定义功能

以下自定义功能已完整保留：

- ✅ 多语言切换（中英文支持）
- ✅ 动态内容更新脚本 (`scripts/update-pages.py`)
- ✅ 分类筛选系统
- ✅ 时间线展示
- ✅ 主题切换（深色/浅色模式）
- ✅ 子菜单导航
- ✅ 所有 CSS 样式和 JavaScript 功能

## 发布新文章

```bash
# 创建新文章
hexo new post "文章标题"

# 编辑文章（在 source/_posts/ 目录下）
# 添加 Front-matter:
# ---
# title: 文章标题
# date: 2024-01-01 12:00:00
# categories:
#   - 分类名
# tags:
#   - 标签名
# ---

# 生成并预览
hexo clean
hexo generate
python3 scripts/update-pages.py
hexo server

# 提交并推送
git add .
git commit -m "new post: 文章标题"
git push
```

## 注意事项

1. **不要删除 `.nojekyll` 文件** - 该文件告诉 GitHub Pages 跳过 Jekyll 构建
2. **每次发布新文章后运行更新脚本** - `python3 scripts/update-pages.py`
3. **确保 GitHub Pages 设置正确** - 使用 GitHub Actions 或指向 `gh-pages` 分支

## 技术栈

- Hexo 8.1.1
- Node.js 18+
- Python 3.x (用于自定义脚本)
- EJS 模板引擎
