# Data definition

We are providing you with a small set of simplified real-world data. A
database dump is provided that includes the following information:

## Ports

Information about ports, including:

* 5-character port code
* Port name
* Slug describing which region the port belongs to

## Regions

A hierarchy of regions, including:

* Slug - a machine-readable form of the region name
* The name of the region
* Slug describing which parent region the region belongs to

## Prices

Individual daily prices between ports, in USD.

* 5-character origin port code
* 5-character destination port code
* The day for which the price is valid
* The price in USD

# Assignment

1. Develop an HTTP-based API capable of handling the GET and POST requests described
below in [GET Request Task](#get-request-task) and [POST Request Task](#post-request-task). Our stack is based on Flask, but you are free to choose
anything you like. All data returned is expected to be in JSON format. Please demonstrate your knowledge of SQL (as opposed to using ORM querying tools) in at least one part.
2. Describe the system you would design for handling the [Batch Processing Task](#batch-processing-task).


## GET Request Task

### Part 1

Implement an API endpoint that takes the following parameters:

* date_from
* date_to
* origin
* destination

and returns a list with the average prices for each day on a route between port codes *origin* and *destination*.

Both the *origin, destination* params accept either port codes or region slugs, making it possible to query for average prices per day between geographic groups of ports.

    curl http://127.0.0.1/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main

    [
        {
            "day": "2016-01-01",
            "average_price": 129
        },
        {
            "day": "2016-01-02",
            "average_price": 139
        },
        ...
    ]


### Part 2

Make a second API endpoint return an empty value (JSON null) for days
on which there are less than 3 prices in total.

    curl http://127.0.0.1/rates_null?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main

    [
        {
            "day": "2016-01-01",
            "average_price": 129
        },
        {
            "day": "2016-01-02",
            "average_price": null
        },
        {
            "day": "2016-01-03",
            "average_price": 215
        },
        ...
    ]

## POST Request Task

### Part 1

Implement an API endpoint where you can upload a price, including
the following parameters:

* date_from
* date_to
* origin_code,
* destination_code
* price


### Part 2

Extend that API endpoint so that it could accept prices in
different currencies. Convert into USD before
saving. [https://openexchangerates.org/](https://openexchangerates.org/) provides
a free API for retrieving currency exchange information.


## Batch Processing Task

Imagine you need to receive and update batches of tens of thousands of new prices, conforming to a similar format. Describe, using a couple of paragraphs, how you would design the system to be able to handle those requirements. Which factors do you need to take into consideration?


# Extra details

* Keep your solution in a Version Control System of your
  choice. *Provide the solution as a public repository that can be
  easily cloned by our development team.*

* Provide any instructions needed to set up the system in `README.md`.

* Ensure the API handles errors and edge cases properly.

* Use dates in YYYY-MM-DD format for the API. There is no need for more
  complicated date processing.

* You are encouraged to modify or extend the database schema if you think a different model fits the task better.

* If you have any questions, please don't hesitate to contact us at tech-recruitment@xeneta.com

* Please let us know how much time you spent on the task, and of any difficulties that you ran into.


# Initial setup

We have provided a simple Docker setup for you, which will start a
PostgreSQL instance populated with the assignment data. You don't have
to use it, but you might find it convenient. If you decide to use
something else, make sure to include instructions on how to set it up.

You can execute the provided Dockerfile by running:

```bash
docker build -t ratestask .
```

This will create a container with the name *ratestask*, which you can
start in the following way:

```bash
docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask
```

You can connect to the exposed Postgres instance on the Docker host IP address,
usually *127.0.0.1* or *172.17.0.1*. It is started with the default user `postgres` and `ratestask` password.

```bash
PGPASSWORD=ratestask psql -h 127.0.0.1 -U postgres
```

alternatively, use `docker exec` if you do not have `psql` installed:

```bash
docker exec -e PGPASSWORD=ratestask -it ratestask psql -U postgres
```

Keep in mind that any data written in the Docker container will
disappear when it shuts down. The next time you run it, it will start
with a clean state.
