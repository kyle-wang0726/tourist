from DrissionPage import ChromiumPage
sights = []
with open('Sights.txt', 'r', encoding="UTF-8") as file:
    for line in file:
        pos = line.find('.')
        if pos != -1:
            sights.append(line[pos+1:].rstrip())
#1.根据sights获取对应网址
dp = ChromiumPage()
dp.listen.start('https://m.ctrip.com/restapi/soa2/20591/getGsOnlineResult')
websites = []
#对每个获取sight对应的网址
for sight in sights:
    dp.get("https://you.ctrip.com/globalsearch/?keyword="+sight)
    resp = dp.listen.wait()
    json_data = resp.response.body #返回JSON数据，字典
    if len(json_data) > 1:
        for item in json_data['homeItems']:
            if item['tab']['word'] == "景点":
                websites.append(item['items'][0]['url'])
                break
#print(websites)
dp.listen.stop()
uwebsites = []
for website in websites:
    for uwebsite in uwebsites:
        if website == uwebsite:break
    else:
        uwebsites.append(website)
with open('websites.txt', 'a', encoding="UTF-8") as file:
    for website in uwebsites:
        file.write(website + '\n')
