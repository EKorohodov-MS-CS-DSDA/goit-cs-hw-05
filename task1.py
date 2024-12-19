import asyncio
import argparse
from aiopath import AsyncPath
from aioshutil import copyfile
import logging

FORMAT = "%(threadName)s %(asctime)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt="%H:%M:%S")

async def copy_file(source: AsyncPath, destination: AsyncPath) -> None:
    try:
        await destination.mkdir(parents=True, exist_ok=True)

        destination_file = destination / source.name
        await copyfile(source, destination_file)
        logging.debug(f"Copied {source.name} to {destination_file}")
    except Exception as e:
        logging.error(e)

async def read_folder(source: AsyncPath, destination: AsyncPath) -> None:
    await destination.mkdir(parents=True, exist_ok=True)

    read_ops = []
    async for child in source.iterdir():
        if await child.is_file():
            destination_path = destination / child.suffix[1:]
            read_ops.append(copy_file(child, destination_path))
        elif await child.is_dir():
            read_ops.append(read_folder(child, destination))

    await asyncio.gather(*read_ops)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy files from source to destination")
    parser.add_argument("source", type=str)
    parser.add_argument("destination", type=str)

    args = parser.parse_args()
    asyncio.run(read_folder(AsyncPath(args.source), AsyncPath(args.destination)))
    # asyncio.run(read_folder(AsyncPath("data"), AsyncPath("dest")))
