# backend-practice

A project made to practice Postgres SQL, FastAPI and Docker.

A full-stack website that allow user to sign up, login and edit their data like password/birthday.

## .env

- POSTGRES_PASSWORD: password for postgres SQL container
- PGADMIN_DEFAULT_EMAIL: default email for pgadmin container
- PGADMIN_DEFAULT_PASSWORD: default password for pgadmin container
- DATABASE_URL:url for alembic (postgresql://<username>:<password>@<server:port>/<db_name>)
- POSTGRES_USER: user of postgre
- JWT_SECRET: jwt secret for backend

## How to use

1. fill in .env
2. `poetry install`
3. `docker-compose up -d` for postgresql and pgadmin
4. `poetry run uvicorn main:app --reload` for backend
5. `cd ./frontend` and `npm run dev` for frontend
6. open `localhost:5173 to open frontend`

## Details

- Use docker to set up PostgreSQL and PgAdmin
- Use React and Vite for frontend
- Use FastAPI and PostgreSQL for backend
- Use Alembic for database migration
- Use poetry for package management