from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "family_name";
        ALTER TABLE "user" DROP COLUMN "name";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "family_name" VARCHAR(50);
        ALTER TABLE "user" ADD "name" VARCHAR(50);"""
