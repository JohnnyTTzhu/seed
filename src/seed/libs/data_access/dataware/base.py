class DataModel(object):
    def __init__(self, db, sql, query, dimensions, indexs):
        self.db = db
        self.sql = sql
        self.query = query
        self.dimensions = dimensions
        self.indexs = indexs
        self.gen_sql()

    def gen_sql(self):
        """ 用维度和指标把SQL包一层
        """
        select_fileds = [item['dimension'] for item in self.dimensions]\
            + [item['index'] for item in self.indexs]
        self.sql = """
            SELECT
                {select_fileds}
            FROM (
                {origin_sql}
            ) a
        """.format(select_fileds=','.join(select_fileds), origin_sql=self.sql)

    def format_sql(self):

        for key, value in self.query.items():
            if isinstance(value, list):
                self.query[key] = '(%s)' % ', '.join([str(item) for item in value])

        return self.sql.format(**self.query)

    def query_data(self):
        sql = self.format_sql()
        print(sql)
        return self.db.query(sql), sql