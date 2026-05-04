# JWKS-server3

## Overview

This project enhance the security and functionality of the JWKS server by incorporating AES encryption for private keys, implementing user registration and logging authentication requests

-----------------------------------------------------

## Features

* User registration with UUID-generated passwords
* Password hashing using Argon2
* Authentication endpoint with credential verification
* Logging of all authentication requests (IP, timestamp, user ID)
* JWKS endpoint that returns stored keys
* Key expiration support

-----------------------------------------------------

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env` file:

```env
NOT_MY_KEY=your_32_byte_secret_key
```

3. Insert a key:

```bash
python seed_keys.py
```

4. Run server:

```bash
python app.py
```

-----------------------------------------------------

## API Endpoints

### Register

`POST /register`
Creates a new user and returns a generated password.

### Authenticate

`POST /auth`
Verifies user credentials and logs the request.

### JWKS

`GET /jwks`
Returns all valid (non-expired) keys.

-----------------------------------------------------





