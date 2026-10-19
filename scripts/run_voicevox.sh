#!/bin/bash

function check_voicevox(){
    local mode="$1"
    ps -eo pid=,args= | while read -r pid token rest; do
        # 自分自身のPIDならスキップ
        if [ "$pid" = "$$" ]; then
            continue
        fi
        
        # 2個目のトークンに VOICEVOX や .mount_VOICE が含まれるか判定
        if [[ "$token" == *VOICEVOX.AppImage* ]] || [[ "$token" == *.mount_VOICE* ]]; then            
            # ros2やlaunch、スクリプト自身などの除外
            if [[ "$token" =~ (ros2|launch|run_voicevox\.sh|grep) ]]; then
                continue
            fi
            if [ "$mode" = "kill" ]; then
                echo "  -> Killing old VOICEVOX PID $pid: $token" >&2
                kill -9 "$pid" 2>/dev/null
            else
                echo "  [CHECK] PID: $pid | Token: $token" >&2
            fi
        fi
    done
}

function main(){
    if [ "$#" -lt 1 ]; then
        echo "Usage: $0 <path_to_voicevox_appimage> [voicevox_args...]" >&2
        exit 1
    fi
    VOICEVOX_PATH="$1"
    shift  # 第一引数をシフトし、残りの引数（$@）をVOICEVOXへのオプションとして保持
    echo "Cleaning up stale VOICEVOX processes..." >&2
    check_voicevox kill
    
    # プロセスが完全に消えるのを少し待つ
    sleep 0.5
    
    if command -v x-terminal-emulator &> /dev/null; then
        # x-terminal-emulator -e bash -c "\"$VOICEVOX_PATH\" \"$@\"; exec bash"
        x-terminal-emulator -e bash -c "\"$VOICEVOX_PATH\" \"$@\"" &
    else
        echo "Can not find x-terminal-emulator." >&2
        exit 1
    fi
    echo "VOICEVOX launched successfully." >&2
    return 0
}

main "$@"
