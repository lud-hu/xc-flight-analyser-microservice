# XC Flight Analyser Microservice

This is a small microservice that provides an endpoint for POSTing a recorded GPS flight log (igc file). It then returns a JSON file with several different evaluations and calculated values about the flown distance (taking into account the international competition rules).

It is basically a wrapper around [XCSoar](https://github.com/XCSoar/XCSoar)'s C++ code that does the calculations.

## Technology

This project uses a docker container that serves a [Flask](https://github.com/pallets/flask/) & [Gunicorn](https://github.com/benoitc/gunicorn) webserver. It has one endpoint that takes POST requests with a file, which is then evaluated.

## Usage

### Start the server
Just start the docker container, e.g. with contained the docker compose file:

```bash
$ docker-compose up
```

You can also [deploy this on Google Cloud Run](https://www.youtube.com/watch?v=t5EfITuFD9w).

### Fire the request

Just use a normal HTTP POST request to send the file as multipart/form-data at the endpoint */analyse*

```bash
curl 'http://127.0.0.1:8080/analyse' -H 'Content-Type: multipart/form-data' -F 'file=@flight.igc'
```

### Response

The response will contain data about
- contest distances and details
- flight phases
- flight performance
- wind speeds

E.g.:
```json
{'contests': {
    'olc_plus': {
        'classic': {
            'distance': 22071.043042087873,
            'duration': 5732,
            'score': 22.071043042087872,
            'speed': 3.850495994781555,
            'turnpoints': [
                    {'location': {
                            'latitude': 45.82480000001414,
                            'longitude': 11.774750000003634
                        },
                        'time': 37117
                    },
                    ...
                ]
            }
        }
    },
    ...
}
```

For more details please checkout the [XCSoar Project](https://github.com/XCSoar/XCSoar/blob/master/test/src/AnalyseFlight.cpp).

## Used libraries / frameworks
Docker image:
- https://hub.docker.com/_/python

Frameworks:
- https://github.com/pallets/flask/
- https://github.com/benoitc/gunicorn

Log evaluation:
- https://github.com/skylines-project/py-xcsoar
- https://github.com/XCSoar/XCSoar/tree/master/python
