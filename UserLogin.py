from flask_login import UserMixin

import Models
import database


class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = database.getUserByIdForLogin(user_id)
        return self

    def create(self, user):
        self.__user = user
        print(self.__user)
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        if self.__user:
            return self.__user['id']
        else:
            return False