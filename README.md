# Calendar Optimizer (under development)

## Scope (Objective and Key Features):

This project consists of an interface to optimize the selection of activities to be performed based on user preferences and provided constraints. The user specifies the activities they would like to choose from, and the times they are available to perform them, along with any other potential constraints, and any other potential restrictions (such as having at least 1 hour of free time per day or not scheduling two activities simultaneously). Additionally, it's possible to assign a subjective value to each activity, and this application will compute the choice of activities that maximizes the sum of values without violating the given constraints.

As a result, it is possible, for instance, to choose from various courses with overlapping schedules a set of courses with no schedule conflicts, considering the lowest possible total cost. A more complex example: the user might represent a university department seeking to maximize the quantity of courses offered in a semester, ensuring there are no room or scheduling conflicts, and that no professor exceeds an 8-hour workday.

This project is being developed as a practical assignment for the Software Engineering course at the Federal University of Minas Gerais (UFMG).


## Team Members and respective Roles:

Ana Luiza - Backend 

Artur Gaspar - Fullstack 

Denilson Martins - Fullstack 

~Vinicius Bonfim - Front End~ 

## Technologies (language, frameworks and DB):

Backend: Python (Django)

Database: MySQL

Integer Programming Solver: GLPK

Frontend: Django Templates


## Product Backlog:

1) As a user, I would like to perform CRUD (Create, Read, Update, Delete) operations for activities in the system (time, location, involved individuals, associated value).

2) As a user, I would like to be able to specify alternative timings, locations, and individuals for each activity, in addition to my value preferences for each activity.

3) As a user, I would like to determine the optimal choice of activities I can perform based on my preferences and constraints.

4) As a user, I would like to export and import data for my activities and optimal choices.

5) As a user, I would like to grant other users access to my activities and optimal choices (read and/or edit).

6) As an admin, I would like to limit the amount of resources available to each user.

7) As an admin, I would like to be able to ban and reinstate users.

8) As a user, I would like to view my activities in a calendar format.

9) As a user, I would like to export my activities to Google Calendar.

10) As a user, I would like to configure activities on a weekly, monthly, or annual scope.


## Sprint Backlog:

Stories 1, 2, 3 and 4 of the Product Backlog (as an extra we did a very simple authentication).


## Tasks and Responsible Parties:

1) As a user, I would like to perform CRUD (Create, Read, Update, Delete) operations for activities in the system (time, location, involved individuals, associated value).

- Set up Pipenv (Denilson)
- Prepare the database and Django models (Ana)
- Implement basic CRUD operations in the Back-End (Denilson)
- Create and test initial activities (Artur)
- Implement an initial version of the Read, Update, and Delete interfaces (Artur)
- Implement an initial version of the Create interface (Denilson)
- Enhance the page interface (Denilson)

2) As a user, I would like to be able to specify alternative timings, locations, and individuals for each activity, in addition to my value preferences for each activity.

- Create main classes in the Back-End (Denilson)
- Model this data in the database (Ana)
- Create simple examples for testing (Artur)
- Develop a Front-End interface for specifying this information (Denilson)

3) As a user, I would like to determine the optimal choice of activities I can perform based on my preferences and constraints.

- Install and set up the Mixed-Integer Programming solver (Artur)
- Implement problem modeling as Integer Programming (Artur)
- Convert data from the format available in the Back-End to the solver's format (Artur)
- Test constraints and optimal values for different scenarios (Artur)

4) As a user, I would like to export and import data for my activities and optimal choices.

- Implement data representation of activities in JSON format (Artur)
- Implement functionality for import and export data buttons in the Front-End (Artur)
- Verify if the same file format continues to work on different browsers and operating systems (Ana)
- Enhance the Front-End interface (Denilson)


## Set up

Proceed to README-SETUP 

