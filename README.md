# Akira_Project
 Akira Project is an Learning Management System which is next version of OnCl - Edu. Cloud

### To make me live you need to follow the below instructions,
1. [Install Stabled Python](https://www.python.org/downloads/windows/)
2. Install the virtualenv package <code> pip install virtualenv </code>
3. Create the virtual environment <code> virtualenv venv </code>
4. Activate the virtual environment <code> venv\Scripts\activate </code>
> From now on, Any python commands you use will work with your virtual environment.
> To deactive the virtual environemnt use can type the below command or else you can continue with the next instruction [5].
> Deactivate the virtual environment <code> deactivate </code>
5. My Requirements <code> py -m pip install -r requirements.txt </code>
6. For Packaging Up Your Model Changes Into Individual Migration Files <code> py manage.py makemigrations </code>
7. For Applying Those To Your Database <code> py manage.py migrate </code>
8. To Start My Server <code> py manage.py runserver </code>
9. To View On Browser http://127.0.0.1:8000/ [Local Host Address]