from collections import defaultdict
import math
from database import db
from models import Interaction

class ItemBasedCF:
    def __init__(self):
        self.user_item_matrix = None
        self.item_similarity_matrix = None
        self.items = None
        self.users = None

    def build_user_item_matrix(self):
        """构建用户-物品矩阵"""
        interactions = Interaction.get_all()
        self.users = set()
        self.items = set()
        
        user_item_matrix = defaultdict(dict)
        
        for interaction in interactions:
            user_id = interaction.user_id
            game_id = interaction.game_id
            
            self.users.add(user_id)
            self.items.add(game_id)
            
            # 计算用户对物品的兴趣度
            interest = 0
            if interaction.clicked:
                interest += 1
            if interaction.subscribed:
                interest += 2
            if interaction.disliked:
                interest -= 1
            if interaction.review_score:
                interest += interaction.review_score
            
            user_item_matrix[user_id][game_id] = interest
        
        self.user_item_matrix = user_item_matrix

    def build_item_similarity_matrix(self):
        """构建物品相似度矩阵"""
        if not self.user_item_matrix:
            self.build_user_item_matrix()
        
        # 计算物品之间的共现次数
        item_count = defaultdict(int)
        item_sim_matrix = defaultdict(dict)
        
        for user, items in self.user_item_matrix.items():
            for item1 in items:
                item_count[item1] += 1
                for item2 in items:
                    if item1 == item2:
                        continue
                    if item2 not in item_sim_matrix[item1]:
                        item_sim_matrix[item1][item2] = 0
                    item_sim_matrix[item1][item2] += 1
        
        # 计算物品相似度
        for item1, related_items in item_sim_matrix.items():
            for item2, count in related_items.items():
                item_sim_matrix[item1][item2] = count / math.sqrt(item_count[item1] * item_count[item2])
        
        self.item_similarity_matrix = item_sim_matrix

    def recommend(self, user_id, top_n=10):
        """为指定用户生成推荐"""
        if not self.user_item_matrix or not self.item_similarity_matrix:
            self.build_user_item_matrix()
            self.build_item_similarity_matrix()
        
        # 获取用户已交互的物品
        user_items = self.user_item_matrix.get(user_id, {})
        
        # 计算推荐分数
        recommendations = defaultdict(float)
        for item, score in user_items.items():
            for related_item, similarity in self.item_similarity_matrix.get(item, {}).items():
                if related_item not in user_items:
                    recommendations[related_item] += score * similarity
        
        # 按分数排序并返回前N个推荐
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        return sorted_recommendations

def recommend_games(user_id, top_n=10):
    """为用户推荐游戏"""
    recommender = ItemBasedCF()
    recommender.build_user_item_matrix()
    recommender.build_item_similarity_matrix()
    return recommender.recommend(user_id, top_n)