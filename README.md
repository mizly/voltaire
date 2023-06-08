# Voltaire

Voltaire is an open-source web app designed with French Immersion teachers in mind.
It offers an intuitive set of tools to assess and record students' progress in learning the grammar of the language.
Students can use Voltaire as a simple progress tracker, while teachers can use Voltaire to sort out the chaos in managing several of their classes.

## Development

Voltaire was written in Python using the Flask web framework.
The Google OAuth API was used to incorporate login via Google account.
MongoDB was used to host the database for client information.
Development was done in VS Code and Atom.

## Downloading the Code

To run Voltaire, you'll need to create a [virtual environment or venv](https://docs.python.org/3/library/venv.html).

From your terminal of choice, activate the venv

(Windows) `root\venv\scripts\activate`

And use pip to download the corresponding packages from the `requirements.txt` file

(Windows) `pip install -r requirements.txt`

Additionally, you'll need two .json files with the following keys:

`client_secret.json`
```
{
    "web": {
        "client_id": {},
        "project_id": {},
        "auth_uri": {},
        "token_uri": {},
        "auth_provider_x509_cert_url": {},
        "client_secret": {},
        "redirect_uris": {},
        "javascript_origins": {}
    }
}
```

`database.json`
```
{
    "connection": "{MongoDB server connection key}",
    "teachers": [{List of emails that should be recognized as teachers}]
}
```