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

### ターミナル1：VOICEVOX Engineの起動

ROS 2ノードを起動する前に、VOICEVOX Engineを起動します。以下のいずれか1つの方法を使用してください。複数の方法を同時に実行すると、ポート`50021`が競合します。

#### 方法A：VOICEVOXアプリから起動する

Ubuntuのアプリ一覧を開き、`VOICEVOX`を検索して起動します。

VOICEVOXの画面が表示されたら、アプリを閉じずに起動したままにしてください。VOICEVOXアプリを起動すると、内部のVOICEVOX Engineも自動的に起動します。

別のターミナルを開き、次のコマンドで起動状態を確認します。

```bash
curl --fail --silent http://127.0.0.1:50021/version
echo
```

次のようにバージョン番号が表示されれば起動成功です。

```text
"0.xx.x"
```

#### 方法B：VOICEVOXアプリをターミナルから起動する

公式インストーラーを標準設定で使用した場合、次のコマンドで起動できます。

```bash
~/.voicevox/VOICEVOX.AppImage
```

このターミナルはVOICEVOXを起動したままにしておきます。

ファイルが見つからない場合は、インストール先を確認します。

```bash
find ~/.voicevox -maxdepth 2 -type f -name 'VOICEVOX*.AppImage'
```

実行権限のエラーが出る場合は、次を実行してから再度起動します。

```bash
chmod +x ~/.voicevox/VOICEVOX.AppImage
~/.voicevox/VOICEVOX.AppImage
```

起動後、別のターミナルで確認します。

```bash
curl --fail --silent http://127.0.0.1:50021/version
echo
```

### ターミナル2：ROS 2ノードの起動

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run oit_voicevox voicevox_node
```

このターミナルは、ノードを起動したままにしておきます。

### ターミナル3：文章の送信

別のターミナルを開きます。

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

起動中のノードを確認します。

```bash
ros2 node list
```

VOICEVOXノードが表示されることを確認してください。

次に、テスト文章を送信します。

```bash
ros2 topic pub --once /speak std_msgs/msg/String "{data: 'こんにちは。VOICEVOXの動作確認です。'}"
```

PCのスピーカーから文章が読み上げられれば、動作確認は完了です。

## 購読トピックの確認

`/speak`へ送信しても発話しない場合は、ノードが購読しているトピックを確認します。

```bash
ros2 node list
```

表示されたVOICEVOXノード名を使って、次を実行します。

```bash
ros2 node info /voicevox_node
```

`Subscribers`欄に、次のような`std_msgs/msg/String`型のトピックが表示されます。

```text
/speak: std_msgs/msg/String
```

トピック名が`/speak`以外の場合は、実際に表示された名前へ文章を送信してください。

```bash
ros2 topic pub --once 実際のトピック名 std_msgs/msg/String \
  "{data: 'こんにちは。VOICEVOXの動作確認です。'}"
```

## 終了方法

ROS 2ノードを起動しているターミナルで、`Ctrl + C`を押します。

VOICEVOX Engineも不要になった場合は、VOICEVOXを終了してください。

## よくあるエラー

### `Package 'oit_voicevox' not found`

ワークスペースを読み込めていません。

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

改善しない場合は、もう一度ビルドします。

```bash
cd ~/ros2_ws
colcon build --packages-select oit_voicevox
source install/setup.bash
```

### VOICEVOX Engineへ接続できない

次のコマンドで確認します。

```bash
curl http://127.0.0.1:50021/version
```

接続できない場合は、VOICEVOX Engineを起動してください。また、ROS 2ノードとVOICEVOX Engineが同じPC上で動作していることを確認してください。

### 発話メッセージを送っても音が出ない

まず音声デバイスを確認します。

```bash
aplay -l
```

次に、PCがミュートになっていないか、正しい音声出力先が選択されているか確認してください。

### Pythonの`requests`が見つからない

```bash
sudo apt install python3-requests
```

### コードを更新した後に変更が反映されない

再ビルドと環境の再読み込みが必要です。

```bash
cd ~/ros2_ws
colcon build --packages-select oit_voicevox
source install/setup.bash
```

## ライセンス・利用上の注意

VOICEVOXおよび各音声キャラクターを利用する場合は、それぞれの利用規約を確認してください。

https://voicevox.hiroshiba.jp/term/
