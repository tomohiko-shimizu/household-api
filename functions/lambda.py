import json
import pymysql
import os

db_host = os.environ['DBHost']
db_port = int(os.environ['DBPort'])
db_user = os.environ['DBUser']
db_password = os.environ['DBPassword']
db_name = os.environ['DBName']

def get_connection():
    return pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db_name)
def list_revenue(event, context):
    conn = get_connection()
    query = """
    SELECT
        JSON_ARRAYAGG(d)
    FROM
    (SELECT
      JSON_OBJECT(
            'id',
            r.id,
            'category',
            rc.category_name,
            'category_id',
            rc.id,
            'date',
            r.date,
            'price',
            r.price,
            'detail',
            r.detail
        
      ) as d
    FROM revenue r
    INNER JOIN
        revenue_category rc
    ON
        r.category_id = rc.id
    ORDER BY r.date DESC) t;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchone()
    return  {"statusCode": 200, "body": data[0]}

def put_revenue(event, context):
    put_data = json.loads(event['body'])
    unset_require_params = {'category_id', 'price', 'date'} - put_data.keys()
    if (len(unset_require_params) > 0):
        return {"statusCode": 400, "body": ','.join(unset_require_params)}
    if "detail" not in put_data:
        put_data["detail"] = None
    print(put_data)
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    insert into revenue(
        category_id, 
        price, 
        date,
        detail
    ) VALUES(
        %(category_id)s, 
        %(price)s, 
        %(date)s,
        %(detail)s
    );
    """
    cursor.execute(query, put_data)
    conn.commit()
    conn.close()
    return  {"statusCode": 200}

def list_revenue_category(event, context):
    conn = get_connection()
    query = """
    SELECT
        JSON_ARRAYAGG(d)
    FROM
    (SELECT
        JSON_OBJECT(
            'id',
            id,
            'category_name',
            category_name
        ) AS d
    FROM
        revenue_category
    ORDER BY id ASC) t;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchone()
    return  {"statusCode": 200, "body": data[0]}

def list_expense(event, context):
    conn = get_connection()
    query = """
        SELECT
            JSON_ARRAYAGG(d)
        FROM
        (select 
            JSON_OBJECT(
                "id",
                e.id,
                "category",
                ec.category_name,
                "category_detail",
                ecd.category_detail_name,
                "category_id",
                ec.id,
                "category_detail_id",
                ecd.id,
                "detail",
                e.detail,
                "date",
                e.date,
                "price",
                e.price,
                "place",
                e.place
            ) AS d
        from 
            expense e 
        INNER JOIN expense_category_detail ecd 
            ON e.category_detail_id = ecd.id 
        INNER JOIN expense_category ec 
            ON ecd.category_id = ec.id
        ORDER 
            BY e.date ASC) t;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchone()
    return  {"statusCode": 200, "body": data[0]}

def put_expense(event, context):
    put_data = json.loads(event['body'])
    unset_require_params = {'category_detail_id', 'price', 'date'} - put_data.keys()
    if len(unset_require_params) > 0:
        return {"statusCode": 400, "body": ','.join(unset_require_params + ' is not set')}
    if "detail" not in put_data:
        put_data["detail"] = None
    if "place" not in put_data:
        put_data["place"] = None
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    insert into expense(
        category_detail_id, 
        price, 
        date,
        detail,
        place
    ) VALUES(
        %(category_detail_id)s, 
        %(price)s, 
        %(date)s,
        %(detail)s,
        %(place)s
    );
    """
    cursor.execute(query, put_data)
    conn.commit()
    conn.close()
    return  {"statusCode": 200}

def list_expense_category(event, context):
    conn = get_connection()
    query = """
    SELECT
        JSON_ARRAYAGG(d)
    FROM
    (
        SELECT
            JSON_OBJECT(
                'id',
                ec.id,
                'category_name',
                category_name,
                'category_detail',
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'id',
                        ecd.id,
                        'category_detail',
                        ecd.category_detail_name
                    )
                )
            ) AS d
        FROM
            expense_category ec
        INNER JOIN
            expense_category_detail ecd
        ON ec.id = ecd.category_id
        GROUP BY ec.id, category_name
    ) t
    """
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchone()
    return  {"statusCode": 200, "body": data[0]}

