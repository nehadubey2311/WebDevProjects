document.addEventListener("DOMContentLoaded", function () {
  const likeButton = document.querySelector(".like-btn");
  const userQuestionPage = document.querySelector("#submit-ques-btn");

  // Do below section when page loaded is articles view
  if (likeButton) {
    let articleId = likeButton.dataset.like;
    // update like button count and like/unlike status
    updateLikeButton(articleId);

    // attach event listener to like/unlike button
    likeButton.addEventListener("click", likeUnlikeArticle);
  }

  // attach event listener when element (Q&A page) exists on DOM
  if (userQuestionPage) {
    userQuestionPage.addEventListener("click", () => submitUserQuestion());
  }
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

/**
 * This allows user to submit questions to be answered by admin user.
 * After submitting the question this would refresh the page to
 * display all questions by all users including the latest
 * submitted question
 */
function submitUserQuestion() {
  const quesContent = document.querySelector("#user-ques-content").value;

  fetch("/user_questions/submit_question", {
    method: "POST",
    body: JSON.stringify({
      content: quesContent,
    }),
  })
    .then((response) => response.json())
    .then((response) => {
      // Note: I had to use below if to throw error
      // to be able to catch later, without doing this
      // I was not able to catch error as thrown by backend
      if (response.error) {
        // throw error returned by backend
        throw new Error(response.error);
      }
    })
    .catch((error) => alert(error));
}
