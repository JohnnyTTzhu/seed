import re
import json

from seed.libs.data_access.formatters.base import BaseFormatter


class TableFormatter(BaseFormatter):
    def __init__(self, *args, **kwargs):
        super(TableFormatter, self).__init__(*args, **kwargs)

    def format_data(self):
        # table_keys = self.title_flags + [*self.dims_set.keys()]
        table_keys = [item['dimension'] for item in self.dimensions] + [item['index'] for item in self.indexs]

        # 得到table的表格数据
        table_datas = self._convert_table_data(table_keys, self.data)

        # 对表格数据进行排序
        table_datas = self._sort_table_column(table_datas)

        # 处理比率类型数据
        # table_datas = self._convert_rate_data(table_keys, table_datas)

        # 得到table的显示项
        display_name = self._get_display_name(table_keys)

        return {"data": table_datas, "displayName": display_name}

    def _convert_table_data(self, table_keys, datas):
        # 将数据从中间格式转换成表格格式
        table_datas = []

        for key, values in datas.items():
            values.update(json.loads(key))
            row = {}
            for key in table_keys:
                row[key] = values.get(key, '-')

            table_datas.append(row)

        return table_datas

    def _sort_table_column(self, data):
        # TODO 进行table类型的排序

        order_fields = [item['dimension'] for item in self.dimensions] + [item['index'] for item in self.indexs]

        # 改成按多种排序
        data = sorted(
            data,
            key=lambda k: [(k[order_field] if k[order_field] else 0) for order_field in order_fields],
            reverse=True
        )

        return data

    # def _convert_rate_data(self, table_keys, datas):
    #     """处理比率类型指标的数据"""
    #     table_datas = []

    #     for data in datas:
    #         row = {}
    #         for index in self.indexs:
    #             row[key] = format_data(index['rate'], data.get(key, '-'))

    #         table_datas.append(row)

    #     return table_datas

    def _get_display_name(self, keys):
        # 获取displayName格式的数据显示
        titles = []

        dim_display_map = {}

        for item in self.dimensions:
            dim_display_map[item['dimension']] = item['name']

        for item in self.indexs:
            dim_display_map[item['index']] = item['name']

        for key in keys:
            titles.append({"name": key, "displayName": dim_display_map[key]})

        return titles