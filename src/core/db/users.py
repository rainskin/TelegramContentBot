from datetime import datetime

import config
import loader


class Users:

    def __init__(self):
        self.db = loader.db
        self.collection = self.db['users']

    async def add_user(self, name, username, user_id):
        doc = {
            'name': name,
            'username': username,
            'id': user_id,
            'registration_date': datetime.now(),
            'is_active': True,
        }

        await self.collection.insert_one(doc)

    async def is_new(self, user_id):
        doc = await self.collection.find_one({'id': user_id})
        return not bool(doc)

    async def get_sale_group_id(self, user_id):
        doc = await self.collection.find_one({'id': user_id})
        return doc.get('sale_group_id') if doc else None

