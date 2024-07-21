import requests
import re
import parsel
import os
import time
start = time.time()
def scrapePage(url,isNewChapter):
    response = requests.get(url=url,headers=headers)
    # print(response.text)
    selector = parsel.Selector(response.text)
    title = selector.css('#nr_title::text').get()
    content = selector.css('#nr1::text').getall()
    if '... -->>' in content[-1]:
        content[-1] = content[-1].strip('... -->>').rstrip()[:-3]
    content = '\n'.join(content)
    # print(title,'\n',content2)
    if(isNewChapter):
        file.write(title + '\n')


    #Check if there is next page
    if("-->>" in response.text):
        nextPageUrl = 'https://m.xbiqugew.com/book/' + bookid + '/' + selector.css('.next a::attr(href)').getall()[1]
        file.write(content)
        scrapePage(nextPageUrl,isNewChapter=False)
    else:
        file.write(content + '\n')
urllist = list()
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0'
    }
def scrapeUrls(url):

    html_data = requests.get(url=url, headers=headers).text
    selector = parsel.Selector(html_data)
    a = selector.css('.last9 li a::attr(href)').getall()
    print(html_data)
    # if('下一页' in html_data):
    #     print(re.findall('<tr><td><a href="(.*?)">下一页</a></td><td>',html_data))
    #     return scrapeUrls(url=, currentlist=a)
    # else:
    return a



index_url = input("输入xbiquegw.com目录页链接 (示例：https://m.xbiqugew.com/chapters_54510/)：")
bookid = re.findall('\d+\.\d+|\d+',index_url)[0]

html_data = requests.get(url=index_url,headers=headers).text
selector = parsel.Selector(html_data)
print(html_data)
novelname = re.findall('<title>(.*?)章节目录 第1页-笔趣阁</title>',html_data)[0]
print(novelname)
urlpagecount = re.findall('第1页 / 共(.*?)页',html_data)[0]
for i in range(1,int(urlpagecount)+1):
    urllist += scrapeUrls(index_url+str(i))
print(urlpagecount)


print(len(urllist))
folder = f'{novelname}\\'
if not os.path.exists(folder):
    os.mkdir(folder)
with open(folder + novelname + '.txt', mode='a', encoding='utf-8') as file:
    file.truncate(0)
file=open(folder + novelname+'.txt', mode='a',encoding='utf-8')
for url in urllist:
    scrapePage(url,isNewChapter=True)

print('Scrape finished in ' + str(time.time() - start) + ' ms!')



