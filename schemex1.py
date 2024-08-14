from sqlalchemy import create_engine, inspect
from sqlalchemy.engine.url import URL
import snowflake.connector as sf

SF_USER = 'SHYAAM'
SF_PASSWORD = 'Shyaamkumar@31'
SF_ACCOUNT = 'oy99057.ap-southeast-1'
SF_WAREHOUSE = 'COMPUTE_WH'
SF_DATABASE = 'MEC'
SF_SCHEMA = 'MEC2'  
SF_ROLE = 'ACCOUNTADMIN'

# Function to create SQLAlchemy engine for Snowflake
def connect_to_snowflake(user, password, account, warehouse, database, schema, role):
    try:
        # Create connection string using URL.create
        connection_string = URL.create(
            drivername='snowflake',
            username=user,
            password=password,
            host=f'{account}',  # Use account name without .snowflakecomputing.com
            database=database,
            query={
                'warehouse': warehouse,
                'schema': schema,
                'role': role
            }
        )
        # Create the SQLAlchemy engine
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"Error creating Snowflake engine: {e}")
        raise

# Function to retrieve schema information using SQLAlchemy engine
def get_schema_info(engine):
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        schema_info = {}

        for table in tables:
            columns = inspector.get_columns(table)
            schema_info[table] = {col['name']: str(col['type']) for col in columns}
        
        return schema_info
    except Exception as e:
        print(f"Error retrieving schema info: {e}")
        raise

def convert_schema(schema):
    type_mapping = {
        'DECIMAL': 'NUMBER',
        'VARCHAR': 'VARCHAR',
        'DATE': 'DATE',
        'TIMESTAMP': 'TIMESTAMP',
        'TIME': 'TIME'
    }

    converted_schema = {}

    for table_name, columns in schema.items():
        formatted_columns = []
        for column_name, column_type in columns.items():
            # Capitalize the first letter of each column name
            formatted_column_name = column_name.capitalize()

            # Determine the new data type
            new_type = 'UNKNOWN'
            for key in type_mapping:
                if key in column_type.upper():
                    new_type = type_mapping[key]
                    break

            # Append the formatted column string
            formatted_columns.append(f"{formatted_column_name} {new_type}")

        # Join columns and create final formatted schema
        formatted_schema = f"({', '.join(formatted_columns)})"
        converted_schema[table_name] = formatted_schema

    return converted_schema

def schemex():
    # Connect to Snowflake using SQLAlchemy
    engine = connect_to_snowflake(SF_USER, SF_PASSWORD, SF_ACCOUNT, SF_WAREHOUSE, SF_DATABASE, SF_SCHEMA, SF_ROLE)

    # Retrieve schema information
    schema_info = get_schema_info(engine)
    ex = ""
    # Convert and print schema information
    converted_schema = convert_schema(schema_info)
    for table_name, schema in converted_schema.items():
        ex+=(f"{table_name}{schema}\n")
    return ex
print(schemex())