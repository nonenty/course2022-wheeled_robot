import threading

if __name__ == "__main__":
    global vel
    t=threading.Thread(target=receive)
    t.start()
    while True:
