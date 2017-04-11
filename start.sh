export LD_LIBRARY_PATH=/home/work/thirdparty/anaconda2/lib:$LD_LIBRARY_PATH
uwsgi -s /tmp/uwsgi_charts.sock -w run:app -M -p 48 -t 30  -R 10000  --pidfile uwsgi.pid -d uwsgi.log
