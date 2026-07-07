from app.infrastructure.persistence.session import SessionLocal

from app.infrastructure.persistence.seeders.role_seeder import seed_roles
from app.infrastructure.persistence.seeders.user_seeder import seed_users

db = SessionLocal()

try:
    seed_roles(db)
    seed_users(db)

finally:
    db.close()