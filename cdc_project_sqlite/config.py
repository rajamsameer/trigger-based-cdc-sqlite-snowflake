import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Path to your SQLite database
SQLITE_DB_PATH = "cdc_database.db"

# Snowflake connection configuration
SNOWFLAKE_CONFIG = {
    "user": os.getenv("SNOWFLAKE_USER"),             # SAMEER423
    "password": os.getenv("SNOWFLAKE_PASSWORD"),     # S@meer423
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),       # SVTTSFN-SF71117
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),   # COMPUTE_WH
    "database": os.getenv("SNOWFLAKE_DATABASE"),     # SNOWFLAKE
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),         # ACCOUNT_USAGE
}
