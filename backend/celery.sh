#!/bin/bash

if [ -d env ]; then
    source env/bin/activate
else
    echo "需要环境python env"
fi

appname="celery_task:app"
logfile="logs/celery.log"
pidfile="tmp/celery.pid"
beat_file="tmp/celery-beat-schedule"
worker_num=4
celery_name="celery_w1"

# Celery启动命令
START_CMD="celery multi start $celery_name -A $appname -c $worker_num -s $beat_file -B -E -l info --logfile=$logfile --pidfile=$pidfile"
RESTART_CMD="celery multi restart $celery_name -A $appname -c $worker_num -s $beat_file -B -E -l info --logfile=$logfile --pidfile=$pidfile"
STOP_CMD="celery multi stop $celery_name -A $appname --pidfile=$pidfile"

pids=$(pgrep -f $celery_name)

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
  $RESTART_CMD
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
