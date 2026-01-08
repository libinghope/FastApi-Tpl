import os
import shutil
import sys
import asyncio
from worker.database_worker import create_initial_data, reset_database


def main():
    while True:
        print(
            """
            请选择要执行的操作:
            0、exit program
            1、create super user
            2、reset database(删除并重建数据库)
            3、delete all py cache files
            4、send test sms
            5、create initial data
            6、create 3d asset data
            7、download metadata files
        """
        )
        selection = input("")
        if selection.isdigit():
            selection = int(selection)
        else:
            print(f"未知的选项{selection}")
            continue
        if selection == 0:
            break

        elif selection == 1:
            asyncio.run(create_super_user())

        elif selection == 2:
            asyncio.run(reset_database())

        else:
            print(f"未知的选项{selection}")



def delete_pycache(directory="."):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                full_path = os.path.join(root, dir_name)
                print(f"Deleting: {full_path}")
                shutil.rmtree(full_path)  # 使用shutil.rmtree来递归删除文件夹及其内容


if __name__ == "__main__":
    main()
