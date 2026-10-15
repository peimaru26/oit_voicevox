#!/bin/bash
function main(){
    local -r PACKAGE_DIR=$(cd "$(dirname "$0")" && pwd)
    local -r SRC_DIR=$(dirname "${PACKAGE_DIR}")
    local -r ROS2_WS=$(dirname "${SRC_DIR}")
    local BUILD_ALL=0
    local REBUILD=0
    local CLEAN=0
    while getopts arc opt
    do
        case ${opt} in
            "a" ) BUILD_ALL=1 ;;
            "r" ) REBUILD=1 ;;
            "c" ) CLEAN=1 ;;
        esac
    done
    local BUILD_OPT="--symlink-install"
    local BUILD_DIR="${ROS2_WS}/build"
    local INSTALL_DIR="${ROS2_WS}/install"
    
    if [ ${BUILD_ALL} -eq 0 ];then
        local NODE=$(cd $(dirname $0);pwd)
        NODE=`echo "$NODE" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
        BUILD_OPT="${BUILD_OPT} --packages-select ${NODE}"
        BUILD_DIR="${BUILD_DIR}/${NODE}"
        INSTALL_DIR="${INSTALL_DIR}/${NODE}"
    fi
    
    if [ ${REBUILD} -eq 1 -o ${CLEAN} -eq 1 ];then
        echo "rm -fr ${BUILD_DIR} ${INSTALL_DIR}"
        rm -fr ${BUILD_DIR} ${INSTALL_DIR}
    fi
    
    if [ ${CLEAN} -eq 0 ];then
        echo "cd ${ROS2_WS} && colcon build ${BUILD_OPT}"
        cd ${ROS2_WS} && colcon build ${BUILD_OPT}
    fi
}

main "$@"
