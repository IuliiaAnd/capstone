import { getCookie } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.new-thought').forEach(form => {
    form.onsubmit = (event) => {
      event.preventDefault();
      submitForm(form);
    };
  });

  randomQuote()
  
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach((tooltip) => {
    new bootstrap.Tooltip(tooltip);
  });
});

function submitForm(form) {
  const negativeForm = document.getElementById('negative-form-flex');
  const positiveForm = document.getElementById('positive-form-flex');

  const formData = new FormData(form);

  fetch(form.action, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
  .then(response => {
    if (response.ok) {
      if (form === negativeForm.querySelector('form')) {
        negativeForm.style.display = 'none';
        positiveForm.style.display = 'flex';
      } else {
        document.querySelector('.rebound').style.display = 'block';
        negativeForm.style.display = 'none';
        positiveForm.style.display = 'none';
      }
    } else {
      console.error('Failed to submit the form.');
    }
  })
}

const quotes = [
  "Success is not final; failure is not fatal: It is the courage to continue that counts. — Winston Churchill",
  "The road to success and the road to failure are almost exactly the same. — Colin R. Davis",
  "Success is getting what you want; happiness is wanting what you get.― W. P. Kinsella",
  "If you are working on something that you really care about, you don’t have to be pushed. The vision pulls you. — Steve Jobs",
  "Goal setting is the secret to a compelling future. — Tony Robbins",
  "Opportunity is missed by most people because it is dressed in overalls and looks like work. — Thomas Edison",
  "One man with courage makes a majority. — Andrew Jackson",
  "You can’t be that kid standing at the top of the waterslide, overthinking it. You have to go down the chute. — Tina Fey",
  "Coming together is a beginning. Keeping together is progress. Working together is success. — Henry Ford",
  "Don’t let someone else’s opinion of you become your reality. — Les Brown"
];

function randomQuote() {
  const randomIndex = Math.floor(Math.random() * quotes.length);
  const quote = quotes[randomIndex];
  document.querySelector('.random-quote').innerText = quote;
}


