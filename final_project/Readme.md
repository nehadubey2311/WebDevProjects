# Notes
1. Acknowledge storing DB password for the purpose of this project in settings.py. WOuld be storing as `secret.json` file as per: https://stackoverflow.com/a/42077576

# Using MySql as db
For using MySql followed below steps:
1. Installed MySql DB
2. Installed mysqlclient
3. Installed PyMySql
4. export DYLD_LIBRARY_PATH="/usr/local/mysql/lib:$PATH"

# For guest articles
When guest articles are submitted admin needs to approve and assign category to them

## Timeline:
**4/23:** 
- [x] html basic layout

**4/24:** 
- [x] admin can add articles
- [x] comments by logged-in users
- [x] like/unlike by logged-in users

**4/25:** 
- [ ] categories for articles
- [x] sub-menu as per categories
- [x] pagination
- [x] adding to 'My Articles'

**4/29:** 
- [x] guest author article submission
- [x] display approved articles only
- [ ] ask questions Q&A
- [x] display date posted/author for articles

**5/1:**  
- [x] social media links
- [x] suggesting articles, most liked ones

**5/2:**  
- [x] connect us right pane
- [ ] Newsletter

**5/6:**  
- [ ] API for finance news & index
- [ ] filter on left pane

**5/7:**  
- [ ] Testing, bring it together

**5/8:**  
- [ ] Improve UI
- [ ] Detailed readme

**5/9:** 
- [ ] Submit

## from css:
/* .navbar .nav-item:hover .nav-link{   } */
