from openai import AzureOpenAI
import pandas as pd
import json
from sqlalchemy import create_engine
import os

# DB connection string
db_uri = "postgresql://ITCUSR:Ol652vc61R6W@172.24.2.108:5432/itc_db"
engine = create_engine(db_uri)


def get_unique_values_from_db(table_name, config_dict):
    try:
        # Extract column names from filters
        config_dict = json.loads(config_dict)
        columns = [f["column"] for f in config_dict["filters"]]

        # Build SQL query to fetch distinct values for each column
        result_dict = {}
        with engine.connect() as conn:
            for col in columns:
                query = f'SELECT DISTINCT "{col}" FROM "{table_name}" WHERE "{col}" IS NOT NULL'
                df = pd.read_sql(query, conn)

                # Convert to sorted list
                distinct_vals = sorted(df[col].dropna().astype(str).tolist())
                result_dict[col] = distinct_vals

        # Update filters with distinct values
        for f in config_dict["filters"]:
            if not f["allow_partial_match"]:
                pass
            else:
              col = f["column"]
              f["distinct_values"] = result_dict.get(col, [])

        return config_dict

    except Exception as e:
        return {"status": "error", "message": str(e)}

def table_top5_to_json(table_name):
    # Query the top 5 rows from Postgres
    query = f'SELECT * FROM "{table_name}" LIMIT 5'
    df = pd.read_sql(query, engine)

    # Convert column names to lowercase
    df.columns = df.columns.str.lower()

    # Get column data types from Postgres
    dtype_query = f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
    """
    dtype_df = pd.read_sql(dtype_query, engine)

    # Build final JSON structure
    final_config = {
        "table_name": table_name,
        "columns": [
            {
                "name": row["column_name"],
                "type": row["data_type"]
            }
            for _, row in dtype_df.iterrows()
        ],
        "data": json.loads(df.to_json(orient="records"))
    }

    # Return as pretty JSON
    return json.dumps(final_config, indent=4)


API_KEY="Bz9KGnL3xV7WliAKwWKPqCyc7j3o8nVejFAt6L6Di4iz7KPo2EiFJQQJ99BCACYeBjFXJ3w3AAABACOGqJwG"
API_VERSION="2024-08-01-preview"
AZURE_ENDPOINT="https://covalenseazureopenaieastus.openai.azure.com/"
MODEL_NAME="gpt-4o-mini-dev"

client = AzureOpenAI(
  api_key = API_KEY,  
  api_version = API_VERSION,
  azure_endpoint = AZURE_ENDPOINT
)

example = """{
    "worker_name": "atta_oos_fy_2023_25_analyzer",
    "description": "Analyzes Out of Stock (OOS) metrics for various SKUs over time, focusing on sales performance, forecasts, and supply chain visibility.",
    "knowledge": "This data worker provides insights into Out of Stock events by analyzing quantities, forecasts, market SKUs, and various distribution channels. The data will assist stakeholders in monitoring stock levels, identifying trends in stock shortfalls, and making informed decisions on inventory management. Metrics are numeric and can be aggregated over time, allowing for detailed analysis.",
    "database_info": {
        "type": "postgres",
        "schema": "public"
    },
    "max_limits": {
        "max_rows": 2000,
        "max_filters": 7,
        "max_aggregations": 10,
        "max_group_by_columns": 6
    },
    "source": {
        "type": "PHYSICAL_TABLE",
        "config": {
            "table_name": "atta_oos_fy_2023_25"
        }
    },
    "columns": [
        {
            "name": "Market_SKU",
            "type": "text",
            "description": "Stock Keeping Unit identifier for specific market products.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "Calendar_Day",
            "type": "timestamp",
            "description": "The specific date for the data entry.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "Distribution_Channel",
            "type": "text",
            "description": "The channel through which the product is distributed.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "Distribution_Channel_Discription",
            "type": "text",
            "description": "Description of the distribution channel.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "Sales_Office",
            "type": "text",
            "description": "Sales office code from where the sales data originates.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "Sales_Office_Location",
            "type": "text",
            "description": "Location of the sales office.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "Variant",
            "type": "text",
            "description": "The variant of the product being analyzed, distinguishing it from other products within the same category.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "Grammage",
            "type": "text",
            "description": "Product weight in grams.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "MSKU_Standardized",
            "type": "text",
            "description": "Standardized SKU format for inventory management.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "ROWNUM",
            "type": "float",
            "description": "Row number identifier.",
            "requires_quotes": false,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "SNOP_Dv",
            "type": "text",
            "description": "Sales & Operations Planning division.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "CCIS_category",
            "type": "text",
            "description": "CCIS category classification.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "CCIS_sub_category_desc",
            "type": "text",
            "description": "CCIS sub-category description.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "CCIS_brand_desc",
            "type": "text",
            "description": "CCIS brand description.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        },
        {
            "name": "CCIS_variant_desc",
            "type": "text",
            "description": "CCIS variant description.",
            "requires_quotes": true,
            "is_nullable": true,
            "is_pii": false
        }
    ],
    "filters": [
        {
            "column": "Calendar_Day",
            "operators": [
                ">=",
                "<",
                "="
            ],
            "description": "Filter by specific date or range.",
            "force_lowercase": false,
            "allow_partial_match": false
        },
        {
            "column": "Market_SKU",
            "operators": [
                "=",
                "IN"
            ],
            "description": "Filter by market SKU(s).",
            "force_lowercase": false,
            "allow_partial_match": true
        },
        {
            "column": "Sales_Office",
            "operators": [
                "=",
                "IN"
            ],
            "description": "Filter by sales office code(s).",
            "force_lowercase": false,
            "allow_partial_match": true
        },
        {
            "column": "Brand",
            "operators": [
                "=",
                "IN"
            ],
            "description": "Filter by brand(s).",
            "force_lowercase": false,
            "allow_partial_match": true
        },
        {
            "column": "Category",
            "operators": [
                "=",
                "IN"
            ],
            "description": "Filter by category(s).",
            "force_lowercase": false,
            "allow_partial_match": true
        }
    ],
    "aggregations": [
    { "function": "SUM", "applicable_columns": ["opl_quantity", "forecast_qty", "net_shortfall", "wd_weighted_oos_flag", "weighted_oos", "__wd__oos__numeric__", "__wd__oos__weighted_"], "alias_template": "total_{column}" },
    { "function": "AVG", "applicable_columns": ["opl_quantity", "forecast_qty", "net_shortfall", "wd_weighted_oos_flag", "weighted_oos", "__wd__oos__numeric__", "__wd__oos__weighted_"], "alias_template": "avg_{column}" },
    { "function": "COUNT", "applicable_columns": ["market_sku", "sales_office", "brand", "category"], "alias_template": "count_{column}" },
    { "function": "SUM", "applicable_columns": ["opl_quantity"], "alias_template": "weekly_total_{column}", "group_by": "DATE_TRUNC('week', calendar_day)" },
    { "function": "SUM", "applicable_columns": ["opl_quantity"], "alias_template": "monthly_total_{column}", "group_by": "DATE_TRUNC('month', calendar_day)" },
    { "function": "SUM", "applicable_columns": ["opl_quantity"], "alias_template": "quarterly_total_{column}", "group_by": "DATE_TRUNC('quarter', calendar_day)" },
    { "function": "SUM", "applicable_columns": ["opl_quantity"], "alias_template": "yearly_total_{column}", "group_by": "DATE_TRUNC('year', calendar_day)" }
  ],
    "group_by_options": [
        "Calendar_Day",
        "Market_SKU",
        "Sales_Office",
        "Brand",
        "Category",
        "Variant"
    ]
}
"""

system_prompt = """You are an intelligent agent who can generate a json config file which will give clear instructions to an LLM to generate proper sql queries to build an SQLTool.\n
                    Here is an EXAMPLE:{example}\n\n.
                    INSTRUCTIONS:\n
                        1. Provide suitable worker_name based on the table name and tabular data.\n
                        2. Provide a detailed description of what this SQLTool is for.\n
                        3. Provide required knowledge to LLM based on the tabular data.\n
                        4. Max_limits shouls be same as in the example given, table name should be same as the given table name.\n
                        5. Data-types: for date columns use 'timestamp', for strings use 'text', for integers use 'integer', for float use 'float' and for boolean use 'boolean'. Don't use any other data type.
                        5. Must include all the coulmns from the given table data, also give should and approptiate descriptions for each column, keep these as given:\n "requires_quotes": true, "is_nullable": true, "is_pii": false. \n
                        6. Use filters on dimension columns. Use aggregations on fact columns.Also in group_by columns include the columns which can be grouped based on their values.\n
                        7. In aggregations MUST include weekly, monthly, querterly, yearly which are all possible based on the date columns(Postgres aggregations).\n
                    For the following table data, Strictly provide in the same format without any deviation. Also must include all the columns from the table. Don't give anything extra apart from the config json.\n
                    
                    TABLE NAME: {table_name}\n
                    TABLE DATA:\n {table_data}"""

table_name = "bi_customer_interact_fy_2023_25"   # your table name here
table_data = table_top5_to_json(table_name)
final_prompt = system_prompt.format(table_name=table_name, table_data=table_data,example=example)

config = client.chat.completions.create(
        model=MODEL_NAME,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": final_prompt},
        ]
    )

print(config.choices[0].message.content)
final_config = get_unique_values_from_db(table_name,config.choices[0].message.content)
output_dir = "updated_config_files"
os.makedirs(output_dir, exist_ok=True)

# Save JSON file inside the folder
output_path = os.path.join(output_dir, f"{table_name}.json")
with open(output_path, 'w') as json_file:
    json.dump(final_config, json_file, indent=4) 

print(f"JSON data saved to {output_path}")