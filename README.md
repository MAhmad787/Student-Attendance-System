# Student Attendance System
#### Video Demo: [Watch Video Demo](https://youtu.be/2JN7y3JY9x4)

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Admin Role](#admin-role)
- [Teacher Role](#teacher-role)
- [Student Role](#student-role)
- [Project Files Overview](#project-files-overview)
- [Installation Guide](#installation-Guide)

## Project Description

Welcome to the Student Attendance System, a comprehensive web application developed to streamline administrative and educational tasks within educational institutions.

This project leverages a combination of HTML, CSS, Bootstrap, and JavaScript for the frontend, while Python Flask powers the backend. The application's data is managed efficiently using SQLite, ensuring data reliability and integrity.

The Student Attendance System is designed to simplify various administrative and educational tasks, offering distinct user roles for administrators, teachers, and students. Administrators can efficiently manage courses, teachers, students, and attendance records, while teachers can easily record attendance and access student information for their classes. Students, in turn, have convenient access to their course details.

### Project Files Overview


- **Static:** The static directory houses static files, including CSS stylesheets, JavaScript files, images, and other assets. These files are responsible for defining the application's appearance and enabling client-side interactivity.

- **app.py:** The central Python script, app.py, serves as the backbone of your application, encompassing Flask application setup, route definitions, view functions, and other backend logic. It handles incoming HTTP requests and generates appropriate responses.

- **requirements.txt:** The requirements.txt file enumerates all Python packages and their versions required to run the application. It simplifies the setup of a consistent development environment for others interested in running your project.

- **README.md:** The README file serves as vital project documentation, furnishing an overview of your project, usage instructions, and essential information for developers and users alike.

- **Templates:** The templates directory contains all HTML templates used to render web pages within the application. These templates handle the presentation of information and user interactions, covering areas such as user registration, login, dashboards, and role-specific pages.

##### Templates

The "templates" directory plays a pivotal role in the Student Attendance System, as it houses all the HTML templates responsible for rendering the web pages of the application. These templates serve as the visual interface through which users interact with the system and access its features. Each template is designed to provide a user-friendly and intuitive experience for different aspects of the application. Here's an overview of some key templates within this directory:

- **Registration and Login Templates:** The registration and login templates facilitate user account creation and authentication. They include forms for users to input their credentials, ensuring a secure and straightforward onboarding process.

- **Dashboard Templates:** The dashboard templates offer role-specific views, providing admins, teachers, and students with a tailored experience. Administrators can manage courses, teachers, and students, while teachers can record attendance and access student information. Students, in turn, can view their course details.

- **Role-Specific Templates:** Within the "templates" folder, you'll find templates specific to each user role, such as admin, teacher, and student. These templates display role-specific information and functionalities, ensuring a coherent and efficient user experience.

- **Attendance Templates:** Templates related to attendance management enable teachers to record and review attendance data. These templates are essential for tracking student participation and performance.


## Features

### Admin Role

- **Manage Admin Profiles:** Administrators can edit their profile information, encompassing name, email, institute, and password.
- **Manage Courses:** Administrators wield the ability to create, edit, and delete courses. They also gain access to a comprehensive list of all courses.
- **Manage Teachers:** Administrators can add, edit, and remove teachers. An overview of all teachers is readily available.
- **Manage Students:** Administrators enjoy the flexibility to add, edit, and remove students, accompanied by a comprehensive list of all students.
- **View Reports:** Administrators gain insights through reports on attendance and student performance.

### Teacher Role

- **Manage Teacher Profile:** Teachers can conveniently view and update their profile information, covering name, email, subject, qualification, and password.
- **View Assigned Courses:** Teachers gain visibility into the courses assigned to them.
- **Manage Students:** Teachers access a comprehensive list of students enrolled in their assigned courses.
- **Record Attendance:** Teachers can efficiently record attendance for their students.
- **View Attendance Reports:** Teachers possess the capability to review attendance reports for their classes.

### Student Role

- **Manage Student Profile:** Students can view and update their profile details, encompassing name, email, username, and password.
- **View Course Details:** Students effortlessly access detailed information regarding the course they are enrolled in.
- **View Teacher Information:** Students can conveniently access information about their respective teacher.



## Installation Guide

### 1. Clone the application

Clone the flask application repository. You can do this using either the HTTPS method in the terminal with the following command:
`git clone https://github.com/mahmad787/Student-Attendance-System.git`

Or, alternatively, you can use GitHub Desktop which is a more user-friendly option. Install [GitHub Desktop](https://desktop.github.com/).

### Cloning the Flask Application Using GitHub Desktop

- Launch GitHub Desktop.

- Click on the **File** menu on the top left corner, then select **Clone repository** or press **Ctrl+Shift+O**.

- In the clone dialog, select the **URL** option.

- Paste the repository URL `git clone https://github.com/mahmad787/Student-Attendance-System.git` and choose a local path for the cloned repository.

- Finally, click the "Clone" button to clone the repository to your local machine.

### 2. Selecting the Correct Branch for Your Work

To switch between branches using the terminal, use the following command: `git checkout <branchname>`.

If you are using GitHub Desktop, click on the "Current Branch" tab and a dropdown menu will appear. Select the desired branch from the dropdown menu.

### 3. Creating and Activating a Virtual Environment

- If you are in the repository directory, navigate to a parent directory by running `cd ..`.

- Create a virtual environment using the following command: `python3 -m venv <env_name>`. Replace <env_name> with the desired name for your virtual environment.

- Activate the virtual environment using the following command:
  - Bash (Linux/MacOS)
    ```Bash
    source <env_name>/bin/activate
    ```
  - PowerShell (Windows)
    ```PowerShell
    <env_name>\Scripts\activate
    ```
  Note: On Windows, if you encounter an error while running the above command, you can temporarily fix it by running `Set-ExecutionPolicy Unrestricted -Scope Process`.

- After activating the virtual environment, navigate to the repository main directory.
- To deactivate the virtual environment, use the following command:

  - Bash (Linux/MacOS)
    ```Bash
    deactivate
    ```
  - PowerShell (Windows)
    ```PowerShell
    <env_name>\Scripts\deactivate.bat
    ```
## 4. Install the required packages

Install the required packages from the requirements.txt file by running the following command: `pip install -r requirements.txt`.

## 7. Starting the Application and Logging In

- To start the application, run the following command in your terminal: `flask run`.

- To log in, you can either create a new account or use the following credentials:
  - Username: `ahmad`.
  - Password: `12345678`.
