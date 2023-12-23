# Flask_CRUD
CS Elective
Final Exam Drill. CSE1

Activity: Building a CRUD REST API with MySQL, Testing, and XML/JSON Output

In this hands-on activity, you will be creating a CRUD (Create, Read, Update, Delete) REST API for your chosen MySQL database (from
our recent activity). The API will allow users to interact with the database and will act as an Interface to any client that understands
JSON or XML. You will also set up tests to ensure the functionality of the API, and provide the option to format the API output as XML
or JSON.

This project aims to show our skills by building a CRUD (Create, Read, Update, Delete) REST API using Flask and MySQL, and perform several tasks related to testing, formatting options, security, and documentation. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Authentication](#authentication)
- [Testing](#testing)

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Set up the database
5. Configure environment variables
6. Run the application

## Usage
This is just a simple CRUD of customers table in customers and jobs data model (or database).

### POST /users

   ```http
   http://127.0.0.1:5000/login
   users:{
     "admin": "password",
     "username": "password"
   }
  ```

### TESTING
  ```bash
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"password\"}" http://127.0.0.1:5000/login
curl -X GET -H "Authorization: Bearer <the key>" http://127.0.0.1:5000/protected
start http://127.0.0.1:5000/customers
```

