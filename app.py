#  micro framework-vid frameworkov
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class FeedBack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback_name = db.Column(db.String(100), nullable=False)
    short_feedback = db.Column(db.String(300), nullable=False)
    feed_back = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<FeedBack %r>' % self.id


@app.route('/')  #golovna storinka
def index():
    return render_template('index.html')


@app.route('/about')  #pro nas page
def about():
    return render_template('about.html')


@app.route('/categor')  #categor page
def categor():
    return render_template('categor.html')


@app.route('/costs')  #costs page
def costs():
    return render_template('costs.html')


@app.route('/contacts')  #contact page
def contacts():
    return render_template('contacts.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/cont')
def cont():
    return render_template('cont.html')


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/about')
    except:
        return 'Problem'


@app.route('/posts/<int:id>/update', methods=['POSTS', 'GET'])
def post_update(id):
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При додавані статті виникла помилка'
    else:
        article = Article.query.get(id)
        return render_template('post_update.html', article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При додавані статті виникла помилка'
    else:
        return render_template('create-article.html')


@app.route('/create_feedback', methods=['POST', 'GET'])
def create_feed_back():
    if request.method == 'POST':
        feedback_name = request.form['feedback_name']
        short_feedback = request.form['short_feedback']
        feed_back = request.form['feed_back']

        article = FeedBack(feedback_name=feedback_name, short_feedback=short_feedback, feed_back=feed_back)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return 'При додавані статті виникла помилка'
    else:
        return render_template('create_feed_back.html')


if __name__ == "__main__":
    app.run(debug=True)
