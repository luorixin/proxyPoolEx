from proxypool.scheduler import Scheduler
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    try:
        s = Scheduler()
        s.run()
    except Exception as e:
        print("调度发送错误,重启中", e.args)
        main()

if __name__ == '__main__':
    main()
