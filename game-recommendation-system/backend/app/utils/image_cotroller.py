import os
from PIL import Image

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
    default_image_path = os.path.join(base_folder, 'defaultGameImage.jpg')
    if not os.path.exists(default_image_path):
        raise FileNotFoundError("默认图片文件不存在")
    return default_image_path