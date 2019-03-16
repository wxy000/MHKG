#!/bin/bash
# 初始化
LOGS_PATH="/root/MHKG/Django/logs"
YESTERDAY=$(date -d "yesterday" +%Y%m%d)
# 按天切割日志
mv ${LOGS_PATH}/nginx_access.log ${LOGS_PATH}/nginx_access_${YESTERDAY}.log
# 向nginx主进程发送USR1信号，重新打开日志文件，否则会继续往mv后的文件写数据的。原因在于：linux系统中，内核是根据文件描述符来找文件的。如果不这样操作导致日志切割失败。
kill -USR1 `ps axu | grep "nginx: master process" | grep -v grep | awk '{print $2}'`

# 执行python脚本，将刚刚切割的日志文件存入mongo
sleep 5
/usr/bin/python /root/MHKG/Django/toolkit/getNginxLogs.py ${LOGS_PATH}/ nginx_access_${YESTERDAY} .log

echo "" > ${LOGS_PATH}/uwsgi.log

# 删除7天前的日志
cd ${LOGS_PATH}
# find . -mtime +7 -name "*20[1-9][3-9]*" | xargs rm -f
# 或者
find . -mtime +7 -name "nginx_access_*" | xargs rm -f

exit 0
