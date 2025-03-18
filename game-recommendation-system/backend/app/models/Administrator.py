from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import text
from database import db

SUPER_ADMIN = 'superadmin'
SUPER_ADMIN_PASSWORD = '123456'

class Administrator(db.Model):
    __tablename__ = 'administrators'

    # 管理员信息
    id = db.Column(db.Integer, primary_key=True)
    admin_type = db.Column(db.String(64), nullable=False)  # 可以是 'admin' 或 'superAdmin'
    admin_name = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, id, admin_type, admin_name, password):
        self.id = id
        self.admin_type = admin_type
        self.admin_name = admin_name
        self.password = generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return f"<Administrator {self.admin_name} ({self.admin_type})>"
    
    @staticmethod
    def get_next_id():
        """获取下一个可用的编号"""
        result = db.session.execute(text("SELECT MAX(id) FROM administrators"))
        max_id = result.scalar()
        return max_id + 1 if max_id is not None else 0

    @staticmethod
    def add(admin_type, admin_name, password):
        """添加管理员"""
        # 检查管理员名称是否已存在
        existing_admin = db.session.execute(
            text("SELECT * FROM administrators WHERE admin_name = :admin_name"),
            {'admin_name': admin_name}
        ).fetchone()
        if existing_admin:
            raise ValueError("管理员名称已存在")

        # 检查 admin_type 是否有效
        if admin_type not in ['admin', 'superAdmin']:
            raise ValueError("无效的管理员类型")

        new_admin = Administrator(id = Administrator.get_next_id(), admin_type=admin_type, admin_name=admin_name, password=password)
        db.session.add(new_admin)
        db.session.commit()

    '''
    @staticmethod
    def query(admin_name=None):
        """根据管理员名称查询管理员"""
        if admin_name:
            return db.session.execute(
                text("SELECT * FROM administrators WHERE admin_name = :admin_name"),
                {'admin_name': admin_name}
            ).fetchone()
        else:
            return db.session.execute(text("SELECT * FROM administrators")).fetchall()'
    '''

    @staticmethod
    def get_admin_by_name(admin_name):
        """根据管理员名称获取管理员"""
        return db.session.execute(
            text("SELECT * FROM administrators WHERE admin_name = :admin_name"),
            {'admin_name': admin_name}
        ).fetchone()

    @staticmethod
    def check_password(admin, password):
        """检查密码是否正确"""
        return check_password_hash(admin.password, password)

    def update(self, admin_type=None, admin_name=None, password=None):
        """更新管理员信息"""
        if admin_name and admin_name != self.admin_name:
            # 检查新的管理员名称是否已存在
            existing_admin = db.session.execute(
                text("SELECT * FROM administrators WHERE admin_name = :admin_name"),
                {'admin_name': admin_name}
            ).fetchone()
            if existing_admin:
                raise ValueError("管理员名称已存在")
            self.admin_name = admin_name

        if admin_type:
            # 检查 admin_type 是否有效
            if admin_type not in ['admin', 'superAdmin']:
                raise ValueError("无效的管理员类型")
            self.admin_type = admin_type

        if password:
            self.password = generate_password_hash(password).decode('utf-8')

        db.session.commit()

    def delete(self):
        """删除管理员"""
        db.session.delete(self)
        db.session.commit()