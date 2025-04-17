from ..models import Interaction, User, Game
from collections import defaultdict
import math
from database import db

score_impact_factor={
    1.0: 0,
    2.5: 0.5,
    4.0: 1.0,
    5.0: 1.2,
}

default_implicit_interaction_score ={
    'clicked': 1,
    'subscribed': 2,
    'disliked': -1,
}

def get_user_interaction_matrix():
    """获取所有的交互矩阵信息，包括显式评分和隐式行为的权重"""
    interactions = Interaction.get_all()
    user_ids = {interaction.user_id for interaction in interactions}
    game_ids = {interaction.game_id for interaction in interactions}

    user_interaction_matrix = {user_id: {game_id: 0.0 for game_id in game_ids} for user_id in user_ids}

    # 遍历交互记录，计算每个用户的每个游戏的综合评分
    for interaction in interactions:
        user_id = interaction.user_id
        game_id = interaction.game_id
        final_score = 0.0
        if interaction.review_score != 0.0:
            for score_range, impact in score_impact_factor.items():
                if interaction.review_score <= score_range:
                    final_score = interaction.review_score * impact
                    break
        implicit_score = 0
        if interaction.clicked:
            implicit_score += default_implicit_interaction_score['clicked']
        if interaction.subscribed:
            implicit_score += default_implicit_interaction_score['subscribed']
        if interaction.disliked:
            implicit_score += default_implicit_interaction_score['disliked']

        if final_score == 0.0:
            final_score = implicit_score

        user_interaction_matrix[user_id][game_id] = final_score
    
    return user_interaction_matrix


def calculate_user_interaction_sparsity() -> float:
    """计算用户交互矩阵的稀疏性。
    返回:
        sparsity (float): 用户交互矩阵的稀疏性
    """
    interactions = Interaction.get_all()
    user_num = User.query.count()
    game_num = Game.query.count()
    total_possible_interactions = user_num * game_num
    actual_interactions = len(interactions)
    sparsity = actual_interactions / total_possible_interactions
    return sparsity


def improved_cosine_similarity(user_interaction_matrix, target_user_id, n=5):
    """
    基于改进的相似性算法计算与目标用户最相似的用户集
    参数:
        user_interaction_matrix (dict): 用户交互矩阵，格式为 {user_id: {game_id: final_score}}
        target_user_id (int): 目标用户ID
        n (int): 返回的相似用户数量,默认为5
    返回:
        similar_users (list): 与目标用户最相似的用户列表，格式为 [(user_id, similarity)]
    """
    target_user_interactions = user_interaction_matrix.get(target_user_id, {})
    target_user_avg = sum(target_user_interactions.values()) / len(target_user_interactions) if target_user_interactions else 0.0
    similarities = {}

    for user_id, interactions in user_interaction_matrix.items():
        if user_id == target_user_id:
            continue

        current_user_avg = sum(interactions.values()) / len(interactions) if interactions else 0.0

        numerator = 0.0
        denominator_a = 0.0
        denominator_b = 0.0
        
        for game_id in interactions:
            target_score = target_user_interactions.get(game_id, 0.0)
            current_score = interactions[game_id]
            numerator += (target_score - target_user_avg) * (current_score - current_user_avg)
            denominator_a += (target_score - target_user_avg) ** 2
            denominator_b += (current_score - current_user_avg) ** 2

        if denominator_a == 0 or denominator_b == 0:
            similarity = 0.0
        else:
            similarity = numerator / ( (denominator_a ** 0.5) * (denominator_b ** 0.5) )
        
        similarities[user_id] = similarity

    similar_users = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:n]
    return similar_users


def generate_game_recommendations(user_interaction_matrix, target_user_id, similar_users, top_n=10):
    """
    生成游戏推荐结果。
    
    参数:
        user_interaction_matrix (dict): 用户交互矩阵，格式为 {user_id: {game_id: final_score}}
        target_user_id (int): 目标用户ID
        similar_users (list): 与目标用户最相似的用户列表，格式为 [(user_id, similarity)]
        top_n (int): 推荐的游戏数量，默认为10
    
    返回:
        recommendations (list): 推荐的游戏列表，格式为 [(game_id, predicted_score)]
    """

    target_user_interactions = user_interaction_matrix.get(target_user_id, {}) 
    target_user_avg = sum(target_user_interactions.values()) / len(target_user_interactions) if target_user_interactions else 0.0
    similar_user_ids = [user_id for user_id, similarity in similar_users]

    similar_users_interactions = {user_id: user_interaction_matrix.get(user_id, {}) for user_id in similar_user_ids}
    recommendations = {}

    for user_id, interactions in similar_users_interactions.items():
        for game_id, score in interactions.items():
            if game_id in target_user_interactions:
                if target_user_interactions[game_id] != 0.0:
                    if target_user_interactions[game_id] != 1.0:
                        continue

            similarity = dict(similar_users)[user_id]
            predicted_score = target_user_avg + (similarity * (score - target_user_avg))

            if game_id in recommendations:
                recommendations[game_id].append(predicted_score)
            else:
                recommendations[game_id] = [predicted_score]

    averaged_recommendations = {}
    for game_id, scores in recommendations.items():
        averaged_score = sum(scores) / len(scores)
        averaged_recommendations[game_id] = averaged_score

    sorted_recommendations = sorted(averaged_recommendations.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return sorted_recommendations

