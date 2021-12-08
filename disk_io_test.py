import os
import asyncio
import aiofiles


def _create_large_file(file):
    print(f'Creating a large file @ {file}...')
    contents = '\n'.join([f'this is line number {i}' for i in range(10000000)])
    with open(file, 'w') as fp:
        fp.write(contents)
    
    print(f'Wrote {file}!')


async def read_file_async(file):
    print(f'Starting to read {file}...')
    
    async with aiofiles.open(file) as fp:
        contents = await fp.read()
    
    print(f'Finished reading {file}!')
    return contents

async def arbitrary_async_process():
    while True:
        print('If I show up between "Starting to read ..." and "Finished reading"..., disk-IO can and should be awaited.')
        await asyncio.sleep(.1)


async def main():
    file = 'a_big_log.log'
    _create_large_file(file)

    read_task = asyncio.create_task(read_file_async(file))
    other_task = asyncio.create_task(arbitrary_async_process())

    await read_task

    print(f'Removing {file}...')
    os.remove(file)


if __name__ == '__main__':
    asyncio.run(main())
   
