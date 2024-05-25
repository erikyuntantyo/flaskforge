# FlaskForge: A RESTful API using Flask

FlaskForge is a RESTful API built using the Flask framework. It allows users to perform CRUD (Create, Read, Update, Delete) operations on various resources. The API is designed to be simple, yet powerful, and is easy to integrate with other applications.

## Installation

**Clone the repository:**

```bash
$ git clone https://github.com/erikyuntantyo/flaskforge.git
```

## With Virtual Environment

**Navigate into the FlaskForge directory:**

```bash
$ cd flaskforge
```

**Create and activate the virtual environment:**

- On Windows

```bash
$ python -m venv .venv
$ .venv\Scripts\activate.bat
```

- On Linux or OSX:

```bash
$ python -m venv .venv
$ source .venv\bin\activate
```

**Install the required dependencies:**

```bash
$ pip install -r requirements.txt
```

## Your First FlaskForge Project

**Default endpoint:**

The default endpoint is `/`, which returns an object containing the version number of the API.

**Custom endpoint:**

To setup custom endpoints, modify the `register_routes` method in `utils/boot.py`. For example:

```python
service_factory.register_routes({
    "/auth/<custom_endpoint>": AuthSvc(Methods.POST),  # Allow POST method to be available for the service with custom endpoint
    "/users": UsersSvc()  # Restricted service to be accessed by internal service only
})
```

Service have 6 default methods, there are:

| Methods    | Description
|---   |---
| `ALL` | Allow all methods available in endpoint
| `POST` | Allow post method available in endpoint
| `GET` | Allow get method available in endpoint
| `FIND`    | Allow find method available in endpoint
| `PATCH`   | Allow patch method available in endpoint
| `DELETE`  | Allow delete method available in endpoint

> **NB:** If one of the methods is not declared in the service, then the service will not have public access, only available to internal service and can use all methods.

**Start server:**

To start the server, navigate to the project directory and run the following command:

```bash
$ python app.py
```

This will start the server on `http://localhost:3131`.

## Try Endpoints

Now, head on over to **POST** request to [http://localhost:3131/](http://localhost:3131/), and it will return:
```json
{
    "apiVersion": "1.0.0"
}
```

## Unit Tests

Unit tests for the FlaskForge API are written using pytest.
