set -o errexit


python manage.py collecstatic --no-input

python manage.py migrate