from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "bussiness" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(400) NOT NULL UNIQUE,
    "description" TEXT,
    "business_address_id" BIGINT REFERENCES "exchangeaddress" ("id") ON DELETE CASCADE
);
        ALTER TABLE "user" ADD "chat_id" BIGINT NOT NULL UNIQUE;
        CREATE UNIQUE INDEX "uid_user_chat_id_2fc9b8" ON "user" ("chat_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_user_chat_id_2fc9b8";
        ALTER TABLE "user" DROP COLUMN "chat_id";
        DROP TABLE IF EXISTS "bussiness";"""
