Data definition
---------------------

We are providing you with a small set of simplified real-world data. A
database dump is provided that includes the following information:

Ports
=====

Information about ports, including:

* 5-character Port Code
* Port Name
* Slug that describes which Region does the port belong in

Regions
=======

A hierarchy of Regions, including:

* Machine-readable form of the Region name
* The name of the Region
* Slug that describes which parent Region does the Region belong in

Prices
======

Individual daily prices between ports, in USD. 

* 5-character Origin Port Code
* 5-character Destination Port Code
* The day on which the price is valid on
* The price in USD

Assignment
----------

Develop an HTTP-based API capable of executing the tasks described
below. Our stack is based on Flask, but you are free to choose
anything you like. All data returned is expected to be in JSON format.

GET requirements
================

1. Implement an API endpoint that takes the following parameters:
   *date_from, date_to, origin_code, destination_code* and returns a
   list with the average price on this route for each day.

2. Extend the API endpoint so that it could take either *origin_code,
   destination_code* or *origin_slug, destination_slug* making it
   possible to query for average prices for groups of ports.
   
3. Make it possible to return an empty value for days on which
   there are less than 3 prices in total.

4. If there are not enough prices to get an average for *at least one*
   day in the selected range, include more ports by following the
   region hierarchy "up", until you can find enough prices
   to aggregate.
   
POST requirements
=================

1. Implement an API endpoint where you can upload a price, including
   the following parameters: *date_from, date_to, origin_code,
   destination_code, price*
   
2. Extend that API endpoint so that it could accept prices in
   different currencies. Convert into USD before
   saving. [https://openexchangerates.org/](Openexchangerates) provide
   a free API for retrieving currency exchange information.
   
3. Create another API endpoint that is able to take in a batch of new
   prices. Consider what would happen if the request is very large and
   ran on a system with very low timeouts.
   
Extra details
=============

* Keep your solution in a Version Control System of your
  choice. Provide the solution as a public repository that can be
  easily cloned by our development team.
  
* Provide any instructions needed to set up the system in `README.md`.

* Ensure the API handles errors and edge cases properly.

* Use dates in YYYY-MM-DD format for the API. There is no need of more
  complicated date processing.
  


Initial setup
-------------

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
