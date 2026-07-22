import os
import subprocess
import tempfile

import requests
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class VoicevoxNode(Node):

    def __init__(self):
        super().__init__("voicevox_node")

        # ROS 2パラメータ
        self.declare_parameter("speaker_id", 3)
        self.declare_parameter(
            "voicevox_url",
            "http://127.0.0.1:50021"
        )

        self.speaker_id = self.get_parameter("speaker_id").value
        self.voicevox_url = self.get_parameter("voicevox_url").value.rstrip("/")

        # /voicevox/speakトピックを受信
        self.subscription = self.create_subscription(
            String,
            "/voicevox/speak",
            self.speak_callback,
            10
        )

        self.get_logger().info(
            "VOICEVOX発話ノードを起動しました。"
            "/voicevox/speakトピックを待っています。"
        )

    def speak_callback(self, msg):
        text = msg.data.strip()

        if not text:
            self.get_logger().warning("空の文章を受信しました。")
            return

        self.get_logger().info(f"受信した文章: {text}")

        wav_path = None

        try:
            # 音声合成用のクエリを作成
            query_response = requests.post(
                f"{self.voicevox_url}/audio_query",
                params={
                    "text": text,
                    "speaker": self.speaker_id
                },
                timeout=30
            )
            query_response.raise_for_status()

            # 音声を生成
            synthesis_response = requests.post(
                f"{self.voicevox_url}/synthesis",
                params={
                    "speaker": self.speaker_id
                },
                json=query_response.json(),
                timeout=30
            )
            synthesis_response.raise_for_status()

            # 一時的なWAVファイルとして保存
            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as wav_file:
                wav_file.write(synthesis_response.content)
                wav_path = wav_file.name

            # スピーカーから再生
            subprocess.run(
                ["aplay", "-q", wav_path],
                check=True
            )

            self.get_logger().info("発話が完了しました。")

        except requests.RequestException as error:
            self.get_logger().error(
                f"VOICEVOXとの通信に失敗しました: {error}"
            )

        except (OSError, subprocess.CalledProcessError) as error:
            self.get_logger().error(
                f"音声の再生に失敗しました: {error}"
            )

        finally:
            if wav_path is not None and os.path.exists(wav_path):
                os.remove(wav_path)


def main(args=None):
    rclpy.init(args=args)

    node = VoicevoxNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
