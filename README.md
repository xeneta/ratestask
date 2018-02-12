# Development section 

## Data definition

We are providing you with a small set of simplified real-world data. A
database dump is provided that includes the following information:

### Ports

Information about ports, including:

* 5-character Port Code
* Port Name
* Slug that describes which Region does the port belong in

### Regions

A hierarchy of Regions, including:

* Slug - a machine-readable form of the Region name
* The name of the Region
* Slug that describes which parent Region does the Region belong in

### Prices

Individual daily prices between ports, in USD.

* 5-character Origin Port Code
* 5-character Destination Port Code
* The day on which the price is valid on
* The price in USD

## Assignment

Develop an HTTP-based API capable of executing the tasks described
below. Our stack is based on Flask, but you are free to choose
anything you like. All data returned is expected to be in JSON format.

Please display us your knowledge of raw SQL (as opposed to using ORM querying tools) in at least one part.


### GET requirements

Implement an API endpoint that takes the following parameters:
*date_from, date_to, origin, destination* and returns a list with the
average prices for each day on a route between Port Codes *origin* and
*destination*. Both *origin, destination* params accept either Port
Codes or Region slugs, making it possible to query for average prices
per day between geographic groups of ports.

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

### POST requirements

Implement an API endpoint where you can upload a price, including
the following parameters: *date_from, date_to, origin_code,
destination_code, price*

## Extra details

* Keep your solution in a Version Control System of your
  choice. *Provide the solution as a public repository that can be
  easily cloned by our development team.*

* Provide any instructions needed to set up the system in `README.md`.

* Ensure the API handles errors and edge cases properly.

* Use dates in YYYY-MM-DD format for the API. There is no need of more
  complicated date processing.

* You are encouraged to modify or extend the database schema if you think a different model fits task better.

* If you have any questions, don't hesitate to ask us.

* We would like your feedback - Let us know how much time you spent on
  the task or about any difficulties you run into.


## Initial setup

We have provided a simple Docker setup for you, which will start a
Postgres instance populated with the assignment data. You don't have
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

You can connect to the exposed Postgres instance on the address
provided by docker, usually *172.17.0.1*. It is started with the
default user 'postgres' and no password.

```bash
psql -h 172.17.0.1 -U postgres
```

# Theoretical section

In this section we will provide a description of a largely extended
version of the service implemented above. Provide answers at a
high-level, using a couple of paragraphs for each question.

## Service definition

Imagine that for this service you need to receive and update big
batches of new prices, ranging within tens of thousands of items,
conforming to a similar format. Every batch of items needs to be
processed together, either all items go in, or none of them does.

Both the incoming data updates and requests for data can be highly
sporadic - there might be large periods without much activity,
followed by periods of heavy activity.

Being a paid service, high availability is very much a requirement.

How would you design the system? Provide a high-level diagram, along
with a few paragraphs describing the choices you've made and what
factors do you need to take into consideration?

## Additional questions

Please provide a couple of paragraphs, answering how you would
structure and scale the system in at least *at least* one of the
following situations:

1. The batch updates have started to become very large, but the
   requirements for their processing time are strict. 
   
2. Code updates need to be pushed out frequently. This needs to be
   done without the risk of stopping an update already being
   processed, nor a data response being lost.

3. For development and staging purposes, you need to start up a number
   of scaled-down versions of the system.
