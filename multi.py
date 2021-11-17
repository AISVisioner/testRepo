# import multiprocessing
from concurrent import futures
import concurrent
import time

def do_something(duration=1):
    print(f'Just {duration} sec...')
    time.sleep(duration)
    return f'...I\'m here after {duration} sec!'

if __name__ == '__main__':
    start = time.perf_counter()

    with futures.ProcessPoolExecutor() as executor:
        seconds = list(range(5,0,-1))
        # results = [executor.submit(do_something, duration) for duration in seconds]
        
        # for f in futures.as_completed(results):
        #     print(f.result())

        results = executor.map(do_something, seconds)
        for result in results:
            print(result)

    # processes = []
    # for _ in range(1):
    #     p = multiprocessing.Process(target=do_something, args=[1.5])
    #     p.start()
    #     processes.append(p)
    # for process in processes:
    #     process.join()

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} sec.')