from prisma import Prisma

_prisma = Prisma()


async def get_prisma_client() -> Prisma:
    if not _prisma.is_connected():
        await _prisma.connect()
    return _prisma
