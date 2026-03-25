# Hexo 博客快速启动指南

## 🚀 一键启动（推荐）

### Windows 用户
双击运行 `start.bat` 文件，或打开命令行执行：
```cmd
start.bat
```

### Linux/Mac 用户
在终端执行：
```bash
./start.sh
```

## 📦 使用 npm 脚本

```bash
# 首次安装依赖
npm install

# 完整启动（生成 + 更新 + 服务器）
npm start

# 仅生成静态文件并运行更新脚本
npm run build

# 仅启动服务器（不重新生成）
npm run server

# 清理缓存
npm run clean
```

## 🔧 手动命令方式

```bash
# 1. 安装依赖（首次运行）
npm install

# 2. 清理缓存
npx hexo clean

# 3. 生成静态文件
npx hexo generate

# 4. 运行更新脚本
python3 update-pages.py

# 5. 启动本地服务器
npx hexo server
```

访问地址：http://localhost:4000

## 📝 常用操作

### 新建文章
```bash
npx hexo new post "文章标题"
```

### 发布文章
编辑 `source/_posts/文章标题.md` 后，重新运行启动脚本即可。

### 部署到 GitHub Pages
```bash
npm run deploy
```

## ⚠️ 注意事项

1. **Python 脚本已移出 scripts 目录**：`update-pages.py` 现在位于项目根目录，避免 Hexo 启动时报错
2. **需要 Python 环境**：确保已安装 Python 3.x
3. **需要 Node.js 环境**：确保已安装 Node.js 14+
4. **GitHub Pages 配置**：已添加 `.nojekyll` 文件和 GitHub Actions 工作流，自动部署无需担心 Jekyll 错误

## 🛠️ 故障排除

### 问题：提示 "require() of ES Module" 错误
**解决**：不要使用 Hexo Pro Desktop 等过时的图形界面工具，直接使用命令行或一键启动脚本。

### 问题：Python 脚本执行失败
**解决**：
- Windows: 尝试将 `python3` 改为 `python`
- 检查 Python 是否正确安装并添加到环境变量

### 问题：端口被占用
**解决**：使用其他端口启动
```bash
npx hexo server -p 4001
```
