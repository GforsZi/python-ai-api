from sqlalchemy import select
from app.core.seeder import BaseSeeder, register_seeder
from app.modules.roles.models import Role


@register_seeder
class RoleSeeder(BaseSeeder):
    order = 10

    async def run(self) -> None:
        default_roles = [
            {"name": "admin", "description": "Full access to all resources", "is_admin": True},
            {"name": "moderator", "description": "Can manage content and users", "is_admin": False},
            {"name": "user", "description": "Standard access for regular users", "is_admin": False},
        ]

        for role_data in default_roles:
            result = await self.session.execute(
                select(Role).where(Role.name == role_data["name"])
            )
            existing = result.scalar_one_or_none()

            if not existing:
                self.session.add(Role(**role_data))
                await self.log(f"Role '{role_data['name']}' created.")
            else:
                await self.log(f"Role '{role_data['name']}' already exists, skipped.")

        await self.session.commit()
