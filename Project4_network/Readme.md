models:
    1. Users:
        follows
        
    2. Posts:
        foreign key - user id
        post content
        date created
        num likes (default 0)

## Questions:
1. MVC style: util.py objective
2. @csrf_exempt for edit post


## TODOs:
1. follow/unfollow UX
2. null, blank = null, verify
3. Error handling for add post
4. Following page when none followed
5. Index page update
6. snake case vs camel case
7. pagination function reuse
8. Edit self posts only - security concern??? - TODO check author is editing post
9. add getor404 function call for all GETs from db
10. ; for js files

post = get_object_or_404(BlogPost, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)


## url.py
1. snake case
