document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#newPost").addEventListener("click", () => {
        addNewPost();
    });

    // Attach event listener for all post edit buttons
    document.querySelectorAll(".edit").forEach(element => {
        element.addEventListener("click", editPost);
    });

    // Update all liked/unliked heart button color as per 
    // liked/unliked by current logged in user
    document.querySelectorAll(".like-btn").forEach(element => {
        updateLikeButton(element);
    });

    // Attach event listener for all like button
    document.querySelectorAll(".like-btn").forEach(element => {
        element.addEventListener("click", likeUnlikePost);
    });
});

function addNewPost() {
    console.log("adding...");
    const postContent = document.querySelector("#postContent").value;
    console.log(`post content is: ${postContent}`);

    fetch("/addPost", {
        method: "POST",
        body: JSON.stringify({
            content: postContent,
        }),
    })
    .then(() => window.location.reload());
}

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
    });
}

function updateLikeButton(element) {
    /**
     * get logged in user
     * check if user exists in post.likes via fetch call
     * accordingly update like button color
     * update likes count
     */
    const postId = element.attributes['id'].nodeValue;
    fetch(`/post/${postId}/liked`, {
        method: "GET"
    }).then((response) => response.json())
    .then((response) => {
        const status = response["message"];
        element.setAttribute('class', status);
        element.innerHTML = `&hearts; ${response["likes"]}`
    });
}

function likeUnlikePost() {
    console.log('like post here...');
}
