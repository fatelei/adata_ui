#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AData UI - 股票数据分析应用

入口文件：main.py
负责应用的初始化、路由定义和启动
"""

# 导入必要的库和模块
from nicegui import ui, app
import sys
import os
from pathlib import Path

# 导入已拆分的页面模块
from adata_ui.pages.stock_page import load_stock_info_page
from adata_ui.pages.market_page import load_stock_market_page
from adata_ui.pages.concept_page import load_concept_page

# 导入应用配置和工具函数
from adata_ui.utils.app_config import setup_app, show_error, set_loading

# 初始化应用配置
setup_app()

# 初始化全局存储
def initialize_storage():
    """初始化应用存储
    
    注意：只存储可JSON序列化的数据，不存储UI组件，
    避免在JSON序列化时出现TypeError
    """
    app.storage.general.update({
        'loading': False,
        'error_message': '',
        'last_error_time': 0,
        'current_page': 'home',
        'selected_stock': None,
        'concept_source': 'ths',
        'last_selected_stock': None
    })

# 创建导航栏组件
def create_navbar():
    """创建应用导航栏组件
    
    返回：导航栏UI元素
    """
    with ui.header(elevated=True).style('background: linear-gradient(90deg, #165DFF 0%, #0040C1 100%); color: white;').classes('items-center justify-between h-16 px-6'):
        ui.label('AData UI').style('font-size: 1.5rem; font-weight: 600; color: white')
        with ui.row().classes('gap-4'):
            ui.button('首页', on_click=lambda: ui.navigate.to('/')).props('flat text-color=white')
            ui.button('股票信息', on_click=lambda: ui.navigate.to('/stock')).props('flat text-color=white')
            ui.button('股票行情', on_click=lambda: ui.navigate.to('/market')).props('flat text-color=white')
            ui.button('概念板块', on_click=lambda: ui.navigate.to('/concept')).props('flat text-color=white')
            ui.button('数据导出', on_click=lambda: ui.navigate.to('/export')).props('flat text-color=white')
    
# 创建主内容区域函数
def create_main_content():
    """创建主内容区域
    
    返回：主内容UI元素
    """
    return ui.column().classes('flex-1 p-6')

# 首页路由
@ui.page('/')
def index_page():
    """首页 - 应用的主入口页面"""
    # 创建导航栏
    create_navbar()
    
    # 创建主内容区域
    with create_main_content():
        # 全局错误提示检查
        if 'error_message' in app.storage.general and app.storage.general['error_message']:
            ui.notify(app.storage.general['error_message'], color='negative')
            app.storage.general['error_message'] = ''
            
        ui.label('欢迎使用 AData UI').style('font-size: 1.5rem; font-weight: 600; margin-bottom: 2rem; color: #165DFF')
        
        # 功能介绍卡片
        with ui.grid(columns=2, rows=2).classes('gap-6'):
            # 股票信息卡片
            with ui.card().classes('p-6 shadow-md border-0 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors').on('click', lambda: ui.navigate.to('/stock')):
                ui.icon('account-balance', size='48px').props('color=primary')
                ui.label('股票信息查询').style('font-size: 1.1rem; font-weight: 500; margin-top: 1rem;')
                ui.label('查询和查看详细的股票基本信息').style('color: #666; margin-top: 0.5rem;')
            
            # 股票行情卡片
            with ui.card().classes('p-6 shadow-md border-0 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors').on('click', lambda: ui.navigate.to('/market')):
                ui.icon('query-stats', size='48px').props('color=success')
                ui.label('股票行情查询').style('font-size: 1.1rem; font-weight: 500; margin-top: 1rem;')
                ui.label('查看股票K线图和历史交易数据').style('color: #666; margin-top: 0.5rem;')
            
            # 概念板块卡片
            with ui.card().classes('p-6 shadow-md border-0 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors').on('click', lambda: ui.navigate.to('/concept')):
                ui.icon('category', size='48px').props('color=warning')
                ui.label('概念板块查询').style('font-size: 1.1rem; font-weight: 500; margin-top: 1rem;')
                ui.label('了解市场热点和板块轮动情况').style('color: #666; margin-top: 0.5rem;')
            
            # 数据导出卡片
            with ui.card().classes('p-6 shadow-md border-0 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors').on('click', lambda: ui.navigate.to('/export')):
                ui.icon('download', size='48px').props('color=info')
                ui.label('数据导出').style('font-size: 1.1rem; font-weight: 500; margin-top: 1rem;')
                ui.label('导出分析数据为Excel或CSV格式').style('color: #666; margin-top: 0.5rem;')
        
        # 系统信息卡片
        with ui.card().classes('p-6 shadow-md border-0 rounded-xl mt-6'):
            ui.label('系统信息').style('font-size: 1.1rem; font-weight: 500; margin-bottom: 1rem;')
            ui.label('版本: 1.0.0').style('color: #666;')
            ui.label('更新时间: 2024-01-01').style('color: #666; margin-top: 0.5rem;')

# 股票信息页面路由
@ui.page('/stock')
def stock_page():
    """股票信息页面 - 查看股票基本信息"""
    # 创建导航栏
    create_navbar()
    
    # 创建主内容区域
    with create_main_content():
        # 全局错误提示检查
        if 'error_message' in app.storage.general and app.storage.general['error_message']:
            ui.notify(app.storage.general['error_message'], color='negative')
            app.storage.general['error_message'] = ''
    
    # 调用已拆分的页面加载函数
    load_stock_info_page()

# 股票行情页面路由
@ui.page('/market')
def market_page():
    """股票行情页面 - 查看股票K线图和历史数据"""
    # 创建导航栏
    create_navbar()
    
    # 创建主内容区域
    with create_main_content():
        # 全局错误提示检查
        if 'error_message' in app.storage.general and app.storage.general['error_message']:
            ui.notify(app.storage.general['error_message'], color='negative')
            app.storage.general['error_message'] = ''
            
    # 调用已拆分的页面加载函数
    load_stock_market_page()

# 概念板块页面路由
@ui.page('/concept')
def concept_page():
    """概念板块页面 - 查看市场热点和板块轮动"""
    # 创建导航栏
    create_navbar()
    
    # 创建主内容区域
    with create_main_content():
        # 全局错误提示检查
        if 'error_message' in app.storage.general and app.storage.general['error_message']:
            ui.notify(app.storage.general['error_message'], color='negative')
            app.storage.general['error_message'] = ''
            
    # 调用已拆分的页面加载函数
    load_concept_page()

# 数据导出页面路由
@ui.page('/export')
def export_page():
    """数据导出页面 - 导出分析数据"""
    # 创建导航栏
    create_navbar()
    
    # 创建主内容区域
    with create_main_content():
        # 全局错误提示检查
        if 'error_message' in app.storage.general and app.storage.general['error_message']:
            ui.notify(app.storage.general['error_message'], color='negative')
            app.storage.general['error_message'] = ''
            
        ui.label('数据导出').style('font-size: 1.2rem; font-weight: 500; margin-bottom: 1rem;')
        
        with ui.card().classes('p-6 shadow-md border-0 rounded-xl'):
            ui.label('请选择要导出的数据类型:').style('margin-bottom: 1rem;')
            
            # 使用列表格式而不是字典格式，确保正确显示标签
            data_type = ui.select([
                '股票数据',
                '行情数据',
                '概念板块数据'
            ]).props('outlined').classes('w-full mb-4')
            # 设置默认值
            data_type.value = '股票数据'
            
            # 使用列表格式而不是字典格式，确保正确显示标签
            format_type = ui.select([
                'Excel (.xlsx)',
                'CSV (.csv)'
            ]).props('outlined').classes('w-full mb-4')
            # 设置默认值
            format_type.value = 'Excel (.xlsx)'
            
            # 映射显示值到内部值
            def get_internal_values():
                # 映射显示值到内部值
                data_mapping = {
                    '股票数据': 'stock',
                    '行情数据': 'market', 
                    '概念板块数据': 'concept'
                }
                format_mapping = {
                    'Excel (.xlsx)': 'excel',
                    'CSV (.csv)': 'csv'
                }
                return data_mapping.get(data_type.value, 'stock'), format_mapping.get(format_type.value, 'excel')
            
            ui.button('导出数据', on_click=lambda: export_data(*get_internal_values()), icon='download').props('color=success')

# 导出数据函数
def export_data(data_type, format_type):
    """导出数据"""
    set_loading(True)
    try:
        # 模拟数据导出
        ui.notify(f'正在导出{data_type}数据为{format_type}格式...', color='primary')
        ui.notify('导出成功！', color='success')
    except Exception as e:
        show_error(f'导出失败: {str(e)}')
    finally:
        set_loading(False)

# 应用启动前初始化
@app.on_startup
def startup():
    """应用启动时执行的初始化操作"""
    initialize_storage()
    print('AData UI 应用启动成功')

# 应用停止时清理
@app.on_shutdown
def shutdown():
    """应用停止时执行的清理操作"""
    print('AData UI 应用已停止')

# 启动应用
if __name__ in {'__main__', '__mp_main__'}:
    # 从环境变量获取端口，如果没有则使用默认值8080
    port = int(os.environ.get('PORT', 8080))
    # 从环境变量获取是否启用热重载
    reload = os.environ.get('RELOAD', 'True').lower() == 'true'
    
    ui.run(
        title='AData UI - 股票数据分析平台',
        port=port,
        reload=reload,
        show=False,
        dark=None,  # 自动检测系统主题
    )

# 让应用可以作为Python模块运行
if __name__ == '__main__':
    # 这部分会在直接运行脚本时执行
    pass