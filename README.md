# Intranet
An intranet built for a small company to display department specific dashboards for easy viewing of information.

## Languages
Main functionality is developed with Flask (Python), utilising Flasks render template to serve the frontend.
Database connectivity is developed with flask-mysqldb and pure SQL.
Styling was done with tailwindcss, with responsiveness in mind.

## Functions
### User Features
- Quick links section that allows department users to create hotlinks that need to be stickied.
- Notices section that allows department users to create 'posts' to keep other users up to date.
- Job Attention section that allows department users to create 'jobs' with varying levels of urgency to draw attention to required jobs.
- Overview section that provides a pie chart breakdown of the current job attention jobs, and a list of department users, displaying department admins with a dedicated icon.
### Admin Features
- Admin panel with all actions like creating, editing and archiving anything in department sections logged to a sortable table.
- List of users that have been created and are pending activation, for review and activation from admins.
- List of current users for user management, changing the users department, and setting the user to a department admin.
### Technical Features
- Passwords securely stored in a hashed and salted format, using werkzeug.
 
## Running locally
1. Clone the repository into a folder.
2. Create a virtual env with python ```python -m venv .venv```
3. Activate the virtual env ```.venv\Scripts\Activate```
4. Install the required packages ```pip install -r requirements.txt```
5. Configure database connection in __init__.py and execute the database.sql file in a database viewer
6. Run flask ```flask --app __init__ run```
7. Navigate to http://localhost:5000/

## Screenshots
- Department Dashboard <br>
![image](https://github.com/user-attachments/assets/d8d91b2b-0927-477e-b0e0-c10ad9702bfb)
<br>
- Adding a new link to Quick Links <br>
![image](https://github.com/user-attachments/assets/dc24f876-021f-47b5-9ede-e85f1cb017a7)
<br>
- Job Attention Board Item <br>
![image](https://github.com/user-attachments/assets/12fa71d3-066b-4e8e-8af0-b3f9470079fb)
<br>
- Adding a new job to the Attention Board <br>
![image](https://github.com/user-attachments/assets/f235f8d2-34be-4e54-8c3e-5ae3465f4c2f)
<br>
- Notice Board Item <br>
![image](https://github.com/user-attachments/assets/e7a9dbf6-db51-4b80-ac70-6b2b4764771d)
<br>
- Department Overview <br>
![image](https://github.com/user-attachments/assets/9c364e6f-a9c3-4275-bcd0-da08d01c6323)
<br>
- Admin Panel Dashboard <br>
![image](https://github.com/user-attachments/assets/8f6f887d-fd8f-42c3-a600-ee5a740169ca)
<br>
- Log Item <br>
![image](https://github.com/user-attachments/assets/7b40acba-0c8d-4c03-a650-ff8ba164d7e7)
<br>
- Activate Account Item <br>
![image](https://github.com/user-attachments/assets/6e9687c2-4a6c-4289-8de2-9be8021aa7ca)
<br>
- Manage Account Item <br>
![image](https://github.com/user-attachments/assets/1d65d92b-b1ad-4f0e-938b-5b8a9655c7cd)
<br>








