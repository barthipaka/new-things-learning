import json
import uuid
from typing import List, Dict, Any, Type, Union
import pandas as pd
import json
import logging
from neuro_san.interfaces.coded_tool import CodedTool
from langchain_community.utilities import SQLDatabase

import os


# required_env = ["DB_USERNAME", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
# missing = [var for var in required_env if not os.getenv(var)]
# if missing:
#     raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# db_uri = (
#     f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
#     f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
# )

db_uri = os.getenv('db_uri')

class ExecuteSQLQuery(CodedTool):

    def __init__(self):
        self.db = SQLDatabase.from_uri(db_uri)
        

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """
        :param args: An argument dictionary whose keys are the parameters
                to the coded tool and whose values are the values passed for them
                by the calling agent.  This dictionary is to be treated as read-only.

                The argument dictionary expects the following keys:
                    "search_terms"

        :param sly_data: A dictionary whose keys are defined by the agent hierarchy,
                but whose values are meant to be kept out of the chat stream.

                This dictionary is largely to be treated as read-only.
                It is possible to add key/value pairs to this dict that do not
                yet exist as a bulletin board, as long as the responsibility
                for which coded_tool publishes new entries is well understood
                by the agent chain implementation and the coded_tool implementation
                adding the data is not invoke()-ed more than once.

                Keys expected for this implementation are:
                    None

        :return:
            In case of successful execution:
                A list of dictionary of search results
            otherwise:
                a text string an error message in the format:
                "Error: <error message>"
        """

        logger = logging.getLogger(self.__class__.__name__)
        logger.info(">>>>>>>>>>>>>>>>>>>Executing SQL Query...>>>>>>>>>>>>>>>>>>")
        logger.info("SQL Query: %s", args.get("sql_query"))

        results = self._run(args.get('sql_query'))
        logger.info("Results : %s", results)

        return results

    def _run(
        self,
        query: str,
    ) -> str:
        """
        Executes a SQL query and saves the result as a Parquet file.
        Returns the file name or an error message.
        """
        try:
            result_proxy = self.db.run(query, fetch="cursor")
            columns = list(result_proxy.keys())
            rows = result_proxy.fetchall()
        except Exception as e:
            return f"ERROR: An exception occurred while executing the query. Details: {e}"

        try:
            if not rows:
                return "ERROR: Query executed successfully, but returned no results. Check with GetColumnsUniqueValuesTool"
            df = pd.DataFrame(rows, columns=columns)
            # parquet_filename = f"{uuid.uuid4()}.parquet"
            # df.to_parquet(parquet_filename, engine='pyarrow', index=False)
            results_md = df.to_markdown()
            return f"{results_md}"
        except Exception as e:
            return f"Error: An exception occurred while processing the results. Details: {e}"