# 解决某一对象不能被json序列化的问题
class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()

            if isinstance(obj, InsuranceCompany):
                return obj.to_dict()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


# 传入还有多个字典对象的list,返回给你一个excel的文件流
def create_excel(xlsdate, onelist, fields_list):
        """
        生成表格
        :param xlsdate: excel名称 
        :param onelist: list[dict]
        :param fields_list: list[dict.keys]
        :return: excel文件流
        """ 
        filename = xlsdate
        fp = io.BytesIO()
        # workbook = xlwt.Workbook(fp)
        workbook = xlsxwriter.Workbook(fp)
        no_book_sheet = workbook.add_worksheet(name="订单")
        for field in range(0, len(fields_list)):
            no_book_sheet.write(0, field, fields_list[field])

        for row in range(1, len(onelist) + 1):
            for col in range(0, len(fields_list)):
                no_book_sheet.write(row, col, u'%s' % onelist[row-1].get(fields_list[col]))

        workbook.close()
        fp.seek(0)
        return (fp,filename)
        # return (workbook,filename)
        
        
# 给models类添加to_dict()方法，使使用属性更方便
 def to_dict(self):
        column_name_list = [
            value[0] for value in self._sa_instance_state.attrs.items()
        ]
        return dict(
            (column_name, getattr(self, column_name, None)) \
            for column_name in column_name_list
        )
        
 
# 同步models类
sqlacodegen  "mysql+pymysql://username:password@host/db_name" > model.py
