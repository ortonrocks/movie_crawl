import time
import requests
import json
from bs4 import BeautifulSoup
import csv
def on_movie_crawl():
    with open('data/on_movie_info.csv','w',newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ "movie_name", "movie_type" , "movie_date" , "movie_context" ,'movie_pic',"movie_trailer"])
    for page in range(1,9):
        page_url = "https://movies.yahoo.com.tw/movie_intheaters.html?page={}".format(page)
        page_res = requests.get(page_url)
        page_res.encoding = 'utf-8'
        soup = BeautifulSoup(page_res.text, 'lxml')
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
                #print(objSoup)

            # infos.append({
            try:
                movie_pic = soup.select("div.movie_intro_foto")[0].find("img")["src"]
            except:
                movie_pic='https://th.bing.com/th/id/OIP.0huqk9YReEVyDmbj973p1wHaDK?pid=ImgDet&rs=1'

            try:
                movie_name = soup.select("div.movie_intro_info_r")[0].find("h1").text
            except:
                movie_name ='none'
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
                movie_context = movie_context.replace("★",'')
                movie_context = movie_context.replace("'", '')

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

            with open('data/on_movie_info.csv','a+',newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ movie_name, movie_type_list , movie_date , movie_context , movie_pic,movie_trailer ])

            csvfile.close()

