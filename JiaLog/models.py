from flask_sqlalchemy import SQLAlchemy
from JiaLog.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    my_title = db.Column(db.String(60))
    my_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    notes = db.relationship('Note', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        notes = self.notes[:]
        for note in notes:
            note.category = default_category

        db.session.delete(self)
        db.session.commit()


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    like = db.Column(db.Integer, default=0)
    can_comment = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='notes')
    comments = db.relationship('Comment', back_populates='note', cascade='all')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    note = db.relationship('Note', back_populates='comments')
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', back_populates='replied', cascade='all')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
