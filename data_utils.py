import adata
import pandas as pd
import asyncio
from typing import Optional, Dict, Any, List

class DataLoader:
    """数据加载器类，用于处理与adata库的交互"""
    
    @staticmethod
    async def get_all_stocks(search_text: Optional[str] = None) -> pd.DataFrame:
        """
        获取所有股票代码
        
        Args:
            search_text: 搜索文本，用于过滤股票代码或名称
            
        Returns:
            包含股票信息的DataFrame
        """
        try:
            # 使用adata获取所有股票代码
            df = adata.stock.info.all_code()
            
            # 如果有搜索文本，进行过滤
            if search_text:
                df = df[df['stock_code'].str.contains(search_text) | 
                       df['short_name'].str.contains(search_text)]
            
            return df
        except Exception as e:
            raise Exception(f'获取股票列表失败: {str(e)}')
    
    @staticmethod
    async def get_stock_market(stock_code: str, k_type: int = 1, 
                             start_date: str = '2023-01-01') -> pd.DataFrame:
        """
        获取股票行情数据
        
        Args:
            stock_code: 股票代码
            k_type: K线类型 (1:日K, 2:周K, 3:月K)
            start_date: 开始日期，格式为'YYYY-MM-DD'
            
        Returns:
            包含行情数据的DataFrame
        """
        try:
            # 使用adata获取行情数据
            df = adata.stock.market.get_market(
                stock_code=stock_code, 
                k_type=k_type, 
                start_date=start_date
            )
            return df
        except Exception as e:
            raise Exception(f'获取股票{stock_code}行情数据失败: {str(e)}')
    
    @staticmethod
    async def get_concept_list(source: str = 'ths') -> pd.DataFrame:
        """
        获取概念板块列表
        
        Args:
            source: 数据源 ('ths':同花顺, 'east':东方财富)
            
        Returns:
            包含概念信息的DataFrame
        """
        try:
            if source == 'ths':
                df = adata.stock.info.all_concept_code_ths()
            else:
                df = adata.stock.info.all_concept_code_east()
            return df
        except Exception as e:
            raise Exception(f'获取{"同花顺" if source == "ths" else "东方财富"}概念列表失败: {str(e)}')
    
    @staticmethod
    async def get_concept_stocks(concept_code: str, source: str = 'ths') -> pd.DataFrame:
        """
        获取概念包含的股票列表
        
        Args:
            concept_code: 概念代码
            source: 数据源 ('ths':同花顺, 'east':东方财富)
            
        Returns:
            包含成分股信息的DataFrame
        """
        try:
            if source == 'ths':
                df = adata.stock.info.concept_constituent_ths(concept_code)
            else:
                df = adata.stock.info.concept_constituent_east(concept_code)
            return df
        except Exception as e:
            raise Exception(f'获取概念{concept_code}股票列表失败: {str(e)}')
    
    @staticmethod
    async def get_concept_constituents(concept_code: str, source: str = 'ths') -> pd.DataFrame:
        """
        获取概念板块成分股
        
        Args:
            concept_code: 概念代码
            source: 数据源 ('ths':同花顺, 'east':东方财富)
            
        Returns:
            包含成分股信息的DataFrame
        """
        try:
            if source == 'ths':
                df = adata.stock.info.concept_constituent_ths(concept_code)
            else:
                df = adata.stock.info.concept_constituent_east(concept_code)
            return df
        except Exception as e:
            raise Exception(f'获取概念{concept_code}成分股失败: {str(e)}')
    
    @staticmethod
    async def get_stock_concepts(stock_code: str, source: str = 'ths') -> pd.DataFrame:
        """
        获取股票所属概念
        
        Args:
            stock_code: 股票代码
            source: 数据源 ('ths':同花顺, 'east':东方财富)
            
        Returns:
            包含概念信息的DataFrame
        """
        try:
            if source == 'ths':
                df = adata.stock.info.get_concept_ths(stock_code)
            else:
                df = adata.stock.info.get_concept_east(stock_code)
            return df
        except Exception as e:
            raise Exception(f'获取股票{stock_code}所属概念失败: {str(e)}')
    
    @staticmethod
    async def set_proxy(is_proxy: bool = True, ip: Optional[str] = None, 
                       proxy_url: Optional[str] = None) -> None:
        """
        设置代理
        
        Args:
            is_proxy: 是否使用代理
            ip: 代理IP和端口，格式为'ip:port'
            proxy_url: 获取代理IP的链接
        """
        try:
            adata.proxy(is_proxy=is_proxy, ip=ip, proxy_url=proxy_url)
        except Exception as e:
            raise Exception(f'设置代理失败: {str(e)}')

class DataTransformer:
    """数据转换工具类，用于处理数据格式转换"""
    
    @staticmethod
    def df_to_dict_list(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        将DataFrame转换为字典列表，用于NiceGUI表格
        
        Args:
            df: 输入的DataFrame
            
        Returns:
            字典列表
        """
        # 处理可能的NaN值
        df = df.fillna('')
        
        # 转换为字典列表
        return df.to_dict('records')
    
    @staticmethod
    def format_number(value: Any) -> str:
        """
        格式化数字显示
        
        Args:
            value: 需要格式化的值
            
        Returns:
            格式化后的字符串
        """
        try:
            # 如果是数字类型
            if isinstance(value, (int, float)):
                # 根据大小选择合适的格式
                if abs(value) >= 10000:
                    return f"{value:,.0f}"
                elif abs(value) >= 1:
                    return f"{value:.2f}"
                else:
                    return f"{value:.4f}"
            return str(value)
        except:
            return str(value)

# 创建全局数据加载器实例
data_loader = DataLoader()
data_transformer = DataTransformer()