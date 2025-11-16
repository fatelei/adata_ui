# 数据加载模块
import os
import asyncio
import time
import random
import pandas as pd
from typing import Dict, List, Optional

class DataLoader:
    """数据加载器类，负责获取各类股票数据"""
    
    def __init__(self):
        # 初始化数据源配置
        self.sources = {
            'ths': '同花顺',
            'eastmoney': '东方财富',
        }
        # 模拟数据缓存
        self._stock_cache: Dict[str, pd.DataFrame] = {}
        self._concept_cache: Dict[str, pd.DataFrame] = {}
    
    async def get_stock_list(self, market='all', limit=100, offset=0):
        """获取股票列表
        
        Args:
            market: 市场类型 ('sh', 'sz', 'all')
            limit: 返回数量限制
            offset: 偏移量
            
        Returns:
            pandas DataFrame: 股票列表数据
        """
        try:
            # 模拟异步加载
            await asyncio.sleep(0.5)
            
            # 由于是演示，返回模拟数据
            stocks = []
            for i in range(limit):
                code = f"{random.choice(['600', '601', '000', '002'])}{random.randint(100, 999)}"
                name = f"股票{i + offset + 1}"
                market_type = 'sh' if code.startswith('6') else 'sz'
                
                if market == 'all' or market == market_type:
                    stocks.append({
                        'code': code,
                        'name': name,
                        'market': market_type,
                        'price': round(random.uniform(5, 100), 2),
                        'change_rate': round(random.uniform(-10, 10), 2)
                    })
            
            return pd.DataFrame(stocks)
        except Exception as e:
            print(f"获取股票列表失败: {str(e)}")
            return pd.DataFrame()
    
    async def get_stock_market_data(self, code, days=30):
        """获取股票行情数据
        
        Args:
            code: 股票代码
            days: 获取天数
            
        Returns:
            pandas DataFrame: 行情数据
        """
        try:
            # 模拟异步加载
            await asyncio.sleep(0.8)
            
            # 生成模拟的K线数据
            dates = pd.date_range(end=pd.Timestamp.now(), periods=days)
            
            # 生成随机价格数据，保持一定的连续性
            base_price = random.uniform(10, 50)
            prices = []
            current_price = base_price
            
            for date in dates:
                # 跳过非交易日（周末）
                if date.weekday() >= 5:
                    continue
                    
                change = random.uniform(-2, 2)
                current_price = max(1, current_price + change)
                prices.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(current_price, 2),
                    'high': round(current_price + random.uniform(0, 1), 2),
                    'low': round(current_price - random.uniform(0, 1), 2),
                    'close': round(current_price + random.uniform(-0.5, 0.5), 2),
                    'volume': random.randint(100000, 10000000)
                })
            
            return pd.DataFrame(prices)
        except Exception as e:
            print(f"获取股票行情数据失败: {str(e)}")
            return pd.DataFrame()
    
    def get_stock_data(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取指定股票在指定日期范围内的数据"""
        # 检查缓存
        cache_key = f"{stock_code}_{start_date}_{end_date}"
        if cache_key in self._stock_cache:
            return self._stock_cache[cache_key]
        
        # 模拟API调用延迟
        time.sleep(0.5)
        
        # 生成模拟数据
        # 计算日期范围
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        date_range = pd.date_range(start=start, end=end)
        
        # 生成基础价格
        base_price = random.uniform(10, 100)
        
        # 生成模拟数据
        data = []
        for date in date_range:
            # 跳过非交易日（周末）
            if date.weekday() >= 5:
                continue
                
            # 生成当天价格
            change = random.uniform(-2, 2)
            base_price = max(1, base_price + change)
            
            # 生成开盘价、最高价、最低价、收盘价
            open_price = round(base_price * random.uniform(0.98, 1.02), 2)
            close_price = round(open_price * random.uniform(0.95, 1.05), 2)
            high_price = round(max(open_price, close_price) * random.uniform(1.01, 1.03), 2)
            low_price = round(min(open_price, close_price) * random.uniform(0.97, 0.99), 2)
            
            # 生成成交量
            volume = round(random.uniform(10000, 10000000), 0)
            
            # 生成成交额
            amount = round(volume * close_price, 2)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': open_price,
                'close': close_price,
                'high': high_price,
                'low': low_price,
                'volume': volume,
                'amount': amount
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 缓存结果
        self._stock_cache[cache_key] = df
        
        return df
    
    async def get_concept_list(self, source: str = 'ths') -> pd.DataFrame:
        """获取概念板块列表"""
        # 检查缓存
        cache_key = f"concepts_{source}"
        if cache_key in self._concept_cache:
            return self._concept_cache[cache_key]
        
        # 模拟异步加载
        await asyncio.sleep(0.5)
        
        # 模拟概念板块数据
        concept_names = [
            '人工智能', '新能源汽车', '半导体', '光伏', '锂电池', 
            '5G通信', '生物医药', '芯片概念', '航天军工', '云计算',
            '区块链', '大数据', '元宇宙', '氢能源', '绿色电力',
            '机器人', '储能', '物联网', '国产软件', '智能驾驶'
        ]
        
        data = []
        for i, name in enumerate(concept_names):
            # 生成概念代码
            code = f"{source.upper()}_CONCEPT_{i:03d}"
            
            # 生成随机涨跌幅
            change = round(random.uniform(-8, 8), 2)
            
            # 生成包含股票数
            stock_count = random.randint(10, 100)
            
            # 生成平均价格
            avg_price = round(random.uniform(15, 80), 2)
            
            data.append({
                'concept_code': code,
                'concept_name': name,
                'change': change,
                'stock_count': stock_count,
                'avg_price': avg_price
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 缓存结果
        self._concept_cache[cache_key] = df
        
        return df
    
    async def get_concept_stocks(self, concept_code):
        """获取概念板块成分股
        
        Args:
            concept_code: 概念板块代码
            
        Returns:
            pandas DataFrame: 成分股列表
        """
        try:
            # 模拟异步加载
            await asyncio.sleep(0.5)
            
            # 模拟成分股数据
            stocks = []
            stock_count = random.randint(10, 30)
            
            for i in range(stock_count):
                code = f"{random.choice(['600', '601', '000', '002'])}{random.randint(100, 999)}"
                stocks.append({
                    'code': code,
                    'name': f"个股{i + 1}",
                    'price': round(random.uniform(5, 100), 2),
                    'change_rate': round(random.uniform(-10, 10), 2),
                    'volume_ratio': round(random.uniform(0.1, 3), 2)
                })
            
            return pd.DataFrame(stocks)
        except Exception as e:
            print(f"获取概念板块成分股失败: {str(e)}")
            return pd.DataFrame()
    
    def get_concept_constituents(self, concept_code: str, source: str = 'ths') -> pd.DataFrame:
        """获取概念板块包含的股票列表"""
        # 模拟API调用延迟
        time.sleep(0.5)
        
        # 模拟股票数据
        stock_prefixes = ['600', '601', '603', '000', '002', '300']
        industries = ['科技', '金融', '医药', '制造', '消费', '能源']
        
        data = []
        # 生成5-15只股票
        count = random.randint(5, 15)
        
        for i in range(count):
            # 生成股票代码
            prefix = random.choice(stock_prefixes)
            code = f"{prefix}{random.randint(100, 999)}"
            
            # 生成股票名称
            industry = random.choice(industries)
            name = f"{industry}{random.randint(100, 999)}"
            
            data.append({
                'stock_code': code,
                'stock_name': name
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        return df
    
    def get_stock_basic_info(self, stock_code: str) -> Dict:
        """获取股票基本信息"""
        # 模拟股票基本信息
        industries = ['科技', '金融', '医药', '制造', '消费', '能源']
        markets = ['上证', '深证', '创业板', '科创板']
        
        info = {
            'stock_code': stock_code,
            'stock_name': f"{random.choice(industries)}{random.randint(100, 999)}",
            'industry': random.choice(industries),
            'market': random.choice(markets),
            'list_date': f"20{random.randint(00, 22)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'total_share': round(random.uniform(1, 100), 2),
            'float_share': round(random.uniform(0.5, 90), 2),
            'pe': round(random.uniform(10, 100), 2),
            'pb': round(random.uniform(1, 10), 2),
            'eps': round(random.uniform(0.1, 5), 2)
        }
        
        return info
    
    def get_index_data(self, index_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取指数数据"""
        # 模拟指数数据
        # 计算日期范围
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        date_range = pd.date_range(start=start, end=end)
        
        # 生成基础点数
        base_point = random.uniform(2000, 5000)
        
        # 生成模拟数据
        data = []
        for date in date_range:
            # 跳过非交易日（周末）
            if date.weekday() >= 5:
                continue
                
            # 生成当天点数变化
            change = random.uniform(-50, 50)
            base_point = max(1000, base_point + change)
            
            # 生成开盘点、最高点、最低点、收盘点
            open_point = round(base_point * random.uniform(0.995, 1.005), 2)
            close_point = round(open_point * random.uniform(0.99, 1.01), 2)
            high_point = round(max(open_point, close_point) * random.uniform(1.001, 1.003), 2)
            low_point = round(min(open_point, close_point) * random.uniform(0.997, 0.999), 2)
            
            # 生成成交量
            volume = round(random.uniform(5000000, 50000000), 0)
            
            # 生成成交额
            amount = round(random.uniform(5000000000, 50000000000), 2)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': open_point,
                'close': close_point,
                'high': high_point,
                'low': low_point,
                'volume': volume,
                'amount': amount
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        return df
    
    def clear_cache(self):
        """清除缓存"""
        self._stock_cache.clear()
        self._concept_cache.clear()


class DataTransformer:
    """数据转换工具类"""
    
    @staticmethod
    def df_to_dict_list(df):
        """将DataFrame转换为字典列表
        
        Args:
            df: pandas DataFrame
            
        Returns:
            list: 字典列表
        """
        if df.empty:
            return []
        return df.to_dict('records')
    
    @staticmethod
    def format_number(value, decimals=2):
        """格式化数字
        
        Args:
            value: 数字值
            decimals: 小数位数
            
        Returns:
            str: 格式化后的字符串
        """
        if pd.isna(value):
            return '-'
        return f"{value:.{decimals}f}"
    
    @staticmethod
    def format_volume(volume):
        """格式化成交量
        
        Args:
            volume: 成交量
            
        Returns:
            str: 格式化后的字符串
        """
        if pd.isna(volume):
            return '-'
        if volume >= 100000000:
            return f"{volume/100000000:.2f}亿"
        elif volume >= 10000:
            return f"{volume/10000:.2f}万"
        return str(volume)


# 创建全局数据加载器实例
data_loader = DataLoader()


class DataLoader:
    """
    数据加载器类，负责从各种来源加载数据
    实际使用时，这里应该替换为真实的数据API调用
    """
    
    def __init__(self):
        """初始化数据加载器"""
        # 初始化数据源配置
        self.sources = {
            'ths': '同花顺',
            'eastmoney': '东方财富',
        }
        # 模拟数据缓存
        self._stock_cache: Dict[str, pd.DataFrame] = {}
        self._concept_cache: Dict[str, pd.DataFrame] = {}
    
    def get_stock_data(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取指定股票在指定日期范围内的数据
        实际使用时，这里应该调用真实的股票数据API
        
        Args:
            stock_code: 股票代码
            start_date: 开始日期，格式为'YYYY-MM-DD'
            end_date: 结束日期，格式为'YYYY-MM-DD'
            
        Returns:
            pd.DataFrame: 包含股票数据的DataFrame
        """
        # 检查缓存
        cache_key = f"{stock_code}_{start_date}_{end_date}"
        if cache_key in self._stock_cache:
            return self._stock_cache[cache_key]
        
        # 模拟API调用延迟
        time.sleep(0.5)
        
        # 生成模拟数据
        # 计算日期范围
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        date_range = pd.date_range(start=start, end=end)
        
        # 生成基础价格
        base_price = random.uniform(10, 100)
        
        # 生成模拟数据
        data = []
        for date in date_range:
            # 跳过非交易日（周末）
            if date.weekday() >= 5:
                continue
                
            # 生成当天价格
            change = random.uniform(-2, 2)
            base_price = max(1, base_price + change)
            
            # 生成开盘价、最高价、最低价、收盘价
            open_price = round(base_price * random.uniform(0.98, 1.02), 2)
            close_price = round(open_price * random.uniform(0.95, 1.05), 2)
            high_price = round(max(open_price, close_price) * random.uniform(1.01, 1.03), 2)
            low_price = round(min(open_price, close_price) * random.uniform(0.97, 0.99), 2)
            
            # 生成成交量
            volume = round(random.uniform(10000, 10000000), 0)
            
            # 生成成交额
            amount = round(volume * close_price, 2)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': open_price,
                'close': close_price,
                'high': high_price,
                'low': low_price,
                'volume': volume,
                'amount': amount
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 缓存结果
        self._stock_cache[cache_key] = df
        
        return df
    
    def get_concept_list(self, source: str = 'ths') -> pd.DataFrame:
        """
        获取概念板块列表
        实际使用时，这里应该调用真实的概念板块API
        
        Args:
            source: 数据源，如'ths'（同花顺）或'eastmoney'（东方财富）
            
        Returns:
            pd.DataFrame: 包含概念板块数据的DataFrame
        """
        # 检查缓存
        cache_key = f"concepts_{source}"
        if cache_key in self._concept_cache:
            return self._concept_cache[cache_key]
        
        # 模拟API调用延迟
        time.sleep(0.3)
        
        # 模拟概念板块数据
        concept_names = [
            '人工智能', '新能源汽车', '半导体', '光伏', '锂电池', 
            '5G通信', '生物医药', '芯片概念', '航天军工', '云计算',
            '区块链', '大数据', '元宇宙', '氢能源', '绿色电力',
            '机器人', '储能', '物联网', '国产软件', '智能驾驶'
        ]
        
        data = []
        for i, name in enumerate(concept_names):
            # 生成概念代码
            code = f"{source.upper()}_CONCEPT_{i:03d}"
            
            # 生成随机涨跌幅
            change = round(random.uniform(-8, 8), 2)
            
            # 生成包含股票数
            stock_count = random.randint(10, 100)
            
            # 生成平均价格
            avg_price = round(random.uniform(15, 80), 2)
            
            data.append({
                'concept_code': code,
                'concept_name': name,
                'change': change,
                'stock_count': stock_count,
                'avg_price': avg_price
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 缓存结果
        self._concept_cache[cache_key] = df
        
        return df
    
    def get_concept_constituents(self, concept_code: str, source: str = 'ths') -> pd.DataFrame:
        """
        获取概念板块包含的股票列表
        实际使用时，这里应该调用真实的概念成分股API
        
        Args:
            concept_code: 概念代码
            source: 数据源
            
        Returns:
            pd.DataFrame: 包含概念成分股数据的DataFrame
        """
        # 模拟API调用延迟
        time.sleep(0.5)
        
        # 模拟股票数据
        stock_prefixes = ['600', '601', '603', '000', '002', '300']
        industries = ['科技', '金融', '医药', '制造', '消费', '能源']
        
        data = []
        # 生成5-15只股票
        count = random.randint(5, 15)
        
        for i in range(count):
            # 生成股票代码
            prefix = random.choice(stock_prefixes)
            code = f"{prefix}{random.randint(100, 999)}"
            
            # 生成股票名称
            industry = random.choice(industries)
            name = f"{industry}{random.randint(100, 999)}"
            
            data.append({
                'stock_code': code,
                'stock_name': name
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        return df
    
    def get_stock_basic_info(self, stock_code: str) -> Dict:
        """
        获取股票基本信息
        实际使用时，这里应该调用真实的股票信息API
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Dict: 包含股票基本信息的字典
        """
        # 模拟股票基本信息
        industries = ['科技', '金融', '医药', '制造', '消费', '能源']
        markets = ['上证', '深证', '创业板', '科创板']
        
        info = {
            'stock_code': stock_code,
            'stock_name': f"{random.choice(industries)}{random.randint(100, 999)}",
            'industry': random.choice(industries),
            'market': random.choice(markets),
            'list_date': f"20{random.randint(00, 22)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'total_share': round(random.uniform(1, 100), 2),
            'float_share': round(random.uniform(0.5, 90), 2),
            'pe': round(random.uniform(10, 100), 2),
            'pb': round(random.uniform(1, 10), 2),
            'eps': round(random.uniform(0.1, 5), 2)
        }
        
        return info
    
    def get_index_data(self, index_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取指数数据
        实际使用时，这里应该调用真实的指数数据API
        
        Args:
            index_code: 指数代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            pd.DataFrame: 包含指数数据的DataFrame
        """
        # 模拟指数数据
        # 计算日期范围
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        date_range = pd.date_range(start=start, end=end)
        
        # 生成基础点数
        base_point = random.uniform(2000, 5000)
        
        # 生成模拟数据
        data = []
        for date in date_range:
            # 跳过非交易日（周末）
            if date.weekday() >= 5:
                continue
                
            # 生成当天点数变化
            change = random.uniform(-50, 50)
            base_point = max(1000, base_point + change)
            
            # 生成开盘点、最高点、最低点、收盘点
            open_point = round(base_point * random.uniform(0.995, 1.005), 2)
            close_point = round(open_point * random.uniform(0.99, 1.01), 2)
            high_point = round(max(open_point, close_point) * random.uniform(1.001, 1.003), 2)
            low_point = round(min(open_point, close_point) * random.uniform(0.997, 0.999), 2)
            
            # 生成成交量
            volume = round(random.uniform(5000000, 50000000), 0)
            
            # 生成成交额
            amount = round(random.uniform(5000000000, 50000000000), 2)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': open_point,
                'close': close_point,
                'high': high_point,
                'low': low_point,
                'volume': volume,
                'amount': amount
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        return df
    
    def clear_cache(self):
        """清除缓存"""
        self._stock_cache.clear()
        self._concept_cache.clear()


# 创建全局数据加载器实例
data_loader = DataLoader()