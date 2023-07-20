# umapyoiの共通ライブラリ

## logger

### 使い方

```python
import os
from umalib.logger import getlogger
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
logger=getlogger(__name__,LOG_LEVEL)

logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
```

## database

### 使い方

```python
import os
from umalib.database import MysqlOperator
DB_HOST = os.environ["DB_HOST"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_USERNAME = os.environ["DB_USERNAME"]
connection=MysqlOperator(DB_HOST,DB_PASSWORD,DB_USERNAME,"horsetable")

connection.insert(data_dict={"col1":1,"col2":"aaa"}, table_name="BUY")
connection.insert(data_dict=[{"col1":1,"col2":"aaa"},{"col1":2,"col2":"bbb"}], table_name="BUY")
# 以下は面倒なのでコードを参照してください
connection.select:dict
connection.select:list
connection.update
connection.select_where
connection.exec_sql
```
