"""
You will need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the str ID of a user, and return the corresponding user object. For example:

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
It should return None (not raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and processing will continue.)
"""
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))  # Almacena el hash de la contraseña

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        if password==self.password:
            return True
        else:
            return False
    @staticmethod
    def get(user_id):
        return User.query.get(int(user_id))
