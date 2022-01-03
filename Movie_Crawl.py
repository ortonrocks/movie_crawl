import os.path
import time
import requests
import json
from bs4 import BeautifulSoup
import csv
import datetime
import os
from datetime import datetime
import pymysql

### Yahoo 即將上映電影資訊 ###
def comingsoon_yahoo_movie():
    with open('data/coming_movie.csv','w',newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ "movie_name", "movie_type" , "movie_date" , "movie_context" ,'movie_pic',"movie_trailer"])
    for page in range(1,7):
        page_url = "https://movies.yahoo.com.tw/movie_comingsoon.html?page={}".format(page)
        page_res = requests.get(page_url)
        page_res.encoding = 'utf-8'
        soup = BeautifulSoup(page_res.text, 'html')
        total=[]
        time.sleep(2)
        for i in range (len(soup.select("div.release_btn.color_btnbox"))):
            movie_info=soup.select("div.release_btn.color_btnbox")[i]
            movie_link=movie_info.find("a")["href"]
            total.append(movie_link)

        for url in total:
            url=url
            res = requests.get(url)
            res.encoding='utf-8'
            soup = BeautifulSoup(res.text, 'html')

            try:
                movie_pic = soup.select("div.movie_intro_foto")[0].find("img")["src"]
            except:
                movie_pic='https://th.bing.com/th/id/OIP.0huqk9YReEVyDmbj973p1wHaDK?pid=ImgDet&rs=1'
                

            movie_name = soup.select("div.movie_intro_info_r")[0].find("h1").text
            try:
                movie_date = soup.select("div.movie_intro_info_r")[0].find_all("span")[0].text.split("：")[1]
            except:
                movie_date ='無上映日期'
                

            try:
                movie_context = soup.select("div.gray_infobox_inner")[0].find_all("span")[0].text  
                movie_context = movie_context.replace("\n","")
                movie_context = movie_context.replace("\r\xa0\r","")
                movie_context = movie_context.replace(" ",'')
                movie_context = movie_context.replace("'",'')
                movie_context = movie_context.replace("★",'')
                
            except:
                movie_context ='無內容'
            try:
                movie_trailer = soup.select("div.l_box_inner")[0].find("a")["href"]
            except:
                movie_trailer ='https://movies.yahoo.com.tw/index.html'
                
            try:
                get_movie=soup.select("div.level_name_box")
                movie_type_list=''
                for i in range(len(get_movie[0].select('a'))):
                    movie_type = get_movie[0].select('a')[i].text
                    movie_type=movie_type.replace("\n",'')
                    movie_type=movie_type.replace(" ",'')
                    try:
                        movie_type_list+=str(movie_type.split('/')[1]+'，')
                        movie_type_list+=str(movie_type.split('/')[0]+'，')

                    except:
                        movie_type_list+=str(movie_type+'，')
            except:
                movie_type_list='無'

            print( movie_name,'\n', movie_type_list ,'\n', movie_date ,'\n', movie_context ,'\n', movie_pic,'\n',movie_trailer,'\n')

            with open('data/coming_movie.csv','a+',newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ movie_name, movie_type_list , movie_date , movie_context , movie_pic,movie_trailer ])

            csvfile.close()

### Yahoo 電影評論 ###
def comment_yahoo_movie():
    total=[]
    with open('data/movie_comment.csv','w',newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([ "movie_name", "movie_comment"])
    csvfile.close()

    for page in range(1,10):
        url = "https://movies.yahoo.com.tw/movie_intheaters.html?page={}".format(page)
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html')
        
        time.sleep(2)
        
        for i in range (len(soup.select("div.release_btn.color_btnbox"))):
            movie_info=soup.select("div.release_btn.color_btnbox")[i]
            movie_link=movie_info.find("a")["href"]
            total.append(movie_link)
            
            
    for num in range(len(total)):
        time.sleep(2)
        mid = total[num].split('-')[-1]
        comment_url= F'https://movies.yahoo.com.tw/movieinfo_review.html/id={mid}?sort=update_ts&order=desc&page=2'
        res = requests.get(comment_url)
        print(comment_url)
        
        res.encoding='utf-8'
        soup = BeautifulSoup(res.text, 'html')
        movie_name = soup.select("div.inform_r")[0].find("h1").text.split("\n", 1 )[0]
        movie_comment = soup.select("div.movie_tab")[0].find_all('li')[5].find("a")["href"]
        try:
            itemsobj =soup.select('div.page_numbox')[0].find_all('li')[-3].find("a").text
        except:
            pass

        page = int(itemsobj)

        for i in range(1,page+1):

            url=F'https://movies.yahoo.com.tw/movieinfo_review.html/id={mid}?sort=update_ts&order=desc&page={i}'
            res = requests.get(url)
            res.encoding='utf-8'
            soup = BeautifulSoup(res.text, 'html')

            try:
                comment_list=soup.select("ul.usercom_list")[0]
                for j in range(len(comment_list.select("span"))):
                    movie_comment = comment_list.select("span")[j].text
                    if (j+1)%3==0:
                        print(movie_name,movie_comment)
                        with open('data/movie_comment.csv','a+',newline='',encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([ movie_name, movie_comment])
                            csvfile.close()
            except:
                pass

### Yahoo 電影排行榜 ###
def chart_yahoo_movie():
    url = "https://movies.yahoo.com.tw/chart.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html')
    items = soup.select('div.tr')
    total=[]

    for i in range(1,len(items)):
        try:
            link = items[i].select('div.td')[3].select('a')[0]['href']
        except IndexError:
            pass
        total.append(link)

    with open('data/movie_hot.csv','w',newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ "movie_name", "movie_type" , "movie_date" , "movie_context" ,'movie_pic',"movie_trailer"])
                csvfile.close()
    for url in total:
            url=url
            res = requests.get(url)
            res.encoding='utf-8'
            soup = BeautifulSoup(res.text, 'html')
            try:
                movie_pic = soup.select("div.movie_intro_foto")[0].find("img")["src"]
            except:
                movie_pic='https://th.bing.com/th/id/OIP.0huqk9YReEVyDmbj973p1wHaDK?pid=ImgDet&rs=1'

            movie_name = soup.select("div.movie_intro_info_r")[0].find("h1").text
            try:
                movie_date = soup.select("div.movie_intro_info_r")[0].find_all("span")[0].text.split("：")[1]
            except:
                movie_date ='無上映日期'

            try:
                movie_context = soup.select("div.gray_infobox_inner")[0].find_all("span")[0].text  
                movie_context = movie_context.replace("\n","")
                movie_context = movie_context.replace("\r\xa0\r","")
                movie_context = movie_context.replace("'","")
                movie_context = movie_context.replace(" ",'')
                movie_context = movie_context.replace("★",'')
            except:
                movie_context ='無內容'
                
            try:
                movie_trailer = soup.select("div.l_box_inner")[0].find("a")["href"]
            except:
                movie_trailer ='https://movies.yahoo.com.tw/index.html'

            try:
                get_movie=soup.select("div.level_name_box")
                movie_type_list=''
                for i in range(len(get_movie[0].select('a'))):
                    movie_type = get_movie[0].select('a')[i].text
                    movie_type=movie_type.replace("\n",'')
                    movie_type=movie_type.replace(" ",'')
                    try:
                        movie_type_list+=str(movie_type.split('/')[1]+'，')
                        movie_type_list+=str(movie_type.split('/')[0]+'，')

                    except:
                        movie_type_list+=str(movie_type+'，')
            except:
                movie_type_list='無'

            print( movie_name,'\n', movie_type_list ,'\n', movie_date ,'\n', movie_context ,'\n', movie_pic,'\n',movie_trailer,'\n')

            with open('data/movie_hot.csv','a+',newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ movie_name, movie_type_list , movie_date , movie_context , movie_pic,movie_trailer ])
            csvfile.close()

### Yahoo 上映中電影資訊 ###
def on_yahoo_movie():
    with open('data/on_movie.csv','w',newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ "movie_name", "movie_type" , "movie_date" , "movie_context" ,'movie_pic',"movie_trailer"])
    for page in range(1,9):
        page_url = "https://movies.yahoo.com.tw/movie_intheaters.html?page={}".format(page)
        page_res = requests.get(page_url)
        page_res.encoding = 'utf-8'
        soup = BeautifulSoup(page_res.text, 'html')
        total=[]
        time.sleep(2)
        for i in range (len(soup.select("div.release_btn.color_btnbox"))):
            movie_info=soup.select("div.release_btn.color_btnbox")[i]
            movie_link=movie_info.find("a")["href"]
            total.append(movie_link)

        for url in total:
            url=url
            res = requests.get(url)
            res.encoding='utf-8'
            soup = BeautifulSoup(res.text, 'html')

            try:
                movie_pic = soup.select("div.movie_intro_foto")[0].find("img")["src"]
            except:
                movie_pic='https://th.bing.com/th/id/OIP.0huqk9YReEVyDmbj973p1wHaDK?pid=ImgDet&rs=1'
                

            movie_name = soup.select("div.movie_intro_info_r")[0].find("h1").text
            try:
                movie_date = soup.select("div.movie_intro_info_r")[0].find_all("span")[0].text.split("：")[1]
            except:
                movie_date ='無上映日期'
                

            #             想加 '上映日期： ' 可另開一行跑for迴圈
            try:
                movie_context = soup.select("div.gray_infobox_inner")[0].find_all("span")[0].text  
                movie_context = movie_context.replace("\n","")
                movie_context = movie_context.replace("\r\xa0\r","")
                movie_context = movie_context.replace(" ",'')
                movie_context = movie_context.replace("'","")
                movie_context = movie_context.replace("★",'')
                
            except:
                movie_context ='無內容'
            try:
                movie_trailer = soup.select("div.l_box_inner")[0].find("a")["href"]
            except:
                movie_trailer ='https://movies.yahoo.com.tw/index.html'
                
            try:
                get_movie=soup.select("div.level_name_box")
                movie_type_list=''
                for i in range(len(get_movie[0].select('a'))):
                    movie_type = get_movie[0].select('a')[i].text
                    movie_type=movie_type.replace("\n",'')
                    movie_type=movie_type.replace(" ",'')
                    try:
                        movie_type_list+=str(movie_type.split('/')[1]+'，')
                        movie_type_list+=str(movie_type.split('/')[0]+'，')

                    except:
                        movie_type_list+=str(movie_type+'，')
            except:
                movie_type_list='無'

            print( movie_name,'\n', movie_type_list ,'\n', movie_date ,'\n', movie_context ,'\n', movie_pic,'\n',movie_trailer,'\n')

            with open('data/on_movie.csv','a+',newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ movie_name, movie_type_list , movie_date , movie_context , movie_pic,movie_trailer ])

            csvfile.close()

### PTT 電影版 文章標題 ###
def ptt_movie_crawler():
    import requests
    from bs4 import BeautifulSoup
    import datetime
    import time
    import csv
    url='https://www.ptt.cc/bbs/movie/index.html'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'   
    }
    req=requests.get(url,headers=headers)
    soup=BeautifulSoup(req.text,'html.parser')
    finish=0
    with open ('data/ptt_movie_content_and_link.csv','w',newline='') as f:
                    writer=csv.writer(f)
                    writer.writerow(["title","aricleURL"]) 
    while True:
        if finish==1:
            break
        time.sleep(3)
        page=soup.select('div.btn-group')
        pageURL=page[1].select('a')[1]['href']
        crawlURL='https://www.ptt.cc'+str(pageURL)
        req=requests.get(crawlURL,headers=headers)
        soup=BeautifulSoup(req.text,'html.parser')
        
        titletags=soup.select('div.title')
        for titletag in titletags:
            try:
                date=soup.select('div.date')
                date1='2021/'+date[0].text
                data_time=datetime.datetime.strptime(date1,'%Y/%m/%d')
                now=datetime.datetime.now()
                date_cross=now-data_time
                if date_cross.days > 30:
                    finish=1       
                title=titletag.select_one('a').text       
                aricleURL='https://www.ptt.cc'+titletag.select_one('a')['href']
                print(title,date_cross.days)
                print(aricleURL)  
                print('========')
                with open ('data/ptt_movie_content_and_link.csv','a+',newline='') as f:
                    writer=csv.writer(f)
                    writer.writerow([title,aricleURL])            
            except AttributeError as e:
                pass 
            except UnicodeEncodeError as u:
                pass

### Dcard 電影版 近30日文章標題跟部分內文 ###
def dcard_crawler():
  url='https://www.dcard.tw/f/movie?latest=true'
  headers={
      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
  }

  res= requests.get(url,headers=headers)
  soup=BeautifulSoup(res.text,'html.parser')
  with open ('data/dcard_crawl.csv','w',newline='',encoding='utf-8-sig') as f:
    writer=csv.writer(f)
    writer.writerow(['title','articleUrl'])
  finish=False
  for i in range(len(soup.select('article.tgn9uw-0.dRhFWg'))):

    url='https://www.dcard.tw/f/movie?latest=true'
    try:
        blog_title=soup.select('article.tgn9uw-0.dRhFWg')[i].select('h2.bqeEAL')[0].text
    except:
        blog_title=''
    try:
        blog_comment=soup.select('article.tgn9uw-0.dRhFWg')[i].select("div.pmuXC")[0].text
    except:
        blog_comment=''
    print(blog_comment)
    blog_id=soup.select('article.tgn9uw-0.dRhFWg')[i].select('a.bJQtxM')[0]["href"].split('/')[-1]



    url1=f'https://www.dcard.tw/f/movie/p/{blog_id}'
    print(url1)
    res= requests.get(url1,headers=headers)
    soup1=BeautifulSoup(res.text,'html.parser')
    now=datetime.now()
    correct_time='2021年'+str(soup1.select("div.iDjmxJ")[-1].text.split(' ')[0])
    date_time=datetime.strptime(correct_time,'%Y年%m月%d日') 
    daycross=(now-date_time).days
    time.sleep(1.5)
    print(daycross)
    print(blog_title)
    print(blog_id)
    print('------')
    with open ('data/dcard_crawl.csv','a+',newline='',encoding='utf-8') as f:
      writer=csv.writer(f)
      writer.writerow([blog_title,blog_comment])

  last_id=soup.select('article.tgn9uw-0.dRhFWg')[29].select('a.bJQtxM')[0]["href"].split('/')[-1]
  print(last_id)
  finish=0
  while finish==0:
    time.sleep(3)

    url2='https://www.dcard.tw/service/api/v2/forums/movie/posts?limit=30&before='+str(last_id)
    print(url2)
    res= requests.get(url2,headers=headers)
    soup2=BeautifulSoup(res.text,'html.parser')
    api_text=json.loads(soup2.text)
    last_id=api_text[29]["id"]
    for api_num in range(len(api_text)):
      try:
        blog_comment=api_text[api_num]["excerpt"]
      except:
        blog_comment=' '
      try:
        create_time=api_text[api_num]["createdAt"]
      except:
        create_time
      try:
        blog_title=api_text[api_num]["title"]
      except:
        blog_title=' '
      try:
        correct_time=create_time.split('T')[0]
        date_time=datetime.strptime(correct_time,'%Y-%m-%d')
        movie_id=api_text[api_num]["id"]
        day_cross=(now-date_time).days
      except:
        day_cross=0
      print(blog_title)
      print(movie_id,day_cross)
      print(blog_comment)
      print('---------')
        
      if day_cross>30:
        finish=1


    with open ('data/dcard_crawl.csv','a+',newline='',encoding='utf-8') as f:
      writer=csv.writer(f)
      writer.writerow([blog_title,blog_comment])

  f.close()

### 清除電影資料表內所有內容 ###
def clean_table(data_type):

    table_name=f'{data_type}'

    conn=pymysql.connect(** config)

    cur=conn.cursor()

    delete_previous_data=f'delete from {table_name}'
    cur.execute(delete_previous_data)
    conn.commit()
    conn.close()
    cur.close()
    print('Clean tables successfully')

### 插入爬蟲資料至電影資料表 ###
def insert_table(data_type):
    mid=-1
    movie_list=[]
    with open(f'data/{data_type}.csv',encoding='utf-8') as csvfile:
        rows=csv.reader(csvfile)

        for row in rows:
            mid+=1
            row.insert(0,mid)
            movie_list.append(row)

    conn = pymysql.connect(**config)
    print('MySQL successfully connected')

    cur = conn.cursor()

    for i in range(1,len(movie_list)):
        insert_user_sql="insert into {} (movie_name,movie_type,movie_date,movie_content,movie_pic,movie_trailer) values ('{}','{}','{}' ,'{}','{}','{}' )".format(data_type,movie_list[i][1],movie_list[i][2],movie_list[i][3],movie_list[i][4],movie_list[i][5],movie_list[i][6])
        print(insert_user_sql)
        cur.execute(insert_user_sql)
        conn.commit()
    cur.close() 
    conn.close()

### clean_table + insert_table ###
def update_movie_table(table_name):
    clean_table(table_name)
    insert_table(table_name)

def check_data():
    conn = pymysql.connect(**config)
    print('successfully connected')

    cur = conn.cursor()

    get_data_sql = "select * from yahoo_movie;"
    cur.execute(get_data_sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

if __name__ == "__main__" :

    # 創立爬蟲資料路徑 #
    if os.path.exists("data"):
        pass
    else:
        os.mkdir("data")
    
    # 爬蟲 #
    print("[INFO] Crawling...")
    chart_yahoo_movie()
    comment_yahoo_movie()
    comingsoon_yahoo_movie()
    on_yahoo_movie()    
    ptt_movie_crawler()
    dcard_crawler()
    
    # 雲端MySQL連線參數 #
    config = {
        'host': '35.229.212.128',
        'port': 3306,
        'user': 'ortonrocks',
        'passwd': 'jimmy19971027',
        'db': 'try',
        'charset': 'utf8mb4',
        'local_infile': 1
    }
    
    # 更新資料庫電影表內容 #
    print("[INFO] MySQL Tables Updating...")
    update_movie_table('on_movie')
    update_movie_table('coming_movie')
    update_movie_table('movie_hot')

    print("[INFO] Finished")
    
    



