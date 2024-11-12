import { getCookie } from './utils.js';
import { edit, saveEdit, deleteLog, showDeleteModal } from './dashboard.js';

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('#load-more-btn').forEach(button => {
    button.onclick = () => {
      loadMoreContent(button);         
    };
  });

  showDeleteModal()
  
  window.onscroll = function() {    
    scrollFunction()
  };
  let topBtn = document.getElementById('top-btn');  
  topBtn.onclick = () => {
    document.querySelector('header').scrollIntoView({ behavior: 'smooth', block: 'start' });
  } 

  let sortSelect = document.getElementById('sort-select');
  sortSelect.addEventListener('change', (event) => {
    loadSortedLogs(event.target.value);
  });
});
// Created separate function to fetch logs to avoid repetition
function fetchLogs(url,successCallback,errorCallback){
  $.ajax({
    url: url,
    type: 'GET',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
    success: function(response) {
      successCallback(response);
    },
    error: function(error) {
      errorCallback('Error fetching logs:', error);
    }
  });
}

function loadSortedLogs(sortValue) {
  const url = new URL(window.location.href);
  url.searchParams.set('sort', sortValue);   // Append sort parameter to the URL
  url.searchParams.set('page', 1);           // Set the page number to 1 when sorting

  fetchLogs(url, (data) => {
    // If sorting by 'oldest'
    if (sortValue === 'oldest') {
      data.logs.sort(function(a, b) {
        const dateA = new Date(a.timestamp);
        const dateB = new Date(b.timestamp);
        return dateA - dateB;
      });
    // If sorting by 'newest'
    } else if (sortValue === 'newest') {
      data.logs.sort(function(a, b) {
        const dateA = new Date(a.timestamp);
        const dateB = new Date(b.timestamp);
        return dateB - dateA;
      });
    }
    // Create sorted logs and append them to the container
    const logsContainer = document.getElementById('logs-container');
    logsContainer.innerHTML = '';
    
    data.logs.forEach(log => {
      const logItem = createLog(log);
      logsContainer.appendChild(logItem);
    });

    attachEditLogHandler();  // Attached handlers for the editing logs
    attachDeleteLogHandler();  // Attached handlers for deleting logs

    let loadButton = document.getElementById('load-more-btn');      
    if (loadButton) {
      if (data.has_next) {
        loadButton.style.display = 'block';
        loadButton.dataset.page = parseInt(loadButton.dataset.page) + 1;
      } else {
        loadButton.style.display = 'none';
      }
    }
  });
} 

function loadMoreContent(button) {
  const currentPage = button.dataset.page;
  const url = new URL(window.location.href);
  url.searchParams.set('page', parseInt(currentPage) + 1);
  url.searchParams.set('sort', document.querySelector('select[name="sort"]').value); // Preserve sort order

  fetchLogs(url, (data)=>{
    const logsContainer = document.getElementById('logs-container');
    data.logs.forEach(log => {
      const logItem = createLog(log);
      logsContainer.appendChild(logItem);
    });

    document.querySelector('.body').style.backgroundSize = 'cover';

    attachEditLogHandler();  // Attached handlers for the editing logs
    attachDeleteLogHandler();  // Attached handlers for deleting logs

    if (data.has_next) {
      button.dataset.page = parseInt(currentPage) + 1;
    } else {
      button.style.display = 'none';
    }
  });
}
// Visibility of "Back to top" button
function scrollFunction(){
  let topBtn = document.getElementById('top-btn');
  if (window.scrollY > 20) {
    topBtn.style.display = 'block';
  } else {
    topBtn.style.display = 'none';
  }
}
// Created separate function for log element
function createLog(log){
  const logItem = document.createElement('div');
  logItem.className = 'single-log';
  logItem.id = `log-${ log.id }`;  
  //Created an array of tag options
  const tagChoices = [
    { value: 'WORK', label: 'Work' },
    { value: 'PERSONAL', label: 'Personal' },
    { value: 'RELATIONSHIP', label: 'Relationship' },
    { value: 'STUDIES', label: 'Studies' },
    { value: 'MONEY', label: 'Money' },
    { value: 'FAMILY', label: 'Family' },
    { value: 'HEALTH', label: 'Health' },
  ];
  //HTML for the tag dropdown options
  const options = tagChoices.map(choice => `
    <option value="${choice.value}">${choice.label}</option>
  `).join('');

  logItem.innerHTML = `
    <p class="log-entry log-entry-${ log.id }">${log.entry}</p>
    <textarea id="edit-log-${ log.id }" class="edit-log" style="display:none;"></textarea>
    <select id="edit-tag-${ log.id }" class="edit-tag" style="display:none;">
     ${options}
    </select>
    <p class="error-message" id="error-${ log.id }" style="color: red; display: none;"></p>
    <div>
      <span>${log.timestamp}</span>
      <span id="tag-${ log.id }">${log.tag}</span>
    </div>
    <div>              
      <button class="edit-button" data-log-id="${ log.id }">
        <i class="bi bi-pencil-square"></i>
      </button>
      <button class="delete-log-btn" data-log-id="${ log.id }">
        <i class="bi bi-trash"></i>
      </button>
      <button class="save-button btn btn-light" data-log-id="${ log.id }" style="display:none;">
        Save
      </button>              
    </div>`;
  return logItem;
}

function attachDeleteLogHandler(){
  showDeleteModal() 
  
  document.getElementById('delete-confirm-btn').onclick = function() {
    const logId = this.getAttribute('data-log-id'); 
    deleteLog(logId);
    window.location.reload(true);
  };
}

function attachEditLogHandler(){
  document.querySelectorAll('.edit-button').forEach(button => {
    button.onclick = () => {
      edit(button);         
    };
  });

  document.querySelectorAll('.save-button').forEach(button => {
    button.onclick = () => {        
      saveEdit(button);
    };
  });
}