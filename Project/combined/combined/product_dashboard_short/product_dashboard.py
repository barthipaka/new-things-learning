# Copyright © 2025 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

import logging
from typing import Any
from typing import Dict
import json
from neuro_san.interfaces.coded_tool import CodedTool
from coded_tools.postgres_agent.execute_sql import ExecuteSQLQuery
from coded_tools.postgres_agent.read_parquet import InsightsGenerator

logger = logging.getLogger(__name__)


class BuildPrompt(CodedTool):

    def __init__(self):
        self.default_path = 'coded_tools/postgres_agent/resources/customer_360.json'
        self.docs_path = {
            "ab_experiments": "coded_tools/schema_configs/gold_ab_experiment_results_v1.json",
            "conversion_funnel": "coded_tools/schema_configs/gold_conversion_funnel_v1.json",
            "crash_rate": "coded_tools/schema_configs/gold_crash_rate_v1.json",
            "feature_adoption": "coded_tools/schema_configs/gold_feature_adoption_metrics.json",
            "product_usage":"coded_tools\schema_configs\gold_product_usage_metrics_daily.json",
            "web_vitals": "coded_tools\schema_configs\gold_web_vitals_summary_v1.json"
        }

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> str:
        worker_name: str = args.get("worker_name", None)
        question: str = args.get("query", None)
        logger.debug("############### Prompt Building... ###############")
        logger.debug("User Query: %s", question)
        logger.debug("Worker Name: %s", worker_name)
        if worker_name is None:
            return "Error: No app name provided."
        config_path = self.docs_path.get(worker_name, self.default_path)
        config = self._load_config(config_path)
        sql_generation_prompt = self._build_prompt(config)
        prompt_str = sql_generation_prompt.format(input=question)
        print(f"--- Generated Prompt for LLM ---\n{prompt_str}\n")
        logger.debug("############### Documents extraction done ###############")
        if not prompt_str:
            logger.debug("No Prompt generated.")
            return f"Generate SQL query for: {question}"
        return prompt_str
    
    def _load_config(self,path: str) -> Dict[str, Any]:
        print("Load config path", path)
        with open(path) as f:
            return json.load(f)
        
    def _build_prompt(self,config:Dict[str, Any]) -> str:
        """
        Builds a detailed, database-specific prompt for the LLM based on the JSON config.
        """
        prompt_parts = [
            "You are an expert SQL writer. Translate the user's question into a single, valid, and executable SQL query based strictly on the schema and rules below."
        ]

        # --- Database Info ---
        db_info = config.get("database_info", {})
        db_type = db_info.get("type", "SQL")
        db_schema = db_info.get("schema", "")
        table_prefix = f"{db_schema}." if db_schema else ""

        db_rules = [
            "## Database and Query Rules",
            f"- Target database: **{db_type.upper()}**",
            f"- Schema: `{db_schema}` (always prefix table names with `{db_schema}.`).",
            "- Always use original column names in WHERE, JOIN, and GROUP BY.",
            "- Use aliases ONLY in SELECT output (e.g., `AS \"alias\"`). In all other clauses (WHERE, JOIN, GROUP BY, ORDER BY), use the original column names",
            "- If `Requires Quotes` is true, strictly wrap column names in double quotes in all places of sql query.",
            "- If rules conflict, always prioritize explicit query constraints (e.g., LIMIT, DISTINCT, allowed operators) over optional constructs (e.g., window functions, case expressions)."
            "- Do not invent columns, tables, or functions."
            "- Do not use WINDOW FUNCTIONS."
        ]
        prompt_parts.append("\n".join(db_rules))

        # --- 3. Data Source Definition (Table, Join, or CTE) ---
        source_info = config.get("source", {})
        source_type = source_info.get("type")
        source_config = source_info.get("config", {})
        source_section = ["## Data Source Definition"]

        if source_type in ["PHYSICAL_TABLE", "VIEW"]:
            table_name = source_config.get("table_name", "unknown_table")
            source_section.append(f"You will query a single table: `{table_prefix}{table_name}`.")

        elif source_type == "MULTI_TABLE_JOIN":
            source_section.append("You must query multiple tables using the exact aliases and join conditions below:")
            for t in source_config.get("tables", []):
                source_section.append(f"- Table: `{table_prefix}{t['name']}` AS `{t['alias']}`")
            for j in source_config.get("joins", []):
                source_section.append(f"- {j['type']} JOIN condition: `{j['on']}`")

        elif source_type == "CTE":
            cte_name = source_config.get("cte_name", "DynamicCTE")
            cte_sql = source_config.get("cte_sql", "")
            source_section.append(
                f"You will query from a Common Table Expression (CTE). "
                f"Your final query MUST start with this exact CTE block, followed by a SELECT on `{cte_name}`."
            )
            source_section.append(f"**CTE Definition Block:**\n```sql\n{cte_sql}\n```")

        prompt_parts.append("\n".join(source_section))

        # --- Columns Table ---
        columns = config.get("columns", [])
        col_table = ["## Available Columns", "| Column | Alias | Type | Typecast Policy | Requires Quotes | Description |",
                    "|--------|-------|------|----------------|----------------|-------------|"]
        for col in columns:
            col_table.append(f"| {col['name']} | {col.get('alias','')} | {col['type']} | {col.get('type_cast', '')} | {col.get('requires_quotes', False)} | {col['description']} |")
        prompt_parts.append("\n".join(col_table))

        # --- Filters ---
        filters = ["## Filtering Rules"]
        for f in config.get("filters", []):
            filters.append(f"- On `{f['column']}` allowed operators: {', '.join(f['operators'])}. {f.get('description','')}")
        prompt_parts.append("\n".join(filters))

        # --- Aggregations ---
        aggs = ["## Aggregation Rules"]
        for agg in config.get("aggregations", []):
            aggs.append(f"- {agg['function']} on {', '.join(agg['applicable_columns'])} (alias: \"{agg['alias_template']}\")")
        if config.get("group_by_options"):
            aggs.append(f"- Group by options: {', '.join(config['group_by_options'])}")
        prompt_parts.append("\n".join(aggs))

        # --- Window Functions ---
        win_funcs = config.get("window_functions", [])
        if win_funcs:
            wf = ["## Window Functions"]
            for wf_def in win_funcs:
                wf.append(f"- {wf_def['function']}() OVER (PARTITION BY {', '.join(wf_def['partition_by'])} ORDER BY {', '.join(wf_def['order_by'])}) AS \"{wf_def['alias']}\"")
            prompt_parts.append("\n".join(wf))

        # --- Ordering Rules ---
        ord_rules = config.get("ordering_rules", {})
        if ord_rules:
            order_section = ["## Ordering Rules",
                            f"- Allowed ORDER BY columns: {', '.join(ord_rules['allowed_columns'])}",
                            f"- Note: {ord_rules['note']}"]
            prompt_parts.append("\n".join(order_section))

        # --- Case Expressions ---
        case_exprs = config.get("case_expressions", [])
        if case_exprs:
            case_section = ["## Case Expressions"]
            for ce in case_exprs:
                case_section.append(f"- {ce['expression']} AS {ce['name']}")
            prompt_parts.append("\n".join(case_section))

        # --- Distinct Rules ---
        distinct_rules = config.get("distinct_rules", {})
        if distinct_rules:
            distinct_section = ["## Distinct Rules",
                                f"- Allowed: {distinct_rules.get('allow_distinct', False)}",
                                f"- Rule: {distinct_rules.get('rule','')}"]
            prompt_parts.append("\n".join(distinct_section))

        # --- Forbidden Rules ---
        forbids = config.get("forbidden_rules", [])
        if forbids:
            forbid_section = ["## Forbidden Rules"]
            for r in forbids:
                forbid_section.append(f"- {r}")
            prompt_parts.append("\n".join(forbid_section))

        # --- Query Constraints ---
        limits = config.get("max_limits", {})
        limit_section = ["## Query Constraints",
                        f"- Final query MUST end with LIMIT {limits.get('max_rows', 1000)}",
                        f"- No more than {limits.get('max_filters', 5)} conditions in WHERE clause."]
        prompt_parts.append("\n".join(limit_section))

        # --- Final Task ---
        prompt_parts.append(
            "## Final Task\n"
            "Translate the user's question into a single, valid SQL query.\n"
            "**User Question:** {input}\n"
            "**Output Format:** The SQL must be returned as plain text, no markdown, no comments, no explanations, no code fences."
        )

        final_prompt_str = "\n\n".join(prompt_parts)
        return final_prompt_str
