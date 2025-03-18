from flask_admin.contrib.sqla import ModelView

class NewsView(ModelView):
    column_list = ('id', 
                   'type', 
                   'image', 
                   'title', 
                   'description', 
                   'date'
                   )