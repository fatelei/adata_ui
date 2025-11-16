# 股票数据分析应用入口文件
import sys
import os

# 导入模块化组件
from nicegui import ui, app
from adata_ui.utils.app_config import setup_app
from adata_ui.pages.stock_page import load_stock_info_page
from adata_ui.pages.market_page import load_stock_market_page
from adata_ui.pages.concept_page import load_concept_page

# 设置应用配置
setup_app()

# 创建主页面路由和布局
@ui.page('/')
def main_page():
    # 全局加载指示器
    app.storage.general['loading'] = False
    
    # 全局错误提示
    if 'error_message' in app.storage.general and 'last_error_time' in app.storage.general:
        if app.time() - app.storage.general['last_error_time'] < 5:  # 5秒内显示
            ui.notify(app.storage.general['error_message'], color='negative')
            del app.storage.general['error_message']
            del app.storage.general['last_error_time']
    
    # 创建响应式布局
    with ui.header(elevated=True).style('background: linear-gradient(90deg, #165DFF 0%, #0040C1 100%); color: white;').classes('items-center justify-between h-16 px-6'):
        ui.label('AData UI').style('font-size: 1.5rem; font-weight: 600; color: white')
        ui.button(on_click=lambda: ui.open('/'), icon='home').props('flat text-color=white')
    
    # 创建侧边栏导航
    with ui.sidebar().props('width=240').classes('bg-gray-50 border-r border-gray-200'):
        # 股票代码查询
        ui.button('股票代码查询', on_click=lambda: load_stock_info_page()).props('flat text-color=primary').style('width: 100%; justify-content: start; transition: all 0.3s ease;')
        
        # 股票行情查询
        ui.button('股票行情查询', on_click=lambda: load_stock_market_page()).props('flat text-color=primary').style('width: 100%; justify-content: start; transition: all 0.3s ease;')
        
        # 概念板块查询
        ui.button('概念板块', on_click=lambda: load_concept_page()).props('flat text-color=white').style('transition: all 0.3s ease;')
    
    # 主内容区域
    with ui.column().classes('flex-1 p-6') as main_content:
        app.storage.general['main_content'] = main_content
        
        # 欢迎页面内容
        with ui.card().classes('overflow-hidden shadow-md border-0 rounded-xl w-full max-w-3xl mx-auto').style('background-color: #ffffff;'):
            # 卡片头部
            with ui.element('div').classes('bg-gradient-to-r from-blue-50 to-indigo-50 p-6 border-b border-gray-100'):
                ui.label('欢迎使用股票数据分析系统').style('font-size: 1.5rem; font-weight: 600; color: #165DFF; margin: 0')
            
            # 内容区域
            with ui.element('div').classes('p-6'):
                ui.label('本系统提供以下功能：').style('font-weight: 600; color: #333; margin-bottom: 1rem')
                
                with ui.row().classes('gap-6 flex-wrap justify-center'):
                    # 功能卡片 1
                    with ui.card().classes('p-5 text-center w-64 border-0 shadow-lg hover:shadow-xl transition-shadow duration-300').style('border-radius: 12px;'):
                        ui.icon('description', size='48px').props('color=primary')
                        ui.label('股票信息查询').style('font-weight: 600; margin-top: 1rem;')
                        ui.label('查询股票基本信息、代码等').style('color: #666; margin-top: 0.5rem;')
                    
                    # 功能卡片 2
                    with ui.card().classes('p-5 text-center w-64 border-0 shadow-lg hover:shadow-xl transition-shadow duration-300').style('border-radius: 12px;'):
                        ui.icon('trending-up', size='48px').props('color=secondary')
                        ui.label('股票行情查询').style('font-weight: 600; margin-top: 1rem;')
                        ui.label('查看K线图表、交易数据等').style('color: #666; margin-top: 0.5rem;')
                    
                    # 功能卡片 3
                    with ui.card().classes('p-5 text-center w-64 border-0 shadow-lg hover:shadow-xl transition-shadow duration-300').style('border-radius: 12px;'):
                        ui.icon('category', size='48px').props('color=success')
                        ui.label('概念板块查询').style('font-weight: 600; margin-top: 1rem;')
                        ui.label('分析概念板块、成分股等').style('color: #666; margin-top: 0.5rem;')
                
                with ui.row().classes('mt-6 justify-center gap-4'):
                    ui.button('股票信息查询', on_click=lambda: load_stock_info_page(), icon='description').props('color=primary')
                    ui.button('股票行情查询', on_click=lambda: load_stock_market_page(), icon='trending-up').props('color=secondary')
                    ui.button('概念板块查询', on_click=lambda: load_concept_page(), icon='category').props('color=success')

# 启动应用
if __name__ == '__main__':
    ui.run(title='股票数据分析系统', reload=True)