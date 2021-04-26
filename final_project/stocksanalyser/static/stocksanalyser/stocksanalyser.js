document.addEventListener("DOMContentLoaded", function () {
  const likeButton = document.querySelector(".like-btn");
  let articleId = likeButton.dataset.like;
  // update like button count and like/unlike status
  updateLikeButton(articleId);

  // attach event listener to like/unlike button
  likeButton.addEventListener("click", likeUnlikeArticle);
});

/**
 * Enables a user to like/unlike an article depending on current state.
 * when promise received call updateLikeButton to reflect like/unlike status and count
 */
function likeUnlikeArticle() {
  let articleId = this.dataset.like;
  fetch(`/article/${articleId}/like_unlike_article`, {
    method: "POST",
    body: JSON.stringify({
      articleId: articleId,
    }),
  })
    .then((response) => response.json())
    .then((response) => {
      if (!response.error) {
        postId = this.dataset.like;
        updateLikeButton(articleId);
      } else {
        throw new Error(response.error);
      }
    })
    .catch((error) => alert(error));
}

/**
 * This updates like button for all articles. Updates the like button
 * color if liked by logged-in user and update likes count
 *
 * @param articleId: id of article being updated
 */
function updateLikeButton(articleId) {
  const element = document.querySelector(`#like-${articleId}`);
  fetch(`/article/${articleId}/liked`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((response) => {
      const status = response.message;
      element.setAttribute("class", status);
      element.innerHTML = `&hearts; ${response.likes}`;
    });
}
