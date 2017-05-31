# Log Analysis Project
## Udacity Full Stack Nanodegree

### Project Overview
For this project, I was tasked to create a reporting tool that prints out reports (in plain text) based on the data in a database. This reporting tool is a Python program using the `psycopg2` module to connect to the database.

### Assignment
The reporting tool needed to answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### How to Run the Code
This section will describe the SQL views I created for the code to function properly and how to run the program.

#### Required SQL Views
This program uses four SQL views.

**For Problem 2:**

> `CREATE VIEW articles_by_author AS
SELECT title, name
FROM articles, authors
WHERE articles.author = authors.id;`

> `CREATE VIEW articles_by_view AS
SELECT articles.title, COUNT(log.id) AS views
FROM articles, log
WHERE log.path = CONCAT('/articles/', articles.slug)
GROUP BY articles.title
ORDER BY views desc;`

**For Problem 3:**

>`CREATE VIEW errors AS
SELECT DATE(time) as day, CAST(COUNT(status) AS FLOAT) AS errors
FROM log
WHERE NOT status='200 OK'
GROUP BY day
ORDER BY day;`

>`CREATE VIEW total AS
SELECT DATE(time) AS day, CAST(COUNT(status) AS FLOAT) AS total
FROM log
GROUP BY day
ORDER BY day;`

#### Running the Program
*These instructions assume you have the Udacity-provided Virtual machine and Udacity-provided database*

First, you'll need to create the views listed above:
1. Within the VM, navigate to `cd /vagrant`
2. Run `psql`
3. Connect to the database `\c news`
4. Enter the views listed above
5. Exit `psql`

With those view created, run the `log_analysis.py` file:
1. Place the `log_analysis.py` file within the same directory as the VM and SQL file provided by Udacity.
2. If you haven't already, launch the VM:
	a. `vagrant up` -- only required once
	b. `vagrant ssh` -- required each time
3. Within the VM, navigate to `cd /vagrant`
4. Execute the file `python log_analysis.py`