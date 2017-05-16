import threading
import time


def timerFun(title, msg):
    print(title)
    print(msg)


def main():
    title = "ttttt"
    msg = "mmmmm"
    timer = threading.Timer(0.1, timerFun, (title, msg))
    timer.start()
    while True:
        time.sleep(100)

    print("main thread end")


if __name__ == '__main__':
    main()
