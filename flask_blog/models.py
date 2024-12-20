from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Category(db.Model):
    """
    Category - категория поста
    id - уникальный ключ
    name - имя категории
    posts - свзяь с постами
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    """
    Tag - тэг поста
    id - уникальный ключ
    name - имя категории
    posts - свзяь с постами
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary='post_tag', backref='tags', lazy=True)

    def __repr__(self):
        return f'<Tag {self.name}>'

# Создание таблицы с помощью средств SQLAlchemy
post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                    )


class Post(db.Model):
    """
        Основная модель в таблице
        id - Уникальный ключ
        title - заголовок
        content - текст поста
        date - дата публикации
        category_id - номер категории поста
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def repr(self):
        return f'<Post {self.title}>'

    @classmethod
    def newest_first(cls):
        return cls.query.order_by(cls.date.desc())
