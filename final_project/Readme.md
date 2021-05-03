# Notes:
* Used MySql as DB. Noted down list of steps below that needed to be done on my mac to be able to use MySql.
* DB user/password has been stored in `settings.py` as clear text for the purposes of ease for grading the assignment.
* Social media urls (facebook, twitter) are working with actual urls linked to them.
* Below is a list of features that any user can access:
    * Reading articles
    * Connect on social media links access
    * Access to suggested articles
    * Register as a user
* Below is a list of features that logged-in users can access in addition to above:
    * like/unlike articles
    * Ability to add articles to `My Articles` to save them
    * Add comments on articles
    * Submit articles to be reviewed by admin. They will only be published on blog once approved by admin
    * Ask questions from admin under Q&A menu/page

# MySql set-up
For using MySql followed below steps:
1. Installed MySql DB from https://dev.mysql.com/downloads/mysql/
2. Installed mysqlclient
3. Installed PyMySql
4. export DYLD_LIBRARY_PATH="/usr/local/mysql/lib:$PATH"
5. export PATH=${PATH}:/usr/local/mysql/bin
6. create db by:
    * login to db as: mysql -u root -p password
    * create db: mysql> CREATE DATABASE blog_db;
7. DB user/password need to be set as root/password during install else edit settings.py

# Description of files in project:
## stocksanalyser.js
This javascript file is used for two purposes.
* To implement like/unlike functionality
* To let users submit questions under `Q&A` section
Since these two actions asynchronously update number of likes and update question on UI respectively. For rest of the project javascript is not used.

## layout.html
This is the basic html layout that other templates extend.

## index.html
This is the template that renders articles as per the url visited. When root url (http://localhost:8000) it renders all articles regardless of categoties they belong. When visiting `Investing`, `Learn Technical Analysis` or `Learn Fundamental Analysis` it renders articles for just that category. Providing articles as per menu clicked is managed by `views.py` by providing only a subset of articles to `index.html`.

## article.html
This is used to render an article view to the user. This also displays like/unlike and adding/removing articles to `My Articles` section depending on it's state. In addition it also adds commenting feature on articles.

## guest_article.html
This template provides for logged in users to be able to submit articles to be reviewed by admin.

## user_questions.html
This template provides a form for the users to submit questions to the admin. It also displays all questions previously added by any user.

## login.html, register.html
These are taken from class projects. They provide the login view and user register view to the user.

## styles.css
For setting blog background/banner image and ither styling.

## settings.py
MySql DB settings have been added to this file to enable the application use it.

# Decription of specific design decisions
## Storing DB user/password
For the ease of grading the assignment DB user/password is stored as clear text in `settings.py` file. For a real life use case I would have rather stored them in secrets.json or environment variables instead (https://stackoverflow.com/a/42077576).

## Blog menu as static categories
I have decided to use static categories for articles since wanted them to be menu for the blog as well. Intentionally did not choose them to be dynamically generated and extendable from admin panel or by users visiting blog.

## Javascript pops up alerts on catching error
When javascript catches error it would create alert pop-ups. I considered adding more intricate functionality like adding a hidden element on DOM that could display this error message instead but for the scope of this project decided to keep alert pop-ups.


------------------------------------

**5/7:**  
- [ ] Testing, bring it together

**5/9:** 
- [ ] Submit