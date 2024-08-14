import snowflake.connector as sf
import pandas as pd

#SF_USER = 'SRIMATHI'
#SF_PASSWORD = 'Shri@1608'
#SF_ACCOUNT = 'wu16729.ap-southeast-1'
#SF_WAREHOUSE = 'COMPUTE_WH'
#SF_DATABASE = 'MEC'
#SF_SCHEMA = 'MEC'
#SF_ROLE = 'ACCOUNTADMIN'

SF_USER = 'SHYAAM'
SF_PASSWORD = 'Shyaamkumar@31'
SF_ACCOUNT = 'oy99057.ap-southeast-1'
SF_WAREHOUSE = 'COMPUTE_WH'
SF_DATABASE = 'MEC'
SF_SCHEMA = 'MEC2'
SF_ROLE = 'ACCOUNTADMIN'

def execute_mysql_query(sql):
    try:
        # Establish connection
        conn = sf.connect(
            user=SF_USER,
            password=SF_PASSWORD,
            account=SF_ACCOUNT,
            warehouse=SF_WAREHOUSE,
            database=SF_DATABASE,
            schema=SF_SCHEMA,
            role=SF_ROLE
        )
        print("Connection established")

        # Execute query
        cursor = conn.cursor()
        cursor.execute(sql)
        
        # Fetch results
        results = cursor.fetchall()

        # Get column names
        columns = [col[0] for col in cursor.description]
        
        # Handle duplicate column names
        column_counts = {}
        new_columns = []
        for col in columns:
            if col in column_counts:
                column_counts[col] += 1
                new_columns.append(f"{col}_{column_counts[col]}")
            else:
                column_counts[col] = 0
                new_columns.append(col)
        
        # Create DataFrame with unique column names
        df = pd.DataFrame(results, columns=new_columns)

        # Close cursor and connection
        cursor.close()
        conn.close()

        return df

    except sf.Error as e:
        e=str(e)
        if "Numeric value" in e:
            return f"An error occurred: {e}"
        elif "Duplicate Column" in e:
            return "Try to be more specific since the required tables contain duplicate columns"
        else:
            return f"An error occurred: {e}"