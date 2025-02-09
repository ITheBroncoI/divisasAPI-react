FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /divisasAPI
WORKDIR /divisasAPI
COPY requirements.txt /divisasAPI/
RUN pip install -r requirements.txt
COPY . /divisasAPI/
CMD python manage.py runserver  0.0.0.0:8080
