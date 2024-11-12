Designing and implementing a web application of your own with Python and JavaScript.
YouTube - https://youtu.be/SuMQoCj26rI
# YinYang: A Mental Health and Goal-Setting App
# Distinctiveness and Complexity: 
YinYang is a mental wellness app designed to help users build a positive mindset by balancing their negative and positive thoughts. Inspired by personal experiences, the app offers a structured way to shift focus towards the good in life. For every negative thought logged, users are prompted to submit a counteracting positive thought, fostering emotional balance and self-awareness.

This project was built using the knowledge acquired during the course and is distinct from any previously submitted projects. It utilizes Django for the backend, with a user authentication system, custom models for managing thoughts and goals, and a dynamic user interface created using Bootstrap CSS and custom CSS. The application also incorporates responsive design principles, ensuring usability across various devices.

## Key features of the application include:

- **Responsive Design**.
- **Gamification Elements**. Badges are awarded to users for achieving milestones, adding an engaging and motivational layer to the user experience.
- The project includes **unit tests** and **Selenium tests** for the user interface.
- **Ajax** is used for dynamic sorting and loading logs, ensuring smooth and uninterrupted interaction.
- Users can filter logs by category and thought type using the **django-filters** package. 
- **Visual Representation of Data**. Thought and goal patterns are visually represented using charts rendered by **ApexCharts**, providing users with insights into their progress.

# User experiance:
When users open the application, they are greeted with a welcoming message and presented with the option to either log in or register. After logging in or creating an account, the user is directed to the index page, which displays a form for logging a negative thought.

## Logging Thoughts

**Negative Thought and Positive Thought:** Once the negative thought is submitted, the user is prompted to log a counter-positive thought through a secondary form.

After both forms are submitted, a rebound message is displayed, suggesting the user either visit their dashboard or log another set of thoughts.

## Dashboard Overview

**Charts and Tracking:** On the dashboard, users can view charts that track the quantities and categories of their logs, offering visual insights into their thought patterns.

**Recent Logs:** The first 8 logs are displayed on the dashboard.

**Log Management:** Users can edit or delete logs directly from the dashboard.

**See All Button:** "See All" button redirects the user to the "Logs" page, where all logs are displayed.

**Goal Setting:** Users can set up to 5 goals at a time, which are displayed on their dashboard. If user tries to submit 6th goal, an error message is displayed. Users delete a goal directly from the dashboard.

**Goal Completion:** Upon completing a goal, a pop-up notification appears, congratulating the user on their success.

## Filtering and Sorting:

On the "Logs" page, users can filter logs by category and thought type, as well as sort them by date. Logs on this page can also be edited or deleted.

**Load More Button:** When user clicks on "Load More" button more logs are displayed on the page.

## Badges and Profile

**Badge Rewards:** Users earn badges as they achieve milestones. Pop-up message is displayed, when a badge earned. All available and earned badges are displayed on the profile page.

**Profile Features:** The profile page includes a customizable profile card, where users can change their profile image.

**Completed goals link:** A link is provided on the profile page that redirects users to a dedicated page displaying all of their completed goals.

## Future Expansion

**Scalability Potential:** To ensure future scalability, the profile page includes placeholders for features like fitness videos, sleep sound guides, and meditation tutorials, which can be integrated later to enhance the user experience.

# File Structure

- **requirements.txt**: Necessary packages for the project and other dependencies.
- **yinyang/**: Main application directory
- **media/**: Stores user profile images.
- **static/**: Contains two folders **js** and **styles** with CSS, JavaScript, and image files used in the application.
- **templates/**: Includes 8 HTML templates for rendering views such as the index page, comleted goals, dashboard, layout, login, logs, profile and register.
- **admin.py**: Registers the models to be accessible in the Django admin panel.
- **filters.py**: Provides filtering functionality using the django-filters package.
- **forms.py**: Defines forms for creating and editing thoughts, goals, and user profile images.
- **test_selenium.py**: Includes Selenium tests for UI functionality.
- **tests.py**: Contains unit tests for models and views.
- **models.py**: Contains 4 application models: `User`, `Thought`, `Goal`, and `Rewards`.
- **views.py**: Implements the logic for handling user requests, managing authentication, and rendering responses.

# Running the Application

To run the YinYang application:

1. **Clone the Repository**:
- git clone "url"
- cd "your-project-directory"

2. **Install the Dependencies:**
Use the requirements.txt file to install all the required packages: 
- pip install -r requirements.txt

3. **Running the Application**:
- python manage.py migrate
- python manage.py runserver

4. **Access the Application:** 
Open your web browser and go to http://127.0.0.1:8000/ to view the application.

### Notes:
- Current superuser: username juliaand; password:juliaand
- Other user: username: jane; password:jane

