# Dann's Store API
> RESTful API for dann's book store

[![Build Status](https://travis-ci.com/danuluma/dannstore.svg?branch=develop)](https://travis-ci.com/danuluma/dannstore)  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://raw.githubusercontent.com/danuluma/dannstore/develop/LICENSE)

[![Maintainability](https://api.codeclimate.com/v1/badges/aff46e1c9a8c80f7235d/maintainability)](https://codeclimate.com/github/danuluma/dannstore/maintainability)  [![Coverage Status](https://coveralls.io/repos/github/danuluma/dannstore/badge.svg)](https://coveralls.io/github/danuluma/dannstore)

<!-- # WIP -->
This is the api backend for dann's bookstore. It's intended for use internally within a single store. There are currently two categories of users: attendants and admins/owner. Each user is identified by an access token which allows appropriate access level to be granted to him/her.
This api provides and interface for the users to interact with the database via the available rest endpoints.


## Local Installation Guide

## Requirements
This project is written in python3.7 hence requires python >3.6 to be installed on your local environment. Download and install the latest version for your OS from https://www.python.org/downloads/

It's best to install this project in a virtual environment. Please first install virtualenv package which we'll use to create a virtual environment later by running
```pip install virtualenv```.

You may also need to install virtual environment wrapper to easily work with virtual environments.
```pip install virtualenvwrapper```
For windows users, please use ```pip install virtualenvwrapper-win```.


## Installation

* Clone this repo to your local computer using ```git clone https://github.com/danuluma/dannstore.git```
* Switch into the project directory ```cd dannstore```
* Create a virtual environment ```mkvirtualenv dannstore```. You can replace ```dannstore``` with a name of your liking.
* Activate your virtual environment ```source dannstore/bin/activate```
* Install the project's dependencies by running ```pip install -r requirements.txt```
* Copy .env.sample to .env ```cp .env.sample .env```
* Run the app locally with ```python3 run.py```
* Now lets create the databases ```psql -p 5432 -h localhost -U postgres -c 'create database testing;'```
```psql -p 5432 -h localhost -U postgres -c 'create database development;'```
* When prompted for a password, please use ```postgres``` else you'll have to update the ```HOST_PASSW``` value in the .env file
* If you followed along properly, the app will create the necessary tables on its own during the first run


## Usage

The following endpoints are currently available:

## Version 1
* Versin 1 uses data structures(lists and dictionaries) to store data.

### Endpoints
|  URL Endpoint | HTTP Request  |  Access | Status  |
|---|---|---|---|
|  /api/v1/reg |  POST | It registers a new user  |  Private (Only the owner can add new attendants) |
|  /api/v1/login |  POST | It authenticates a user and generates access_token  |  Public |
|  /api/v1/products | GET  |  Fetch all products |  Public |
|  /api/v1/products/productID | GET  |  Get a specific product using the product’s id |  Public |
|  /api/v1/sales |  GET |  Fetch all sale records | Private (Only admins/owner can view all sales)  |
|  /api/v1/sales/saleID| GET | Get a specific sale record using the sale record Id. | Private(Only admins/record creator can view)  |
|  /api/v1/products |  POST |  Create a new product record. |  Private (Only admins/owner can add products) |
|  /api/v1/sales |  POST |  Create a sale record.  |  Private (Only attendants can create sale records) |


## Usage example
* Please look here --> [Examples](https://documenter.getpostman.com/view/5303933/RWguvGJK) for usage examples of the api endpoints and expected results.
* To test using curl, first set up the project as described in installation procedure.
* Run the app in the terminal then open another terminal window to test the endpoints.
* Select `curl` on the top right of this [page](https://documenter.getpostman.com/view/5303933/RWguvGJK). Copy and run examples on your local terminal.


## Version 2
* Version 2 uses a postgres database to store data

### Endpoints

|  URL Endpoint | HTTP Request  |  Access | Status  |
|---|---|---|---|
|  /api/v2/signup |  POST | It registers a new user  |  Private (Only the owner can add new attendants) |
|  /api/v2/login |  POST | It authenticates a user and generates access_token  |  Public |
|  /api/v2/logout |  DELETE | It logs out a user  |  Public |
|  /api/v2/users/userID |  GET | it retrieves a user by ID |  Private(Only the admin can access) |
|  /api/v2/users/userID |  PUT | It promotes or demotes a user |  Private(Only the owner can access) |
|  /api/v2/users |  GET | It retrieves all the users in the database  |  Private(Only admins can access) |
|  /api/v2/users |  DELETE | It deletes a user by userID  |  Private(Only the owner can access) |
|  /api/v2/products | GET  |  Fetch all products |  Public |
|  /api/v2/products/productID | GET  |  Get a specific product using the product’s id |  Public |
|  /api/v2/products |  POST |  Create a new product record. |  Private (Only admins/owner can add products) |
|  /api/v2/products |  PUT |  Updates a product record. |  Private (Only admins/owner can edit products) |
|  /api/v2/products |  DELETE |  Deletes a product record. |  Private (Only admins/owner can delete products) |
|  /api/v2/sales |  POST |  Create a sale record.  |  Private (Only attendants can create sale records) |
|  /api/v2/sales/saleID| GET | Get a specific sale record using the sale record Id. | Private(Only admins/record creator can view)  |
|  /api/v2/sales |  GET |  Fetch all sale records | Private (Only admins/owner can view all records)


## Usage example
* Please look here --> [Examples](https://documenter.getpostman.com/view/5303933/RWgxvvVD) for usage examples of the api endpoints and expected results.
* To test using curl, first set up the project as described in installation procedure.
* Run the app in the terminal then open another terminal window to test the endpoints.
* Select `curl` on the top right of this [page](https://documenter.getpostman.com/view/5303933/RWgxvvVD). Copy and run examples on your local terminal.




## Testing
* To run automatic test on the project, simply run ```python3 -m unittest``` while in the project's root directory.
* Check on the terminal output for the test results

* You can manually test each of the endpoints using postman
* See an example below
![Postman example](https://res.cloudinary.com/danuluma/image/upload/v1539902345/Screenshot_from_2018-10-19_01-30-39.png)


## Release History

* v1
    * The first stable release
    * Uses data structures to store data
* v2
    * The second stable release
    * Uses postgres database to store data


## Demo
* [Heroku](https://dannstore.herokuapp.com)
* [Documentation v1](https://documenter.getpostman.com/view/5303933/RWguvGJK)
* [Documentation v2](https://documenter.getpostman.com/view/5303933/RWgxvvVD)



## Credits
#### [Andela](https://andela.com/)
#### [Edward Mudaida](https://github.com/EdwardMudaida)
#### [Daniel Maina](https://github.com/danielwangai)

## Author
#### [Dann](https://github.com/danuluma)

## License
[MIT](https://raw.githubusercontent.com/danuluma/dannstore/develop/LICENSE)

## Contributing

1. Fork this on [Github](https://github.com/danuluma/dannstore/fork)
2. Create your feature branch (`git checkout -b ft-fooBar-<issueID>`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin ft-fooBar-<issueID>`)
5. Create a new Pull Request
