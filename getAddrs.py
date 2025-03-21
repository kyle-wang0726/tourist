import mysql.connector

def fetch_and_save_locations():
    # 配置数据库连接参数
    config = {
        'user': 'root',       # 替换为你的数据库用户名
        'password': 'wxw20050726',   # 替换为你的数据库密码
        'host': 'localhost',           # 替换为你的数据库主机地址
        'database': 'tourist_db',          # 替换为你的数据库名称
        'raise_on_warnings': True
    }

    try:
        # 建立数据库连接
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # 执行SQL查询语句
        query = "SELECT id,location FROM districts"
        cursor.execute(query)

        # 获取所有结果
        locations = [(row[0], row[1]) for row in cursor.fetchall()]
        # print(locations)
        # # 去重处理
        # unique_locations = list(set(locations))

        # 将去重后的结果写入文件
        with open("addrs.txt", "w", encoding="UTF-8") as file:
            for location in locations:
                file.write(f"{location[0]},{location[1]}\n")

        print("Locations have been successfully saved to addrs.txt")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # 确保关闭数据库连接
        if cnx.is_connected():
            cursor.close()
            cnx.close()

if __name__ == "__main__":
    fetch_and_save_locations()