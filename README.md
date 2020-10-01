# Tech+ UW Portal for an amazing project

## About
The Tech+ UW Portal is the main landing site for current/prospective members and sponsors to learn about Tech+. Moreover, this portal also enables mentors and mentees to update their profiles and potentially maintain mentor-mentee relationships.

## Running the Server-Side API
The server-side API is a **dockerized** application, hence you will need the following installations on your machine: 
- [Docker](https://docs.docker.com/desktop/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

The API can then be run by running the following commands on your terminal: 
```shell
cd portal_api
docker-compose up -d --build
```

To test that the API is working as expected, you can hit the **health** endpoint by entering *http://localhost:8080/health* in your browser. The following response should be returned: 

```json
{"status": "Healthy!"}
```

## Testing the Server-Side API
**Note**: If in running the following commands, you get the following error: 
```shell
the input device is not a TTY.  If you are using mintty, try prefixing the command with 'winpty'
```
simply prefix the command with 'winpty'

**Note**: The following commands assume that the server-side API is already running using the following command: 
```shell
cd portal_api
docker-compose up -d --build
```

Run the flake8 linter which is part of the build pipeline by running the following command:  
```shell
docker-compose exec flask flake8
```

If you get the aforementioned error, run the same command with prefixed with *winpty*, as follows:  
```shell
winpty docker-compose exec flask flake8
```

Run the tests which are part of the build pipeline by running the following command:  
```shell
docker-compose exec flask python -m pytest "tests"
```

If you get the aforementioned error, run the same command with prefixed with *winpty*, as follows:  
```shell
winpty docker-compose exec flask python -m pytest "tests"
```
