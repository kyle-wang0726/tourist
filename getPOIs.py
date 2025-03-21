
import requests
import mysql.connector
import time
#1.预处理获取数据
key = 'aeae9e71779d0755e8eeda5cf3092def' #换成自己的key
maxPageNum = 10
maxTryTimes = 4
addrs = []
with open('addrs.txt', 'r', encoding="UTF-8") as f:
    for line in f:
        line = line.strip().split(',')
        if line:
            ppos = line[1].find('（')
            if ppos != -1: line[1] = line[1][:ppos]
            if line[1]:
                addrs.append(line)
#addrs=[('id','addr')]
#print(addrs)
#2.连接数据库准备
print("Loading to dataBase...")
    #(1) 连接到MySQL数据库
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="wxw20050726",
    database="tourist_db" #需提前创建bigmap数据库
)
cursor = db.cursor()

    #(2) 创建表结构
    # 创建Districts表
cursor.execute("""drop table if exists pois;""")
create_pois_table = """
create table pois
(
    bid      int          not null comment '所属景区类别',
    id       char(10)     not null,
    pid      char(10)     null comment '父poi的ID',
    x        double(9, 6) not null,
    y        double(9, 6) not null,
    name     varchar(50)  not null,
    type     varchar(50)  not null,
    rating   varchar(4)   null,
    photourl varchar(150) null,
    primary key (id, bid)
);
"""
cursor.execute(create_pois_table)

    #(3) 插入数据样式
insert_POIs_query = """
INSERT IGNORE INTO pois (bid, id, pid, x, y, name, type, rating, photourl)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
"""
# for district in districts:
#     cursor.execute(insert_district_query, (district['id'], district['name'], district['location'], district['avgScore'], district['heat'], district['introduction'], district['openTime']))

#3.连接高德地图API获取数据
for addrItem in addrs:
    bid = int(addrItem[0])
    addr = addrItem[1]
    pageNum = 1
    tryTimes = 0
    while pageNum <= maxPageNum and tryTimes <= maxTryTimes:
        resp = requests.get(f"https://restapi.amap.com/v5/place/text?keywords={addr}&page_size=25&page_num={pageNum}&key={key}&show_fields=business,photos")
        if not resp.ok: break
        data = resp.json()
        if (data.get('count', 'None')=='None'):
            tryTimes += 1
            time.sleep(0.5) #API有访问流量限制
            continue
        cnt = int(data.get('count', '0'))
        if cnt<=0: break
        if cnt<25: pageNum=maxPageNum
        for poi in data["pois"]:
            rating = poi.get("business",'')
            if rating: rating = rating.get('rating','')
            photourl = poi.get("photos",'')
            if photourl: photourl = photourl[0].get('url','')
            pos = poi["location"].find(',')
            x = float(poi["location"][:pos])
            y = float(poi["location"][pos+1:])
            #重复问题？限制主关键字(id,bid)，insert ignore
            cursor.execute(insert_POIs_query,(bid, poi["id"],poi["parent"], x, y, poi["name"], poi["type"], rating, photourl))
        pageNum += 1
    db.commit()
    print(f"{addr} finished..")

#(3)关闭连接
cursor.close()
db.close()
