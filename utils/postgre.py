import psycopg2


class DBOperation:
    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(DBOperation, self).__new__(self)
            print("Create class.")
            self.conn = psycopg2.connect(
                host="192.168.26.101",
                database="aiagent",
                user="aiagent",
                password="mypassword"
            )
        return self._instance

    def get_component_list(self, component) -> list:
        sql = "select component_name from aiagent_schema.component_relations where component_name = %s"
        component_list = []
        # if component != None:
        #     sql = sql + " and component_name=\'" + component + "\';"
        # else:
        #     sql = sql + ";"
        cursor = self.conn.cursor()
        print(sql)
        cursor.execute(sql, (component,))
        rows = cursor.fetchall()
        for row in rows:
            component_list.append(row)
        cursor.close()
        return component_list

#dboperation = DBOperation()
#dboperation.get_component_list("xrcd_payload")