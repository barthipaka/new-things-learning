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
from typing import Union

from neuro_san.interfaces.coded_tool import CodedTool
import pandas as pd

logger = logging.getLogger(__name__)


class InsightsGenerator(CodedTool):
    """
    A tool that updates a running cost each time it is called.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates the passed running cost each time it's called.
        :param args: A dictionary with the following keys:
                    "running_cost": the running cost to update.

        :param sly_data: A dictionary containing parameters that should be kept out of the chat stream.
                         Keys expected for this implementation are:
                         None

        :return: A dictionary containing:
                 "running_cost": the updated running cost.
        """
        tool_name = self.__class__.__name__
        logger.debug("========== Calling %s ==========", tool_name)
        # Parse the arguments
        logger.debug("args: %s", args)
        file_path = args.get('file_path')
        if file_path:
            df = pd.read_parquet(file_path)
        else:
            return "File path not provided"
        
        csv_data = df.to_csv(index=False)
        

        logger.debug("-----------------------")
        logger.debug("========== Done with %s ==========", tool_name)
        return f'{csv_data}'
