FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN git clone https://github.com/gothinkster/django-realworld-example-app.git /drf_src
WORKDIR /test_kanban
RUN cd /test_kanban
RUN pip install -r requirements.txt

EXPOSE 8080

CMD python manage.py makemigrations kanban && python manage.py migrate && python manage.py runserver
