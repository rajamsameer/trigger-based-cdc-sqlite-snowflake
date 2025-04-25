# import snowflake.connector
# from config import SNOWFLAKE_CONFIG

# def load_to_snowflake(changes):
#     conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
#     cursor = conn.cursor()

#     for change in changes:
#         cursor.execute("""
#             INSERT INTO user_changes_snowflake (operation, changed_data, changed_at)
#             VALUES (%s, %s, %s)
#         """, (change['operation'], change['changed_data'], change['changed_at']))

#     conn.commit()
#     cursor.close()
#     conn.close()




import json
import snowflake.connector
from config import SNOWFLAKE_CONFIG

def load_to_snowflake(changes):
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO USER_CHANGES_SNOWFLAKE (operation, changed_data, changed_at)
        SELECT %s, TO_VARIANT(PARSE_JSON(%s)), %s
    """

    for row in changes:
        json_data = json.dumps(row["changed_data"], separators=(",", ":"))  # compact JSON
        cursor.execute(
            insert_query,
            (
                row["operation"],
                json_data,
                row["changed_at"]
            )
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data inserted into Snowflake successfully.")






