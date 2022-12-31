import enum
from core import db
from core.apis.decorators import Principal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum


class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class AssignmentStateEnum(str, enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False,
                           onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Assignment %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def upsert(cls, assignment_new: 'Assignment'):
        assignment = Assignment.get_by_id(assignment_new.id)
        if assignment_new.id:
            assertions.assert_valid(AssignmentStateEnum.DRAFT, 'only assignment in draft state can be edited')
            assignment.content = assignment_new.content
        else:
            assignment = assignment_new
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    @classmethod
    def submit_grade(cls, _id, _grade, _principal: Principal):
        assignment = Assignment.get_by_id(_id)

        if assignment:
            assertions.assert_valid(assignment.state.name == AssignmentStateEnum.DRAFT.name, 'only a submitted assignment can be graded')
            assignment.grade = GradeEnum(_grade)
        else:
            assertions.assert_found(assignment, 'No assignment was found')

    @classmethod
    def submit(cls, _id, teacher_id, principal: Principal):
        assignment = Assignment.get_by_id(_id)

        if assignment.state.name != AssignmentStateEnum.DRAFT.name:
            assertions.assert_valid(AssignmentStateEnum.DRAFT.name == assignment.state.name,
                                    "only a draft assignment can be submitted")
        else:
            assignment.teacher_id = teacher_id
            assignment.state = AssignmentStateEnum.SUBMITTED

        db.session.flush()
        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        return cls.filter(cls.student_id == student_id).all()

    @classmethod
    def get_assignments_by_teacher(cls, teacher_id):
        return cls.filter(cls.teacher_id == teacher_id).all()
