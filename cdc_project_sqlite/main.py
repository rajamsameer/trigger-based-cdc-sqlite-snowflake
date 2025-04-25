from extract_cdc import extract_cdc_data
from load_to_snowflake import load_to_snowflake

def run_cdc_pipeline():
    print("Extracting CDC data from SQLite...")
    changes = extract_cdc_data()
    
    if changes:
        print(f"Found {len(changes)} changes. Loading into Snowflake...")
        load_to_snowflake(changes)
        print("CDC Data loaded successfully!")
    else:
        print("No new changes detected.")

if __name__ == "__main__":
    run_cdc_pipeline()



# from extract_cdc import extract_changes
# from load_to_snowflake import load_to_snowflake

# if __name__ == "__main__":
#     changes = extract_changes()
#     load_to_snowflake(changes)
#     print("✅ CDC sync complete.")
