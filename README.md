# oit_voicevox

VOICEVOX EngineをROS 2から利用するための音声合成ノードです。

ROS 2の`std_msgs/msg/String`メッセージとして文章を送信すると、VOICEVOX Engineへ音声合成を要求し、生成された音声をPCのスピーカーから再生します。

## 動作確認環境

- Ubuntu 24.04 LTS
- ROS 2 Jazzy
- Python 3
- VOICEVOX Engine
- 音声出力が可能なPC

ROS 2 JazzyはUbuntu 24.04を対象としています。

## 処理の流れ

1. ROS 2トピックから文章を受信
2. VOICEVOX Engineへ音声クエリを送信
3. 音声データを生成
4. 生成した音声をスピーカーから再生

## 事前準備

### 1. ROS 2 Jazzyのインストール

ROS 2 Jazzyが未導入の場合は、公式手順に従ってインストールしてください。

https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

インストール後、ROS 2の環境を読み込みます。

```bash
source /opt/ros/jazzy/setup.bash
```

毎回実行したくない場合は、次の設定を追加します。

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 2. 必要なパッケージのインストール

```bash
sudo apt update
sudo apt install -y \
  git \
  curl \
  alsa-utils \
  python3-requests \
  python3-rosdep \
  python3-colcon-common-extensions
```

`rosdep`を初めて使用する場合は、次を実行します。

```bash
sudo rosdep init
rosdep update
```

`sudo rosdep init`で「already been initialized」と表示された場合は、そのまま次へ進んでください。

### 3. VOICEVOX Engineの準備

VOICEVOXを公式サイトからダウンロードしてインストールします。

https://voicevox.hiroshiba.jp/

VOICEVOXを起動した状態で、次のコマンドを実行してください。

```bash
curl http://127.0.0.1:50021/version
```

バージョン番号が返れば、VOICEVOX Engineは正常に起動しています。

例：

```text
"0.xx.x"
```

`Failed to connect`や`Connection refused`と表示された場合は、VOICEVOX Engineが起動していません。VOICEVOXを起動してから、もう一度確認してください。

## インストール

### 1. ROS 2ワークスペースの作成

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### 2. リポジトリのクローン

```bash
git clone https://github.com/peimaru26/oit_voicevox.git
```

このリポジトリがPrivateの場合は、GitHubアカウントへのログインとリポジトリへのアクセス権が必要です。

### 3. 依存パッケージのインストール

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

### 4. ビルド

```bash
cd ~/ros2_ws
colcon build --packages-select oit_voicevox
```

次のように表示されればビルド成功です。

```text
Summary: 1 package finished
```

### 5. ワークスペースの読み込み

```bash
source ~/ros2_ws/install/setup.bash
```

新しいターミナルを開くたびに、このコマンドを実行する必要があります。

## 動作確認

動作確認では、VOICEVOX Engine、ROS 2ノード、テストメッセージ送信の順に起動します。

### ターミナル1：VOICEVOX Engineの確認

VOICEVOXを起動してから、次を実行します。

```bash
curl http://127.0.0.1:50021/version
```

バージョン番号が返ることを確認してください。

### ターミナル2：ROS 2ノードの起動

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
