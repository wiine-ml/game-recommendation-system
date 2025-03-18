from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy import text
from database import db

class News(db.Model):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)  # 新闻类型
    image = Column(String(255), nullable=False)  # 图片路径
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)

    def __init__(self, type, image, title, description, date):
        self.type = ''
        self.image = image
        self.title = title
        self.description = description
        self.date = date

    @staticmethod
    def add_news(type, image, title, description, date):
        """
        添加一条新闻记录
        :param type : 新闻类型 (str)
        :param image: 图片路径 (str)
        :param title: 标题 (str)
        :param description: 描述 (str)
        :param date: 日期 (datetime.date)
        :return: 新添加的新闻对象
        """
        new_news = News(type=type, image=image, title=title, description=description, date=date)
        db.session.add(new_news)
        db.session.commit()
        return new_news
    
    @staticmethod
    def update_news(news_id, type, image=None, title=None, description=None, date=None):
        """
        更新新闻记录
        :param news_id: 新闻 ID (int)
        :param type : 新闻类型 (str)
        :param image: 新图片路径 (str) - 可选
        :param title: 新标题 (str) - 可选
        :param description: 新描述 (str) - 可选
        :param date: 新日期 (datetime.date) - 可选
        :return: 更新后的新闻对象或 None
        """
        # 构建更新语句
        update_fields = {}
        if image is not None:
            update_fields['image'] = image
        if title is not None:
            update_fields['title'] = title
        if description is not None:
            update_fields['description'] = description
        if date is not None:
            update_fields['date'] = date
        if not update_fields:
            return None  # 没有需要更新的字段
        result = db.session.execute(
            text("UPDATE news SET " + ", ".join([f"{k} = :{k}" for k in update_fields.keys()]) + " WHERE id = :news_id"),
            {**update_fields, 'news_id': news_id}
        )
        if result.rowcount == 0:
            return None
        return 1
    
    @staticmethod
    def delete_news(news_id):
        """
        删除新闻记录
        :param news_id: 新闻 ID (int)
        :return: 删除成功返回 True，否则返回 False
        """
        result = db.session.execute(text("DELETE FROM news WHERE id = :news_id"), {'news_id': news_id})
        return result.rowcount > 0
    
    @staticmethod
    def get_all_news():
        """
        获取所有新闻记录
        :return: 新闻列表
        """
        result = db.session.execute(text("SELECT * FROM news ORDER BY date DESC"))
        news_list = []
        for row in result:
            news = {
                'id': row.id,
                'type': row.type,
                'image': row.image,
                'title': row.title,
                'description': row.description,
                'date': str(row.date)
            }
            news_list.append(news)
        return news_list

    @classmethod
    def get_news_by_id(cls,news_id):
        """"
        根据 ID 获取新闻记录
        :param news_id: 新闻 ID (int)
        :return: 新闻对象或 None
        """
        return cls.query.get(news_id)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'image': self.image,
            'title': self.title,
            'description': self.description,
            'date': str(self.date)
        }