import requests
from bs4 import BeautifulSoup
import mysql.connector

# 最大评论数
maxCommentLen = 10

# **预处理** - 读取 websites.txt
websites = []
with open('websites.txt', 'r', encoding="UTF-8") as file:
    for line in file:
        line = line.strip()
        if line:
            websites.append(line)

# **2. 爬取数据**
districts = []
id = 0

for website in websites:
    print(f"正在爬取：{website}")
    resp = requests.get(website)
    soup = BeautifulSoup(resp.text, 'html.parser')

    id += 1
    district = {}

    # **景点 ID**
    district['id'] = id

    # **景点名称**
    name = soup.find('div', class_='title').text.strip()
    district['name'] = name
    print(f"景点名称: {name}")

    # **位置**
    location = soup.find('p', class_='baseInfoText')
    district['location'] = location.text.strip() if location else "未知"

    # **评分**
    avgScore = soup.find('p', class_='commentScoreNum')
    district['avgScore'] = float(avgScore.text.strip()) if avgScore else 0.0

    # **热度**
    heat = soup.find('div', class_='heatScoreText')
    district['heat'] = float(heat.text.strip()) if heat else 0.0

    # **简介**
    introduction = ''
    intro = soup.find('div', class_='LimitHeightText')
    if intro:
        intro_ps = intro.find_all('p')
        for p in intro_ps:
            if p.text:
                introduction += p.text.strip()
    if not introduction:
        introduction = "暂无简介"
    district['introduction'] = introduction[:996] + '...' if len(introduction) > 996 else introduction

    # **开放时间**
    openTime = soup.find_all('div', class_='moduleContent')
    if openTime:
        openTime = openTime[1].text.strip() if len(openTime) > 1 else openTime[0].text.strip()
    else:
        openTime = "未知"
    # **防止存储超长**
    district['openTime'] = openTime[:196] + '...' if len(openTime) > 196 else openTime

    # **图片 URL** - 取 banner 图
    imageUrl = soup.find('div', class_='swiper-slide swiperItem')
    if imageUrl:
        imageUrl = imageUrl.get('style')
        if imageUrl and 'url(' in imageUrl:
            imageUrl = imageUrl.split('url(')[1].split(')')[0].strip('"')
    else:
        imageUrl = "https://via.placeholder.com/150"  # 默认图片
    district['imageUrl'] = imageUrl

    districts.append(district)

# **3. 存入 MySQL**
print("正在存储到数据库...")

# **连接 MySQL**
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="wxw20050726",
    database="tourist_db"
)
cursor = db.cursor()

# **删除旧表**
cursor.execute("DROP TABLE IF EXISTS Districts;")

# **创建新表**
create_districts_table = """
CREATE TABLE Districts (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    location VARCHAR(100) NOT NULL,
    avgScore FLOAT(2,1),
    heat FLOAT(3,1),
    introduction VARCHAR(1000),
    openTime VARCHAR(200),
    imageUrl VARCHAR(300)
) COMMENT '景区信息表';
"""
cursor.execute(create_districts_table)

# **插入数据**
insert_district_query = """
INSERT INTO Districts (id, name, location, avgScore, heat, introduction, openTime, imageUrl)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""
for district in districts:
    cursor.execute(insert_district_query, (
        district['id'],
        district['name'],
        district['location'],
        district['avgScore'],
        district['heat'],
        district['introduction'],
        district['openTime'],
        district['imageUrl']
    ))

# **提交事务**
db.commit()

# **关闭连接**
cursor.close()
db.close()
print("数据存储完毕！")
