
# The project is written using django rest framework

Instructions:
  - pip install -r requirements.txt
  - ./manage.py migrate
  - ./manage.py runserver

Testing:
  - cd data_inputs/
  - curl -X POST -H "Content-Type: application/json" --data "$(cat input-0.json)" http://127.0.0.1:8000/api/v1/attack\?vm_id\=vm-a211de
  - curl -X POST -H "Content-Type: application/json" --data "$(cat input-2.json)" http://127.0.0.1:8000/api/v1/stats/

Unit tests:
  - ./manage.py test 
