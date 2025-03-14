from core import db
from core.libs import helpers


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    # def __repr__(self):
    #     return '<User %r>' % self.username

    @classmethod
    def filter(cls, *criterion):
        return db.session.query(cls).filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.filter(cls.email == email).first()
    
    # @classmethod
    # def add_user(cls, new_user:'User'):
    #     user = new_user
    #     db.session.add(new_user)

    #     db.session.flush()
    #     return user
    
    # @classmethod
    # def get_user_list(cls):
    #     users = cls.filter().all()
    #     return users
        

