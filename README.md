[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Flask login template

> Describes a simple entrypoint template to build login functionality for the flask application.
> 
> ⚠️ This application is created for the demo references only.

## Tools

### Production

- python 3.6, 3.7, 3.8
- [sqlalchemy](https://www.sqlalchemy.org/) database
- [flask](https://flask.palletsprojects.com/en/1.1.x/) web framework

### Development

- [black](https://black.readthedocs.io/en/stable/) code formatter


## Quick start
> Please make sure your DB is created (`site_users.db` file should be present, for more details please refer to [database creation](#create-db)).

```
git clone git@github.com:vyahello/flask-login-template.git
pip install -r requirements.txt
flask run
```

Then please open `http://localhost:5000` endpoint in the browser.

## Development notes

### API

This application supports the following API endpoints:
  - `/` or `index.html` - home page of an app
  - `/create_user` - creates a fresh user into database
  - `/login` - logins the user
  - `/logout` - logouts the current user
  - `/dashboard` - shows the dashboard page, accessible only for logged in users

### Create DB

Please follow the next instructions to create DB from the scratch:
```bash
python
Python 3.8.5 (default, Jul 26 2020, 21:03:43)
>>> from login import db
>>> db.create_all()
>>> exit()

ls login/site_users.db
login/site_users.db
```

### Meta

Author – _Volodymyr Yahello_. 

Distributed under the `MIT` license. See [LICENSE](LICENSE.md) for more information.

You can reach out me at:
* [vyahello@gmail.com](vyahello@gmail.com)
* [https://twitter.com/vyahello](https://twitter.com/vyahello)
* [https://www.linkedin.com/in/volodymyr-yahello-821746127](https://www.linkedin.com/in/volodymyr-yahello-821746127)

### Contributing
I would highly appreciate any contribution and support. If you are interested to add your ideas into project please follow next simple steps:

1. Clone the repository
2. Configure `git` for the first time after cloning with your `name` and `email`
3. `pip install -r requirements.txt` to install all project dependencies
4. `pip install -r requirements-dev.txt` to install all development project dependencies
5. Create your feature branch (`git checkout -b feature/fooBar`)
6. Commit your changes (`git commit -am 'Add some fooBar'`)
7. Push to the branch (`git push origin feature/fooBar`)
8. Create a new Pull Request
