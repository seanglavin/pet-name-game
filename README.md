Access PostgreSQL shell:
    psql -U sean -d petnamegamedb


Exit shell:
    \q
s

Commands container from the terminal:
    docker exec -it pet-name-game_fastapi_1 [alembic revision --autogenerate -m "init"]