import aiofiles

async def read_file(path):
    async with aiofiles.open(path , mode='rb') as f:
        contents = await f.read()
    return contents
