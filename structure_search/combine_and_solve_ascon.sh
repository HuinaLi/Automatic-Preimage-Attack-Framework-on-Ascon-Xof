#!/bin/bash
set -e

ShowUsage() {
    echo "Usage: "
    echo ""
    echo "bash $0 ROUNDS A D n0 B alg_BASE file A_path DQ_path n0_path B_path solutions_count"
    echo ""
  }

if [ "${11}" = "" ] || [ "$1" = "--help" ] || [ "$1" = "help" ]; then
    ShowUsage $0
    exit 1
fi

## Q= 0 in our para settings
ROUNDS=$1
A=$2
D=$3
n0=$4
B=$5
alg_BASE=$6
file=$7
A_path=$8
DQ_path=$9
n0_path=${10}
B_path=${11}
solutions_count=${12}

BASE=`cd $(dirname "$0");pwd`
echo "bash $0 ${ROUNDS} ${A} ${D} ${n0} ${B} ${alg_BASE} ${file} ${A_path} ${DQ_path} ${n0_path} ${B_path} ${solutions_count}"
cd ${BASE}

# combine cnf
combine() {
    echo "start modifying and combining cnf"
    cd ${BASE}
    python combine_object_cnf_ascon.py -f1 ${alg_BASE}/${file}.cnf -f2 ${A_path} -f3 ${DQ_path} -f4 ${n0_path} -f5 ${B_path} -o ${alg_BASE}/ascon_A${A}_D${D}_n0${n0}_B${B}.cnf -r ${ROUNDS}
    echo "output cnf file: ${alg_BASE}/ascon_A${A}_D${D}_n0${n0}_B${B}.cnf"
}

# solve
solve() {
    echo "start solving $1"
    echo "output solution file: ${alg_BASE}/ascon_A${A}_D${D}_n0${n0}_B${B}_solution$1.txt"
    set +e
    #nohup cryptominisat5 -t 5 ${alg_BASE}/ascon_A${A}_D${D}_Q${Q}_B${B}.cnf </dev/null >${alg_BASE}/ascon_A${A}_D${D}_n0${n0}_B${B}_solution$1.txt 2>&1
    nohup /home/n2107349e/cadical/build/cadical ${alg_BASE}/ascon_A${A}_D${D}_n0${n0}_B${B}.cnf </dev/null >${alg_BASE}/ascon_A${A}_D${D}_n0${n0}_B${B}_solution$1.txt 2>&1
    set -e
}

# add ban to cnf
ban() {
    echo "start adding ban $1"
    python read_and_ban_solution_ascon.py -c ${alg_BASE}/ascon_A${A}_D${D}_n0${n0}_B${B}.cnf -s ${alg_BASE}/ascon_A${A}_D${D}_n0${n0}_B${B}_solution$1.txt -r ${ROUNDS}
    rm -rf ${alg_BASE}/ascon_A${A}_D${D}_n0${n0}_B${B}_solution$1.txt
}

# iterated solve
iterated_solve() {
    cd ${BASE}
    i=$1
    while true
    do
        solve $i
        CUR_TIME=`date +%Y/%m/%d/%H:%M:%S`
        echo "current time is: ${CUR_TIME}"
        ban $i
        i=$(expr ${i} + 1)
    done
}

main() {
    START_TIME=`date +%Y/%m/%d/%H:%M:%S`
    echo "start time is: ${START_TIME}"

    if [ "${solutions_count}" = "" ]
    then 
        combine 
        solutions_count=1
    fi

    START_TIME=`date +%Y/%m/%d/%H:%M:%S`
    ST=`date +%s.%N`
    echo "solve start time is: ${START_TIME}"

    iterated_solve ${solutions_count}

    ED=`date +%s.%N`
    END_TIME=`date +%Y/%m/%d/%H:%M:%S`
    EXECUTING_TIME=$(printf "%.6f" `echo "${ED} - ${ST}" | bc`)
    echo "total time is: ${EXECUTING_TIME}"
}

main $@
