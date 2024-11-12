import { getCookie } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.new-goal');
  form.onsubmit = (event) => {
    event.preventDefault();
    setGoal(form);
  };
  
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach((tooltip) => {
    new bootstrap.Tooltip(tooltip);
  });

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

  showDeleteModal()

  //Modal backdrop freeze fix
  document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('hidden.bs.modal', () => {
      // Remove 'modal-open' class
      document.body.classList.remove('modal-open');
      // Ensure scrolling is allowed
      document.body.style.overflow = '';
      // Remove any existing backdrops
      document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
    });
  });
  
  document.getElementById('delete-confirm-btn').onclick = function() {
    const logId = this.getAttribute('data-log-id'); 
    deleteLog(logId);
  }; 

  updateCheckboxListeners();
  updateDeleteGoalBtn();
  pieChartThoughts();
  pieChartGoals()
});

let chartNegative;
let chartPositive;
let chartGoals;

function setGoal(form){
  const formData = new FormData(form);

  fetch(form.action, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {           
      const newGoal = data.goal; 
      pieChartGoals();
      // Create new goal element and append     
      const newGElement = document.createElement('div');
      newGElement.className = 'single-goal';
      newGElement.id = `goal-${newGoal.id}`;       
      newGElement.innerHTML = `
        <input type="checkbox" id="goal-${newGoal.id}" class="goal-checkbox">
        <label for="goal-${newGoal.id}">${newGoal.description}</label>
        <label for="goal-category-${newGoal.id}">${newGoal.category}</label>
        <button type="button" class="delete-goal-btn" data-goal-id="${newGoal.id}"><i class="bi bi-x"></i></button> 
      `
      document.querySelector('.set-goals').appendChild(newGElement);           
      updateCheckboxListeners();
      updateDeleteGoalBtn();
      form.reset();      
    // Show error message if goal creation fails
    } else {
      const errorMessage = document.getElementById("goal-message-error");
      errorMessage.style.display='block';
      setTimeout(() => {
        errorMessage.style.display = 'none';   // Hide error message after 3 seconds
      }, 3000);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    errorMessage.style.display='block';
      setTimeout(() => {
        errorMessage.style.display = "none";
      }, 3000);
  });
}

function goalCompleted(goalId, isCompleted){
  fetch(`/complete_goal/${goalId}`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ is_completed: isCompleted })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success && isCompleted) {
      const badgeInfo = data.new_badge;
      if (badgeInfo!== null) {
        showBadgeModal(badgeInfo);        
      } else {
      //Completion model        
      const myModal = new bootstrap.Modal(document.getElementById('myModal'));
      myModal.show();
      }      
    }
  })
  .catch(error => {
    console.error("Fetch error:", error);
  });
}

function checkboxListener() { 
  if (this.checked){
    const goalId = this.id.split('-')[1]; // Get goalId from the checkbox ID
    const isCompleted = this.checked;
    goalCompleted(goalId, isCompleted);
    //Remove element
    const postEl = document.getElementById(`goal-${goalId}`);
    if (postEl) {
      postEl.remove();
    } else {
      console.error('Element not found for goalId:', goalId);
    }              
  }  
}

function updateCheckboxListeners() {
  document.querySelectorAll('.goal-checkbox').forEach(checkbox => {
    checkbox.removeEventListener('change', checkboxListener);//Duplicate listeners fix
    checkbox.addEventListener('change', checkboxListener);
  });
}

function updateDeleteGoalBtn(){
  document.querySelectorAll('.delete-goal-btn').forEach(button => {
    button.addEventListener('click', (event) => {
      const buttonEl = event.target.closest('.delete-goal-btn');
      const goalId = buttonEl.getAttribute('data-goal-id');
      deleteGoal(goalId);
    });
  });
}

function showBadgeModal(badgeInfo) {
  const newBadgeModalEl = document.getElementById('new-badge-modal');
  document.querySelector(".badge-info").innerHTML = badgeInfo;
  
  if (newBadgeModalEl) {
    const myModal = new bootstrap.Modal(newBadgeModalEl);
    myModal.show();
  }
}

// ApexCharts documentation https://apexcharts.com/docs/installation/
function pieChartThoughts() {  
  const tagChartsEl = document.getElementById('tag-charts');
  const negativeContainer = document.getElementById('negative-pie-chart');
  const positiveContainer = document.getElementById('positive-pie-chart');

  if (!tagChartsEl) {
    return;
  }

  const userId = tagChartsEl.getAttribute('data-user-id');

  fetch(`/dashboard/${userId}/chart_data_thoughts`, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(data => {   
    const negativeData = data.negative.map(item => ({ name: item.tag || 'Unknown', y: item.count }));
    const positiveData = data.positive.map(item => ({ name: item.tag || 'Unknown', y: item.count }));

    const optionsNegative = {
      series: negativeData.map(item => item.y),
      noData: {
        text: 'No Data Available',
        align: 'center',
        verticalAlign: 'middle',
        offsetX: 0,
        offsetY: 0,
        style: {
          color: 'black',
          fontSize: '14px',
          fontFamily: undefined
        }
      },
      chart: {
        type: 'donut',
        height: 200,
        width: '100%',
        animations: {
          enabled: true,
          easing: 'ease-in-out',
          speed: 1500,
          animateGradually: {
              enabled: true,
              delay: 200
          },
          dynamicAnimation: {
              enabled: true,
              speed: 350
          }
        }
      },
      labels: negativeData.map(item => item.name),
      legend: {
        show: true,
        fontSize: '10px',
        position: 'right'
      },
      plotOptions: {
        pie: {
          expandOnClick: false,
          donut: {
            size: '50%'
          }
        },                    
      },
      theme: {
        palette: 'palette3' // upto palette10
      }        
    };

    const optionsPositive = {
      series: positiveData.map(item => item.y),
      noData: {
        text: 'No Data Available',
        align: 'center',
        verticalAlign: 'middle',
        offsetX: 0,
        offsetY: 0,
        style: {
          color: 'black',
          fontSize: '14px',
          fontFamily: undefined
        }
      },
      chart: {
        type: 'donut',
        height: 200,
        width: '100%',
        animations: {
          enabled: true,
          easing: 'ease-in-out',
          speed: 1500,
          animateGradually: {
            enabled: true,
            delay: 200
          },
          dynamicAnimation: {
            enabled: true,
            speed: 350
          }
        }
      },
      labels: positiveData.map(item => item.name),
      legend: {
        show: true,
        fontSize: '10px',
        position: 'right'
      },
      plotOptions: {
        pie: {
          expandOnClick: false,
          donut: {
            size: '50%'
          },
        },                    
      },
      theme: {
        palette: 'palette4' // upto palette10
      }
    };

    if (chartNegative) {
      chartNegative.destroy();
    }
    if (chartPositive) {
      chartPositive.destroy();
    }
    
    chartNegative = new ApexCharts(negativeContainer, optionsNegative);
    chartPositive = new ApexCharts(positiveContainer, optionsPositive);

    chartNegative.render().catch(error => console.error('Error rendering negative chart:', error));
    chartPositive.render().catch(error => console.error('Error rendering positive chart:', error));
  })
  .catch(error => console.error('Error fetching data:', error));
}

function pieChartGoals() { 
  const tagChartsEl = document.getElementById('tag-charts');  

  if (!tagChartsEl) {
    return;
  }
  
  const userId = tagChartsEl.getAttribute('data-user-id');
  
  fetch(`/dashboard/${userId}/chart_data_goals`, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(data => {    
    const goalsData = data.goals.map(item => ({ name: item.category, y: item.count })); 
    const optionsGoals = {
      series: goalsData.map(item => item.y),
      noData: {
        text: 'No Data Available',
        align: 'center',
        verticalAlign: 'middle',
        offsetX: 0,
        offsetY: 0,
        style: {
          color: 'black',
          fontSize: '14px',
          fontFamily: undefined
        }
      },
      chart: {
        type: 'donut',
        height: 200,
        width: '100%',
        animations: {
          enabled: true,
          easing: 'ease-in-out',
          speed: 1500,
          animateGradually: {
            enabled: true,
            delay: 200
          },
          dynamicAnimation: {
            enabled: true,
            speed: 350
          }
        }
      },
      labels: goalsData.map(item => item.name),
      legend: {
        show: true,
        fontSize: 10,
        position: 'right',
      },
      plotOptions: {
        pie: {
          expandOnClick: false,
          donut: {
            size: '50%'
          }
        },                    
      },
      theme: {
        palette: 'palette4' // upto palette10
      }      
    };

    if (chartGoals) {
      chartGoals.destroy();
    }
      
    chartGoals = new ApexCharts(document.querySelector("#goals-pie-chart"), optionsGoals);
    chartGoals.render().catch(error => console.error('Error rendering goals chart:', error));      
  })
  .catch(error => console.error('Error fetching data:', error));
}

export function edit(button) {
  const logId = button.dataset.logId;
  const saveBtn = document.querySelector(`.save-button[data-log-id="${logId}"]`);
  const logEntry = document.querySelector(`.log-entry-${logId}`);
  const editTextarea = document.getElementById(`edit-log-${logId}`);
  const editTag = document.getElementById(`edit-tag-${logId}`);
    
  // Hide old content and show textarea
  logEntry.style.display = 'none';
  editTextarea.style.display = 'block';
  editTag.style.display = 'block';  
  // Insert old content into textarea
  editTextarea.value = logEntry.innerText;  
  // Hide edit button and show save button
  button.style.display = 'none';
  saveBtn.style.display = 'inline';  
}

export function saveEdit(button){
  const logId = button.dataset.logId;
  const newContent = document.getElementById(`edit-log-${logId}`).value;  
  const logEntry = document.querySelector(`.log-entry-${logId}`);
  const editTextarea = document.getElementById(`edit-log-${logId}`);
  const errorMessage = document.getElementById(`error-${logId}`);
  const newTag = document.getElementById(`edit-tag-${ logId }`).value;
  const oldTag = document.getElementById(`tag-${ logId }`);

  fetch(`/edit_log/${logId}/`,{
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ 
      entry: newContent,
      tag: newTag 
    })
  })
  .then(response => response.json())
  .then(data => {
    if(data.status === 'success'){
      // Insert new content into log
      logEntry.innerText = newContent;
      logEntry.style.display = 'block';
      oldTag.innerText = newTag;       
      // Hide textarea and error message
      editTextarea.style.display = 'none';
      document.getElementById(`edit-tag-${ logId }`).style.display = 'none';
      errorMessage.style.display = 'none';
      // Display edit button instead of save button
      document.querySelector(`.edit-button[data-log-id="${logId}"]`).style.display = 'inline';
      button.style.display = 'none';
    } else {
      errorMessage.style.display = 'block';
      errorMessage.innerText = "This field can not be empty";            
    }  
  })
}

export function deleteLog(){
  const logId = document.getElementById('delete-confirm-btn').getAttribute('data-log-id');
  fetch(`/delete_log/${logId}/`,{
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken') 
    }
  })
  .then(response => response.json())
  .then(data=>{
    if(data.status === 'success'){      
      pieChartThoughts();
      const logEl = document.getElementById(`log-${logId}`);
      if (logEl) {
        logEl.remove();
      }      
      // Close the modal
      const deleteModal = document.getElementById('delete-modal');
      const myModal = bootstrap.Modal.getInstance(deleteModal);
      myModal.hide();     
    } else {
      alert('Failed to delete log: ' + (data.error || 'Unknown error'));
    }
  })
}

function deleteGoal(goalId){  
  fetch(`/delete_goal/${goalId}/`,{
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken') 
    }
  })
  .then(response => response.json())
  .then(data=>{
    if(data.status === 'success'){
      pieChartGoals();
      const goalEl = document.getElementById(`goal-${goalId}`);
      if (goalEl) {
        goalEl.remove();
      }
    } else {
      alert('Failed to delete goal: ' + (data.error || 'Unknown error'));
    }
  })
}

export function showDeleteModal(){
  document.querySelectorAll('.delete-log-btn').forEach(button => {
    button.onclick = () => {
      const deleteModal = document.getElementById('delete-modal');
      const myModal = new bootstrap.Modal(deleteModal);

      const confirmDeleteBtn = document.getElementById('delete-confirm-btn');
      confirmDeleteBtn.setAttribute('data-log-id', button.dataset.logId);
    
      myModal.show();         
    };
  });
}