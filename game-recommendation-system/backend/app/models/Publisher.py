from datetime import timezone
from sqlalchemy import desc, or_, text
from database import db

# 游戏与发行商的关联表
game_publishers = db.Table(
    'game_publishers',
    db.Column('GameID', db.Integer, db.ForeignKey('games.id'), primary_key=True),
    db.Column('PublisherID', db.Integer, db.ForeignKey('publishers.PublisherID'), primary_key=True),
    db.Column('is_promoted', db.Boolean, default=False)  # 是否为推广游戏
)

class Publisher(db.Model):
    __tablename__ = 'publishers'

    PublisherID = db.Column(db.Integer, primary_key=True)
    PublisherName = db.Column(db.String(255), nullable=False)
    PublisherAvatar = db.Column(db.String(255), nullable=True)
    PublisherProfile = db.Column(db.Text, nullable=True)
    PublisherWebsite = db.Column(db.String(255), nullable=True)
    PublisherHeadIllstration = db.Column(db.String(255), nullable=True)

    PublisherPassword = db.Column(db.String(255), nullable=True)
    
    Address = db.Column(db.String(255), nullable=True)
    ContactEmail = db.Column(db.String(255), nullable=True)
    FoundedYear = db.Column(db.Integer, nullable=True)

    # 与游戏表的关联关系
    games = db.relationship(
        'Game',
        secondary=game_publishers,
        back_populates='publishers',
        lazy='dynamic'
    )

    