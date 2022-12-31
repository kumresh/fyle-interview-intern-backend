from marshmallow import Schema, EXCLUDE, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_enum import EnumField
from core.models.assignments import Assignment, GradeEnum
from core.models.users import User
from core.models.students import Student
from core.models.teachers import Teacher
from core.libs.helpers import GeneralObject


class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student

    id = auto_field(required=False, allow_none=True)
    user_id = auto_field(required=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
    #
    # @post_load
    # def initiate_class(self, data_dict, **kwargs):
    #     return Student(**data_dict)


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher

    id = auto_field(required=False, allow_none=True)
    user_id = auto_field(required=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)

    # @post_load
    # def initiate_class(self, data_dict, **kwargs):
    #     return Teacher(**data_dict)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

    id = auto_field(required=False, allow_none=True)
    username = auto_field(required=True)
    email = auto_field(required=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)

    # @post_load
    # def initiate_class(self, data_dict, **kwargs):
    #     return User(**data_dict)


class AssignmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment
        unknown = EXCLUDE

    id = auto_field(required=False, allow_none=True)
    content = auto_field(required=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
    teacher_id = auto_field(dump_only=True)
    student_id = auto_field(dump_only=True)
    grade = auto_field(dump_only=True)
    state = auto_field(dump_only=True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return Assignment(**data_dict)


class AssignmentSubmitSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True, allow_none=False)
    teacher_id = fields.Integer(required=True, allow_none=False)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)


class SubmitGradeSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True, allow_none=False)
    grade = EnumField(GradeEnum, by_value=True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)
