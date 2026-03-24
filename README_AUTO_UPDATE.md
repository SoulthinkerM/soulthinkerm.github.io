# 博客自动更新功能说明

## 功能概述

本博客现已支持**自动更新**功能，当你发布新文章后，以下内容会自动同步更新：

- ✅ **内容时间线** (`/timeline/`) - 按时间顺序展示所有文章
- ✅ **最新文章** (首页) - 展示最新的 10 篇文章
- ✅ **标签分类** (`/works/tag-categories/`) - 按分类展示文章
- ✅ **分类页面** (`/categories/*/`) - 各分类下的文章列表

## 使用方法

### 方式一：手动运行更新脚本

每次发布新文章（Hexo generate 后），运行以下命令：

```bash
python3 /workspace/scripts/update-pages.py
```

脚本会自动：
1. 扫描 `archives` 目录中的所有文章
2. 提取文章标题、日期、链接、语言等信息
3. 更新上述各个页面的内容

### 方式二：Git 自动触发（推荐）

已配置 Git post-commit 钩子，每次提交后会自动运行更新脚本：

```bash
# 添加新文章并提交
git add .
git commit -m "new: 发布新文章"

# 提交后会自动：
# 1. 运行更新脚本
# 2. 如果有页面更新，自动创建一个新的提交
```

## 文件结构

```
/workspace/
├── scripts/
│   └── update-pages.py      # 核心更新脚本
├── .git/hooks/
│   └── post-commit          # Git 自动触发钩子
├── timeline/
│   └── index.html           # 时间线页面（自动更新）
├── categories/
│   └── */index.html         # 分类页面（自动更新）
├── works/
│   └── tag-categories/
│       └── index.html       # 标签分类页面（自动更新）
└── index.html               # 首页（自动更新）
```

## 多语言支持

脚本会自动识别文章的语言（通过 URL 中的 `/zh/` 或 `/en/` 路径），并在对应语言的页面中显示：

- 中文文章 → 显示在中文界面
- 英文文章 → 显示在英文界面

## 自定义配置

如需修改更新逻辑，编辑 `/workspace/scripts/update-pages.py`：

```python
# 可配置项
ARCHIVES_DIR = WORKSPACE / 'archives'     # 文章归档目录
CATEGORIES_DIR = WORKSPACE / 'categories' # 分类目录
TIMELINE_FILE = WORKSPACE / 'timeline' / 'index.html'
INDEX_FILE = WORKSPACE / 'index.html'
TAGS_FILE = WORKSPACE / 'works' / 'tag-categories' / 'index.html'
```

## 注意事项

1. **先生成再更新**：确保先用 Hexo 生成静态文件（`hexo generate`），再运行更新脚本
2. **备份重要修改**：如果手动修改了页面模板，请先备份，因为脚本会覆盖部分内容
3. **Git 钩子仅限本地**：`.git/hooks/post-commit` 不会被推送到远程仓库，其他协作者需要自行配置

## 故障排除

### 问题：脚本运行后页面没有变化

**原因**：可能是 archives 目录中没有新的文章链接

**解决**：
1. 检查是否已运行 `hexo generate`
2. 确认 `archives/*/index.html` 中有新文章的链接

### 问题：分类页面没有更新

**原因**：文章 URL 中不包含分类关键词

**解决**：
- 确保文章 URL 包含分类名称（如 `人生游戏化`、`随笔` 等）
- 或在脚本的 `extract_categories()` 函数中添加新的分类映射

---

**技术支持**：如有问题，请查看脚本输出日志或联系管理员。
