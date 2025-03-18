# 游戏推荐系统

## 简介
游戏推荐系统是一个基于Vue.js和Python Flask的Web应用程序，旨在为用户提供个性化的游戏推荐服务。该项目包括一个前端界面，允许用户查看推荐的游戏列表、设置账户信息以及上传头像。后端部分负责处理数据请求、推荐算法逻辑以及与数据库的交互。

## 项目结构
game-recommendation-system/  
├── backend/                 # 后端服务  
│   ├── app/                # 应用核心  
│   │   ├── __init__.py     # Flask应用初始化  
│   │   ├── routers/        # API路由模块  
│   │   │   ├── __init__.py# 路由蓝图注册  
│   │   │   ├── user.py     # 用户相关路由（头像上传/获取）  
│   │   │   └── recommendation.py # 推荐系统路由  
│   │   ├── models/         # 数据模型   
│   │   ├── views/         # Flask-Admin视图定义  
│   │   └── utils/         # 工具模块  
│   │       └── collaborative_filtering.py # 协同过滤推荐算法  
│   ├── dataset/            # 数据集存储  
│   │   └── IGN games from best to worst.csv # 游戏数据集  
│   ├── datainsert.py       # 数据导入脚本(SQLite)  
│   └── run.py              # 服务启动入口  
│   └── database.py         # 创建全局的 SQLAlchemy 实例  
│   └── config.py           # 运行配置  
│  
└── frontend-web/           # 前端应用  
    ├── src/  
    │   ├── components/     # Vue组件  
    │   │   └── ContentAccountInfo.vue # 账户信息组件（含头像上传）  
    │   ├── services/       # 服务模块  
    │   │   └── UserInfoStore.js # Vuex用户状态管理  
    │   └── assets/  
    │       └── base.css    # 基础样式  
    ├── vite.config.js      # Vite构建配置  
    ├── package.json        # 项目依赖配置  
    └── eslint.config.js    # ESLint配置   

## 后端说明

后端主要使用Flask框架进行开发，Flask-admin用于管理后台界面。后端代码位于`game-recommendation-system/backend/`目录下，其中包括路由定义、视图配置、数据库连接和数据插入模块。
运行在port:5000

- `app/routers/__init__.py`：定义了用户路由。
- `app/routers/user.py`：包含了用户相关的路由处理函数。
- `app/view/__init__.py`：初始化视图模块。
- `config.py`：项目配置文件，定义了不同的环境配置。
- `dataset/IGN games from best to worst.csv`：包含游戏评分和详情的CSV文件数据集。
- `datainsert.py`：实现从CSV文件插入数据到SQLite数据库的功能。
- `run.py`：项目的启动文件，负责初始化Flask应用并运行。




## 前端主要依赖项
Vue.js: ^3.5.13  
Vuex: ^4.1.0  
Axios: ^1.8.1  
Vite: ^6.1.0  
Prettier: ^3.5.1  

## 前端说明

前端主要使用Vue 3进行开发，Vuex用于状态管理，确保用户信息和游戏数据能够全局共享和管理。Vite作为构建工具，提供快速的开发体验。  
前端代码位于`game-recommendation-system/frontend-web/src/`目录下  
样式文件位于`src/assets/`目录下  
组件文件位于`src/components/`目录下  
服务文件位于`src/services/`目录下  

- `ContentAccountInfo.vue`：用于显示用户账户信息以及上传头像的功能。
- `UserInfoStore.js`：Vuex store模块，负责用户信息的存储和操作，如设置用户ID、上传头像等。
- `base.css`：项目的基础样式文件，定义了颜色变量等。
- `vite.config.js`：Vite配置文件，用于配置开发服务器和构建选项。
- `package.json`：项目依赖配置文件。
- `package-lock.json`：锁定项目的依赖版本。

---

## 图片示例
![image](README_IMG\1.png)
![image](README_IMG\2.png)
![image](README_IMG\3.png)
![image](README_IMG\4.png)
![image](README_IMG\5.png)
![image](README_IMG\6.png)
![image](README_IMG\7.png)
![image](README_IMG\8.png)
