from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():

    s = session()
    label, _id = request.query["label"], request.query["id"]
    row = s.query(News).filter(News.id == _id).all()[0]
    row.label = label
    s.add(row)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():

    s = session()

    number_of_pages = 10
    url = "https://news.ycombinator.com/newest?next=27321578&n=61"
    news = get_news(url, number_of_pages)

    for article in news:
        article_id = int(article['article_id'])
        row = s.query(News).filter(News.article_id == article_id).all()
        if not row:

            new_entry = News(title=article.get('title'), author=article.get('author'), url=article.get(
                'url'), comments=article.get('comments'), points=article.get('points'), article_id=article.get('article_id'))
            s.add(new_entry)
            s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
