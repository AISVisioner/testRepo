import asyncio

# default function <- returns a value
def main():
    print("Hello, World!")
main()

# async function <- returns a coroutine object
async def main():
    print("Hello, World!")
# asyncio.run() creates an event loop to start the async function
asyncio.run(main())

async def foo(text):
    print(text)
    # unlike time.sleep(), asyncio.sleep() creates an coroutine object
    # it needs to be awaited for the execution
    # await can be used inside the async function
    await asyncio.sleep(1)