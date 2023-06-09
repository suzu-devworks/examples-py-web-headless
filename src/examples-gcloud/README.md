# examples-gcloud

Google Cloud API programming examples.

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

## References

- https://developers.google.com/drive/api/guides/about-sdk?hl=ja
- https://developers.google.com/sheets/api/guides/concepts?hl=ja
- https://googleapis.dev/python/google-auth/latest/index.html
- https://docs.gspread.org/en/latest/index.html

## Setup

Clone the repository:

```shell
clone https://github.com/suzu-devworks/examples-py-web-headless.git

cd examples-py-web-headless

```

Create a virtualenv in advance:

```shell
python -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
pip install pdm

```

Here's how this project is setup:

```shell
cd src/examples-gcloud

# select interpreter
pdm use

# install dependencies and self.
pdm install

```

## Configure Google Clound API

Goto google cloud platforms site:

- https://console.cloud.google.com/welcome

### Enable APIs

1. APIs & Services > Library
2. Enable [Google Drive API] and [Google Sheets API]

### When use service acount (silent login).

1. IAM and Admin > Service Accounts > CREATE SERVCIE ACCOUNT
   > - Service account details:  
   >   Input service account id.
   > - Grant this service account access to project:  
   >   Select Editor role.
   > - DONE
2. select created servcie account
3. service account > KEYS > ADD KEY(Create new key)
   > - type(JSON) > Create
4. json file will be downloaded automatically.
5. Rename the file to `service_account.json` and add it to your project
6. _Grant permissions for Google services to service accounts_

### When use user account (oauth login).

1. APIs & Services > OAuth consent screen
   > - User type: External > create
   > - OAuth consent screen:
   >   - App name: any name
   >   - User support email: your email
   >   - Email addresses: your email
   > - Test user:
   >   - ADD USERS: your email.
2. Credentials > CREATE CREDENTIALS > OAuth client ID
   > - Select Application Type: Desktop app
   > - CREATE
3. Download json file.
4. Rename the file to `client_secret.json` and add it to your project

## Create project

This project was generated with the command:

```shell
mkdir -p src/examples-gcloud
cd src/examples-gcloud

# create new pyproject.toml
pdm init
pdm add -d flake8 mypy black isort pytest-cov pyclean

pdm add gspread google-api-python-client google-auth google-auth-oauthlib

```
