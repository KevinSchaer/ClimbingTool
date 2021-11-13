# ClimbingTool - Final Project

## About CS50

The project was created as a final project in the [CS50 course](https://cs50.harvard.edu/x/2021/) at Harvard University. CS50 is an openware course and is taught by David J. Malan.  It is an introduction to Computer Science for majors and non-majors to develop computational thinking skills using languages like C, Python, and JavaScript. The languages are supplemented with SQL, HTML, and CSS in the context of web application development.

## Introduction to the Project

The ClimbingTool is designed to help climbers manage their progress by storing data on routes, spots and personal performance in a database via a web application.

The tool gives the user a graphical and tabular overview of their own climbing progress on their front page. The climber can search for, and edit already climbed routes based on various criteria. Furthermore, the user can search for other climbers in the database and view their progress.

Indeed, users can delete their accounts and change their passwords. The tool does not collect any personal data of the user during use that would allow unique identification, which fulfils the guidelines of the GDPR.

## Architecture

The ClimbingTool consists of a frontend and backend.

### Frontend
The frontend respectively the user interface is realized with HTML. CSS and the Bootstrap framework are used for the design. JavaScript and Ajax are used to integrate and display dynamic elements. For example, for the search function for additional users, only a part of the displayed web page is replaced with Ajax. The open-source JavaScript library Chart.js is used to design interactive graphics on the climbers' progress.


### Backend
The backend is implemented using the Python web framework Flask. Flask ensures communication between the frontend and the database. It processes and provides data and performs plausibility checks on incoming data. SQLite realizes the relational database system.

## Launch the Application locally

1. Use Python version 3.9 or newer
2. Clone the source code: `https://github.com/KevinSchaer/ClimbingTool.git`
3. Install required packages: `pip install -r requirements.txt`
4. Initialize the database by running `database.py` (only required for first use)
5. Run the app: `flask run` (may differ depending on your system and IDE used)
6. Open your Browser: `http://127.0.0.1:5000/`

## Demonstration

The video demonstrating the application can be found [here](https://youtu.be/5QD2fwyykeE).
