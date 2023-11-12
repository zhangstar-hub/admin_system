#!/bin/bash

if [ -d env ]; then
    source env/bin/activate
else
    echo "需要环境python env"
fi

if [ -f tmp/gunicorn.pid ]; then
    pid=$(cat tmp/gunicorn.pid)
else
    pid=-1
fi
progress_name="gunicorn_backend"
pids=$(pgrep -f $progress_name)

START_CMD="gunicorn -n $progress_name -c config/gunicorn_config.py backend.wsgi:application"
RESTART_CMD="kill -HUP $pid"
STOP_CMD="kill $pid"

start() {
  if [ "$pids" ]; then
      echo "进程已经启动了"
      exit 0
  fi
  $START_CMD
}

stop() {
  $STOP_CMD
}

restart() {
  if [ ! "$pids" ]; then
      $START_CMD
  else
      $RESTART_CMD
  fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac

exit 0
