import os
from flask_admin import Admin
from models import db, Users, Characters, Planets, Favourites
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class My_favourites_view(ModelView):
        column_list = ('id', 'user_id', 'character_name', 'planet_name')
        form_columns = ('user_id', 'character_id', 'planet_id')
        can_create = True

    # Add your models here, for example, this is how we add the User model to the admin
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(My_favourites_view(Favourites, db.session))

    # You can duplicate that line to add new models
    # admin.add_view(ModelView(YourModelName, db.session))

if __name__ == '__main__':
    setup_admin(app)
