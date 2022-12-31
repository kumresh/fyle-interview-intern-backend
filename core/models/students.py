from core import db
from core.libs import helpers


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.Sequence('students_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Student %r>' % self.id

    # @classmethod
    # def add_student(cls, new_student:'Student'):
    #     student = new_student
    #     db.session.add(new_student)
    #
    #     db.session.flush()
    #     return student