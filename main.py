import asyncio

from app.main import main

if __name__ == '__main__':
    # HTTP OR GRPC
    asyncio.run(main('HTTP'))
