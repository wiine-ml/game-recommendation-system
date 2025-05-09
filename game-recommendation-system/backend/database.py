from flask_sqlalchemy import SQLAlchemy

# 创建全局的 SQLAlchemy 实例
db = SQLAlchemy()

# 'cosine'或'iuf'
SIMILARITY_METHOD = 'cosine'