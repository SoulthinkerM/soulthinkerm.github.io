@echo off
echo ========================================
echo   Hexo 博客一键启动脚本
echo ========================================
echo.

REM 检查Node.js是否安装
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js
    pause
    exit /b 1
)

REM 检查Python是否安装
where python >nul 2>nul
if %errorlevel% neq 0 (
    where python3 >nul 2>nul
    if %errorlevel% neq 0 (
        echo [错误] 未检测到 Python，请先安装 Python
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

echo [1/4] 检查并安装依赖...
if not exist "node_modules" (
    echo 首次运行，正在安装依赖...
    call npm install
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo 依赖已存在，跳过安装
)

echo.
echo [2/4] 清理缓存...
call npx hexo clean

echo.
echo [3/4] 生成静态文件...
call npx hexo generate
if %errorlevel% neq 0 (
    echo [错误] Hexo 生成失败
    pause
    exit /b 1
)

echo.
echo [4/4] 运行更新脚本...
%PYTHON_CMD% update-pages.py
if %errorlevel% neq 0 (
    echo [警告] 更新脚本执行失败，但网站仍可访问
)

echo.
echo ========================================
echo   启动本地服务器...
echo ========================================
echo 访问地址：http://localhost:4000
echo 按 Ctrl+C 停止服务器
echo.

call npx hexo server
