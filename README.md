# Real-Time Multi-Room Chat System

A real-time chat backend using **Django, Django REST Framework, Django Channels, Redis, and Celery** for managing chat rooms, messages, real-time communication, caching, and scheduled tasks.

## Technologies
* Python
* Django
* Django REST Framework
* Django Channels
* Daphne
* Redis
* Celery
* PostgreSQL
* JWT Authentication
* Swagger / OpenAPI

## Features
* JWT Authentication
* Chat room management
* Multi-room real-time messaging
* WebSocket communication
* Redis caching
* Cache invalidation
* Celery background tasks
* Celery Beat scheduled tasks
* API documentation with Swagger
* PostgreSQL database

## What I Learned
Through this project, I practiced:
* Redis caching
* Cache invalidation
* Django Channels and WebSockets
* ASGI with Daphne
* Celery background tasks
* Celery Beat scheduled tasks
* PostgreSQL database integration
* API testing
* WebSocket testing with `WebsocketCommunicator`
* API documentation with Swagger

## Main Endpoints

### Authentication
```text
POST  /api/token/
POST  /api/token/refresh/
```

### Chat Rooms
```text
GET   /api/rooms/
GET   /api/rooms/<id>/
GET   /api/rooms/<slug>/messages/
POST  /api/new_room/
```

### WebSocket
```text
ws://localhost:8000/ws/chat/<room_slug>/
```

## Background Tasks
Celery is used for background processing, while Celery Beat is used for scheduled tasks.
```text
Celery Worker
→ Processes background tasks
Celery Beat
→ Runs scheduled tasks
Daily Activity Digest
→ Runs every 24 hours
```

## Caching
Redis is used for:
* Django caching
* Channel layers
* Real-time WebSocket communication
Cache invalidation is applied when related data is updated.

## Testing
Run the project tests using:
```bash
python manage.py test .
```


## Swagger
API documentation is available through Swagger.
```text
/api/swagger/schema/
```

## Setup
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

For the real-time features, make sure Redis is running locally.

## Production
The project is prepared for deployment using:
* Daphne for ASGI/WebSocket support
* PostgreSQL for the production database
* Redis for caching and WebSockets
* Celery Worker for background tasks
* Celery Beat for scheduled tasks

## Created By

[**Maryam Al Menshawy**](https://github.com/MariamAlMenshawy)
