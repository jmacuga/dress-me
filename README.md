# DB2 e-commerce shop project

### Setup
1. Fill .env based on .env.example.yml

2. Setup db and web containers:
```
$ docker-compose up -d
```


### Handling migrations:

[Flask-Migrate docs](https://flask-migrate.readthedocs.io/en/latest/)

To generate migration:
```
$ flask db migrate -m "message"
```

To apply the changes described by the migration script to your database:
```
$ flask db upgrade
```