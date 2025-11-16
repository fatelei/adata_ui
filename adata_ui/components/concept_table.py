# 概念表格组件
from nicegui import ui, app


def create_concept_table():
    """
    创建概念列表表格组件
    返回表格实例，方便后续更新数据
    """
    # 创建表格组件 - 改进样式和交互
    table = ui.table(columns=[
        {'name': 'concept_code', 'label': '概念代码', 'field': 'concept_code', 'required': True},
        {'name': 'concept_name', 'label': '概念名称', 'field': 'concept_name', 'required': True},
        {'name': 'change', 'label': '涨跌幅', 'field': 'change', 'required': True},
        {'name': 'stock_count', 'label': '包含股票数', 'field': 'stock_count', 'required': True},
        {'name': 'avg_price', 'label': '平均价格', 'field': 'avg_price', 'required': True},
        {'name': 'action', 'label': '操作', 'field': 'action', 'required': True}
    ], rows=[]).classes('w-full').props('dense').style('border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05);')
    
    # 自定义表头样式
    table.add_slot('header', '''
        <thead class="bg-gradient-to-r from-indigo-50 to-purple-50">
            <tr>
                <th v-for="col in props.cols" :key="col.name" :props="col.props" class="font-medium text-left px-4 py-3 text-gray-700 whitespace-nowrap">
                    {{ col.label }}
                </th>
            </tr>
        </thead>
    ''')
    
    # 自定义行样式和交互效果
    table.add_slot('body', '''
        <tbody>
            <tr v-for="(row, idx) in props.rows" :key="idx" 
                :class="['hover:bg-indigo-50 transition-all duration-150', 
                        idx % 2 === 0 ? 'bg-white' : 'bg-gray-50']">
                <td v-for="col in props.cols" :key="col.name" :props="getCellProps(row, col, idx)">
                    <slot :name="`body-cell-${col.name}`" :props="getCellProps(row, col, idx)">
                        {{ col.formatter ? col.formatter(row[col.field], row) : row[col.field] }}
                    </slot>
                </td>
            </tr>
        </tbody>
    ''')
    
    # 自定义涨跌幅单元格样式 - 增加字体粗细
    table.add_slot('body-cell-change', '''
        <td :props="props">
            <span :style="{fontWeight: '600', color: props.value > 0 ? '#ff4d4f' : props.value < 0 ? '#52c41a' : '#666'}">
                {{ props.value > 0 ? '+' : '' }}{{ props.value }}%
            </span>
        </td>
    ''')
    
    # 自定义其他单元格样式 - 增加字体粗细和样式
    table.add_slot('body-cell-concept_code', '''
        <td :props="props">
            <span style="font-weight: '500'; color: '#4b5563';">
                {{ props.value }}
            </span>
        </td>
    ''')
    
    table.add_slot('body-cell-concept_name', '''
        <td :props="props">
            <span style="font-weight: '600'; color: '#1f2937'; font-size: 1em;">
                {{ props.value }}
            </span>
        </td>
    ''')
    
    table.add_slot('body-cell-stock_count', '''
        <td :props="props">
            <span style="font-weight: '500';">
                {{ props.value }}
            </span>
        </td>
    ''')
    
    table.add_slot('body-cell-avg_price', '''
        <td :props="props">
            <span style="font-weight: '500';">
                {{ props.value.toFixed(2) }}
            </span>
        </td>
    ''')
    
    # 自定义操作列 - 改进按钮样式和交互
    table.add_slot('body-cell-action', '''
        <td :props="props">
            <div class="flex gap-2">
                <button @click="() => viewConceptDetail(props.row.concept_code, props.row.concept_name)" 
                      class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1.5 text-sm rounded-full transition-all duration-200 shadow-sm hover:shadow flex items-center justify-center">
                    查看详情
                </button>
            </div>
        </td>
    ''')
    
    # 注册JavaScript函数调用Python函数
    ui.run_javascript('''
    window.viewConceptDetail = (code, name) => {
        app.storage.general.view_concept_detail(code, name);
    }
    ''')
    
    return table