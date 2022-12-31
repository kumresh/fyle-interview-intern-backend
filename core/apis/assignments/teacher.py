from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher

from .schema import AssignmentSchema, TeacherSchema, SubmitGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


# @teacher_assignments_resources.route('/create', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# def insert_student(incoming_payload):
#     teacher = TeacherSchema().load(incoming_payload)
#     inserted_data = Teacher.add_teacher(teacher)
#     db.session.commit()
#
#     seralize_data = TeacherSchema().dump(inserted_data)
#     return APIResponse.respond(data=seralize_data)


@teacher_assignments_resources.route('assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def submit_grade(p, incoming_payload):
    """Submit an grade"""
    submit_grade_payload = SubmitGradeSchema().load(incoming_payload)

    Assignment.submit_grade(
        _id=submit_grade_payload.id,
        _grade=submit_grade_payload.grade,
        _principal=p
    )


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)
