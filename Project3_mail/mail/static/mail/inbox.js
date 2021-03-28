// Keep track of what mailbox is being displayed
let currentMailbox = "";
// Keep track of current email being read
let currentEmailId = "";

document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => loadMailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => loadMailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => loadMailbox("archive"));
  document.querySelector("#compose").addEventListener("click", composeEmail);

  // By default, load the inbox
  loadMailbox("inbox");

  // Send email when user clicks submit on compose form
  document
    .querySelector("#compose-form")
    .addEventListener("submit", () => sendEmail());

  // Add event listeners to archive/unarchive and reply buttons
  document
    .querySelector("#archive-btn")
    .addEventListener("click", () =>
      readOrArchiveEmail(currentEmailId, "archived", true)
    );

  document
    .querySelector("#unarchive-btn")
    .addEventListener("click", () =>
      readOrArchiveEmail(currentEmailId, "archived", false)
    );

  document
    .querySelector("#reply-btn")
    .addEventListener("click", () => replyEmail(currentEmailId));
});

/**
 * Function to render compose email form
 */
function composeEmail() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#display-email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // clear compose form fields to start with
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

/**
 * Function to load desired mail box as per input param
 * @param mailbox - String input for which mailbox to render
 */
function loadMailbox(mailbox) {
  // set the current mailbox
  currentMailbox = mailbox;

  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#display-email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  // load mailbox
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      if (!emails.error) {
        if (emails.length === 0) {
          document.querySelector("#emails-view").innerHTML +=
            "No emails found.";
        }
        // Print emails
        emails.forEach(displayEmails);
      } else {
        // throw error returned by backend
        throw new Error(emails.error);
      }
    })
    .catch((error) => alert(error));
}

/**
 * To dispaly a list of all emails in 'inbox',
 * 'sent' and 'archived' view
 * @param email - Each 'email' object returned from an array of
 * emails after fetch call to endpoint '/emails/<mailbox>'
 */
function displayEmails(email) {
  // create a new div for displaying email
  const row = document.createElement("div");
  // add css style
  row.classList.add("email-entry");

  if (email.read) {
    row.classList.add("email-background");
  }

  row.innerHTML = `<strong> ${email.sender} </strong>${email.subject}<span class='email-time'>${email.timestamp}</span>`;

  // add event listener to view emails on click
  row.addEventListener("click", function () {
    displayEmail(email.id);
  });

  document.querySelector("#emails-view").append(row);
}

/**
 * Displays each email
 * @param emailId - Email Id for email to be displayed
 */
function displayEmail(emailId) {
  // Show the mailbox and hide other views
  document.querySelector("#display-email-view").style.display = "block";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  currentEmailId = emailId;

  // GET the email
  fetch(`/emails/${emailId}`)
    .then((response) => response.json())
    .then((email) => {
      if (!email.error) {
        // populate values to email view html section
        document.querySelector("#from-user").innerHTML = email.sender;
        document.querySelector("#to-user").innerHTML = email.recipients;
        document.querySelector("#email-subject").innerHTML = email.subject;
        document.querySelector("#email-time").innerHTML = email.timestamp;
        document.querySelector("#email-body").innerHTML = email.body;

        // show/hide archive/unarchive button as per current mailbox
        // and email archive status
        if (currentMailbox !== "sent") {
          if (email.archived) {
            document.querySelector("#archive-btn").style.display = "none";
            document.querySelector("#unarchive-btn").style.display =
              "inline-block";
          } else {
            document.querySelector("#archive-btn").style.display =
              "inline-block";
            document.querySelector("#unarchive-btn").style.display = "none";
          }
        } else {
          document.querySelector("#unarchive-btn").style.display = "none";
          document.querySelector("#archive-btn").style.display = "none";
        }
      } else {
        // throw error returned by backend
        throw new Error(email.error);
      }
    })
    .catch((error) => alert(error));

  // mark email as read
  readOrArchiveEmail(emailId, "read", true);
}

/**
 * Function to send an email after user clicks on submit
 * post composing an email
 */
function sendEmail() {
  // Get form submitted values
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const emailBody = document.querySelector("#compose-body").value;

  // send email
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: emailBody,
    }),
  })
    .then((response) => response.json())
    // load sent mailbox when email sent successfully
    .then((response) => {
      if (!response.error) {
        loadMailbox("sent");
      } else {
        // throw error returned by backend
        throw new Error(response.error);
      }
    })
    .catch((error) => alert(error));

  event.preventDefault();
}

/**
 * Function to mark an email as archive/unarchive
 * or read/unread
 * @param emailId - Email Id that needs action
 * @param action - Action be be performed (archived/read)
 * @param flag - true/false for the action that needs to be taken
 */
function readOrArchiveEmail(emailId, action, flag) {
  fetch(`/emails/${emailId}`, {
    method: "PUT",
    body: JSON.stringify({
      [action]: flag,
    }),
  }).then(() => {
    // if email was marked archived/unarchived
    // then load inbox on success
    if (action === "archived") {
      loadMailbox("inbox");
    }
  });
}

/**
 * Function to reply to an email
 * @param emailId - takes email id for the email to
 *                   which a user is replying
 */
function replyEmail(emailId) {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#display-email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // GET the email
  fetch(`/emails/${emailId}`)
    .then((response) => response.json())
    .then((email) => {
      if (!email.error) {
        // populate values to email view html section
        document.querySelector("#compose-recipients").value = email.sender;

        // check if subject contains 'Re:' and form subject accordingly
        if (!email.subject.toLowerCase().startsWith("re:")) {
          email.subject = "Re: " + email.subject;
        }

        document.querySelector("#compose-subject").value = email.subject;

        // create body text
        const replyEmailBody =
          `\n\n\n---------------------------------------------\n` +
          `"on ${email.timestamp} ${email.sender} wrote:" \n ${email.body}`;

        document.querySelector("#compose-body").value = replyEmailBody;
      } else {
        // throw error returned by backend
        throw new Error(email.error);
      }
    })
    .catch((error) => {
      alert(error);
    });
}
