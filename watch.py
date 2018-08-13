import sys
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from Common.Console import console
import subprocess


def restart_celery_workers():
    """重启celery的worker
    """
    return subprocess.run(
        ['celery', 'control', 'pool_restart'],  stdout=subprocess.PIPE).stdout


def runAutorun():
    """重新运行 run.py

    重新运行 run.py

    Returns:
        string -- 运行结果
    """
    p = subprocess.Popen(
        ['python', '/Users/kaldr/Project/Gamble/run.py'],  stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
    while subprocess.Popen.poll(p) == None:
        # while True:
        r = p.stdout.readline().strip().decode("utf-8")
        if r:
            console.log(r)
    error = p.stderr.read().strip().decode('utf-8')
    if not error == None:
        es = str(error).split('\n')
        for e in es:
            if e:
                console.error(e)
    console.success("[ 运行完成 ]")


class AutoRunHandler(PatternMatchingEventHandler):

    def __init__(self, patterns, ignore_patterns):
        super(AutoRunHandler, self).__init__(
            patterns=patterns, ignore_patterns=ignore_patterns)

    def on_any_event(self, event):
        if ".git" not in event.src_path and "__pycache__" not in event.src_path and ".pyc" not in event.src_path:

            if "TaskQueue" in event.src_path and '.py' in event.src_path:
                console.warn('[ Celery workers restarting... ]')
                result = restart_celery_workers()
                console.success('[ Celery workers restarted ]')

            elif '.py' in event.src_path:
                console.success("[ 程序已重启 ]")
                console.end("[ " + event.src_path.replace("./", "") + " ] " +
                            event.event_type)
                runAutorun()


if __name__ == "__main__":
    console.success("[ 程序已自动监控 ]")
    console.warn("每当保存代码时，根目录下的 run.py 会自动运行。")
    runAutorun()
    # console.log(result)
    path = './'
    event_handler = AutoRunHandler(
        patterns="*.py", ignore_patterns="git/")
    observer = Observer()

    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
