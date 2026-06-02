import os
import sqlalchemy
from sqlalchemy import text
from tqdm import tqdm
import os


def get_records(start_time, end_time, position=None):
    sqluser = os.environ["sqluser"]
    sqlpass = os.environ["sqlpass"]
    sql_url = f'mysql+mysqldb://{sqluser}:{sqlpass}@127.0.0.1:3306/vision_backend'
    start_date = start_time
    end_date = end_time

    engine = sqlalchemy.create_engine(sql_url, poolclass=sqlalchemy.pool.NullPool)
    connection = engine.connect()

    # Select
    sql = f'select * from product_detection_detail_result where c_time between "{start_date}" and "{end_date}"'
    if position is not None:
        sql += f" and position='{position}'"
        pass

    result = connection.execute(text(
        sql))
    
    return result.mappings().all()
    pass
