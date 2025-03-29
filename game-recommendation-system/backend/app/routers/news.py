from flask import Blueprint, request, jsonify, send_file
from ..models import News

import os
from PIL import Image


news_bp = Blueprint('news_api', __name__)


@news_bp.route('/api/news/create', methods=['POST'])
def create_news():
    """创建新闻"""
    #TODOs
    pass


@news_bp.route('/api/news/read', methods=['GET'])
def read_news():
    """获取所有新闻"""
    try:
        news_list = News.get_all_news()
        return jsonify({
            "data": news_list,
            "msg": "获取新闻数据成功",
            "success": True,
        }), 200
    except Exception as e:
        return jsonify({
            'data': None,
            "msg": "获取新闻数据失败" + str(e),
            "success": False
            }), 500
    
    
@news_bp.route('/api/news/read/page/<int:page_id>', methods=['GET'])
def read_page_news(page_id):
    """获取分页的新闻列表"""
    items_per_page = int(request.args.get('items_per_page', 10))  # 每页显示的条数，默认10

    # 查询所有新闻
    query = News.query.order_by(News.date.desc())

    # 获取总条数和总页数
    total_items = query.count()
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # 分页查询
    news = query.paginate(page=page_id, per_page=items_per_page, error_out=False).items

    # 构造返回数据
    news_list = []
    for item in news:
        news_list.append({
            'id': item.id,
            'type': item.type,
            'image': item.image,
            'title': item.title,
            'description': item.description,
            'date': str(item.date)
        })

    return jsonify({
        "data": news_list,  # 修改后的字段名，适配前端组件
        "totalPages": total_pages,
        "msg": "获取分页新闻列表成功",
        "success": True
    }), 200


@news_bp.route('/api/news/read/<int:news_id>', methods=['GET'])
def read_news_by_id(news_id):
    """根据ID获取单条新闻"""
    try:
        news = News.get_news_by_id(news_id)
        if not news:
            return jsonify({
                "msg": "新闻不存在",
                "success": False
            }), 404
        
        # 将新闻对象转换为字典
        news_dict = {
            'id': news.id,
            'type': news.type,
            'image': news.image,
            'title': news.title,
            'description': news.description,
            'date': str(news.date)
        }

        return jsonify({
            "data": news_dict,
            "msg": "获取新闻成功",
            "success": True
        }), 200

    except Exception as e:
        return jsonify({
            "msg": "获取新闻失败: " + str(e),
            "success": False
        }), 500
    

@news_bp.route('/api/news/update/<int:news_id>', methods=['POST'])
def update_news(news_id):
    """更新新闻"""
    #TODOs
    pass


@news_bp.route('/api/news/delete/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    """删除新闻"""
    #TODOs
    pass



def construct_image_path(image_filename):
    """构造图片的完整路径"""
    return os.path.join('images', 'illustrations', image_filename)

def check_image_exists(image_path):
    """检查图片文件是否存在"""
    return os.path.exists(image_path)

def get_default_image_path():
    """获取默认图片的路径"""
    return os.path.join('images', 'illustrations', 'defaultillustrationsImage.jpg')

@news_bp.route('/api/news/img/read/<int:news_id>', methods=['GET'])
def read_news_image(news_id):
    """获取新闻的图片"""
    try:
        # 查询新闻是否存在
        news = News.get_news_by_id(news_id)
        if not news:
            return jsonify({"error": "新闻不存在"}), 404
        
        # 如果新闻没有设置图片，则使用默认图片
        image_filename = news.image if news.image else "defaultillustrationsImage.jpg"
        
        # 构造图片路径
        image_path = construct_image_path(image_filename)
        
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
