# INSTAGRAM INFLUENCER SEARCH PORTAL

[![Instagram search Portal](https://github.com/Nkasi-e/instagram-influencer/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/Nkasi-e/instagram-influencer/actions/workflows/build-deploy.yml) <a href='https://coveralls.io/github/Nkasi-e/instagram-influencer?branch=update-branch'><img src='https://coveralls.io/repos/github/Nkasi-e/instagram-influencer/badge.svg?branch=update-branch' alt='Coverage Status' /></a>

## Features

- [x] Users can create account with just email and password
- [x] Authenticated users can create profile, providing username, followers count and bio
- [x] One user is liable to have a single profile, that means a user cannot create multiple profiles
- [x] visitors can use the search endpoint to search text in username and bio, minimum followers count and maximum followers count
- [x] search result returns a list of profiles that meets the search criterial

## API Documentation

- API allows visitors to search for profile username and bio, and profile counts which can either be minimum or maximum followers count, and also allows only authorized users are allowed to create a profile.

### Models <br>

### Users

| field      | data_type | constraints       | validation                                                                                                |
| ---------- | --------- | ----------------- | --------------------------------------------------------------------------------------------------------- |
| id         | Object    | required          | None                                                                                                      |
| email      | string    | required          | unique, email must conform to email (example: johndoe@gmail.com)                                          |
| password   | string    | required          | pasword must contain at least one uppercase, one lowercase, one number, and must be at least 8 characters |
| created_at | timestamp | automatically set | None                                                                                                      |

### Profile

| field      | data_type     | constraints                          | validation |
| ---------- | ------------- | ------------------------------------ | ---------- |
| id         | integer       | required                             | None       |
| username   | string        | required                             | None       |
| followers  | Integer       | required                             | None       |
| bio        | String(100)   | optional, default value set to None  | None       |
| created_at | timestamp     | required, automatically set          | None       |
| owner_id   | Integer       | required, ForeignKey, Unique         | None       |

### Home Page

- Route: /
- Method: GET
- Header
  - Authorization: None
- Response: Success

```json
{
  "message": "Welcome to Instagram Influencer search portal"
}
```

### Signup User <br>

- Route: /account/signup
- Method: POST
- Header
  - Authorization: None
- Body:

```json
{
  "email": "johndoe@example.com",
  "password": "Password123"
}
```

- Response: Success

```json
{
  "id": 1,
  "email": "johndoe@example.com",
  "created_at": "2023-02-05T15:29:24.712Z"
}
```

### Login User

- Route: /login
- Method: POST
- Body:

```json
{
  "email": "johndoe@example.com",
  "password": "Password123"
}
```

- Response: Success

```json
{
  "email":"johndoe@example.com",
  "access_token": "accesstokenexample&8ofiwhb.fburu276r4ufhwu4.o82uy3rjlfwebj",
  "token_type": "Bearer"
}
```

### Create Profile

- Route: /profile
- Method: POST
- Header
  - Authorization: Bearer {token}
- Body:

```json
{
  "username": "string",
  "followers": 100,
  "bio": "I am a software developer"
}
```

- Response: Success

```json
{
  "username": "string",
  "followers": 100,
  "bio": "I am a software developer",
  "id": 1,
  "created_at": "2023-02-05T19:02:41.204Z",
  "owner": {
    "id": 1,
    "email": "johndoe@example.com",
  }
}
```

### Search Route

- Route: /search
- Method: GET
- Header
  - Authorization: None
- Body:

- Response: Success

```json
[
    {
    "username": "string",
    "followers": 100,
    "bio": "I am a software developer",
    "id": 1,
    "created_at": "2023-02-05T19:02:41.204Z",
    "owner": {
        "id": 1,
        "email": "johndoe@example.com",
    }
    },

    {
    "username": "user",
    "followers": 10,
    "bio": "I am a devOps Engineer",
    "id": 2,
    "created_at": "2023-02-05T19:02:41.204Z",
    "owner": {
        "id": 2,
        "email": "user@example.com",
    }
    },

    {
    "username": "example",
    "followers": 100,
    "bio": "I am a Technical writer",
    "id": 3,
    "created_at": "2023-02-05T19:02:41.204Z",
    "owner": {
        "id": 3,
        "email": "user@example.com",
    }
    },
]
```

### Search Route with query

- Route: /search?text=Engineer&min_followers=100
- Method: GET
- Header
  - Authorization: None
- Body:

- Response: Success

```json
[
    {
  "username": "string",
  "followers": 100,
  "bio": "I am a software developer",
  "id": 1,
  "created_at": "2023-02-05T19:02:41.204Z",
  "owner": {
    "id": 1,
    "email": "johndoe@example.com",
  }
}
]
```

## Getting Started

### Prerequisites

In order to run this project locally, you would need to have the following installed on your local machine.

- Python ^3.10,
- PostgreSQL
- Docker (Optional)

### Installation

- Clone this repository

```bash
git clone [https://github.com/Nkasi-e/instagram-influencer.git]

```

- update env with .env.example.txt
- Download all dependecies using ```pip install -r requirements.txt``` or ```poetry install``` that's if you have poetry installed already on your machine

### to start up server

- run ```uvicorn app.main:app --reload```

### to start up container in detached mode

- run ```docker-compose -f decker-compose-dev.yml up -d```
