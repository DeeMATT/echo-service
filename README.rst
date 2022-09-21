
# HTTP-based throttling echo service

An echo service with throttling to limit the number of API requests made in a certain period.




## Documentation

The /echo endpoint of the service should return the request body as is if the current number of
requests per running minute does not exceed the set rate limit. Otherwise, the endpoint
should respond with an error.

The /rate endpoint can be used to obtain the critical request rate and to set it to a new value.



## Installation

#### Prerequisites
- Redis Server  

### On Local
Install dependencies and start app on local



```bash
  >> pip install poetry        |# install dependency manager|
  >> poetry shell              |# activate virtual environment for app dependencies|
  >> poetry install            |# install app dependencies| 

  >> python3 main.py           |# start the application|

  voila!!!
```
  
### Using Docker
Install dependencies and start app using docker

```bash
  >> chmod +x deploy.sh        |# make the script executable|
  >> sh deploy.sh              |# execute docker shell script to create the docker containers|

  voila!!!
```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`APP_HOST`

`APP_PORT`

`REDIS_HOST`

`REDIS_PORT`
## Running Tests

To run tests, run the following command in project root directory

```bash
  pytest
```


## API Reference [http://127.0.0.1:8000/docs]

#### 1. Echo back a given payload
Accepts a JSON payload and responds back with the same payload if API rate limit isn't exceeded

```http
  POST /echo
```

Sample JSON Request payload
```json
{
    "api_throttling": "testing"
}
```

#### 2. Get the current service API rate limit
Retrieves the number of requests per running minute

```http
  GET /rate
```

Sample JSON Response payload
```json
{
    "rate_limit": "25"
}
```

#### 3. Set the service API rate limit
Set the number of requests per running minute

```http
  POST /rate
```

Sample JSON Request payload
```json
{
    "rate_limit": "25"
}
```
Sample JSON Response payload
```json
{
    "rate_limit": "25"
}
```



## Authors

- [Damilola Odeyemi](https://github.com/DeeMATT)
