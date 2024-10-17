import asyncio


async def print_num():
    print("number printing started")
    for i in range(10):
        print(i)
        await asyncio.sleep(1)

    print("number printing ended")


async def print_alpha():
    print("print alphabet started")
    for i in "qwertyuiopasdfghlkjmnzbxvc":
        print(i)
        await asyncio.sleep(1.5)

    print("alphabet printng ended")


# -------------- SCENERIO-1
# in this case print_alpha() will run in background and for print_num() it will wait till
# its execution completed. print_alpha will run concurrently with print_num but main2
# will not wait for the execution of print_alpha, it'll only wait till the execution of print_num
# and once its completed it will print "main completed", regardless of whether print_alpha() has finished or not.
async def main2():
    print("main started")
    asyncio.create_task(print_alpha())
    await print_num()
    print("main completed")


# calling main2 function
asyncio.run(main2())


# -------------- SCENERIO-2
# we always need to use gather funtion to run async function concurrently and
# main1() will wait for both task to complete, irrespective ki first task phle khatm ho
# gya or task2 is still going on.
# and we always need to wrap them in other async function because directly we can not execute it
# as gather is also a async function
async def main1():
    await asyncio.gather(print_alpha(), print_num())


# calling main1 function
asyncio.run(main1())
