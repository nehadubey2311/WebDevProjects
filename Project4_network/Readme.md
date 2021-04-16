## Notes:
1. Used `render_with_paginator()` in `views.py` as a common function rendering 'All Posts' and 'Following' views. However had to use almost similar lines of code again within 'User Profile' view as 1) it renders a different html template, 2) It requires more arguments to be passed as compared to first function. Didn't reuse it on purpose.

2. Named an endpoint as `liked()` function in `views.py` since it returns the status if a certain post has been liked by current logged in user or not, as against naming it `like()`.
