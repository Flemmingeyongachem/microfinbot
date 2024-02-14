from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "department" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(400) NOT NULL UNIQUE,
    "account_number" BIGINT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "name" VARCHAR(50),
    "family_name" VARCHAR(50),
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "telegram_number" VARCHAR(50) NOT NULL,
    "is_student" BOOL NOT NULL  DEFAULT False,
    "is_staff" BOOL NOT NULL  DEFAULT False,
    "is_business_user" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "exchangeaddress" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "address" VARCHAR(255) NOT NULL UNIQUE,
    "user_id" BIGINT NOT NULL UNIQUE REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "microfinanceaccount" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "account_number" VARCHAR(255) NOT NULL UNIQUE,
    "is_student_account" BOOL NOT NULL  DEFAULT False,
    "is_business_account" BOOL NOT NULL  DEFAULT False,
    "balanace" DECIMAL(15,2) NOT NULL,
    "owner_id" BIGINT NOT NULL UNIQUE REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tagbook" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "owner_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "transaction" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "to_address_id" BIGINT NOT NULL REFERENCES "exchangeaddress" ("id") ON DELETE CASCADE,
    "from_address_id" BIGINT NOT NULL UNIQUE REFERENCES "exchangeaddress" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "tagbook_exchangeaddress" (
    "tagbook_id" BIGINT NOT NULL REFERENCES "tagbook" ("id") ON DELETE CASCADE,
    "exchangeaddress_id" BIGINT NOT NULL REFERENCES "exchangeaddress" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
