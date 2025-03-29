from collections import defaultdict
import math
from database import db
from ..models import Interaction

print

def review_score_normalization(x):
    '评论分数归一化'
    return (x - 0.5) / (5 - 0.5)

def user_interest_value(action: Interaction) -> int:
    '通过交互记录反应'
    
    if action.disliked:
        return 0
    
    res = 0

    if action.clicked: 
        res += 0.3
    if action.subscribed:
        res += 0.6
    if action.review_score != None and action.review_score != 0:
        res += review_score_normalization(action.review_score)

    return res


def get_item_interaction_matrix():
    """
    获取物品交互矩阵，记录每个物品被哪些用户交互过
    返回：
        item_interaction_matrix: 物品交互矩阵，格式为 {item_id: {user_id}}
    """
    interactions = Interaction.get_all()
    item_interaction_matrix = defaultdict(dict)
    
    for interaction in interactions:
        user_id = interaction.user_id
        item_id = interaction.game_id
        item_interaction_matrix[item_id][user_id] = user_interest_value(interaction)
        
    return item_interaction_matrix

def calculate_item_similarity(item_interaction_matrix, similarity_method='cosine'):
    """
    计算物品之间的相似度
    参数：
        item_interaction_matrix: 物品交互矩阵
        similarity_method: 相似度计算方法，可选'cosine'或'iuf'
    返回：
        item_similarity_matrix: 物品相似度矩阵，格式为 {item_id: {similar_item_id: similarity_score}}
    """
    item_similarity_matrix = defaultdict(dict)
    
    # 记录每个物品被多少用户喜欢
    item_user_count = defaultdict(int)
    # 记录物品之间的共现次数
    item_cooccurrence = defaultdict(lambda: defaultdict(int))
    
    # 遍历每个物品及其对应的用户
    for item_id, users in item_interaction_matrix.items():
        item_user_count[item_id] = len(users)
        for user in users:
            for related_item, _ in item_interaction_matrix.items():
                if related_item == item_id:
                    continue
                item_cooccurrence[item_id][related_item] += 1
    
    # 计算相似度
    max_similarity = -1
    for item_id, related_items in item_cooccurrence.items():
        for related_item, cooccurrence in related_items.items():
            if similarity_method == 'cosine':
                similarity = cooccurrence / (math.sqrt(item_user_count[item_id]) * math.sqrt(item_user_count[related_item]))
            elif similarity_method == 'iuf':
                # IUF（Inverse User Frequency）方法，对热门物品的共现进行惩罚
                similarity = cooccurrence / (math.log(1 + item_user_count[item_id]) * math.log(1 + item_user_count[related_item]))
            else:
                similarity = 0.0
            item_similarity_matrix[item_id][related_item] = similarity

            # 更新最大相似度
            if similarity > max_similarity:
                max_similarity = similarity
            
            item_similarity_matrix[item_id][related_item] = similarity
        
        # 归一化处理，将相似度值缩放到0-1之间
        if max_similarity > 0:
            for related_item in related_items:
                item_similarity_matrix[item_id][related_item] /= max_similarity
        else:
            # 如果所有相似度都是0，则保持原值
            for related_item in related_items:
                item_similarity_matrix[item_id][related_item] = 0.0

    
    return item_similarity_matrix

def generate_item_recommendations(user_id, item_interaction_matrix, item_similarity_matrix, top_n=10, top_k=10):
    print('生成推荐物品')
    """
    为指定用户生成基于物品相似度的推荐
    参数：
        user_id: 用户ID
        item_interaction_matrix: 物品交互矩阵
        item_similarity_matrix: 物品相似度矩阵
        top_n: 推荐的物品数量
        top_k: 为每个用户交互的物品查找的最相似物品数量
    返回：
        recommendations: 推荐的物品列表，格式为 [(item_id, recommend_score)]
    """
    # 获取用户交互过的物品
    user_interacted_items = defaultdict(dict)
    for item_id, users in item_interaction_matrix.items():
        for user_id in users:
            user_interacted_items[user_id][item_id] = 1

    user_interacted_items = user_interacted_items.get(user_id, {})

    print(f'user {user_id} interacted items: {user_interacted_items}')
    
    recommendations = defaultdict(float)
    
    # 遍历用户交互过的每个物品
    for item in user_interacted_items:
        # 获取与当前物品最相似的top_k个物品
        similar_items = sorted(item_similarity_matrix[item].items(), key=lambda x: x[1], reverse=True)[:top_k]
        for similar_item, similarity in similar_items:
            # 如果相似物品已经被用户交互过，则跳过

            if similar_item in user_interacted_items:
                continue
            # 累加相似度作为推荐分数
            recommendations[similar_item] += similarity
    
    # 按推荐分数排序并取前top_n个物品
    recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    return recommendations

