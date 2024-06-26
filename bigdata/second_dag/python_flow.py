from __future__ import annotations

import logging
from datetime import datetime
from msvcrt import getch

from airflow import dag, task
from airflow import is_venv_installed



log = logging.getLogger(__name__)

if not is_venv_installed():
    log.warning("The tutorial_taskflow_api_virtualenv example DAG requires virtualenv, please install it.")
else:
    @dag(schedule=None, 
         start_date=datetime(2021, 1, 1), 
         catchup=False, 
         tags=["big_data"])

    def big_data_python_demo():
        """
        ### TaskFlow API example using virtualenv

        This is a simple data pipeline example which demonstrates the use of the TaskFlow API using three simple tasks for Extract, Transform, and Load.
        """
        

        @task.virtualenv(
            use_dill=True,
            system_site_packages=False,
            requirements=["funcsigs"],
        )

        def extract():
            """
            #### Extract task
            A simple Extract task to get data ready for the rest of the data pipeline. In this case, getting data is simulated by reading from a hardcoded JSON string.
            """
            
            import json
            #Do you want to use this data?
            #url = 'https://www.cdc.gov/flu/weekly/index.htm'
            #url = 'https://www.usnews.com/news/health-news/articles/weekly-flu-cases-deaths-hospitalizations'
           
            ## Check if it is sucessful 
            data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

            order_data_dict = json.loads(data_string)
            return order_data_dict

        @task(multiple_outputs=True)
        def clean(order_data_dict: dict):
            """
            #### Transform task
            A simple Transform task which takes in the collection of order data and computes the total order value.
            """

            total_order_value = 0
          

            for value in order_data_dict.values():
                total_order_value += value

            return {"total_order_value": total_order_value}

        @task()
        def load(total_order_value: float):
            """
            #### Load task
            A simple Load task which takes in the result of the Transform task and instead of saving it to end user review, just prints it out.
            """

            print(f"Total order value is: {total_order_value:.2f}")

        order_data = extract()
        order_summary = clean(order_data)
        load(order_summary["total_order_value"])

    python_demo_dag = big_data_python_demo()