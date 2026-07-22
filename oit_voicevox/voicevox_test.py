import requests
from pathlib import Path

# 起動中のVOICEVOXのアドレス
base_url = "http://127.0.0.1:50021"

# 読ませる文章
text = "こんにちは。Pythonから音声を生成しています。"

# ずんだもん・ノーマル
speaker_id = 3

# 音声合成に必要な設定データを作成
query_response = requests.post(
    f"{base_url}/audio_query",
    params={
        "text": text,
        "speaker": speaker_id
    },
    timeout=30
)
query_response.raise_for_status()

# 設定データから音声を生成
synthesis_response = requests.post(
    f"{base_url}/synthesis",
    params={
        "speaker": speaker_id
    },
    json=query_response.json(),
    timeout=30
)
synthesis_response.raise_for_status()

# WAVファイルとして保存
output_path = Path("output.wav")
output_path.write_bytes(synthesis_response.content)

print(f"音声を保存しました: {output_path.resolve()}")
