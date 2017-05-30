# Log Analysis
# Project 2
# Udacity - Full Stack Nanodegree

# import Postgresql library
import psycopg2

# import datetime.date module for datetime.date object manipulation in
# Problem 3
from datetime import date


"""
Here I've listed the VIEWS I created within the news database
to answer the below-listed problem sets

For Problem 2:
CREATE VIEW articles_by_author AS
SELECT title, name
FROM articles, authors
WHERE articles.author = authors.id;

CREATE VIEW articles_by_view AS
SELECT articles.title, COUNT(log.id) AS views
FROM articles, log
WHERE log.path LIKE CONCAT('%', articles.slug)
GROUP BY articles.title
ORDER BY views desc;

For Problem 3:
CREATE VIEW errors AS
SELECT DATE(time) as day, CAST(COUNT(status) AS FLOAT) AS errors
FROM log
WHERE NOT status='200 OK'
GROUP BY day
ORDER BY day;

CREATE VIEW total AS
SELECT DATE(time) AS day, CAST(COUNT(status) AS FLOAT) AS total
FROM log
GROUP BY day
ORDER BY day;
"""

# Display execution response
print(" ")
print("--- Generating Results ---")
print(" ")

# Problem 1: What are the most popular three articles of all time?


def top_three_articles():
    """Return the top three articles by most views"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = """SELECT title, COUNT(log.id) AS views
            FROM articles, log
            WHERE log.path LIKE CONCAT('%', articles.slug)
            GROUP BY articles.title ORDER BY views desc LIMIT 3;"""
    c.execute(query)
    rows = c.fetchall()
    return rows
    db.close()

# Problem 2: Who are the most popular article authors of all time?


def popular_authors():
    """Return the most popular authors based on overall page views"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = """SELECT name, sum(articles_by_view.views) AS views
            FROM articles_by_author, articles_by_view
            WHERE articles_by_author.title = articles_by_view.title
            GROUP BY name ORDER BY views desc;"""
    c.execute(query)
    rows = c.fetchall()
    return rows
    db.close()

# Problem 3: On which days did more than 1% of requests lead to errors?


def high_error_days():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = """SELECT errors.day,
            ROUND(
            ((errors.errors/total.total) * 100)::DECIMAL, 2)::TEXT
            as percentage
            FROM errors, total
            WHERE total.day = errors.day
            AND (((errors.errors/total.total) * 100) > 1.0)
            ORDER BY errors.day;"""
    c.execute(query)
    rows = c.fetchall()
    return rows
    db.close()


# Display header and results for Problem 1
print('**** Top Three Articles by Page View ****')
top_three = top_three_articles()
for i in top_three:
    print('"' + i[0] + '" -- ' + str(i[1]) + " views")

print(" ")  # Display line break for legibility

# Display header and results for Problem 2
print('**** Most Popular Authors Based on Total Article Views ****')
author_popularity = popular_authors()
for i in author_popularity:
    print(i[0] + ' -- ' + str(i[1]) + ' views')

print(' ')  # Display line break for legibility

# Display header and results for Problem 3
print('**** Days Where Errors Exceeded 1%' + ' of Total Views ****')
high_error_results = high_error_days()
for i in high_error_results:
    print(i[0].strftime('%B %d, %Y') + " -- " + i[1] + "%" + " errors")

print(' ')  # Display line break for legibility
