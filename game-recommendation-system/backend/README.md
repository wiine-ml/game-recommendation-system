后端返回状态码
| code | text | description |
| --- | --- | --- |
| 200  | OK   | The request has succeeded. |
| not 200 | error | error occurred. |


---
后端接口设计
| 方法     | 路由                                 | 描述                               | 返回状态码 |
|----------|--------------------------------------|------------------------------------|------------|
| GET      | /api/test                            | 测试连接                          | 200        |
| POST     | /api/user/login                      | 用户登录                          | 200, 401   |
| POST     | /api/admin/login                     | 管理员登录                        | 200, 401   |
| POST     | /api/register                        | 用户注册                          | 200, 400, 409 |
| GET      | /api/notice/<int:notice_id>         | 根据ID获取公告                    | 200, 404   |
| POST     | /api/notice                          | 创建公告                          | 201, 400   |
| GET      | /api/notice/page/<int:page_id>      | 获取分页的公告列表                | 200        |
| PUT      | /api/notice/update/<int:notice_id>  | 更新公告                          | 200, 404   |
| GET      | /api/games/page/<int:page_id>       | 分页获取游戏列表                  | 200        |
| GET      | /api/games/top_subscribed            | 获取最受欢迎的游戏                | 200        |
| GET      | /api/games/top_rated                 | 获取评分最高的游戏                | 200        |
| GET      | /api/games/<int:game_id>            | 根据游戏ID获取游戏详细信息        | 200, 404   |
| POST     | /api/interactions                    | 更新用户与游戏的交互信息         | 200, 400   |
| GET      | /api/interactions/info               | 获取用户的交互信息统计           | 200, 400   |
| GET      | /api/users/page/<int:page>          | 获取分页的用户列表                | 200        |
| POST     | /api/users/search                    | 根据条件搜索用户                  | 200        |
| GET      | /api/reviews/get                    | 获取用户的评论                    | 200, 400, 404 |
| POST     | /api/reviews/create                  | 创建评论                          | 201, 400   |
| POST     | /api/reviews/update                  | 更新评论                          | 200, 404   |
| POST     | /api/reviews/delete                  | 删除评论                          | 200, 404   |
| POST     | /api/reviews/get_all                 | 获取用户所有评论                  | 200, 400   |
| POST     | /api/reviews/clear_multiple          | 清除多条评论                      | 200, 400   |
| GET      | /api/news                            | 获取所有新闻                      | 200        |
| GET      | /api/news/page/<int:page_id>        | 获取分页的新闻列表                | 200        |
| POST     | /api/news                              | 创建新闻                          | 201, 400   |
| GET      | /api/recommendations                 | 获取游戏推荐                      | 200, 400   |


---
游戏数据集来源: https://www.heywhale.com/mw/dataset/65f6e1a29fb3effcf1a59ca1

