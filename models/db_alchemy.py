from main import db


class AssignmentDb(db.Model):
    __tablename__ = 'Assignment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(10))
    max_points = db.Column(db.Integer)
    delivery_date = db.Column(db.String(10))
    content = db.Column(db.String(200))

class AttendanceDb(db.Model):
    __tablename__ = 'Attendance'

    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    presence = db.Column(db.String(1), nullable=False)

class CheckpointAssignmentDb(db.Model):
    __tablename__ = 'Checkpoint_assignment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    assignment = db.Column(db.String(80))
    submissions = db.relationship('CheckpointSubmissionDb', backref='submissions', lazy='dynamic')

class CheckpointSubmissionDb(db.Model):
    __tablename__ = 'Checkpoint_submission'

    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    id_mentor = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    id_assignment = db.Column(db.Integer, db.ForeignKey('Checkpoint_assignment.id'))
    date = db.Column(db.String(10))
    card = db.Column(db.String(10))


class SubmissionDb(db.Model):
    __tablename__ = 'Submission'
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    id_assignment = db.Column(db.Integer, db.ForeignKey('Assignment.id'), nullable=False)
    id_mentor = db.Column(db.Integer, db.ForeignKey('User.id'))
    result = db.Column(db.String(200))
    grade = db.Column(db.Integer)
    date = db.Column(db.String(10))

class TeamDb(db.Model):
    __tablename__ = 'Team'

    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    name = db.Column(db.String(30), nullable=False)

class UserDb(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False, unique=True)
    user_type = db.Column(db.String(30), nullable=False)

    # student_checkpoint_submission = db.relationship('CheckpointSubmissionDb', backref='student_checkpoint_submission_ref', lazy="dynamic",
    #                                                 cascade='all, delete', foreign_keys='CheckpointSubmissionDb.id_student')

    student_checkpoint_submission = db.relationship('CheckpointSubmissionDb', backref='student', cascade='all, delete', lazy="dynamic",
                              foreign_keys='CheckpointSubmissionDb.id_student')
    mentor_checkpoint_submission = db.relationship('CheckpointSubmissionDb', backref='mentor', lazy="dynamic",
                             foreign_keys='CheckpointSubmissionDb.id_mentor')
    student_submission = db.relationship('SubmissionDb', backref='student_submission_ref', cascade='all, delete', lazy="dynamic",
                              foreign_keys='SubmissionDb.id_student')
    mentor_submission = db.relationship('SubmissionDb', backref='mentor_submission_ref', lazy="dynamic",
                             foreign_keys='SubmissionDb.id_mentor')
    teams = db.relationship('TeamDb', backref='teams', cascade='all, delete', lazy='dynamic')
    attendance = db.relationship('AttendanceDb', backref='attendance', lazy='dynamic')
