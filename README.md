
Blog Post Project

This is a Django-based web API for managing and creating blog posts. The project allows users to create, read, update, and delete blog posts.


Features

User Authentication: Register, login using JWT AUthentication.
CRUD Operations: Create, read, update, and delete blog posts.
Search and Filter: Find blog posts by keywords or categories.

### Setup
1. Create and setup a virtualenv manually.
2. Install Dependencies : `pip install -r requirements.txt`
3. Install and setup Postgres
4. Create .env on project level set these env variables
    DB_NAME
    DB_USER
    PASSWORD
    EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD
    DEFAULT_FROM_EMAIL

5. Apply migrations : `python manage.py migrate` 
6. Run Server : `python manage.py runserver`
7. Run Redis server: `redis-server`
8. Run Celery worksers: `celery -A blog worker --loglevel=info`


API'S

Register and Login

http://127.0.0.1:8000/api/auth/register

payload: 
    {
        "username": "user",
        "email":"123@gmail.com",
        "role": "Author/Reader",
        "password":"Shazam@1998"
    }

response:

    {
    "id": 21,
    "username": "maji3d9@gmail.com",
    "role": "Author"
    }

http://127.0.0.1:8000/api/auth/login/

payload:
    {
        "username": "username",
        "password": "password"
    }

response:
{
    "refrest": "token",
    "access": "access"
}

POST APIs

create: http://127.0.0.1:8000/blog_post/api/posts
        payload:
        {
            "title": "two",
            "content": "magin"
        }

        response:
            {
            "id": 4,
            "title": "twso",
            "content": "magin",
            "author": 10,
            "views": 0,
            "created_at": "2025-01-18T12:57:16.906889Z",
            "updated_at": "2025-01-18T12:57:16.906912Z"
            }     

list : http://127.0.0.1:8000/blog_post/api/posts
detail: http://127.0.0.1:8000/blog_post/api/posts/{id}

update: http://127.0.0.1:8000/blog_post/api/posts/{id}
        payload:
        {
            "title": "two",
            "content": "magin"
        }

delete: http://127.0.0.1:8000/blog_post/api/posts/{id}

Like/Dislike APIs

post:  http://127.0.0.1:8000/blog_post/api/posts/12/react/
    payload:
    {
        "reaction": "like/dislike"
    }

    response:
        {
        "id": 1,
        "user": 2,
        "post": 1,
        "reaction": "like",
        "created_at": "2025-01-18T12:58:46.593922Z"
        }

comments api
post:  http://127.0.0.1:8000/blog_post/api/posts/15/comment/
    payload:

    {
        "content": "text"
    }

    response:

        {
        "id": 1,
        "post": 2,
        "content": " cdfd ",
        "user": 5
        }

statastics api

get: http://127.0.0.1:8000/blog_post/api/posts/{id}/stats/ 

    response:

        {
        "id": 2,
        "title": "Same",
        "no_of_likes": 0,
        "no_of_comments": 0,
        "views": 3
        }