import pandas as pd
from ydata_profiling import ProfileReport

import os


import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()


async def ydata_main(session_ID):
    loop = asyncio.get_event_loop()

    await loop.run_in_executor(executor, cpu_bound_task, session_ID)

    return "Done!"


def cpu_bound_task(session_ID):
    dir = f"/home/ksgcpcloud/myapp/csv_data/{session_ID}"
    files = os.listdir(f"/home/ksgcpcloud/myapp/csv_data/{session_ID}/")
    print(files)

    for i in range(len(files)):
        df = pd.read_csv(dir + "/" + files[i])
        profile = ProfileReport(df, title="Report")
        directory_path = f"/home/ksgcpcloud/myapp/reports/{session_ID}/"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print("Directory created")
        else:
            print("Directory already exists")
        profile.to_file(f"/home/ksgcpcloud/myapp/reports/{session_ID}/reports{i}.html")
        # print(df.dtypes)
    # profile.to_file("report.html")
    print("I am 2")
    # return "Data profiling started"


if __name__ == "__main__":
    ydata_main()
