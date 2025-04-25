# import streamlit as st
# import snowflake.connector
# import pandas as pd
# import os
# from dotenv import load_dotenv
# import json

# # Load env
# load_dotenv()

# # Connect to Snowflake
# conn = snowflake.connector.connect(
#     user=os.getenv("SNOWFLAKE_USER"),
#     password=os.getenv("SNOWFLAKE_PASSWORD"),
#     account=os.getenv("SNOWFLAKE_ACCOUNT"),
#     warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
#     database=os.getenv("SNOWFLAKE_DATABASE"),
#     schema=os.getenv("SNOWFLAKE_SCHEMA"),
# )

# # Load data
# def load_data():
#     cur = conn.cursor()
#     cur.execute("SELECT operation, new_data, old_data, changed_by, changed_at FROM user_changes ORDER BY changed_at DESC")
#     rows = cur.fetchall()
#     columns = [col[0] for col in cur.description]
#     df = pd.DataFrame(rows, columns=columns)
#     return df

# # App UI
# st.set_page_config("CDC Dashboard", layout="wide")
# st.title("📊 Change Data Capture Dashboard")

# df = load_data()

# # Filter
# ops = st.multiselect("Filter by Operation", ["INSERT", "UPDATE", "DELETE"], default=["INSERT", "UPDATE", "DELETE"])
# filtered = df[df["OPERATION"].isin(ops)]

# # Display table
# st.subheader("Change Logs")
# st.dataframe(filtered)

# # Show prettified JSON
# def format_json(row):
#     try:
#         return json.dumps(row, indent=2)
#     except:
#         return str(row)

# filtered["new_data"] = filtered["NEW_DATA"].apply(lambda x: format_json(json.loads(x)) if x else "")
# filtered["old_data"] = filtered["OLD_DATA"].apply(lambda x: format_json(json.loads(x)) if x else "")

# with st.expander("📄 JSON View"):
#     for _, row in filtered.iterrows():
#         st.markdown(f"### {row['OPERATION']} @ {row['CHANGED_AT']}")
#         st.code(f"New:\n{row['new_data']}\n\nOld:\n{row['old_data']}", language="json")

# # Chart
# st.subheader("🔢 Operation Breakdown")
# st.bar_chart(filtered["OPERATION"].value_counts())




import streamlit as st
import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv
import json
import plotly.express as px  # <-- added

# Load env
load_dotenv()

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)

# Load data
def load_data():
    cur = conn.cursor()
    cur.execute("SELECT operation, new_data, old_data, changed_by, changed_at FROM user_changes ORDER BY changed_at DESC")
    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]
    df = pd.DataFrame(rows, columns=columns)
    return df

# App UI
st.set_page_config("CDC Dashboard", layout="wide")
st.title("📊 Change Data Capture Dashboard")

df = load_data()

# Filter
ops = st.multiselect("Filter by Operation", ["INSERT", "UPDATE", "DELETE"], default=["INSERT", "UPDATE", "DELETE"])
filtered = df[df["OPERATION"].isin(ops)]

# Display table
st.subheader("Change Logs")
st.dataframe(filtered)

# Show prettified JSON
def format_json(row):
    try:
        return json.dumps(row, indent=2)
    except:
        return str(row)

filtered["new_data"] = filtered["NEW_DATA"].apply(lambda x: format_json(json.loads(x)) if x else "")
filtered["old_data"] = filtered["OLD_DATA"].apply(lambda x: format_json(json.loads(x)) if x else "")

with st.expander("📄 JSON View"):
    for _, row in filtered.iterrows():
        st.markdown(f"### {row['OPERATION']} @ {row['CHANGED_AT']}")
        st.code(f"New:\n{row['new_data']}\n\nOld:\n{row['old_data']}", language="json")

# Donut Chart
st.subheader("🧁 Operation Breakdown (Percentage)")

op_counts = filtered["OPERATION"].value_counts()
op_percent = op_counts / op_counts.sum() * 100
op_df = op_percent.reset_index()
op_df.columns = ["Operation", "Percentage"]

fig = px.pie(
    op_df,
    values="Percentage",
    names="Operation",
    hole=0.5,
    title="INSERT / UPDATE / DELETE Breakdown",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig.update_traces(textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

