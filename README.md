# Practical section

## Premise

Provided are two simplified parts of the same application environment: A database dump and an API service. Your task is to automate setting up the development environment in a reliable and testable manner using "infrastructure as code" principles.

The goal is to end up with a command — or a limited set of commands — that would install the different environments and run them using containers. The code should come with instructions on how to run it and deploy it to arbitrary targets; It could be deployed locally, towards physical machines, or towards virtual nodes in the cloud.

## Running the database

There’s an SQL dump in `db/rates.sql` that needs to be loaded into a PostgreSQL 9.6 database.

After installing the database, the data can be imported through:

```
createdb rates
psql -h localhost -U postgres < db/rates.sql
```

You can verify that the database is running through:

```
psql -h localhost -U postgres -c "SELECT 'alive'"
```

The output should be something like:

```
 ?column?
----------
 alive
(1 row)
```

## Running the API service

Start from the `rates` folder.

### 1. Install prerequisites

```
DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y python-pip
pip install -U gunicorn
pip install -Ur requirements.txt
```

### 2. Run the application
```
gunicorn -b :3000 wsgi
```

The API should now be running on [http://localhost:3000](http://localhost:3000).

### 3. Test the application

Get average rates between ports:
```
curl "http://127.0.0.1:3000/rates?date_from=2016-01-01&date_to=2016-01-31&orig_code=CNGGZ&dest_code=EETLL"
```

The output should be something like this:
```
{
   "rates" : [
      {
         "count" : 3,
         "day" : "2016-01-31",
         "price" : 1154.33333333333
      },
      {
         "count" : 3,
         "day" : "2016-01-30",
         "price" : 1154.33333333333
      },
      ...
   ]
}
```


## Extra details

* Keep your solution in a Version Control System of your
  choice. *Provide the solution as a public repository that can be easily cloned by our development team.*

* The specifications and requirements can change over time, and this needs to be taken into account when designing the solution. Examples: there could be more source code files added; line 2 of any given file might change in the future, and so forth.

* To allow this to sanely run on any machine, it should be possible to provide target or configuration overrides.

* List and describe the tool(s) used, and why they were chosen for the task.

* The configuration file `rates/config.py` has some defaults that will most likely change depending on the solution. It would be beneficial to have a way of more dynamically pass in config values.

* Provide any instructions needed to run the automation solution in `README.md`.

* If you have any questions, please don't hesitate to ask us.

* We would like your feedback - Let us know how much time you spent on the task or about any difficulties you run into.

# Theoretical section
In this section we are seeking high-level answers, using a couple of paragraphs for each question.

## Deploying the service for production
Consider the following statements:

* Please describe what you would like to change — if anything —  to make the provided solution properly scalable and deployable for a production environment.
* Are there any caveats or shortcomings a developer using the solution would need to know.

## Extended service

Imagine that for providing data to fuel this service, you need to receive and insert big batches of new prices, ranging within tens of thousands of items, conforming to a similar format. Each batch of items needs to be processed together, either all items go in, or none of them does.

Both the incoming data updates and requests for data can be highly sporadic - there might be large periods without much activity, followed by periods of heavy activity.

Being a paid service, high availability is very much a requirement.

* How would you design the system?
* How would you set up monitoring to identify bottlenecks as the load grows?
* How can those bottlenecks be addressed in the future?

Provide a high-level diagram, along with a few paragraphs describing the choices you've made and what factors do you need to take into consideration.

## Additional questions

Here are a few possible scenarios where the system requirements change or the new functionality is required:

1. The batch updates have started to become very large, but the requirements for their processing time are strict.

2. Code updates need to be pushed out frequently. This needs to be done without the risk of stopping a data update already being processed, nor a data response being lost.

3. For development and staging purposes, you need to start up a number of scaled-down versions of the system.

Please address *at least* one of the situations. Please describe:

- Which parts of the system are the bottlenecks or problems that might make it incompatible with the new requirements?
- How would you restructure and scale the system to address those?
