# 股票行情查询页面
from nicegui import ui, app
import pandas as pd
import plotly.graph_objects as go
from adata_ui.utils.data_loader import DataLoader, DataTransformer
from adata_ui.utils.app_config import show_error, set_loading


# 创建数据加载器和转换器实例
data_loader = DataLoader()
data_transformer = DataTransformer()


def load_stock_market_page():
    """加载股票行情查询页面"""
    # 不需要从全局存储获取main_content，直接在当前上下文中创建内容
    ui.label('股票行情查询').style('font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; color: #165DFF')
    
    # 创建查询表单
    with ui.card().classes('p-6 shadow-md border-0 rounded-xl mb-6'):
        with ui.row().classes('items-center gap-4'):
            # 股票代码输入
            ui.label('股票代码:')
            stock_code_input = ui.input(placeholder='请输入股票代码，例如：600000').props('outlined')
            
            # 时间范围选择
            ui.label('时间范围:')
            time_range = ui.select([7, 30, 90, 180, 365], value=30).props('outlined')
            
            # 查询按钮
            query_button = ui.button('查询', on_click=lambda: query_stock_data(stock_code_input.value, time_range.value), icon='search').props('color=primary')
    
    # 数据显示区域
    result_container = ui.card().classes('p-6 shadow-md border-0 rounded-xl min-h-[500px]')
    
    # 初始显示提示信息
    with result_container:
        with ui.column().classes('items-center justify-center h-full py-12'):
            ui.icon('query-stats', size='48px').props('color=primary/50')
            ui.label('请输入股票代码并点击查询按钮').style('color: #666; margin-top: 1rem;')
    
    
    async def query_stock_data(code, days):
        """查询股票数据并显示"""
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
            
            # 获取股票数据
            stock_data = await data_loader.get_stock_market_data(code, days)
            
            # 清空结果容器
            result_container.clear()
            
            if stock_data.empty:
                # 显示无数据提示
                with result_container:
                    with ui.column().classes('items-center justify-center h-full py-12'):
                        ui.icon('error-outline', size='48px').props('color=error/50')
                        ui.label('未找到股票数据').style('color: #666; margin-top: 1rem;')
                return
            
            # 显示数据
            with result_container:
                # 股票信息头部
                with ui.row().classes('items-center justify-between mb-4'):
                    ui.label(f'股票代码: {code}').style('font-weight: 600;')
                    
                    # 操作按钮
                    with ui.row().classes('gap-2'):
                        ui.button('刷新', on_click=lambda: query_stock_data(code, days), icon='refresh').props('flat color=primary')
                        ui.button('导出', on_click=lambda: export_data(stock_data), icon='download').props('flat color=success')
                
                # K线图表
                fig = create_kline_chart(stock_data, code)
                plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
                ui.html(plot_div).classes('w-full')
                
                # 数据表格
                ui.label('历史数据').style('font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem;')
                
                # 转换数据为字典列表
                data_list = data_transformer.df_to_dict_list(stock_data)
                
                # 创建表格
                columns = [
                    {'name': 'date', 'label': '日期', 'field': 'date', 'sortable': True},
                    {'name': 'open', 'label': '开盘价', 'field': 'open', 'sortable': True},
                    {'name': 'high', 'label': '最高价', 'field': 'high', 'sortable': True},
                    {'name': 'low', 'label': '最低价', 'field': 'low', 'sortable': True},
                    {'name': 'close', 'label': '收盘价', 'field': 'close', 'sortable': True},
                    {'name': 'volume', 'label': '成交量', 'field': 'volume', 'sortable': True, 'format': lambda v: data_transformer.format_volume(v)}
                ]
                
                ui.table(columns=columns, rows=data_list, pagination={'rowsPerPage': 20}).classes('w-full')
        
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

    def create_kline_chart(stock_data, code):
        """创建K线图表"""
        # 创建K线图
        fig = go.Figure()
        
        # 添加K线
        fig.add_trace(go.Candlestick(
            x=stock_data['date'],
            open=stock_data['open'],
            high=stock_data['high'],
            low=stock_data['low'],
            close=stock_data['close'],
            name='K线'
        ))
        
        # 更新布局
        fig.update_layout(
            title=f'{code} 股票K线图',
            xaxis_title='日期',
            yaxis_title='价格',
            xaxis_rangeslider_visible=False,
            height=500,
            template='plotly_white'
        )
        
        return fig

    def export_data(stock_data):
        """导出数据"""
        try:
            # 创建临时文件路径
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                stock_data.to_csv(tmp.name, index=False)
                tmp_path = tmp.name
            
            # 下载文件
            ui.download(tmp_path, filename='stock_data.csv')
            
            # 删除临时文件
            os.unlink(tmp_path)
            
            ui.notify('数据导出成功', color='success')
        except Exception as e:
            show_error(f'导出失败: {str(e)}')