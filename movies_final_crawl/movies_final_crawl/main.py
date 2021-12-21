from coming_yahoo_movie_final_crawl import coming_movie_crawl
from on_yahoo_movie_final_crawl import on_movie_crawl
#from cv2_to_mysql import input_on_coming_movie_data
import os

if os.path.exists("data"):
   print("exists dir data !")
else:
   os.mkdir("data")

if os.path.exists('data/on_movie_info.csv'):
   os.remove('data/on_movie_info.csv')
   print("delete existed on_movie_info.csv")

if os.path.exists('data/coming_movie_info.csv'):
   os.remove('data/coming_movie_info.csv')
   print("delete existed coming_movie_info.csv")

coming_movie_crawl()
#input_on_coming_movie_data('coming_movie')

on_movie_crawl()
#input_on_coming_movie_data('on_movie')





