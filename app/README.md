
# Rates calculator

An API used for getting returns a list with the average prices for each day on a route between port codes origin and destination.

## Tech used
- Python
- Flask web framework
- SQL

#### Required Parameters

- date_from (Add multiple files to the server) accepts multiple values
- date_to (List all files in the server) accepts no value
- origin (Remove a files in the server)  accepts single value
- destination (Updare a file in the server) accepts single value

#### Steps to run flask server

1. Clone the repo
   ```sh
   git clone https://github.com/Krishnanunni333/ratestask.git
   ```
2. CD into the ratetask/app directory
   ```sh
   cd ratetask/app
   ```
3. Execute the below command to install all dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. To run the app execute the below command
   ```sh
   python app.py
   ```

5. Test the application endpoints using the test script named test.py. Stop the above running app and run below command
   ```sh
   python test.py
   ```



#### Further development
1. Dockerfile is created for the application to be deployed as a container. It can be used to build the image and pushed to a container registry. But it needs networking to the postgres DB and that can be achieved using docker compose. As I was a bit occupied with certain other works and job, didn't implement that.

#### Notes
1. **Instead of connecting to DB everytime, I have implemented a cache-like methodology so that we dont need to query the DB for frequently read and very less written tables like the Ports table and the Regions table** 


