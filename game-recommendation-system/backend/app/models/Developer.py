from datetime import timezone
from sqlalchemy import desc, or_, text
from database import db

# 游戏与开发商的关联表
game_developers = db.Table(
    'game_developers',
    db.Column('GameID', db.Integer, db.ForeignKey('games.id'), primary_key=True),
    db.Column('DeveloperID', db.Integer, db.ForeignKey('developers.DeveloperID'), primary_key=True),
    db.Column('is_promoted', db.Boolean, default=False)  # 是否为推广游戏
)

class Developer(db.Model):
    __tablename__ = 'developers'

    DeveloperID = db.Column(db.Integer, primary_key=True)
    DeveloperName = db.Column(db.String(255), nullable=False)
    DeveloperAvatar = db.Column(db.String(255), nullable=True)#开发商头像路径
    DeveloperProfile = db.Column(db.Text, nullable=True)#开发商简介
    DeveloperWebsite = db.Column(db.String(255), nullable=True)#开发商网站
    DeveloperHeadIllustrations = db.Column(db.String(255), nullable=True)#开发商头图

    DeveloperPassword = db.Column(db.String(255), nullable=True)

    Address = db.Column(db.String(255), nullable=True)
    ContactEmail = db.Column(db.String(255), nullable=True)
    FoundedYear = db.Column(db.Integer, nullable=True)

    # 与游戏表的关联关系
    games = db.relationship(
        'Game',
        secondary=game_developers,
        back_populates='developers',
        lazy='dynamic'
    )