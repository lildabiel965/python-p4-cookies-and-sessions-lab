#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    return jsonify({
        'articles': [
            {
                'id': a.id,
                'author': a.author,
                'title': a.title,
                'preview': a.preview,
                'minutes_to_read': a.minutes_to_read,
                'date': a.date.isoformat()
            } for a in articles
        ]
    }), 200

@app.route('/articles/<int:id>')
def show_article(id):
    if 'page_views' not in session:
        session['page_views'] = 0

    session['page_views'] += 1

    if session['page_views'] <= 3:
        article = db.session.get(Article, id)
        if not article:
            return {'message': 'Article not found'}, 404
        return {
            'id': article.id,
            'author': article.author,
            'title': article.title,
            'content': article.content,
            'preview': article.preview,
            'minutes_to_read': article.minutes_to_read,
            'date': article.date.isoformat()
        }, 200
    else:
        return {'message': 'Maximum pageview limit reached'}, 401

@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to the Blog API',
        'endpoints': {
            'articles': '/articles',
            'article': '/articles/<id>',
            'clear': '/clear'
        }
    }), 200

if __name__ == '__main__':
    app.run(port=5555)
