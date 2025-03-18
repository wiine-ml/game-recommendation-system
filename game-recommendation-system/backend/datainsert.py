import csv
import sqlite3
from datetime import datetime

# 连接到SQLite数据库
conn = sqlite3.connect('instance/GRSystemData.sqlite3')
cursor = conn.cursor()

# 打开CSV文件并读取数据
with open('dataset\IGN games from best to worst.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        # 提取CSV中的数据
        title = row['title']
        score = float(row['score']) if row['score'] else None
        score_phrase = row['score_phrase'] if row['score_phrase'] else None
        platform = row['platform'] if row['platform'] else None
        genre = row['genre'] if row['genre'] else None
        release_year = int(row['release_year']) if row['release_year'] else None
        release_month = int(row['release_month']) if row['release_month'] else None
        release_day = int(row['release_day']) if row['release_day'] else None
        
        # 构造INSERT语句
        sql = """
        INSERT INTO games (
            gameTitle, officalRating, ratingPhrase, gamePlatform, gameGenre,
            releaseYear, releaseMonth, releaseDay
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # 执行INSERT语句
        cursor.execute(sql, (
            title, score, score_phrase, platform, genre,
            release_year, release_month, release_day
        ))
    
    # 提交事务
    conn.commit()

# 关闭数据库连接
conn.close()