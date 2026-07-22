"""
oit_voicevox / launch / voicevox.launch.py

VOICEVOXエンジンの起動 → 起動完了待ち → voicevox_nodeの起動 を
一括で行うlaunchファイル。

使い方:
    ros2 launch oit_voicevox voicevox.launch.py
    ros2 launch oit_voicevox voicevox.launch.py voicevox_path:=/home/xxx/.voicevox/VOICEVOX.AppImage speaker_id:=3
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    # ---- launch引数（環境に合わせて上書き可能）----
    voicevox_path_arg = DeclareLaunchArgument(
        "voicevox_path",
        default_value=PathJoinSubstitution(
            [LaunchConfiguration("home_dir", default="~"), ".voicevox", "VOICEVOX.AppImage"]
        ),
        description="VOICEVOX.AppImageへのパス",
    )
    voicevox_url_arg = DeclareLaunchArgument(
        "voicevox_url",
        default_value="http://127.0.0.1:50021",
        description="VOICEVOXエンジンのURL",
    )
    speaker_id_arg = DeclareLaunchArgument(
        "speaker_id",
        default_value="3",
        description="話者ID",
    )
    no_sandbox_arg = DeclareLaunchArgument(
        "no_sandbox",
        default_value="false",
        description="サンドボックスエラーが出る環境ではtrueにする",
    )

    voicevox_path = LaunchConfiguration("voicevox_path")
    voicevox_url = LaunchConfiguration("voicevox_url")
    speaker_id = LaunchConfiguration("speaker_id")

    # ---- 1. VOICEVOXエンジンを起動 ----
    voicevox_engine = ExecuteProcess(
        cmd=["bash", "-c",
             '"$0" $( [ "$1" = "true" ] && echo --no-sandbox )',
             voicevox_path, LaunchConfiguration("no_sandbox")],
        shell=False,
        output="log",
    )

    # ---- 2. VOICEVOXのHTTPサーバーが応答するまで待機 ----
    wait_for_engine = ExecuteProcess(
        cmd=["bash", "-c",
             'echo "VOICEVOXエンジンの起動を待っています..."; '
             'until curl -sf "$0/version" > /dev/null; do sleep 0.5; done; '
             'echo "VOICEVOXエンジンの起動を確認しました。"',
             voicevox_url],
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
            "speaker_id": speaker_id,
            "voicevox_url": voicevox_url,
        }],
    )

    start_node_when_ready = RegisterEventHandler(
        OnProcessExit(
            target_action=wait_for_engine,
            on_exit=[voicevox_node],
        )
    )

    return LaunchDescription([
        voicevox_path_arg,
        voicevox_url_arg,
        speaker_id_arg,
        no_sandbox_arg,
        voicevox_engine,
        wait_for_engine,
        start_node_when_ready,
    ])
