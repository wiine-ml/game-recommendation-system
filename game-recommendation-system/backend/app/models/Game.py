from datetime import timezone
from sqlalchemy import or_, text
from database import db
from .Interaction import Interaction

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)  # 主键，自动生成编号
    gameTitle = db.Column(db.String(100), nullable=False)  # 游戏名称
    gameGenre = db.Column(db.String(100), nullable=True)  # 游戏类型
    gamePlatform = db.Column(db.String(100), nullable=True)  # 游戏平台
    releaseYear = db.Column(db.Integer, nullable=True)  # 发行年份
    releaseMonth = db.Column(db.Integer, nullable=True)  # 发行月份
    releaseDay = db.Column(db.Integer, nullable=True)  # 发行日
    ratingPhrase = db.Column(db.String(100), nullable=True)  # 评分词

    followers = db.Column(db.Integer, default=0)  # 关注者数量
    rating = db.Column(db.Float, default=0)  # 评分
    officalRating = db.Column(db.Float, nullable=True)  # 官方评分
    gameUrl = db.Column(db.String(200), nullable=True)  # 游戏链接
    gameDeveloper = db.Column(db.String(100), nullable=True)  # 游戏开发商
    gamePublisher = db.Column(db.String(100), nullable=True)  # 游戏发行商
    gameImage = db.Column(db.String(200), nullable=True)  # 游戏图片

    interactions = db.relationship('Interaction', backref='game', lazy='dynamic')  # 与交互表的关联关系

    def __init__(self, gameTitle, gameGenre, gamePlatform, releaseYear, releaseMonth, releaseDay, gamePhrase=None, followers=None, rating=None, officalRating=None, gameDeveloper=None, gamePublisher=None, gameUrl=None, gameImage=None):
        self.gameTitle = gameTitle
        self.gameGenre = gameGenre
        self.gamePlatform = gamePlatform
        self.releaseYear = releaseYear
        self.releaseMonth = releaseMonth
        self.releaseDay = releaseDay
        self.gamePhrase = gamePhrase

        self.gameDeveloper = gameDeveloper
        self.gamePublisher = gamePublisher
        self.followers = followers
        self.rating = rating
        self.officalRating = officalRating
        self.gameImage = gameImage
        self.gameUrl = gameUrl

    def __repr__(self):
        return f"<Game {self.id}: {self.gameTitle}>"

    @staticmethod
    def get_next_id():
        """获取下一个可用的编号"""
        result = db.session.execute(text("SELECT MAX(id) FROM games"))
        max_id = result.scalar()
        return max_id + 1 if max_id is not None else 0

    @staticmethod
    def create_game(gameTitle, gameGenre, gamePlatform, gameDeveloper, gamePublisher, followers, rating, releaseDate, gameImage, gameDescription, gameUrl):
        """创建游戏"""
        next_id = Game.get_next_id()
        new_game = Game(
            id=next_id,
            gameTitle=gameTitle,
            gameGenre=gameGenre,
            gamePlatform=gamePlatform,
            gameDeveloper=gameDeveloper,
            gamePublisher=gamePublisher,
            followers=followers,
            rating=rating,
            releaseDate=releaseDate,
            gameImage=gameImage,
            gameDescription=gameDescription,
            gameUrl=gameUrl
        )
        db.session.add(new_game)
        db.session.commit()
        return new_game

    @staticmethod
    def get_game_by_id(game_id):
        """根据编号获取游戏"""
        return Game.query.get(game_id)

    @staticmethod
    def update_game(game_id, gameTitle=None, gameGenre=None, gamePlatform=None, gameDeveloper=None, gamePublisher=None, followers=None, rating=None, officalRating = None, releaseYear=None, releaseMonth=None, releaseDay=None, gameImage=None, gamePhrase=None, gameUrl=None):
        """更新游戏"""
        game = Game.query.get(game_id)
        if not game:
            raise ValueError("游戏不存在")
        if gameTitle is not None:
            game.gameTitle = gameTitle
        if gameGenre is not None:
            game.gameGenre = gameGenre
        if gamePlatform is not None:
            game.gamePlatform = gamePlatform
        if gameDeveloper is not None:
            game.gameDeveloper = gameDeveloper
        if gamePublisher is not None:
            game.gamePublisher = gamePublisher
        if followers is not None:
            game.followers = followers
        if rating is not None:
            game.rating = rating
        if officalRating is not None:
            game.officalRating = officalRating
        if releaseYear is not None:
            game.releaseYear = releaseYear
        if releaseMonth is not None:
            game.releaseMonth = releaseMonth
        if releaseDay is not None:
            game.releaseDay = releaseDay
        if gameImage is not None:
            game.gameImage = gameImage
        if gamePhrase is not None:
            game.gamePhrase = gamePhrase
        if gameUrl is not None:
            game.gameUrl = gameUrl
        db.session.commit()
        return game

    @staticmethod
    def delete_game(game_id):
        """删除游戏"""
        game = Game.query.get(game_id)
        if not game:
            raise ValueError("游戏不存在")
        db.session.delete(game)
        db.session.commit()

    @staticmethod
    def get_games_by_genre(genre):
        """根据游戏类型查找游戏"""
        if genre == '全部':
            result = db.session.execute(text("SELECT * FROM games"))
            return result.fetchall()
        else:
            genres = [g.strip() for g in genre.split(',')]
    
            # 构造查询条件，使用 or_ 来匹配任意一个标签
            conditions = [Game.gameGenre == g for g in genres]
            query = Game.query.filter(or_(*conditions))
            
            return query.all()
        
    @staticmethod
    def get_top_subscribed_games(page=1, per_page=10):
        """获取根据关注者数量排序的所有游戏，并支持分页"""
        # 查询所有游戏，并计算每个游戏的关注者数量和评分平均分
        query = db.session.query(
            Game,
            db.func.count(Interaction.id).label('subscribed_count'),
            db.func.avg(Interaction.review_score).label('rating_avg')
        ).outerjoin(
            Interaction, Game.id == Interaction.game_id
        ).group_by(
            Game.id
        ).order_by(
            db.desc('subscribed_count')  # 按关注者数量降序排序
        )

        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination

    @staticmethod
    def get_top_rated_games(page=1, per_page=10):
        """获取根据评分平均分排序的所有游戏，并支持分页"""
        # 查询所有游戏，并计算每个游戏的关注者数量和评分平均分
        query = db.session.query(
            Game,
            db.func.count(Interaction.id).label('subscribed_count'),
            db.func.avg(Interaction.review_score).label('rating_avg')
        ).outerjoin(
            Interaction, Game.id == Interaction.game_id
        ).group_by(
            Game.id
        ).order_by(
            db.desc('rating_avg')  # 按评分平均分降序排序
        )

        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination
    
    @staticmethod
    def autocomplete_game_title(input, limit = None):
        """根据用户输入实现自动填充"""
        if not limit:
            limit = 5
        query = Game.query.filter(Game.gameTitle.like(f'%{input}%')).limit(limit)

        return [game.gameTitle for game in query.all()]
    

    @staticmethod
    def get_game_by_title(title):
        """根据游戏名称获取游戏"""
        return Game.query.filter_by(gameTitle=title).first()
        