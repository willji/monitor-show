#/bin/bash
a=(" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" ")
SCRIPT_HOME="."

print_help()
{
    echo
    echo "  scope     command      script"
    echo "-------    ---------    --------"
    echo "[<scope>]  status                      - Get managed scripts status"
    echo "[<scope>]  start     [<script_name>]   - Start script"
    echo "[<scope>]  stop      [<script_name>]   - Stop script"
    echo "[<scope>]  restart   [<script_name>]   - restart script"
    echo "[<scope>]  startall                    - Start all scripts"
    echo "[<scope>]  stopall                     - Stop all scripts"
    echo "[<scope>]  restartall                  - restart all scripts"
    echo
}

print_status()
{
    echo
    echo "------------------------------+------------+-----------"
    echo "script                        |  status    |   pid     "
    echo "------------------------------+------------+-----------"
    for i in `ls -l $SCRIPT_HOME | grep -e "\.pl" -e "\.py" | awk '{ print $NF }'`
        do
            str=`echo $i | awk '{print length($1)}'`
            ps aux | grep $i | grep -v "grep" &>/dev/null
            ret=$?
            if [ $ret -eq 0 ];then
                echo "$i${a:$str}|  Alive     |   `ps -ef | grep $i | grep -v grep | awk '{ print $2 }'`"
            else
                echo "$i${a:$str}|  Down      |   N/A   "
            fi
        done
}

start_app()
{
    local num=0
    for i in `ls -l $SCRIPT_HOME | grep -e "\.pl" -e "\.py" | awk '{ print $NF }'`
    do
    if [ $1 == $i ];then
        num=$((${num}+1))
    fi
    done
    if [ $num -eq 0 ];then
        echo "your script name is error"
        exit 1
    fi
    ps aux | grep -w ${1} | grep -vw "grep" | grep -vw "sh" | grep -vw "bash" &>/dev/null
    ret=$?
    if [ $ret -eq 0 ];then
        echo "${1} is already start"
    else
        if [ "$1" == "splunk_monitor_cps_bgw_prod.pl" ];then
            nohup perl $1 &>/dev/null &
            ret_start=$?
            if [ ${ret_start} -eq 0 ];then
                echo "${1} is start"
            else
                echo "${1} is not start"
            fi
        elif [ "$1" == "splunk_monitor_cps_prod.pl" ];then
            nohup perl $1 &>/dev/null &
            ret_start=$?
            if [ ${ret_start} -eq 0 ];then
                echo "${1} is start"
            else
                echo "${1} is not start"
            fi
        elif [ "$1" == "splunk_monitor_cps_sla_prod.pl" ];then
            nohup perl $1 &>/dev/null &
            ret_start=$?
            if [ ${ret_start} -eq 0 ];then
                echo "${1} is start"
            else
                echo "${1} is not start"
            fi
       elif [ "$1" == "yw_db.py" ];then
            nohup python $1 &>/dev/null &
            ret_start=$?
            if [ ${ret_start} -eq 0 ];then
                echo "${1} is start"
            else
                echo "${1} is not start"
            fi
       elif [ "$1" == "mysql.py" ];then
            nohup python $1 &>/dev/null &
            ret_start=$?
            if [ ${ret_start} -eq 0 ];then
                echo "${1} is start"
            else
                echo "${1} is not start"
            fi
        else
            echo "your script name is error"
        fi
    fi
}

stop_app()
{
    local num=0
    for i in `ls -l $SCRIPT_HOME | grep -e "\.pl" -e "\.py" | awk '{ print $NF }'`
    do
    if [ $1 == $i ];then
        num=$((${num}+1))
    fi
    done
    if [ $num -eq 0 ];then
        echo "your script name is error"
        exit 1
    fi
    ps aux | grep -w ${1} | grep -vw "grep" | grep -vw "sh" | grep -vw "bash" &>/dev/null
    ret=$?
    if [ $ret -eq 0 ];then
        if [ "$1" == "splunk_monitor_cps_bgw_prod.pl" ];then
            kill `ps -ef | grep ${1} | grep -vw "grep" | grep -vw "sh" | grep -vw "bash" | awk '{ print $2 }'`
            ret_kill=$?
            if [ ${ret_kill} -eq 0 ];then
                echo "${1} is stop"
            else
                echo "${1} is not stop"
            fi
        elif [ "$1" == "splunk_monitor_cps_prod.pl" ];then
            kill `ps -ef | grep ${1} | grep -vw "grep" | grep -vw "sh" | grep -vw "bash" | awk '{ print $2 }'`
            ret_kill=$?
            if [ ${ret_kill} -eq 0 ];then
                echo "${1} is stop"
            else
                echo "${1} is not stop"
            fi
        elif [ "$1" == "splunk_monitor_cps_sla_prod.pl" ];then
            kill `ps -ef | grep ${1} | grep -vw "grep" | grep -vw "sh" | grep -vw "bash" | awk '{ print $2 }'`
            ret_kill=$?
            if [ ${ret_kill} -eq 0 ];then
                echo "${1} is stop"
            else
                echo "${1} is not stop"
            fi
        elif [ "$1" == "mysql.py" ];then
            kill `ps -ef | grep ${1} | grep -vw "grep" | grep -vw "sh" | grep -vw "bash" | awk '{ print $2 }'`
            ret_kill=$?
            if [ ${ret_kill} -eq 0 ];then
                echo "${1} is stop"
            else
                echo "${1} is not stop"
            fi
        elif [ "$1" == "yw_db.py" ];then
            kill `ps -ef | grep ${1} | grep -vw "grep" | grep -vw "sh" | grep -vw "bash" | awk '{ print $2 }'`
            ret_kill=$?
            if [ ${ret_kill} -eq 0 ];then
                echo "${1} is stop"
            else
                echo "${1} is not stop"
            fi
        else
            echo "your script name is error"
        fi
    else
        echo "${1} is already stop"
    fi
}

start_all()
{
    local num=0
    for i in `ls -l $SCRIPT_HOME | grep -e "\.pl" -e "\.py" | awk '{ print $NF }'`
        do
            if [ ${num} -eq 0 ];then
                start_app $i
                num=$((${num}+1))
            elif [ ${num} -eq 1 ];then
                sleep 10
                start_app $i
            fi
        done
}

stop_all()
{
    for i in `ls -l $SCRIPT_HOME | grep -e "\.pl" -e "\.py" | awk '{ print $NF }'`
        do
            stop_app $i
        done
}

if [ $# -eq 0 ];then
    echo "Usage: $0  --help"
fi

if [ $# -eq 1 ];then
    case "$1" in
    status)
    print_status
    ;;
    --help)
    print_help
    ;;
    startall)
    start_all
    ;;
    stopall)
    stop_all
    ;;
    restartall)
    stop_all
    sleep 3
    start_all
    ;;
    start)
    echo "Usage: $0 $1 {[<script_name>]}"
    ;;
    stop)
    echo "Usage: $0 $1 {[<script_name>]}"
    ;;
    restart)
    echo "Usage: $0 $1 {[<script_name>]}"
    ;;
    *)
    echo "Usage: $0  --help"
    exit
    esac
fi

if [ $# -eq 2 ];then
    case "$1" in
    start)
    start_app $2
    ;;
    stop)
    stop_app $2
    ;;
    restart)
    stop_app $2
    sleep 3
    start_app $2
    ;;
    *)
    echo "Usage: $0  --help"
    exit
    esac
fi

if [ $# -gt 2 ];then
    echo "Usage: $0  --help"
    exit
fi
