
import json
from dataclasses import asdict
from pathlib import Path
from typing import Tuple

from db.models.collision import Collision
from db.models.intersection import Intersection
from db.models.person import Person
from sqlalchemy import (Engine, Inspector, Label, Row, Select, Table,
                        create_engine, desc, func, inspect, select)
from sqlalchemy.orm import Session
from tqdm import tqdm

# Typing for intermediate intersection information.
IntersectionInfo = Tuple[str, float, float, int, int, int, int]

DATABASE_ROOT = Path("db")
DATABASE_FILE = DATABASE_ROOT / Path("seattle.db")
DATABASE_CACHE = DATABASE_ROOT / Path("cache")


def main() -> None:
    LoadIntersectionCmd().exec()


class LoadIntersectionCmd():
    engine: Engine | None

    def __init__(self) -> None:
        pass

    def exec(self) -> None:
        self.connect_to_db()
        self.verify_db_state()
        self.create_table()
        self.load_table()
        self.do_simple_query()

    def connect_to_db(self) -> None:
        # Create engine / connection to db.
        assert DATABASE_ROOT.exists(), f"{DATABASE_ROOT}/ does not exist!"
        assert DATABASE_FILE.exists(), f"{DATABASE_FILE} does not exist!"
        self.engine = create_engine(f"sqlite:///{DATABASE_FILE}")
        print("connected to db.")

    def verify_db_state(self) -> None:
        insp = inspect(self.engine)
        assert isinstance(insp, Inspector)  # (For typing).
        tables = insp.get_table_names()

        def _assert_table(table: str, *, exists: bool) -> None:
            assert (table in tables) == exists, f"expected that {table} table {exists=}!"

        # Check expected existence of important tables.
        _assert_table(Collision.__tablename__, exists=True)
        _assert_table(Person.__tablename__, exists=True)
        print(f"verified db state. {tables=}")

    def create_table(self) -> None:
        assert self.engine is not None
        assert isinstance(Intersection.__table__, Table)
        Intersection.__table__.drop(bind=self.engine, checkfirst=True)
        Intersection.__table__.create(bind=self.engine, checkfirst=False)
        print("created intersection table. (any existing one dropped)")

    def load_table(self) -> None:
        assert self.engine is not None

        # Collision metrics that we are aggregating for each intersection.
        total_injuries = func.sum(Collision.INJURIES).label('TOTAL_INJURIES')
        total_serious_injuries = func.sum(Collision.SERIOUSINJURIES).label('TOTAL_SERIOUSINJURIES')
        total_fatalities = func.sum(Collision.FATALITIES).label('TOTAL_FATALITIES')
        total_collisions: Label[int] = func.sum(1).label('TOTAL_COLLISIONS')

        # Each intersection is a unique LOCATION-x-y triple.
        # Ideally, all intersection names (i.e. LOCATION) would be unique, but
        # there are a couple occurrences of the same pair of streets crossing
        # each other twice, giving the "same" intersection at two locations.
        stmt = (
            select(
                Collision.LOCATION,
                Collision.x,
                Collision.y,
                total_injuries,
                total_serious_injuries,
                total_fatalities,
                total_collisions)
            .where(Collision.LOCATION.is_not(None))
            .where(Collision.x.is_not(None))
            .where(Collision.y.is_not(None))
            .group_by(Collision.LOCATION, Collision.x, Collision.y)
            .order_by(desc(total_fatalities))
        )

        # Do the query once to get the total count so that when we actually
        # process the results below, we can have a cool loading bar.
        total = self._count_results(stmt)

        print("loading table...")
        with Session(self.engine) as session:
            result = session.execute(stmt)

            with tqdm(total=total) as progress:
                while (batch := result.fetchmany(1000)):
                    intersections = [self._intersection_from_row(row) for row in batch]
                    session.add_all(intersections)
                    session.commit()
                    progress.update(len(intersections))

        print("======= done! ======= \n")

    def _count_results(self, query: Select[IntersectionInfo]) -> int:
        stmt = select(func.count()).select_from(query.subquery())
        with Session(self.engine) as session:
            return session.execute(stmt).fetchone()[0]  # type: ignore

    def _intersection_from_row(
            self, row: Row[IntersectionInfo]) -> Intersection:
        fields = Intersection.__annotations__.keys()  # PEP 557 says ordering is guaranteed.
        kwargs = {k: v for k, v in zip(fields, row)}  # Assumes `row` has the values in same order.
        return Intersection(**kwargs)

    def do_simple_query(self) -> None:
        stmt = select(Intersection).order_by(desc(Intersection.COLLISIONS))
        with Session(self.engine) as session:
            intersection: Intersection = session.execute(stmt).fetchone()[0]  # type: ignore
            print("simple query result (intersection w/ most collisions):")
            print(json.dumps(asdict(intersection), indent=2))


if __name__ == "__main__":
    main()
