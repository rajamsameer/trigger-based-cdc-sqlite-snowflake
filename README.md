# Real-Time Data Synchronization: Trigger-Based CDC from SQLite to Snowflake

## Overview

This project implements a **real-time data synchronization pipeline** using **Trigger-Based Change Data Capture (CDC)** from an **SQLite** database to **Snowflake**. The pipeline utilizes **Python** for the ETL process, with **Streamlit** dashboards for live data visualization.

### Key Technologies:
- **SQLite**: Source database.
- **Snowflake**: Target data warehouse for analytics.
- **Python**: ETL logic, including data extraction, transformation, and loading.
- **Streamlit**: Interactive dashboard for visualizing the synchronized data.

## Features

- **Real-time data capture**: The system uses **triggers** in SQLite to capture data changes (inserts, updates, deletes) in real time.
- **Snowflake Integration**: Automatically loads the captured changes into Snowflake for analytics.
- **Streamlit Dashboard**: Visualizes the data in a user-friendly interface, enabling monitoring and insights.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- SQLite (for local development)
- Snowflake account and credentials
- Streamlit (for dashboard visualization)
  



