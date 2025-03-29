import os
from PIL import Image
import random

def construct_image_path(image_filename, base_folder='images/original_img\\'):
    """构造图片路径"""
    return os.path.join(base_folder, image_filename)

def construct_preview_path(image_filename, base_folder='images/original_img/previews'):
    """构造预览图片路径"""
    return os.path.join(base_folder, image_filename)

def check_image_exists(image_path):
    """检查图片是否存在"""
    return os.path.exists(image_path)

def generate_preview_image(image_path, preview_path, preview_size_x=640, preview_size_y=360):
    """生成预览图片"""
    try:
        with Image.open(image_path) as img:
            # 如果图片尺寸大于预览尺寸，则调整大小
            if img.width > preview_size_x or img.height > preview_size_y:
                img.thumbnail((preview_size_x, preview_size_y))
            
            # 确保预览图存储目录存在
            preview_dir = os.path.dirname(preview_path)
            if not os.path.exists(preview_dir):
                os.makedirs(preview_dir)
            
            # 保存预览图
            img.save(preview_path)
        return True
    except Exception as e:
        print(f"图片处理失败: {str(e)}")
        return False

def get_default_image_path(base_folder='images/original_img'):
    """获取默认图片路径"""
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
    default_image_path = os.path.join(default_image_folder, selected_image)
    
    if not os.path.exists(default_image_path):
        raise FileNotFoundError("默认图片文件不存在")
    
    return default_image_path

def get_image_path(image_filename, base_folder='images/original_img'):
    """获取图片路径，如果不存在则返回随机默认图片路径"""
    image_path = construct_image_path(image_filename, base_folder)
    if check_image_exists(image_path):
        return image_path
    else:
        return get_default_image_path(base_folder)