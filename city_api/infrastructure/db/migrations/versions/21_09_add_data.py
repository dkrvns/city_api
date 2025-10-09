"""fill regions, districts, cities

Revision ID: xxxxxxxxxxxx
Revises: <previous_revision_id>  # ← замени на ID последней миграции (например, создания таблиц)
Create Date: 2025-04-05 12:00:00

"""
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = "f53038e97d0c"
down_revision = "f1d038e97d0c"
branch_labels = None
depends_on = None


def generate_uuid():
    return str(uuid4())


def upgrade() -> None:
    regions = []
    districts = []
    cities = []

    region_names = [
        ("California", "Sacramento"),
        ("Texas", "Austin"),
        ("New York", "Albany"),
    ]

    district_suffixes = ["North", "South", "East", "West", "Central", "Metro"]

    city_templates = [
        ("village", 500),
        ("town", 15000),
        ("city", 500000),
    ]

    for i, (region_name, capital) in enumerate(region_names):
        region_id = generate_uuid()
        regions.append({
            "id": region_id,
            "name": region_name,
            "capital": capital,
            "is_deleted": False
        })

        for j in range(2):
            district_id = generate_uuid()
            district_name = f"{region_name} {district_suffixes.pop(0)}"
            districts.append({
                "id": district_id,
                "region_id": region_id,
                "name": district_name,
                "is_deleted": False
            })

            for k, (obj_type, population) in enumerate(city_templates):
                city_id = generate_uuid()
                city_name = f"{district_name} {obj_type.title()}"
                cities.append({
                    "id": city_id,
                    "district_id": district_id,
                    "name": city_name,
                    "obj_type": obj_type,
                    "population": population,
                    "is_deleted": False
                })

    op.bulk_insert(
        sa.table(
            "region",
            sa.column("id", sa.Uuid),
            sa.column("name", sa.String),
            sa.column("capital", sa.String),
            sa.column("is_deleted", sa.Boolean),
        ),
        regions
    )

    op.bulk_insert(
        sa.table(
            "district",
            sa.column("id", sa.Uuid),
            sa.column("region_id", sa.Uuid),
            sa.column("name", sa.String),
            sa.column("is_deleted", sa.Boolean),
        ),
        districts
    )

    op.bulk_insert(
        sa.table(
            "city",
            sa.column("id", sa.Uuid),
            sa.column("district_id", sa.Uuid),
            sa.column("name", sa.String),
            sa.column("obj_type", sa.String),
            sa.column("population", sa.Integer),
            sa.column("is_deleted", sa.Boolean),
        ),
        cities
    )


def downgrade() -> None:
    op.execute("DELETE FROM city WHERE is_deleted = false")
    op.execute("DELETE FROM district WHERE is_deleted = false")
    op.execute("DELETE FROM region WHERE is_deleted = false")