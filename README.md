# Django Task Management Project

This is a Django-based project designed for managing tasks efficiently. With this app, you can:

- Add new tasks
- Manage existing tasks
- Organize tasks into different statuses

## Getting Started

To run the project, simply use Docker Compose:

```bash
docker-compose up

```


To create a superuser, run the following commands:

```bash

docker-compose up -d db

```

```bash

docker-compose run web python manage.py createsuperuser
```bash
