# Welcome to alexandria-users
Decomposed microservice for only user management service

# Run/Set-up
```console
docker build -t local/alexandria-users:1.0.001 . --no-cache
```

# Goal/Objective

We would be spinning up the User Service and its related dependencies here:

```console
docker-compose up
```

1. You may check the API documentation by hitting http://localhost:9001/docs from your browser
1. It takes the port number 9001 configured in the Dockerfile.

# Below are the services currently available

User APIs
1. TBD

# Tips for implementing a new service
1. Add URL Path in the **urls.py**
2. Tag the URL path in an annotation of respective api definition in **main.py**
3. Implement DB operation ( any of CURD operations ) in **database.py** if required
4. Call the above implemented DB operation in api definition of  **main.py**


# License
Please refer to the LICENSE