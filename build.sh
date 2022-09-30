set -o errexit

#pip install -r requiremenst.txt

python manage.py collecstatic --no-input

python manage.py migrate
