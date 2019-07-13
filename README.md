# Zigway's Test Project

## OBJECTIVE
```txt
Hi Faisal, here's your tech test:

Implement a client and server JWT authentication using Python  backend and React frontend. Please send your projects through Internshala or a GitHub repo together with a demo and documentation of 
1. the project purpose
2. instructions on how to run the project.
```

## Running the project
Assuming nodejs, python3, virtualenv already installed on the machine (running Linux of MacOS).

### 1. Cloning
```bash
git clone https://github.com/Faisal-Manzer/ZigwayTest.git
cd ZigwayTest
```

### 2. Running Django Development Server
**OPEN IN ANOTHER TERMINAL TAB.**
```bash
cd server
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
python3 manage.py runserver
```

### 3. Migrating database [optional]
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

NOTE: Database used in this project is sqlite3, and is **intentionally** committed to the repo.
Also, there exists no model (because JWT is database free) in the project.

### 4. Starting Application
**OPEN IN ANOTHER TERMINAL TAB.**

```bash
cd application
npm install
npm start
```

NOTE: `yarn` was used while developing this project, you should prefer yarn (if installed).


## Understanding the concept
[JWT (JSON web token)](https://jwt.io/introduction/) is a fairly new authentication type which is based on cryptography.  
Backend support with [Django Rest Framework Simple JWT](https://github.com/davesque/django-rest-framework-simplejwt).  

NOTE: Key files (used by RS256 algorithm) were **intentionally** committed to project's repo, which should never be done in any project or production environment.

## Acknowledgment
Thanks, for giving me this opportunity to create this basic application. I am looking forward to working with your organization.