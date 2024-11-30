# nugibot-site

NuGiBot Website for Capstone AWS TimCorp-Academy

## CONTACT MANSUF FOR GETTING THE SECRETS (REQUIRED FOR RUNNING THE SERVER)

## HOW TO RUN (READ THIS BEFORE START RUNNING THE PROJECT)

Clone the repository

```sh
git clone https://github.com/mansuf/nugibot-site
cd nugibot-site
```

Run the migration

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

Start the server in local

```sh
python manage.py runserver
```