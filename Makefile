# AData UI 构建脚本
# 用于在本地环境构建macOS DMG安装包

# 定义变量
APP_NAME = adata_ui
DIST_DIR = dist
BUILD_DIR = build
RESOURCE_DIR = resources
ICON_FILE = icon.icns

# 默认目标
all: dmg

# 安装依赖
install: 
	@echo "正在安装依赖..."
	pip install -r requirements.txt
	pip install pyinstaller pyinstaller-hooks-contrib

# 检查系统是否安装了create-dmg
check-dmg-tool:
	@if ! command -v create-dmg &> /dev/null; then \
		 echo "未找到create-dmg工具，正在安装..."; \
		 brew install create-dmg; \
	fi

# 清理构建文件
clean:
	@echo "正在清理构建文件..."
	-rm -rf $(DIST_DIR)
	-rm -rf $(BUILD_DIR)
	-rm -f $(APP_NAME).spec

# 构建应用
build:
	@echo "正在构建应用..."
	pyinstaller --onefile --windowed --name "$(APP_NAME)" \
		--clean --collect-all nicegui --collect-all adata \
		--copy-metadata nicegui --copy-metadata adata \
		main.py

# 构建DMG安装包
dmg: clean install build check-dmg-tool
	@echo "正在创建DMG安装包..."
	# 确保目录存在
	mkdir -p dmg_assets
	
	# 如果没有图标文件，可以创建一个简单的占位图标
	@if [ ! -f $(ICON_FILE) ]; then \
		 echo "未找到图标文件，使用默认图标..."; \
		 cp -f $(DIST_DIR)/$(APP_NAME).app/Contents/Resources/app_icon.ico $(ICON_FILE) 2>/dev/null || true; \
	fi
	
	# 创建DMG文件
	create-dmg \
		--volname "$(APP_NAME)" \
		--volicon "$(ICON_FILE)" \
		--window-pos 200 120 \
		--window-size 800 400 \
		--icon-size 100 \
		--icon "$(APP_NAME).app" 200 190 \
		--hide-extension "$(APP_NAME).app" \
		--app-drop-link 600 185 \
		"$(DIST_DIR)/$(APP_NAME).dmg" \
		"$(DIST_DIR)/"
	
	@echo "DMG构建完成！文件位置：$(DIST_DIR)/$(APP_NAME).dmg"

# 运行应用
run:
	@python main.py

# 显示帮助
help:
	@echo "使用说明："
	@echo "  make install    - 安装依赖"
	@echo "  make build      - 构建应用"
	@echo "  make dmg        - 构建DMG安装包（推荐）"
	@echo "  make clean      - 清理构建文件"
	@echo "  make run        - 运行应用"
	@echo "  make help       - 显示帮助信息"

.PHONY: all install check-dmg-tool clean build dmg run help