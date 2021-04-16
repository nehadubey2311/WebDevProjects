document.addEventListener("DOMContentLoaded", function () {
  const followButton = document.querySelector("#follow");
  const unfollowButton = document.querySelector("#unfollow");
  // attach event listener only when 'follow'/'unfollow' buttons exist
  if (followButton) {
    document.querySelector("#follow").addEventListener("click", follow);
  }
  if (unfollowButton) {
    document.querySelector("#unfollow").addEventListener("click", unfollow);
  }
});

/**
 * Follow a user when 'follow' button is clicked
 */
function follow() {
  const userId = this.dataset.user;

  fetch(`/profile/${userId}/follow`)
    .then((response) => response.json())
    .then((response) => {
      if (!response.error) {
        // highlight bottons to reflect if user is already being followed or not
        document.querySelector("#follow").style.display = "none";
        document.querySelector("#unfollow").style.display = "block";

        // update 'followers' count
        let count = document.querySelector("#followers-count").innerHTML;
        count++;
        document.querySelector("#followers-count").innerHTML = `${count}`;
      } else {
        throw new Error("Could not follow a user, please try again...");
      }
    })
    .catch((error) => {
      alert(error);
    });
}

/**
 * Unfollow a user when 'unfollow' button is clicked
 */
function unfollow() {
  const userId = this.dataset.user;

  fetch(`/profile/${userId}/unfollow`)
    .then((response) => response.json())
    .then((response) => {
      if (!response.error) {
        // display/hide bottons to reflect if user is being followed or not
        document.querySelector("#follow").style.display = "block";
        document.querySelector("#unfollow").style.display = "none";

        // update 'followers' count
        let count = document.querySelector("#followers-count").innerHTML;
        count--;
        document.querySelector("#followers-count").innerHTML = `${count}`;
      } else {
        throw new Error("Could not unfollow a user, please try again...");
      }
    })
    .catch((error) => {
      alert(error);
    });
}
