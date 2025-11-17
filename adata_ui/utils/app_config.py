# 应用配置模块
import os
import asyncio
import time
import random
import pandas as pd
from nicegui import events
from nicegui import ui, app
from nicegui.events import ValueChangeEventArguments


def setup_app():
    """配置应用的基本设置"""
    # 设置应用标题
    app.config.title = '股票数据分析系统'
    
    # CSS样式将在每个页面函数内部添加
    
    # 设置错误处理
    # 对于NiceGUI，我们使用app.on_exception而不是exception_handlers.append
    app.on_exception(lambda e: show_error(str(e)))
    
    # 初始化全局存储
    app.storage.general['user_settings'] = {}
    
    # NiceGUI中不需要显式的页面加载钩子，我们会在需要的地方调用page_additions函数


import time
def show_error(message):
    """显示错误消息"""
    app.storage.general['error_message'] = message
    app.storage.general['last_error_time'] = time.time()
    ui.notify(message, color='negative')


def page_additions(page):
    """在每个页面加载时添加的内容"""
    # 可以在这里添加全局加载指示器等
    page.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">')


def set_loading(loading=True):
    """设置全局加载状态"""
    app.storage.general['loading'] = loading


# 创建一个简单的模拟DataLoader类
class MockDataLoader:
    def __init__(self):
        pass
    
    def get_stock_data(self, code, start_date, end_date):
        # 返回模拟数据
        return pd.DataFrame()
    
    def get_concept_data(self, source='ths'):
        # 返回模拟数据
        return pd.DataFrame()
    
    def get_stock_info(self, code):
        # 返回模拟数据
        return {}

# 初始化数据加载器
data_loader = None

# 创建主应用程序实例
def create_app():
    """创建并配置主应用程序"""
    global data_loader
    
    # 初始化数据加载器
    data_loader = MockDataLoader()
    
    # 配置应用存储
    app.storage.general['loading'] = False
    app.storage.general['error_message'] = ''
    app.storage.general['last_error_time'] = 0
    app.storage.general['current_page'] = 'market'
    app.storage.general['selected_stock'] = None
    app.storage.general['concept_source'] = 'ths'
    
    # 配置应用
    ui.page_title('股票数据分析平台')
    
    # 创建主容器
    with ui.header(elevated=True).classes('bg-white shadow-sm'):
        with ui.row().classes('items-center w-full justify-between'):
            ui.label('股票数据分析平台').style('font-size: 1.5rem; font-weight: 600; color: #4f46e5;')
            
            # 导航菜单
            with ui.row().classes('gap-4'):
                ui.button('首页', on_click=lambda: navigate_to_page('home')).props('flat')
                ui.button('股票信息', on_click=lambda: navigate_to_page('stock')).props('flat')
                ui.button('股票行情', on_click=lambda: navigate_to_page('market')).props('flat')
                ui.button('概念板块', on_click=lambda: navigate_to_page('concept')).props('flat')
    
    # 主内容区域
    with ui.footer().classes('bg-white border-t border-gray-200 p-4'):
        ui.label('© 2024 股票数据分析平台').classes('text-center')
    
    # 错误通知组件
    @app.storage.general.on('change:error_message')
    def on_error_message_changed(e):
        if e.value and time.time() - app.storage.general['last_error_time'] > 1:
            ui.notify(e.value, color='negative')
    
    return ui

def navigate_to_page(page_name: str):
    """导航到指定页面"""
    app.storage.general['current_page'] = page_name
    ui.clear('main_content')
    
    with ui.container('main_content'):
        if page_name == 'market':
            from adata_ui.pages.market_page import show_market_page
            show_market_page()
        elif page_name == 'concept':
            from adata_ui.pages.concept_page import show_concept_page
            show_concept_page()