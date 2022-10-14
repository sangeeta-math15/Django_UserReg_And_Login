# Django Fundoo Note App 

- Developed Fundoo Notes APP backend using Django.
- we focused on the CRUD applications of Note.
- To give the app a start, run the below command in the Terminal / CMD:
- **django-admin startapp notes** 
- `django-admin startapp notes`
- This will create a new empty Django web-app that will have files inside ‘note_app’ directory in our ‘account’ folder. This web-app can be integrated with our main Django project by including the app name in INSTALLED_APPS.
-  we need to create models for our projects
-  **Migrating the Models**:
-  `python manage.py makemigrations`
-  The next step is to generate tables in the database using the migrations we just created:
-  `python manage.py migrate`
-  **Testing our Models**
- ` python manage.py runserver`
