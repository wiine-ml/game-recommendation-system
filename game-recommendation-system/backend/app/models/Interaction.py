from datetime import datetime, timezone
from sqlalchemy import text
from database import db

class Interaction(db.Model):
    __tablename__ = 'interactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)  

    clicked = db.Column(db.Boolean, nullable=True)  # 是否过点击链接
    subscribed = db.Column(db.Boolean, nullable=True)  # 是否订阅
    disliked = db.Column(db.Boolean, nullable=True)  # 是否不喜欢
    review_score = db.Column(db.Numeric(2, 1), nullable=True)  # 评论分数
    review_text = db.Column(db.Text, nullable=True)  # 评论内容

    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间

    @classmethod
    def create(cls, user_id, game_id, clicked, subscribed, disliked, review_score, review_text):
        """创建新的交互记录"""
        sql = text("""
            INSERT INTO interactions (user_id, game_id, clicked, subscribed, disliked, review_score, review_text, created_at)
            VALUES (:user_id, :game_id, :clicked, :subscribed, :disliked, :review_score, :review_text, :created_at)
            RETURNING id
        """)
        result = db.session.execute(sql, {
            'user_id': user_id,
            'game_id': game_id,
            'clicked': clicked,
            'subscribed': subscribed,
            'disliked': disliked,
            'review_score': review_score,
            'review_text': review_text,
            'created_at': datetime.utcnow()
        })
        new_id = result.fetchone()[0]
        db.session.commit()
        return new_id

    @classmethod
    def get_by_id(cls, interaction_id):
        """根据ID获取交互记录"""
        interaction = db.session.query(cls).filter_by(id=interaction_id).first()
        if interaction:
            return interaction
        return None

    @classmethod
    def get_by_user_and_game(cls, user_id, game_id):
        """根据用户ID和游戏ID获取交互记录"""
        interaction = cls.query.filter_by(user_id=user_id, game_id=game_id).first()
        return interaction

    @classmethod
    def update(cls, interaction_id, **kwargs):
        """更新交互记录"""
        update_fields = []
        parameters = {'id': interaction_id}

        for key, value in kwargs.items():
            if hasattr(cls, key):
                update_fields.append(f"{key} = :{key}")
                parameters[key] = value

        if not update_fields:
            return False

        sql = text(f"""
            UPDATE interactions 
            SET {', '.join(update_fields)} 
            WHERE id = :id
        """)

        db.session.execute(sql, parameters)
        db.session.commit()
        return True

    @classmethod
    def delete(cls, interaction_id):
        """删除交互记录"""
        sql = text("""
            DELETE FROM interactions WHERE id = :id
        """)
        db.session.execute(sql, {'id': interaction_id})
        db.session.commit()
        return True

    @classmethod
    def get_all(cls):
        """获取所有交互记录"""
        sql = text("""
            SELECT * FROM interactions
        """)
        result = db.session.execute(sql)
        interactions = []
        for row in result:
            # 将数据库查询结果转换为字典
            interaction_dict = dict(row._mapping)
            # 创建 Interaction 对象并添加到列表中
            interaction = cls(
                id=interaction_dict['id'],
                user_id=interaction_dict['user_id'],
                game_id=interaction_dict['game_id'],
                clicked=interaction_dict['clicked'],
                subscribed=interaction_dict['subscribed'],
                disliked=interaction_dict['disliked'],
                review_score=interaction_dict['review_score'],
                review_text=interaction_dict['review_text'],
                created_at=interaction_dict['created_at']
            )
            interactions.append(interaction)
        return interactions
    
    @classmethod
    def get_all_by_user(cls, user_id):
        """根据用户ID获取所有交互记录"""
        interactions = cls.query.filter_by(user_id=user_id).all()
        return interactions
    
    @classmethod
    def get_subscribed_count(cls, game_id):
        """统计游戏的关注者数量"""
        return cls.query.filter_by(game_id=game_id, subscribed=True).count()

    @classmethod
    def get_average_rating(cls, game_id):
        """计算游戏的评分平均分"""
        avg_rating = db.session.query(db.func.avg(cls.review_score)).filter_by(game_id=game_id).scalar()
        return round(avg_rating, 1) if avg_rating is not None else 0.0
    
    @classmethod
    def delete_reviews(cls, interaction_id):
        """软删除评论，仅在满足条件时删除表项"""
        # 获取交互记录
        interaction = cls.get_by_id(interaction_id)
        if not interaction:
            return -1
        
        # 更新评论字段
        cls.update(interaction_id, review_score=0, review_text='')
        
        # 检查是否满足删除条件
        if not interaction.clicked and not interaction.subscribed and not interaction.disliked:
            cls.delete(interaction_id)
            return 1
        else:
            return 1