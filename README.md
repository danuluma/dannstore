# Dann's Store API
> RESTful API for dann's book store

[![Build Status](https://travis-ci.com/danuluma/dannstore.svg?branch=develop)](https://travis-ci.com/danuluma/dannstore)  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://raw.githubusercontent.com/danuluma/dannstore/develop/LICENSE)

[![Maintainability](https://api.codeclimate.com/v1/badges/aff46e1c9a8c80f7235d/maintainability)](https://codeclimate.com/github/danuluma/dannstore/maintainability)   [![Coverage Status](https://coveralls.io/repos/github/danuluma/dannstore/badge.svg?branch=ch-update-readme-161247582)](https://coveralls.io/github/danuluma/dannstore?branch=ch-update-readme-161247582)

<!-- # WIP -->
This is the api backend for dann's bookstore. It's intended for use internally within a single store. There are currently two categories of users: attendants and admins/owner. Each user is identified by an access token which allows appropriate access level to be granted to him/her.
This api provides and interface for the users to interact with the database via the available rest endpoints.


## Local Installation Guide

## Requirements
This project is written in python3 hence requires python 3 to be installed on your local environment. Download and install the latest version for your OS from https://www.python.org/downloads/

It's best to install this project in a virtual environment. Please first install virtualenv package which we'll use to create a virtual environment later by running
```pip install virtualenv```.

You may also need to install virtual environment wrapper to easily work with virtual environments.
```pip install virtualenvwrapper```
For windows users, please use ```pip install virtualenvwrapper-win```.


## Installation

* Clone this repo to your local computer using ```git clone https://github.com/danuluma/dannstore.git```
* Switch into the project directory ```cd dannstore```
* Create a virtual environment ```mkvirtualenv dannstore```. You can replace ```dannstore``` with a name of your liking.
* Install the project's dependencies by running ```pip install -r requirements.txt```
* Run the app locally with ```python3 run.py```


## Usage

The following endpoints are currently available:
### Endpoints
|  URL Endpoint | HTTP Request  |  Access | Status  |
|---|---|---|---|
|  /dann/api/v1/reg |  POST | It registers a new user  |  Private (Only the owner can add new attendants) |
|  /dann/api/v1/login |  POST | It authenticates a user and generates access_token  |  Public |
|  /dann/api/v1/products | GET  |  Fetch all products |  Public |
|  /dann/api/v1/products/<productId> | GET  |  Get a specific product using the product’s id |  Public |
|  /dann/api/v1/sales |  GET |  Fetch all sale records | Private (Only admins/owner can view all sales)  |
|  /dann/api/v1/sales/<saleId>
 |  Get a specific sale record using the sale record Id. |  GET | Private(Only admins/record creator can view)  |
|  /dann/api/v1/products |  POST |  Create a new product record. |  Private (Only admins/owner can add products) |
|  /dann/api/v1/sales |  POST |  Create a sale record.  |  Private (Only attendants can create sale records) |



## Testing
* To run automatic test on the project, simply run ```python3 -m unittest``` while in the project's root directory.
* Check on the terminal output for the test results

You can manually test each of the endpoints using postman

## Release History

* v1
    * The first stable release
    * Uses data structures to store data


## Demo
* [Heroku](https://dannstore.herokuapp.com)

## Credits
#### [Andela](https://andela.com/)

## Author
#### [Dann](https://github.com/danuluma)

## License
[MIT](https://raw.githubusercontent.com/danuluma/dannstore/develop/LICENSE)

## Contributing

1. Fork it (<https://github.com/danuluma/dannstore/fork>)
2. Create your feature branch (`git checkout -b ft-fooBar-<issueID>`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin ft-fooBar-<issueID>`)
5. Create a new Pull Request