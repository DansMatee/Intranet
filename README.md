# Intranet
An intranet built for a small company to display department specific dashboards for easy viewing of information.
Screenshots yet to be taken.

## Languages
Main functionality is developed with Flask (Python), utilising Flasks render template to serve the frontend.
Database connectivity is developed with flask-mysqldb and pure SQL.
Styling was done with tailwindcss, with responsiveness in mind.

## Functions
- Quick links section that allows department users to create hotlinks that need to be stickied.
- Notices section that allows department users to create 'posts' to keep other users up to date.
- Job Attention section that allows department users to create 'jobs' with varying levels of urgency to draw attention to required jobs.
- Overview section that provides a pie chart breakdown of the current job attention jobs, and a list of department users, displaying department admins with a dedicated icon.

- Admin panel with all actions like creating, editing and archiving anything in department sections logged to a sortable table.
- List of users that have been created and are pending activation, for review and activation from admins.
- List of current users for user management, changing the users department, and setting the user to a department admin. 
 
