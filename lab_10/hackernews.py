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

    number_of_pages = 5
    url = "https://news.ycombinator.com/newest"
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


@route('/recommendations')
def recommendations():

    s = session()

    classified_news = list()

    unmarked_rows = s.query(News).filter(News.label == None).all()
    marked_rows = s.query(News).filter(News.label != None).all()

    X = list()
    y = list()

    for row in marked_rows:
        title = row.title
        label = row.label
        X.append(title)
        y.append(label)

    model = NaiveBayesClassifier()
    model.fit(X, y)

    for row in unmarked_rows:

        title = row.title
        score = model.predict(title)

        if score == "good":
            score = 0
        elif score == "maybe":
            score = 1
        elif score == "never":
            score = 2
        classified_news.append([score, row])

    print("Before sort")
    print(classified_news[:10])
    classified_news.sort(key=lambda x: x[0])
    print("After sort")
    print(classified_news[:10])
    classified_news = [result[1] for result in classified_news]
    # 1. Получить список неразмеченных новостей из БД
    # 2. Получить прогнозы для каждой новости
    # 3. Вывести ранжированную таблицу с новостями
    return template('news_template', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
