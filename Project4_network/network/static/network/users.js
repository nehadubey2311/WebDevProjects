document.addEventListener("DOMContentLoaded", function () {
    const followButton = document.querySelector("#follow");
    const unfollowButton = document.querySelector("#unfollow");
    // attach event listener only when 'follow' button exists
    if (followButton) {
        document.querySelector("#follow").addEventListener("click", follow);
    }
    if (unfollowButton) {
        document.querySelector("#unfollow").addEventListener("click", unfollow);
    }
});

/**
 * Follow users
 */
function follow() {
    const user_id = this.dataset.user;
    console.log(`adding follower...${user_id}`);
    fetch(`/profile/${user_id}/follow`)
    .then(
        // highlight bottons to reflect if user is already being followed or not
        document.querySelector("#follow").style.display= "none",
        document.querySelector("#unfollow").style.display="block",
    )
    .catch((error) => {
        alert(error);
      });
}

/**
 * Unfollow a user
 */
function unfollow() {
    const user_id = this.dataset.user;
    console.log(`removing followed user...${user_id}`);
    fetch(`/profile/${user_id}/unfollow`)
    .then(
        // highlight bottons to reflect if user is already being followed or not
        document.querySelector("#follow").style.display= "block",
        document.querySelector("#unfollow").style.display="none",
    )
    .catch((error) => {
        alert(error);
      });
}
