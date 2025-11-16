# 概念板块查询页面
from nicegui import ui, app
import pandas as pd
from adata_ui.utils.data_loader import DataLoader, DataTransformer
from adata_ui.utils.app_config import show_error, set_loading


# 创建数据加载器和转换器实例
data_loader = DataLoader()
data_transformer = DataTransformer()


def load_concept_page():
    """加载概念板块查询页面"""
    # 清空主内容区域
    main_content = app.storage.general.get('main_content')
    if main_content:
        main_content.clear()
    
    # 页面标题
    with main_content:
        ui.label('概念板块查询').style('font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; color: #165DFF')
        
        # 创建查询表单
        with ui.card().classes('p-6 shadow-md border-0 rounded-xl mb-6'):
            with ui.row().classes('items-center gap-4'):
                # 概念板块名称输入
                ui.label('板块名称:')
                concept_name_input = ui.input(placeholder='请输入概念板块名称或代码，例如：5G').props('outlined')
                
                # 排序方式选择
                ui.label('排序方式:')
                sort_by_select = ui.select([
                    {'value': 'change', 'label': '涨幅排序'},
                    {'value': 'volume', 'label': '成交量排序'},
                    {'value': 'market_value', 'label': '总市值排序'}
                ], value='change').props('outlined')
                
                # 查询按钮
                query_button = ui.button('查询', on_click=lambda: query_concept_list(concept_name_input.value, sort_by_select.value), icon='search').props('color=primary')
        
        # 数据显示区域
        result_container = ui.card().classes('p-6 shadow-md border-0 rounded-xl min-h-[500px]')
        
        # 初始显示提示信息
        with result_container:
            with ui.column().classes('items-center justify-center h-full py-12'):
                ui.icon('category', size='48px').props('color=primary/50')
                ui.label('请输入概念板块名称并点击查询按钮').style('color: #666; margin-top: 1rem;')
        
    
    # 选中的概念板块
    selected_concept = None
    
    async def query_concept_list(concept_name, sort_by):
        """查询概念板块列表"""
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
            
            # 获取概念板块列表
            concept_list = await data_loader.get_concept_list(concept_name)
            
            # 清空结果容器
            result_container.clear()
            
            if concept_list.empty:
                # 显示无数据提示
                with result_container:
                    with ui.column().classes('items-center justify-center h-full py-12'):
                        ui.icon('error-outline', size='48px').props('color=error/50')
                        ui.label('未找到相关概念板块').style('color: #666; margin-top: 1rem;')
                return
            
            # 根据选择的排序方式排序
            if sort_by == 'change':
                concept_list = concept_list.sort_values('change', ascending=False)
            elif sort_by == 'volume':
                concept_list = concept_list.sort_values('volume', ascending=False)
            elif sort_by == 'market_value':
                concept_list = concept_list.sort_values('market_value', ascending=False)
            
            # 显示概念板块列表
            with result_container:
                # 结果统计信息
                ui.label(f'共找到 {len(concept_list)} 个概念板块').style('margin-bottom: 1rem; font-weight: 500;')
                
                # 表格列定义
                columns = [
                    {'name': 'code', 'label': '板块代码', 'field': 'code', 'sortable': True},
                    {'name': 'name', 'label': '板块名称', 'field': 'name', 'sortable': True},
                    {'name': 'change', 'label': '涨跌幅(%)', 'field': 'change', 'sortable': True, 'format': lambda v: f'{v:+.2f}'},
                    {'name': 'volume', 'label': '成交量(万手)', 'field': 'volume', 'sortable': True, 'format': lambda v: f'{v:.2f}'},
                    {'name': 'market_value', 'label': '总市值(亿)', 'field': 'market_value', 'sortable': True, 'format': lambda v: f'{v:.2f}'},
                    {'name': 'stock_count', 'label': '成分股数量', 'field': 'stock_count', 'sortable': True},
                    {'name': 'op', 'label': '操作', 'field': 'op', 'sortable': False}
                ]
                
                # 准备表格数据
                rows = []
                for _, row in concept_list.iterrows():
                    rows.append({
                        'code': row.get('code', '-'),
                        'name': row.get('name', '-'),
                        'change': row.get('change', 0),
                        'volume': row.get('volume', 0),
                        'market_value': row.get('market_value', 0),
                        'stock_count': row.get('stock_count', 0),
                        'op': '查看成分股'
                    })
                
                # 创建表格
                concept_table = ui.table(columns=columns, rows=rows, pagination={'rowsPerPage': 20}).classes('w-full')
                
                # 自定义涨跌幅单元格样式
                concept_table.add_slot('body-cell-change', r'''  
                    <td :props="props">
                        <span :style="{fontWeight: '600', color: props.value > 0 ? '#ff4d4f' : props.value < 0 ? '#52c41a' : '#666'}">
                            {{ props.value > 0 ? '+' : '' }}{{ props.value }}%
                        </span>
                    </td>
                ''')
                
                # 自定义操作列
                concept_table.add_slot('body-cell-op', r'''  
                    <td :props="props">
                        <button class="text-blue-600 hover:text-blue-800 transition-colors" 
                                @click="show_stocks(props.row.code, props.row.name)">
                            查看成分股
                        </button>
                    </td>
                ''')
                
                # 注册JavaScript函数
                ui.run_javascript(f'''  
                    window.show_stocks = function(code, name) {{
                        pywebview.api.show_concept_stocks(code, name);
                    }};
                ''')
                
                # 导出按钮
                ui.button('导出全部', on_click=lambda: export_concept_list(concept_list)).props('color=success mt-4')
        
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
    
    def export_concept_list(concept_list):
        """导出概念板块列表"""
        try:
            # 创建临时文件路径
            import tempfile
            import os
            import datetime
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                concept_list.to_csv(tmp.name, index=False, encoding='utf-8-sig')
                tmp_path = tmp.name
            
            # 下载文件
            filename = f"concept_list_{timestamp}.csv"
            ui.download(tmp_path, filename=filename)
            
            # 删除临时文件
            os.unlink(tmp_path)
            
            ui.notify('数据导出成功', color='success')
        except Exception as e:
            show_error(f'导出失败: {str(e)}')
    
    # 注册API函数，供JavaScript调用
    @app.expose
    async def show_concept_stocks(concept_code, concept_name):
        """显示概念板块的成分股"""
        nonlocal selected_concept
        selected_concept = (concept_code, concept_name)
        
        # 打开对话框显示成分股
        with ui.dialog() as dialog, ui.card().classes('w-[90vw] max-w-6xl max-h-[80vh] overflow-hidden'):
            # 对话框头部
            with ui.row().classes('items-center justify-between w-full px-6 py-4 border-b'):
                ui.label(f'{concept_name} - 成分股').style('font-size: 1.2rem; font-weight: 600;')
                ui.button('关闭', on_click=dialog.close).props('flat')
            
            # 成分股查询区域
            with ui.card().classes('p-4 shadow-none border-0 mb-4'):
                with ui.row().classes('items-center gap-4'):
                    ui.label('排序方式:')
                    stock_sort_by = ui.select([
                        {'value': 'change', 'label': '涨幅排序'},
                        {'value': 'volume', 'label': '成交量排序'},
                        {'value': 'market_value', 'label': '市值排序'}
                    ], value='change').props('outlined')
                    
                    ui.label('涨跌幅筛选:')
                    change_filter = ui.select([
                        {'value': 'all', 'label': '全部'},
                        {'value': 'up', 'label': '上涨'},
                        {'value': 'down', 'label': '下跌'},
                        {'value': 'limit_up', 'label': '涨停'},
                        {'value': 'limit_down', 'label': '跌停'}
                    ], value='all').props('outlined')
                    
                    ui.button('刷新', on_click=lambda: load_concept_stocks(concept_code, concept_name, stock_sort_by.value, change_filter.value), icon='refresh').props('color=primary')
                    ui.button('导出成分股', on_click=lambda: export_concept_stocks(concept_code, concept_name), icon='download').props('flat color=success')
            
            # 成分股列表容器
            stocks_container = ui.element('div').classes('overflow-auto max-h-[calc(80vh-150px)]')
            
            # 加载成分股
            await load_concept_stocks(concept_code, concept_name, stock_sort_by.value, change_filter.value, stocks_container)
        
        dialog.open()
    
    async def load_concept_stocks(concept_code, concept_name, sort_by, change_filter, container=None):
        """加载概念板块的成分股"""
        # 如果没有指定容器，则获取当前对话框中的容器
        if not container:
            container = ui.get_current_container()
        
        # 设置加载状态
        set_loading(True)
        try:
            # 清空容器
            container.clear()
            
            # 显示加载提示
            with container:
                with ui.column().classes('items-center justify-center h-40'):
                    ui.spinner()
                    ui.label('加载成分股中...')
            
            # 获取成分股列表
            stocks = await data_loader.get_concept_stocks(concept_code)
            
            # 清空容器
            container.clear()
            
            if stocks.empty:
                # 显示无数据提示
                with container:
                    with ui.column().classes('items-center justify-center h-40'):
                        ui.label('暂无成分股数据').style('color: #666;')
                return
            
            # 筛选处理
            if change_filter == 'up':
                stocks = stocks[stocks['change'] > 0]
            elif change_filter == 'down':
                stocks = stocks[stocks['change'] < 0]
            elif change_filter == 'limit_up':
                # 假设涨停为9.9%以上
                stocks = stocks[stocks['change'] >= 9.9]
            elif change_filter == 'limit_down':
                # 假设跌停为-9.9%以下
                stocks = stocks[stocks['change'] <= -9.9]
            
            # 排序处理
            if sort_by == 'change':
                stocks = stocks.sort_values('change', ascending=False)
            elif sort_by == 'volume':
                stocks = stocks.sort_values('volume', ascending=False)
            elif sort_by == 'market_value':
                stocks = stocks.sort_values('market_value', ascending=False)
            
            # 显示成分股列表
            with container:
                # 结果统计
                ui.label(f'共 {len(stocks)} 只成分股').style('margin-bottom: 1rem; font-weight: 500;')
                
                # 表格列定义
                columns = [
                    {'name': 'code', 'label': '股票代码', 'field': 'code', 'sortable': True},
                    {'name': 'name', 'label': '股票名称', 'field': 'name', 'sortable': True},
                    {'name': 'current_price', 'label': '现价', 'field': 'current_price', 'sortable': True},
                    {'name': 'change', 'label': '涨跌幅(%)', 'field': 'change', 'sortable': True},
                    {'name': 'volume', 'label': '成交量(万手)', 'field': 'volume', 'sortable': True},
                    {'name': 'market_value', 'label': '市值(亿)', 'field': 'market_value', 'sortable': True},
                    {'name': 'industry', 'label': '所属行业', 'field': 'industry'},
                    {'name': 'op', 'label': '操作', 'field': 'op', 'sortable': False}
                ]
                
                # 准备表格数据
                rows = []
                for _, row in stocks.iterrows():
                    rows.append({
                        'code': row.get('code', '-'),
                        'name': row.get('name', '-'),
                        'current_price': row.get('current_price', 0),
                        'change': row.get('change', 0),
                        'volume': row.get('volume', 0),
                        'market_value': row.get('market_value', 0),
                        'industry': row.get('industry', '-'),
                        'op': '查看详情'
                    })
                
                # 创建表格
                stocks_table = ui.table(columns=columns, rows=rows, pagination={'rowsPerPage': 20}).classes('w-full')
                
                # 自定义涨跌幅单元格样式
                stocks_table.add_slot('body-cell-change', r'''  
                    <td :props="props">
                        <span :style="{fontWeight: '600', color: props.value > 0 ? '#ff4d4f' : props.value < 0 ? '#52c41a' : '#666'}">
                            {{ props.value > 0 ? '+' : '' }}{{ props.value }}%
                        </span>
                    </td>
                ''')
                
                # 自定义操作列
                stocks_table.add_slot('body-cell-op', r'''  
                    <td :props="props">
                        <button class="text-blue-600 hover:text-blue-800 transition-colors" 
                                @click="view_stock_detail(props.row.code, props.row.name)">
                            查看详情
                        </button>
                    </td>
                ''')
                
                # 注册JavaScript函数
                ui.run_javascript(f'''  
                    window.view_stock_detail = function(code, name) {{
                        pywebview.api.view_stock_detail(code, name);
                    }};
                ''')
        
        except Exception as e:
            show_error(f'加载成分股失败: {str(e)}')
            container.clear()
            with container:
                ui.label(f'加载失败: {str(e)}').style('color: #ff4d4f;')
        finally:
            # 取消加载状态
            set_loading(False)
    
    def export_concept_stocks(concept_code, concept_name):
        """导出概念板块的成分股"""
        async def do_export():
            try:
                # 设置加载状态
                set_loading(True)
                
                # 获取成分股列表
                stocks = await data_loader.get_concept_stocks(concept_code)
                
                if stocks.empty:
                    ui.notify('暂无成分股数据可导出', color='warning')
                    return
                
                # 创建临时文件路径
                import tempfile
                import os
                import datetime
                
                timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                    stocks.to_csv(tmp.name, index=False, encoding='utf-8-sig')
                    tmp_path = tmp.name
                
                # 下载文件
                filename = f"{concept_name}_stocks_{timestamp}.csv"
                ui.download(tmp_path, filename=filename)
                
                # 删除临时文件
                os.unlink(tmp_path)
                
                ui.notify('成分股数据导出成功', color='success')
            except Exception as e:
                show_error(f'导出失败: {str(e)}')
            finally:
                # 取消加载状态
                set_loading(False)
        
        # 异步执行导出
        import asyncio
        asyncio.create_task(do_export())
    
    # 注册API函数，供JavaScript调用
    @app.expose
    def view_stock_detail(stock_code, stock_name):
        """查看股票详情"""
        # 存储当前选中的股票信息
        app.storage.general['last_selected_stock'] = stock_code
        
        # 切换到股票信息页面
        from adata_ui.pages.stock_page import load_stock_info_page
        load_stock_info_page()
        
        # 延迟执行查询，确保页面已经加载完成
        import asyncio
        asyncio.create_task(query_stock_after_delay(stock_code))
    
    async def query_stock_after_delay(stock_code):
        """延迟查询股票信息"""
        # 等待一小段时间，确保页面已经加载完成
        await asyncio.sleep(0.5)
        
        # 这里可以通过JavaScript触发查询按钮的点击事件
        # 或者直接调用stock_page中的查询函数
        ui.run_javascript(f'''  
            // 查找股票代码输入框并设置值
            const inputElements = document.querySelectorAll('input');
            for (let i = 0; i < inputElements.length; i++) {{
                if (inputElements[i].placeholder.includes('请输入股票代码')) {{
                    inputElements[i].value = '{stock_code}';
                    break;
                }}
            }}
            
            // 查找查询按钮并点击
            const buttons = document.querySelectorAll('button');
            for (let i = 0; i < buttons.length; i++) {{
                if (buttons[i].textContent.includes('查询') && !buttons[i].textContent.includes('批量查询')) {{
                    buttons[i].click();
                    break;
                }}
            }}
        ''')