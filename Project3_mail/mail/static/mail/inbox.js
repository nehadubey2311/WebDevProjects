// Keep track of what mailbox is being displayed
let currentMailbox = "";

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => loadMailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => loadMailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => loadMailbox('archive'));
  document.querySelector('#compose').addEventListener('click', composeEmail);
  
  // By default, load the inbox
  loadMailbox('inbox');

  // Send email when user clicks submit
  const composeForm = document.querySelector('#compose-form');
  composeForm.addEventListener('submit', () => sendEmail());
});

function composeEmail() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#display-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function loadMailbox(mailbox) {
  // set the current mailbox
  currentMailbox = mailbox;
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#display-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // load mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    if (emails.length === 0) {
      document.querySelector('#emails-view').innerHTML += 'No emails found.';
    }
    // Print emails
    emails.forEach(displayEmails);
  });
}

function displayEmails(email) {
  // create a new div for displaying email
  const row = document.createElement('div');

  // add css style
  row.classList.add('email-entry');

  if (email.read) {
    row.classList.add('email-background');
  }

  row.innerHTML = `<strong>${email.sender}</strong> ${email.subject} <span class='email-time'>${email.timestamp}</span>`;

  // add event listener to view emails on click
  row.addEventListener('click', function(){
    displayEmail(email.id);
  });

  document.querySelector('#emails-view').append(row);
}

function displayEmail(emailId) {
  // Show the mailbox and hide other views
  document.querySelector('#display-email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  
  // GET the email
  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    // populate values to email view html section
    document.querySelector('#from-user').innerHTML = email.sender;
    document.querySelector('#to-user').innerHTML = email.recipients;
    document.querySelector('#email-subject').innerHTML = email.subject;
    document.querySelector('#email-time').innerHTML = email.timestamp;
    document.querySelector('#email-body').innerHTML = email.body;

    // show/hide archive/unarchive button as per current mailbox
    // and email archive status
    if (currentMailbox !== "sent") {
      if (email.archived) {
        document.querySelector('#archive-btn').style.display = 'none';
        document.querySelector('#unarchive-btn').style.display = 'inline-block';
      }
      else {
        document.querySelector('#archive-btn').style.display = 'inline-block';
        document.querySelector('#unarchive-btn').style.display = 'none';
      }
    } else {
      document.querySelector('#unarchive-btn').style.display = 'none';
      document.querySelector('#archive-btn').style.display = 'none';
    }

  });

  // mark email as read
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  // attach event listeners to archive/unarchive buttons here
  // since we have emailId for each email present here
  document.querySelector('#archive-btn').addEventListener('click', () => archiveEmail(emailId, true));
  document.querySelector('#unarchive-btn').addEventListener('click', () => archiveEmail(emailId, false));

  // attach event listeners to reply button
  document.querySelector('#reply-btn').addEventListener('click', () => replyEmail(emailId));
}

function sendEmail() {
  event.preventDefault();
  // Get form submitted values
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const emailBody = document.querySelector('#compose-body').value;

  // send email
  fetch(
    '/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: emailBody
      })
    }
  )
  // load sent mailbox
  .then(loadMailbox('sent'));
}

function archiveEmail(emailId, flag) {
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: flag,
    })
  })
  .then(loadMailbox('inbox'))
}

function replyEmail(emailId) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#display-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // GET the email
  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    // populate values to email view html section
    document.querySelector('#compose-recipients').value = email.sender;

    // check if subject contains 'Re:' and form subject accordingly
    if( ! email.subject.toLowerCase().startsWith('re:')) {
      email.subject = 'Re: ' + email.subject;
    }

    document.querySelector('#compose-subject').value = email.subject;

    // create body text
    const emailBody = '\n\n\n\n---------------------------------------------\n\n' +
    'on ' + email.timestamp + '  ' + email.sender + 
    '  wrote: \n\n' + email.body;
    document.querySelector('#compose-body').innerHTML = emailBody;
  });
}
