from flask import Blueprint, request, jsonify, send_file
from ..models import Game, Interaction
import random
import os
import zipfile
from io import BytesIO

from ..utils import (
    construct_image_path,
    construct_preview_path,
    check_image_exists,
    generate_preview_image,
    get_default_image_path,
    get_image_path,
)

AdminSetting = None

game_img_bp = Blueprint('game_img_api', __name__)

@game_img_bp.route('/api/games/image/read/<int:game_id>', methods=['GET'])
def read_game_image(game_id):
    """获取游戏图片"""
    try:
        # 查询游戏是否存在
        game = Game.get_game_by_id(game_id)
        if not game:
            return jsonify({"error": "游戏不存在"}), 404
        
        """获取默认图片路径"""
        base_folder='images/original_img'
        default_image_folder = os.path.join(base_folder, 'default_image')
        default_image_files = [
            'default_game_cover_1.jpg',
            'default_game_cover_2.jpg',
            'default_game_cover_3.jpg',
            'default_game_cover_4.jpg',
            'default_game_cover_5.jpg'
        ]
    
        # 随机选择一张默认图片
        selected_image = random.choice(default_image_files)
        # 如果游戏没有设置图片，则使用默认图片
        image_filename = game.gameImage if game.gameImage else selected_image
        
        # 构造图片路径
        image_path = get_image_path(image_filename)
        
        # 检查图片文件是否存在
        if not check_image_exists(image_path):
            # 如果图片不存在，返回默认图片
            default_image_path = get_default_image_path()
            return send_file(default_image_path, mimetype='image/jpeg')
        
        # 返回图片文件
        return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

@game_img_bp.route('/api/games/preview_image/read/<int:game_id>', methods=['GET'])
def read_game_preview_image(game_id):
    """获取游戏预览图片"""
    try:
        # 定义预览图片的尺寸
        Preview_size_x, Preview_size_y = 640, 360

        # 查询游戏是否存在
        game = Game.get_game_by_id(game_id)
        if not game:
            return jsonify({"error": "游戏不存在"}), 404
        
        """获取默认图片路径"""
        base_folder='images/original_img'
        default_image_folder = os.path.join(base_folder, 'default_image')
        default_image_files = [
            'default_game_cover_1.jpg',
            'default_game_cover_2.jpg',
            'default_game_cover_3.jpg',
            'default_game_cover_4.jpg',
            'default_game_cover_5.jpg'
        ]
    
        # 随机选择一张默认图片
        selected_image = random.choice(default_image_files)
        # 如果游戏没有设置图片，则使用默认图片
        image_filename = game.gameImage if game.gameImage else selected_image
        
        # 构造原图路径和预览图路径
        image_path = get_image_path(image_filename)
        preview_image_path = construct_preview_path(image_filename)
        
  # 检查预览图是否存在
        if not check_image_exists(preview_image_path):
            # 如果预览图不存在，检查原图是否存在
            if not check_image_exists(image_path):
                # 如果原图也不存在，返回随机默认图片
                default_image_path = get_image_path("defaultGameImage.jpg")
                return send_file(default_image_path, mimetype='image/jpeg')
            
            # 如果原图存在但预览图不存在，生成预览图
            if not generate_preview_image(image_path, preview_image_path, Preview_size_x, Preview_size_y):
                default_image_path = get_image_path("defaultGameImage.jpg")
                return send_file(default_image_path, mimetype='image/jpeg')
        
        # 返回预览图
        return send_file(preview_image_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@game_img_bp.route('/api/games/promote_image', methods=['GET'])
def read_promote_image():
    """获取前五名游戏的图片"""
    try:
        # 获取前五名游戏（按关注数排序）
        games = Game.query.order_by(Game.followers.desc()).limit(5).all()
        print(games)  # 打印游戏对象，确保查询正确

        if not games:
            return jsonify({"message": "没有游戏数据"}), 200

        # 创建一个内存中的 ZIP 文件
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for game in games:
                # 构造图片路径
                image_filename = game.gameImage if game.gameImage else "defaultGameImage.jpg"
                image_path = construct_image_path(image_filename)
                print(f"图片路径: {image_path}")  # 打印图片路径，检查是否正确

                # 检查图片文件是否存在
                if not check_image_exists(image_path):
                    # 如果图片不存在，使用默认图片
                    default_image_path = get_default_image_path()
                    image_path = default_image_path
                    print(f"使用默认图片: {image_path}")  # 打印默认图片路径

                # 确保文件名唯一，避免重复
                base_name = os.path.basename(image_path)
                unique_name = f"{game.id}_{base_name}"
                zip_file.write(image_path, unique_name)

        # 准备返回 ZIP 文件
        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='top_games_images.zip'
        )

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

