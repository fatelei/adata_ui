# AData UI
股票数据分析应用

## 代码质量

### 使用pre-commit

项目配置了pre-commit钩子，用于在代码提交前自动进行代码检查和格式化：

```bash
# 安装pre-commit和依赖
pip install pre-commit

# 安装pre-commit钩子到git仓库
pre-commit install

# 手动运行所有检查（对所有文件）
pre-commit run --all-files
```

pre-commit会在每次git commit时自动运行以下检查：
- 代码格式化（black）
- 导入语句排序（isort）
- 代码质量检查（ruff）
- 类型检查（mypy）
- 文档字符串检查（pydocstyle）
- 文件格式检查（换行符、空格等）

## 本地构建

### 构建DMG安装包（macOS）

```bash
# 安装依赖
make install

# 构建DMG安装包
make dmg
```

### 其他可用命令

```bash
# 构建应用（不创建DMG）
make build

# 清理构建文件
make clean

# 运行应用
make run

# 显示帮助信息
make help
```

## GitHub Actions

项目配置了GitHub Actions自动化构建：

- **CI流程**：在main/master分支上进行代码检查和测试
- **发布流程**：创建标签时自动构建Windows可执行文件
- **本地构建**：使用Makefile构建macOS DMG安装包

这是一个使用 NiceGUI 为 AData 库创建的可视化界面工具。AData 是一个免费开源的A股量化交易数据库，此界面提供了简单直观的方式来查询和展示股票数据。

## 功能特性

- 股票代码查询和展示
- 股票行情数据查询和图表可视化
- 股票概念和行业信息查询
- 用户友好的界面和操作体验

## 安装和运行

1. 安装依赖：
```bash
uv sync
```

2. 运行应用：
```bash
uv run python main.py
```

## 技术栈

- Python
- NiceGUI（Web界面框架）
- AData（A股数据接口）
- Pandas（数据处理）
- Matplotlib（图表绘制）

## 注意事项

- 本应用依赖于网络连接来获取股票数据
- AData 库可能会有访问限制，如遇到问题可尝试设置代理