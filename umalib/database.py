import logging
import certifi
import pymysql
import pymysql.cursors

class MysqlOperator:
    def __init__(self, DB_HOST: str, DB_USERNAME: str, DB_PASSWORD: str, database: str, logger: logging.Logger):
        self._host = DB_HOST
        self._username = DB_USERNAME
        self._password = DB_PASSWORD
        self._database = database
        self.logger = logger

    def insert(self, data_dict: dict | list, table_name: str) -> bool:
        connection = pymysql.connect(
            host=self._host,
            user=self._username,
            password=self._password,
            database=self._database,
            ssl={
                'ca': certifi.where(),
            },
            cursorclass=pymysql.cursors.DictCursor,
        )
        if isinstance(data_dict, dict):
            try:
                column_name_list = [f"`{key}`" for key in data_dict.keys()]
                columns_name = ", ".join(column_name_list)
                replacement = ", ".join(["%s"] * len(column_name_list))
                sql = f"INSERT INTO `{table_name}` ({columns_name}) VALUES ({replacement})"
                with connection, connection.cursor() as cursor:
                    cursor.execute(sql, list(data_dict.values()))
                    connection.commit()
                return True
            except pymysql.err.IntegrityError as error:
                self.logger.error("Error was happened.")
                self.logger.error(error)
                return False
            except pymysql.err.OperationalError as error:
                self.logger.error("Error was happened.")
                self.logger.error(error)
                return False
        elif isinstance(data_dict, list):
            try:
                column_name_list = [f"`{key}`" for key in data_dict[0].keys()]
                columns_name = ", ".join(column_name_list)
                replacement = "(" + ", ".join(["%s"] * len(column_name_list)) + ")"
                replacement_list = [replacement] * len(data_dict)
                multi_replacement = ",".join(replacement_list)
                sql = f"""
                INSERT INTO `{table_name}` ({columns_name}) 
                    VALUES {multi_replacement}
                """
                all_values = []
                for data in data_dict:
                    all_values.extend(list(data.values()))
                with connection, connection.cursor() as cursor:
                    cursor.execute(sql, all_values)
                    connection.commit()
                return True
            except pymysql.err.IntegrityError as error:
                self.logger.error("Error was happened.")
                self.logger.error(error)
                return False
            except pymysql.err.OperationalError as error:
                self.logger.error("Error was happened.")
                self.logger.error(error)
                return False
        else:
            raise TypeError("Invalid type was specified as 'data_dict'")

    def select(self, columns: str | list, table_name: str) -> dict:
        columns_str = ""
        if isinstance(columns, str):
            columns_str = f"`{columns}`"
            column_list = [columns]
        else:
            columns_str = ", ".join([f"`{column}`" for column in columns])
            column_list = columns

        try:
            sql = f"SELECT {columns_str} FROM `{table_name}`"
            results = self.exec_sql(sql)
            select_result = {}
            for result in results:
                for column in column_list:
                    if column not in select_result:
                        select_result[column] = [result[column]]
                    else:
                        select_result[column].append(result[column])
            return select_result
        except Exception as error:
            self.logger.error("Error was happened.")
            self.logger.error(error)
            return {}

    def update(self, data: dict, table_name: str, **kwargs):
        key_list = []
        val_list = []

        update_list = []
        for key, value in data.items():
            update_list.append(f"{key}=%s")
            val_list.append(value)
        update_sentence = ",".join(update_list)

        for key, value in kwargs.items():
            key_list.append(f"{key}=%s")
            val_list.append(value)
        where_sentence = " AND ".join(key_list)

        sql = f"UPDATE {table_name} SET {update_sentence} WHERE {where_sentence}"
        result = self.exec_sql(sql=sql, value=val_list)
        return result

    def select_where(self, conditions, columns, table):
        if isinstance(columns, list):
            column_str = ", ".join(columns)
        elif isinstance(columns, str):
            column_str = columns
        else:
            raise TypeError("The type of value columns must be list or str.")
        sql = f"SELECT {column_str} FROM {table} WHERE {conditions}"
        results = self.exec_sql(sql)
        return results

    def exec_sql(self, sql, value=None):
        connection = pymysql.connect(
            host=self._host,
            user=self._username,
            password=self._password,
            database=self._database,
            cursorclass=pymysql.cursors.DictCursor,
        )
        if value is None:
            with connection, connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                connection.commit()
        else:
            with connection, connection.cursor() as cursor:
                cursor.execute(sql, value)
                results = cursor.fetchall()
                connection.commit()
        return results
