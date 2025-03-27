from sqlalchemy import Column, Integer, String, Text
from database import db  # 假设您已经在 database.py 中配置了数据库连接

class Mail(db.Model):
    __tablename__ = 'mails'  # 设置表名

    id = Column(Integer, primary_key=True)  # 主键
    senderType = Column(String(50))  # 发件人类型
    senderID = Column(Integer)  # 发件人ID
    receiverType = Column(String(50))  # 收件人类型
    receiverID = Column(Integer)  # 收件人ID
    msgContent = Column(Text)  # 消息内容

    def __init__(self, sender_type, sender_id, receiver_type, receiver_id, msg_content):
        """构造函数，用于初始化对象属性"""
        self.senderType = sender_type
        self.senderID = sender_id
        self.receiverType = receiver_type
        self.receiverID = receiver_id
        self.msgContent = msg_content

    def __repr__(self):
        """返回对象的字符串表示，用于调试和日志记录"""
        return f"<Mail(id={self.id}, senderType='{self.senderType}', senderID={self.senderID}, " \
               f"receiverType='{self.receiverType}', receiverID={self.receiverID}, " \
               f"msgContent='{self.msgContent[:50]}...')>"  # 截取前50个字符以便显示

    def save(self):
        db.session.add(self)
        db.session.commit()