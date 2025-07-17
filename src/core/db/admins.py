import loader


class Admins:

    def __init__(self):
        self.collection = loader.admins

    async def is_admin(self, tg_id: int):
        return await self.collection.find_one({'id': tg_id})

    async def is_superadmin(self, tg_id: int) -> bool:
        admin = await self.collection.find_one({'id': tg_id})

        if admin:
            return admin.get('main admin')
        return False
