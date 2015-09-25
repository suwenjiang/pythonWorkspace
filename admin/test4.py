import threading

def f ():

    print "aaaa"
    print threading.currentThread().name
    print str(threading.activeCount())

for i in range(6):

    t=threading.Thread(target=f,name=str(i))

    t.start()
    t.join()