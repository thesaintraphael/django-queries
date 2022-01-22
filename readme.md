# Django Queries

Simple app to practice django's advanced queries

## Apps

    app - focused on annotations and common orm methods, functions
    agg - focused on aggregations (contain annotations too)
    app_related - focused on select/fetch_related


## Run Locally
     1. Create virtual environment and activate it: 
            python -m venv venv
            venv\scripts\activate
     
     2. Install requirements: 
            pip install -r requirements.txt
     
     3. Migrate db: 
            py manage.py migrate

     4. Run: 
            py manage.py runserver
