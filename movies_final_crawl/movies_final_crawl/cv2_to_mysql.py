import csv 
import pymysql

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '!Qqaz2wsx',
    'db': 'try',
    'charset': 'utf8mb4',
    'local_infile': 1

}


def yahoo_csv_to_mysql(selected_table):
    #connect to database

    #def load_csv(csv_file,table_name,database)
    table_name=F'{selected_table}'

    conn=pymysql.connect(** config)

    cur=conn.cursor()

    #data_sql="LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES" %(csv_file,table_name)
    delete_previous_data=F'delete from {selected_table}'
   # cur.execute(data_sql)
    cur.execute(delete_previous_data)

    conn.commit()
    conn.close()
    cur.close()
    print('reconstruct success')

def input_on_coming_movie_data(selected_table):


    yahoo_csv_to_mysql(selected_table)   
    conn = pymysql.connect(**config)
    print('successfully connected')
    cur = conn.cursor()
    with open(F'data/{selected_table}_info.csv',encoding='utf-8') as r:
        read=csv.reader(r)
        count=0
        for row in read:
            if count>0:
                movie_name=row[0]
                movie_type=row[1]
                movie_date=row[2]
                movie_content=row[3]
                movie_pic=row[4]
                movie_trailer=row[5]

                insert_user_sql=F"insert into {selected_table} (movie_name, movie_type,movie_date,movie_content,movie_pic,movie_trailer) values ('{movie_name}','{movie_type}','{movie_date}','{movie_content}','{movie_pic}','{movie_trailer}')"
                cur.execute(insert_user_sql)
                conn.commit()
            count+=1
    cur.close()
    conn.close()
    r.close()
    print(F'successfully input data to table {selected_table}')            
