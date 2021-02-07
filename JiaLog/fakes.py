from JiaLog.models import Admin, Category, Note, Comment
from JiaLog.extensions import db
import random
from faker import Faker


def fake_admin():
    admin = Admin(
        username='admin',
        my_title="Leo's Page",
        my_sub_title='Welcom Everyone!',
        name='Jia',
        about='hello everyone'
    )
    admin.set_password('12345678')
    db.session.add(admin)
    db.session.commit()


fake = Faker()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except:
            db.session.rollback()


def fake_notes(count=50):
    for i in range(count):
        note = Note(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(note)
    db.session.commit()


def fake_comments(count=500):
    # 审阅过的
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            note=Note.query.get(random.randint(1,Note.query.count()))
        )
        db.session.add(comment)
    salt = int(count*0.1)
    # 未审阅的
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            note=Note.query.get(random.randint(1, Note.query.count()))
        )
        db.session.add(comment)
        comment = Comment(
            author="Jia Yaobo",
            email='ssss@126.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            note=Note.query.get(random.randint(1, Note.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            note=Note.query.get(random.randint(1, Note.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
