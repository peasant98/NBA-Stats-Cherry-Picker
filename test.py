# just some fun practice with multiprocessing
from multiprocessing import Process, Manager

def f(d, d1, l):
    player1_dict = {1: 'hi'}
    player2_dict = {2: 'hi'}
    d.update(player1_dict)
    d.update(player2_dict)

if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    d1 = manager.dict()
    lock = manager.Lock()
    l = manager.list(range(10))

    p = Process(target=f, args=(d, d1, lock))
    p.start()
    p.join()

    print(d)
    print(d1)