
from typing import TypeVar

from db.models.collision import Collision
from db.models.person import Person
from flask import Flask, Response, jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

CONFIG = {
    "DEBUG": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///db/seattle-save.db",
}

app = Flask(__name__)
app.config.from_mapping(CONFIG)
ENGINE = create_engine("sqlite:///db/seattle-save.db")


# ========= #
#   UTILS   #
# ========= #

SelectStatement = TypeVar(
    "SelectStatement",
    Select[tuple[Collision]],
    Select[tuple[Person]]
)


def results_as_json_for_(stmt: SelectStatement) -> Response:
    with Session(ENGINE) as session:
        results = session.execute(stmt).all()  # [(i1,), (i2,), ...]
        results = [row[0] for row in results]  # [i1, i2, ...]
        return jsonify(results)


# ========== #
#   ROUTES   #
# ========== #

@app.get("/collisions/few")
def get_collisions_few() -> Response:
    return results_as_json_for_(
        select(Collision).limit(10)
    )


@app.get("/collisions/many")
def get_collisions_many() -> Response:
    return results_as_json_for_(
        select(Collision).limit(100)
    )


@app.get("/persons/few")
def get_persons_few() -> Response:
    return results_as_json_for_(
        select(Person).limit(10)
    )


@app.get("/persons/many")
def get_persons_many() -> Response:
    return results_as_json_for_(
        select(Person).limit(100)
    )


if __name__ == "__main__":
    app.run(debug=True)
