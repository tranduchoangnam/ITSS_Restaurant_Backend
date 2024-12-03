### Install dependencies
```bash
poetry install
```
### Run app
```bash
poetry run uvicorn backend.main:app --reload
```
### Migrate model to Postgresql.

- In root folder, run command:

  ```bash
    alembic upgrade heads
  ```

- To migrate new content in model to database

  + Migrating the newly changed content in the model into the database:

    ```bash
      alembic revision --autogenerate -m "Comment for change"
    ```

  + Update to the newest version

    ```bash
      alembic upgrade heads
    ```


