#!/usr/bin/env python

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
WHERE log.path = CONCAT('/article/', articles.slug)
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

# Store global database name
DBNAME = 'news'


def executeQuery(query):
    """executeQuery takes a string as a parameter.  It executes the query
    and returns the results as a list of tuples."""
    try:
        db = psycopg2.connect('dbname=' + DBNAME)
        c = db.cursor()
        c.execute(query)
        rows = c.fetchall()
        db.close()
        return rows
    except BaseException:
        print("Unable to connect to the database")


# Problem 1: What are the most popular three articles of all time?
def top_three_articles():
    """Return the top three articles by most views"""
    query = """SELECT title, COUNT(log.id) AS views
            FROM articles, log
            WHERE log.path = CONCAT('/article/', articles.slug)
            GROUP BY articles.title ORDER BY views desc LIMIT 3;"""
    top_three = executeQuery(query)
    # Display header and results for Problem 1
    print('**** Top Three Articles by Page View ****')
    for i in top_three:
        print('"' + i[0] + '" -- ' + str(i[1]) + " views")
    print(" ")  # Display line break for legibility


# Problem 2: Who are the most popular article authors of all time?
def popular_authors():
    """Return the most popular authors based on overall page views"""
    query = """SELECT name, sum(articles_by_view.views) AS views
            FROM articles_by_author, articles_by_view
            WHERE articles_by_author.title = articles_by_view.title
            GROUP BY name ORDER BY views desc;"""
    author_popularity = executeQuery(query)
    # Display header and results for Problem 2
    print('**** Most Popular Authors Based on Total Article Views ****')
    for i in author_popularity:
        print(i[0] + ' -- ' + str(i[1]) + ' views')
    print(' ')  # Display line break for legibility


# Problem 3: On which days did more than 1% of requests lead to errors?
def high_error_days():
    """Return the days where errors exceeded 1%"""
    query = """SELECT errors.day,
            ROUND(
            ((errors.errors/total.total) * 100)::DECIMAL, 2)::TEXT
            as percentage
            FROM errors, total
            WHERE total.day = errors.day
            AND (((errors.errors/total.total) * 100) > 1.0)
            ORDER BY errors.day;"""
    high_error_results = executeQuery(query)
    # Display header and results for Problem 3
    print('**** Days Where Errors Exceeded 1%' + ' of Total Views ****')
    for i in high_error_results:
        print(i[0].strftime('%B %d, %Y') + " -- " + i[1] + "%" + " errors")
    print(' ')  # Display line break for legibility


if __name__ == '__main__':
    print(" ")
    print("--- Generating Results ---")
    print(" ")
    top_three_articles()
    popular_authors()
    high_error_days()
