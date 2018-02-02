# FlowMeasurement

A simple application which compare measurements conducted using two types of flowmeters callibrated in different temperature and pressure conditions.

> **Note**: This application is still under development. I create it because I want to make my dayly work easier and imrove my pogramming skills.

## Gettinng Started

### Environment

- Python 3.6
- Django 1.11

### Installation on a local machine

> **Note**: This examples are based on Ubuntu 16.04 distribution.

#### 1. Install Python and virtual environment packages

> Python 3 is pre-installed on Ubuntu 16.04. You can check the version of Python 3 using ```shell $ python3 -V```

```shell
$ sudo apt-get install python3-pip
$ sudo apt-get install build-essential python-dev libffi-dev libssl-dev
$ sudo apt-get install python3-venv
```

#### 2. Set up a local virtual environment and activate it

```shell
$ mkdir python_envs
$ cd python_envs

$ python3 -m venv flow_measurement_env

$ cd flow_measurement_env
$ source bin/activate
```
#### 3. Clone the repository from github

```shell
git clone https://github.com/elangaar/flow-measurement.git
```

#### 4. Install requirements

```shell
$ cd django-weather-forecast
$ pip install -r Requirements.txt
```
#### 5. Run development server for the project

```shell
$ python3 manage.py runserver
```

### Run automated tests

```shell
$ python3 manage.py test flow_measurement/tests/
```


## License
FlowMeasurements is licensed under the terms of the MIT License (see the file LICENSE).
