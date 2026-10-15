"""
oit_voicevox / launch / voicevox.launch.py

VOICEVOXエンジンの起動 → 起動完了待ち → voicevox_nodeの起動 を
一括で行うlaunchファイル。

使い方:
    ros2 launch oit_voicevox voicevox.launch.py
    ros2 launch oit_voicevox voicevox.launch.py voicevox_path:=/home/xxx/.voicevox/VOICEVOX.AppImage speaker_id:=3
"""
from pathlib import Path
from types import SimpleNamespace

from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, ExecuteProcess,
                            OpaqueFunction, RegisterEventHandler)
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration


def declare_arg(name, default_value, description="", choices=None):
    return SimpleNamespace(
        name=name,
        arg=DeclareLaunchArgument(
            name, default_value=default_value, description=description, choices=choices),
        conf=LaunchConfiguration(name))


voicevox_path = declare_arg("voicevox_path",
                            Path.home() / ".voicevox" / "VOICEVOX.AppImage", "VOICEVOX.AppImageへのパス")
voicevox_url = declare_arg("voicevox_url", "http://127.0.0.1:50021",
                           "VOICEVOXエンジンのURL")
speaker_id = declare_arg("speaker_id", "3", "話者ID")
no_sandbox = declare_arg("no_sandbox", "false", "サンドボックスエラーが出る環境ではtrueにする")


def launch_setup(context, *args, **kwargs):
    voicevox_path_value = voicevox_path.conf.perform(context)
    voicevox_url_value = voicevox_url.conf.perform(context)
    speaker_id_value = int(speaker_id.conf.perform(context))
    no_sandbox_value = no_sandbox.conf.perform(context)

    # ---- 1. VOICEVOXエンジンを起動 ----
    voicevox_engine = ExecuteProcess(
        cmd=["bash", "-c",
             '"$0" $( [ "$1" = "true" ] && echo --no-sandbox )',
             voicevox_path_value, no_sandbox_value],
        shell=False,
        output="log",
    )

    # ---- 2. VOICEVOXのHTTPサーバーが応答するまで待機 ----
    wait_for_engine = ExecuteProcess(
        cmd=["bash", "-c",
             'echo "VOICEVOXエンジンの起動を待っています..."; '
             'until curl -sf "$0/version" > /dev/null; do sleep 0.5; done; '
             'echo "VOICEVOXエンジンの起動を確認しました。"',
             voicevox_url_value],
        shell=False,
        output="screen",
    )

    # ---- 3. voicevox_nodeを起動 ----
    voicevox_node = Node(
        package="oit_voicevox",
        executable="voicevox_node",
        name="voicevox_node",
        output="screen",
        parameters=[{
            "speaker_id": speaker_id_value,
            "voicevox_url": voicevox_url_value,
        }],
    )

    start_node_when_ready = RegisterEventHandler(
        OnProcessExit(
            target_action=wait_for_engine,
            on_exit=[voicevox_node],
        )
    )

    return [voicevox_engine, wait_for_engine, start_node_when_ready]


def generate_launch_description():
    return LaunchDescription([
        voicevox_path.arg, voicevox_url.arg, speaker_id.arg, no_sandbox.arg,
        OpaqueFunction(function=launch_setup)
    ])
