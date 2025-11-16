# 股票信息查询页面
from nicegui import ui, app
import pandas as pd
from adata_ui.utils.data_loader import DataLoader, DataTransformer
from adata_ui.utils.app_config import show_error, set_loading


# 创建数据加载器和转换器实例
data_loader = DataLoader()
data_transformer = DataTransformer()


def load_stock_info_page():
    """加载股票信息查询页面"""
    # 清空主内容区域
    main_content = app.storage.general.get('main_content')
    if main_content:
        main_content.clear()
    
    # 页面标题
    with main_content:
        ui.label('股票信息查询').style('font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; color: #165DFF')
        
        # 创建查询表单
        with ui.card().classes('p-6 shadow-md border-0 rounded-xl mb-6'):
            with ui.row().classes('items-center gap-4'):
                # 股票代码输入
                ui.label('股票代码:')
                stock_code_input = ui.input(placeholder='请输入股票代码，例如：600000').props('outlined')
                
                # 查询按钮
                query_button = ui.button('查询', on_click=lambda: query_stock_info(stock_code_input.value), icon='search').props('color=primary')
                
                # 批量查询按钮
                batch_button = ui.button('批量查询', on_click=show_batch_query_dialog, icon='list').props('flat color=primary')
        
        # 数据显示区域
        result_container = ui.card().classes('p-6 shadow-md border-0 rounded-xl min-h-[500px]')
        
        # 初始显示提示信息
        with result_container:
            with ui.column().classes('items-center justify-center h-full py-12'):
                ui.icon('info', size='48px').props('color=primary/50')
                ui.label('请输入股票代码并点击查询按钮').style('color: #666; margin-top: 1rem;')
        
    
    async def query_stock_info(code):
        """查询单个股票信息"""
        if not code:
            ui.notify('请输入股票代码', color='warning')
            return
        
        # 设置加载状态
        set_loading(True)
        try:
            # 清空结果容器
            result_container.clear()
            
            # 显示加载提示
            with result_container:
                with ui.column().classes('items-center justify-center h-full py-12'):
                    ui.spinner(size='xl', color='#165DFF')
                    ui.label('加载中，请稍候...').style('margin-top: 1rem;')
            
            # 获取股票信息
            stock_info = await data_loader.get_stock_info(code)
            
            # 清空结果容器
            result_container.clear()
            
            if not stock_info:
                # 显示无数据提示
                with result_container:
                    with ui.column().classes('items-center justify-center h-full py-12'):
                        ui.icon('error-outline', size='48px').props('color=error/50')
                        ui.label('未找到股票信息').style('color: #666; margin-top: 1rem;')
                return
            
            # 显示股票信息
            show_stock_info(stock_info)
            
        except Exception as e:
            show_error(f'查询失败: {str(e)}')
            # 清空结果容器
            result_container.clear()
            with result_container:
                with ui.column().classes('items-center justify-center h-full py-12'):
                    ui.icon('error-outline', size='48px').props('color=error/50')
                    ui.label('查询失败，请重试').style('color: #666; margin-top: 1rem;')
        finally:
            # 取消加载状态
            set_loading(False)
    
    def show_stock_info(stock_info):
        """显示股票信息"""
        with result_container:
            # 股票基本信息卡片
            with ui.card().classes('p-4 shadow-sm border-0 rounded-lg mb-4'):
                with ui.row().classes('items-center justify-between'):
                    with ui.column():
                        ui.label(f'{stock_info.get("name", "-")}').style('font-size: 1.2rem; font-weight: 600;')
                        ui.label(f'股票代码: {stock_info.get("code", "-")}').style('color: #666; margin-top: 0.25rem;')
                    
                    with ui.row().classes('items-center'):
                        # 股票状态
                        status = stock_info.get('status', 'unknown')
                        status_color = 'success' if status == 'online' else 'error' if status == 'offline' else 'warning'
                        ui.badge({
                            'online': '交易中',
                            'offline': '已停牌',
                            'unknown': '未知'
                        }.get(status, '未知')).props(f'color={status_color}')
                
                # 股价信息
                with ui.row().classes('items-baseline mt-4 gap-4'):
                    current_price = stock_info.get('current_price', 0)
                    change_percent = stock_info.get('change_percent', 0)
                    
                    ui.label(f'{current_price}').style('font-size: 1.5rem; font-weight: 700;')
                    
                    # 涨跌幅
                    change_color = 'text-red-500' if change_percent > 0 else 'text-green-500' if change_percent < 0 else 'text-gray-500'
                    ui.label(f'{change_percent:+.2f}%').style(f'font-size: 1.1rem; font-weight: 600; {change_color}')
            
            # 详细信息网格
            with ui.grid(columns=2).classes('gap-4'):
                # 公司信息
                with ui.card().classes('p-4 shadow-sm border-0 rounded-lg'):
                    ui.label('公司信息').style('font-weight: 600; margin-bottom: 1rem; color: #333;')
                    
                    info_items = [
                        ('公司全称', 'full_name'),
                        ('所属行业', 'industry'),
                        ('地区', 'area'),
                        ('上市日期', 'list_date'),
                        ('总股本(亿)', 'total_share'),
                        ('流通股本(亿)', 'circulating_share'),
                        ('市盈率(TTM)', 'pe_ttm'),
                        ('市净率', 'pb')
                    ]
                    
                    for label, key in info_items:
                        with ui.row().classes('justify-between items-center py-1 border-b border-gray-100'):
                            ui.label(f'{label}:').style('color: #666;')
                            ui.label(str(stock_info.get(key, '-'))).style('font-weight: 500;')
                
                # 最新财务指标
                with ui.card().classes('p-4 shadow-sm border-0 rounded-lg'):
                    ui.label('财务指标').style('font-weight: 600; margin-bottom: 1rem; color: #333;')
                    
                    finance_items = [
                        ('营业收入(亿)', 'revenue'),
                        ('净利润(亿)', 'net_profit'),
                        ('毛利率(%)', 'gross_margin'),
                        ('净利率(%)', 'net_margin'),
                        ('ROE(%)', 'roe'),
                        ('资产负债率(%)', 'debt_ratio'),
                        ('每股收益(元)', 'eps'),
                        ('每股净资产(元)', 'bps')
                    ]
                    
                    for label, key in finance_items:
                        with ui.row().classes('justify-between items-center py-1 border-b border-gray-100'):
                            ui.label(f'{label}:').style('color: #666;')
                            ui.label(str(stock_info.get(key, '-'))).style('font-weight: 500;')
            
            # 操作按钮
            with ui.row().classes('mt-4 gap-2 justify-end'):
                ui.button('刷新', on_click=lambda: query_stock_info(stock_info.get('code', '')), icon='refresh').props('flat color=primary')
                ui.button('导出信息', on_click=lambda: export_stock_info(stock_info), icon='download').props('flat color=success')
                ui.button('查看行情', on_click=lambda: switch_to_market(stock_info.get('code', '')), icon='show-chart').props('color=primary')
    
    def show_batch_query_dialog():
        """显示批量查询对话框"""
        # 打开对话框
        with ui.dialog() as dialog, ui.card().classes('p-6 max-w-2xl'):
            ui.label('批量查询股票信息').style('font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;')
            
            # 输入框（支持多行）
            ui.label('请输入股票代码，每行一个：')
            batch_input = ui.textarea(placeholder='例如：\n600000\n000001\n000002').classes('w-full h-32 mb-4')
            
            # 结果显示区域
            result_area = ui.element('div')
            
            # 按钮区域
            with ui.row().classes('justify-end gap-2 mt-4'):
                ui.button('取消', on_click=dialog.close).props('flat')
                ui.button('查询', on_click=lambda: batch_query(batch_input.value, result_area)).props('color=primary')
        
        dialog.open()
    
    async def batch_query(codes_text, result_area):
        """批量查询股票信息"""
        if not codes_text:
            ui.notify('请输入股票代码', color='warning')
            return
        
        # 获取股票代码列表
        codes = [code.strip() for code in codes_text.strip().split('\n') if code.strip()]
        if not codes:
            ui.notify('请输入有效的股票代码', color='warning')
            return
        
        # 清空结果区域
        result_area.clear()
        
        # 设置加载状态
        set_loading(True)
        try:
            # 显示加载提示
            with result_area:
                ui.spinner()
                ui.label('正在查询，请稍候...')
            
            # 批量查询
            results = []
            for code in codes:
                try:
                    info = await data_loader.get_stock_info(code)
                    if info:
                        results.append(info)
                except Exception as e:
                    # 单个股票查询失败不影响整体
                    pass
            
            # 清空结果区域
            result_area.clear()
            
            if not results:
                with result_area:
                    ui.label('未查询到任何股票信息').style('color: #666;')
                return
            
            # 显示结果表格
            with result_area:
                ui.label(f'查询到 {len(results)} 只股票').style('margin-bottom: 1rem;')
                
                # 准备表格数据
                table_data = []
                for info in results:
                    table_data.append({
                        'code': info.get('code', '-'),
                        'name': info.get('name', '-'),
                        'industry': info.get('industry', '-'),
                        'current_price': info.get('current_price', '-'),
                        'change_percent': f"{info.get('change_percent', 0):+.2f}%",
                        'pe_ttm': info.get('pe_ttm', '-')
                    })
                
                # 创建表格
                columns = [
                    {'name': 'code', 'label': '股票代码', 'field': 'code', 'sortable': True},
                    {'name': 'name', 'label': '股票名称', 'field': 'name', 'sortable': True},
                    {'name': 'industry', 'label': '所属行业', 'field': 'industry'},
                    {'name': 'current_price', 'label': '当前价', 'field': 'current_price', 'sortable': True},
                    {'name': 'change_percent', 'label': '涨跌幅', 'field': 'change_percent', 'sortable': True},
                    {'name': 'pe_ttm', 'label': '市盈率(TTM)', 'field': 'pe_ttm', 'sortable': True}
                ]
                
                ui.table(columns=columns, rows=table_data, pagination={'rowsPerPage': 10}).classes('w-full')
                
                # 导出按钮
                ui.button('导出全部', on_click=lambda: export_batch_results(results)).props('color=success mt-2')
        
        except Exception as e:
            show_error(f'批量查询失败: {str(e)}')
        finally:
            # 取消加载状态
            set_loading(False)
    
    def export_stock_info(stock_info):
        """导出单个股票信息"""
        try:
            # 创建DataFrame
            df = pd.DataFrame([stock_info])
            
            # 创建临时文件路径
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                df.to_csv(tmp.name, index=False, encoding='utf-8-sig')
                tmp_path = tmp.name
            
            # 下载文件
            filename = f"stock_info_{stock_info.get('code', 'unknown')}.csv"
            ui.download(tmp_path, filename=filename)
            
            # 删除临时文件
            os.unlink(tmp_path)
            
            ui.notify('数据导出成功', color='success')
        except Exception as e:
            show_error(f'导出失败: {str(e)}')
    
    def export_batch_results(results):
        """导出批量查询结果"""
        try:
            # 创建DataFrame
            df = pd.DataFrame(results)
            
            # 创建临时文件路径
            import tempfile
            import os
            import datetime
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                df.to_csv(tmp.name, index=False, encoding='utf-8-sig')
                tmp_path = tmp.name
            
            # 下载文件
            filename = f"batch_stock_info_{timestamp}.csv"
            ui.download(tmp_path, filename=filename)
            
            # 删除临时文件
            os.unlink(tmp_path)
            
            ui.notify('批量数据导出成功', color='success')
        except Exception as e:
            show_error(f'批量导出失败: {str(e)}')
    
    def switch_to_market(code):
        """切换到行情页面"""
        from adata_ui.pages.market_page import load_stock_market_page
        
        # 存储当前股票代码
        app.storage.general['last_selected_stock'] = code
        
        # 加载行情页面
        load_stock_market_page()