document.addEventListener("DOMContentLoaded", function () {
    const newPostDom =  document.querySelector("#newPost");
    // attach event listener only when element is present on DOM since
    // this won't be available on 'following' and 'user profile' page
    if (newPostDom) {
        newPostDom.addEventListener("click", () => {
            addNewPost();
        });
    }

    // Attach event listener for all post edit buttons
    document.querySelectorAll(".edit").forEach(element => {
        element.addEventListener("click", editPost);
    });

    // Update all liked/unliked heart button color as per 
    // liked/unliked by current logged in user
    // red button: liked by logged-in user
    // grey button: not liked by logged-in user
    document.querySelectorAll(".like-btn").forEach(element => {
        const postId = element.attributes['data-like'].nodeValue;
        updateLikeButton(postId);
    });

    // Attach event listener for all like/unlike heart buttons
    document.querySelectorAll(".like-btn").forEach(element => {
        element.addEventListener("click", likeUnlikePost);
    });
});

/**
 * Adds new post as submitted by a user
 */
function addNewPost() {
    const postContent = document.querySelector("#postContent").value;

    fetch("/post/add", {
        method: "POST",
        body: JSON.stringify({
            content: postContent,
        }),
    }).then((response) => response.json())
    .then((response) => {
        if (!response.error) {
            window.location.reload();
        } else {
          // throw error returned by backend
          throw new Error(response.error);
        }
    })
    .catch((error) => alert(error));
}

/**
 * Provides the ability for logged-in user to edit their own posts
 * by pre-filling the textarea with current post content
 */
function editPost() {
    // get existing content of post
    const postId = this.dataset.postId;
    const content = document.querySelector(`.content[data-post-id='${postId}']`).innerHTML;

    // display edit textarea pre-filled with current content and save button
    document.querySelector(`.content[data-post-id='${postId}']`).style.display = "none";
    document.querySelector(`#editPost-${postId}`).style.display = "block";
    document.querySelector(`#editBtn-${postId}`).style.display = "block";
    document.querySelector(`#editPost-${postId}`).innerHTML = content;

    // on clicking 'save' make fetch call to server and save edit
    document.querySelector(`#editBtn-${postId}`).addEventListener("click", () => savePost(postId));
}

/**
 * Saves the edited post by it's author by calling backend
 * and without reloading the page
 * 
 * @param postId: id of the post being edited and saved
 */
function savePost(postId) {
    // Get edited post content
    const updatedContent = document.querySelector(`#editPost-${postId}`).value;

    // save to database
    fetch(`/post/${postId}/edit`, {
        method: "PUT",
        body: JSON.stringify({
            content: updatedContent
        })
    }).then((response) => response.json())
    .then((response) => {
        if (!response.error) {
            // display updated post
            document.querySelector(`.content[data-post-id='${postId}']`).innerHTML = updatedContent;
            document.querySelector(`.content[data-post-id='${postId}']`).style.display = "block";
            document.querySelector(`#editPost-${postId}`).style.display = "none";
            document.querySelector(`#editBtn-${postId}`).style.display = "none";
        } else {
          // throw error returned by backend
          throw new Error(response.error);
        }
    })
    .catch((error) => alert(error));
}

/**
 * This updates like button for all posts. Updates the like button
 * color if liked by logged-in user and update likes count
 * 
 * @param postId: id of posts being updated
 */
function updateLikeButton(postId) {
    const element = document.querySelector(`#like-${postId}`);
    fetch(`/post/${postId}/liked`, {
        method: "GET"
    }).then((response) => response.json())
    .then((response) => {
        const status = response["message"];
        element.setAttribute('class', status);
        element.innerHTML = `&hearts; ${response["likes"]}`
    });
}

/**
 * Enables a user to like/unlike a post depending on current state.
 * when promise received call updateLikeButton to reflect like/unlike status and count
 */
function likeUnlikePost() {
    const post_id = this.dataset.like;
    fetch(`/post/${post_id}/like_unlike_post`, {
        method: "POST",
        body: JSON.stringify({
            post_id: post_id
        })
    }).then((response) => response.json())
    .then((response) => {
        if (!response.error) {
            const post_id = this.dataset.like;
            updateLikeButton(post_id);
        } else {
            throw new Error("Operation can't be executed, please try again !!");
        } 
    })
    .catch((error) => alert(error));
}
