# company-api

## Requirements

Mysql Client 3.5

Python 3.6 or 2.7

## Install dependencies and build

### Running in ubuntu

1. Install packages

    ```
        sudo apt-get -y install python-virtualenv mysql-server mysql-client python3 python3-dev python3-pip python-mysqldb libmysqlclient-dev
    ```

2. Create virtualenv
    ```
        virtualenv --python=/usr/bin/python3 env
        source /home/ubuntu/env/bin/activate
        deactivate
    ```

3. Install all dependencies:
    ```
        pip3 install -r requirements.txt
    ```

4. Init config & database
    ```
        cp src/core/sample.config.env src/config.env
        cd src
        python3 manage.py migrate
    ```

5. Get Google Calendar API credentials
    ```
        https://developers.google.com/calendar/quickstart/go
    ```
6. Build frontend

   Copy *src/frontend/sample.env* to *src/frontend/.env*, and change the config if you want. By default, we don't need
   to change.

   Build the frontend (call these command from the *src/frontend* folder):

   Install dependencies
    ```
    npm install
    ```

   Build for release
    ```
    npm run build
    ```

   Or build for debug
    ```
    npm run watch
    ```

   Collect static files (only need for `production`):
    ```
    python manage.py collectstatic --settings=core.settings.production
    ```

7. Start Server Its recommended running the `development` mode only on your local PC. If you would like to run
   the `production` mode, you should use docker / use proxy server to host static resource / or add `--insecure`
   parameter to force serving of static files with the staticfiles app (More
   detail [here](https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/)).
    ```
        cd src
        python3 manage.py runserver --settings=core.settings.development
    ```

8. For Mac: run before pip install
    ```
        export CFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -I/usr/local/include/ ${CFLAGS}"
        export LDFLAGS="-isysroot $(xcrun --show-sdk-path) -L/usr/local/lib -L/usr/lib"
        export CPPFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -L/usr/lib"
    ```

### Running in windows

1. Install environment and activate :
   ```
      python -m venv venv
      venv\Scripts\activate
   ```

2. Install requirement libraries :

- First you have to comment libraries uWSGI (this only run in Ubuntu)
   ```
      pip install -r requirements.txt
   ```

3. Follow from step 3 to the end in Running with Ubuntu

## Using docker

If you would like to use docker, you can skip the `Install dependencies and build` section. Just follow these steps:

1. Copy and rename these files. Then change the values for `__ERP_PORT__`, `__DJANGO_SETTINGS_MODULE__`, and other environment variables (if needed).
    * `ci/Dockerfile.template` -> `./Dockerfile`
    * `docker-compose.yml.template` -> `./docker-compose.yml`
    * `ci/docker.env.template` -> `./docker.env`
2. From the root folder (where the docker-compose.yml located), run the command:
    ```
    docker-compose up -d --build
    ```

## Adding libraries

1. Adding python libraries:

   If your need add more libraries while developing new feature. Make sure to follow these steps:

   a. First, install the library:
    ```
    pip install <library name>
    ```

   b. Use the library as you want

   c. List the libraries to the requirements.txt
    ```
    pip freeze > requirements.txt
    ```

   d. Commit the requirements.txt within your other codes

2. Adding JavaScript libraries:
   If your need add more JavaScript libraries for frontend. Make sure to follow these steps:

   a. First, install the library (from `src/frontend` folder):
    ```
    npm install <library name>
    ```

   b. Use the library as you want

   d. Commit these files within other changes to gitlab:
    * src/frontend/package.json
    * src/frontend/package-lock.json

### Reset database, run file:
   src/resetBD.sh

### Set up precommit:
   ```
   pre-commit install
   pre-commit install --hook-type commit-msg
   # install latest npm version by using nvm https://github.com/nvm-sh/nvm (Recommended)
   npm install --save-dev @commitlint/{cli,config-conventional}
   ```

### Create api key
   ```
   python3 manage.py create_api_key {name} {scope} {application_id}
   ```
