from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Category, Tag, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)


@app.route('/')
def index():
    """
        Главная страница приложения
        выводит все новейшие посты первыми
    """
    posts = Post.newest_first().all()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    """
        Этот маршрут, позволяет открыть
        отдельный пост
    """
    current_post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=current_post)


@app.route('/category/<int:category_id>')
def category(category_id):
    """
        Этот маршрут, позволяет просматривать посты
        определенной категории
    """
    category_obj = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category_id).order_by(Post.date.desc()).all()
    return render_template('category.html', category=category_obj, posts=posts)


@app.route('/tag/<int:tag_id>')
def tag(tag_id):
    """
        Этот маршрут, позволяет просматривать посты
        определенного тега
    """
    tag_obj = Tag.query.get_or_404(tag_id)
    posts = Post.query.filter(Post.tags.any(id=tag_id)).order_by(Post.date.desc()).all()
    return render_template('tag.html', tag=tag_obj, posts=posts)


@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    """
        Этот маршрут, дает возможность создать новый
        пост использую запрост POST
    """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['category']
        tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags')]
        create_post = Post(title=title, content=content, category_id=category_id)
        for tag_id in tag_ids:
            post_tag = Tag.query.get(tag_id)
            create_post.tags.append(post_tag)
        db.session.add(create_post)
        db.session.commit()
        flash('Запись создана!', 'success')
        return redirect(url_for('index'))
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('new_post.html', categories=categories, tags=tags)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    edit_post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        edit_post.title = request.form['title']
        edit_post.content = request.form['content']
        edit_post.category_id = request.form['category']
        tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags')]
        edit_post.tags = []
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            edit_post.tags.append(tag)
        db.session.commit()
        flash('Запись обновлена!', 'success')
        return redirect(url_for('index'))
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('edit_post.html', post=edit_post, categories=categories, tags=tags)


@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    select_post = Post.query.get_or_404(post_id)
    db.session.delete(select_post)
    db.session.commit()
    flash('Запись удалена!', 'success')
    return redirect(url_for('index'))  


if __name__ == '__main__':
    app.run(debug=True)