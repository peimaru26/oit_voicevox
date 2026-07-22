# oit_voicevox

VOICEVOXをROS 2から利用するための音声合成パッケージです。

`std_msgs/msg/String`型のメッセージを`/voicevox/speak`トピックへ送信すると、VOICEVOX Engineで音声を生成し、PCのスピーカーから再生します。

付属のlaunchファイルを使用すると、次の処理を1つのコマンドで実行できます。

1. VOICEVOX Engineの起動
2. Engineの起動完了待ち
3. `voicevox_node`の起動

## 動作確認環境

- Ubuntu 24.04 LTS
- ROS 2 Jazzy
- Python 3
- VOICEVOX AppImage
- 音声出力が可能なPC

## 事前準備

### 1. ROS 2 Jazzyのインストール

ROS 2 Jazzyが未導入の場合は、公式手順に従ってインストールしてください。

https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

インストール後、ROS 2の環境を読み込みます。

```bash
source /opt/ros/jazzy/setup.bash
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

`sudo rosdep init`で、すでに初期化されていることを示すメッセージが表示された場合は、そのまま次へ進んでください。

### 3. VOICEVOXのインストール

VOICEVOX公式サイトからLinux版をダウンロードし、インストールしてください。

https://voicevox.hiroshiba.jp/

インストール後、VOICEVOXのAppImageが存在する場所を確認します。標準的な保存先は次のとおりです。

```text
/home/ユーザー名/.voicevox/VOICEVOX.AppImage
```

次のコマンドでも検索できます。

```bash
find "$HOME" -maxdepth 4 -type f -name 'VOICEVOX*.AppImage' 2>/dev/null
```

AppImageに実行権限がない場合は、実際の保存先を指定して権限を付与します。

```bash
chmod +x /home/ユーザー名/.voicevox/VOICEVOX.AppImage
```

以降の`voicevox_path`には、ここで確認した絶対パスを指定します。`ユーザー名`の部分をそのまま入力してはいけません。

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

リポジトリがPrivateの場合は、GitHubへのログインとアクセス権が必要です。

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
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

新しいターミナルを開いた場合は、再度この2行を実行してください。

## 動作確認

### ターミナル1：VOICEVOX EngineとROS 2ノードの起動

VOICEVOXアプリを手動で起動する必要はありません。launchファイルがVOICEVOX EngineとROS 2ノードを順番に起動します。

`voicevox_path`には、自分のPCに保存されている`VOICEVOX.AppImage`の絶対パスを指定してください。

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 launch oit_voicevox voicevox.launch.py \
  voicevox_path:=/home/ユーザー名/.voicevox/VOICEVOX.AppImage
```

例えば、AppImageが`/home/oit/.voicevox/VOICEVOX.AppImage`にある場合は、次のように実行します。

```bash
ros2 launch oit_voicevox voicevox.launch.py \
  voicevox_path:=/home/oit/.voicevox/VOICEVOX.AppImage
```

起動処理中は次のメッセージが表示されます。

```text
VOICEVOXエンジンの起動を待っています...
VOICEVOXエンジンの起動を確認しました。
```

2行目が表示されると、VOICEVOX Engineへの接続が完了し、`voicevox_node`が起動します。このターミナルは起動したままにしてください。

### ターミナル2：文章の送信

別のターミナルを開き、ROS 2の環境を読み込みます。

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

次のコマンドでテスト文章を1回だけ送信します。

```bash
ros2 topic pub --once /voicevox/speak std_msgs/msg/String \
  "{data: 'こんにちは'}"
```

PCのスピーカーから「こんにちは」と読み上げられれば、動作確認は完了です。

## launch引数

launchファイルでは、次の引数を指定できます。

| 引数 | 初期値 | 説明 |
| --- | --- | --- |
| `voicevox_path` | `~/.voicevox/VOICEVOX.AppImage` | VOICEVOX AppImageの保存先 |
| `voicevox_url` | `http://127.0.0.1:50021` | VOICEVOX EngineのURL |
| `speaker_id` | `3` | 使用するVOICEVOXの話者ID |
| `no_sandbox` | `false` | サンドボックス関連のエラーが出る場合に`true`を指定 |

話者IDを変更する場合は、次のように指定します。

```bash
ros2 launch oit_voicevox voicevox.launch.py \
  voicevox_path:=/home/ユーザー名/.voicevox/VOICEVOX.AppImage \
  speaker_id:=3
```

サンドボックス関連のエラーが出る場合は、次のように起動します。

```bash
ros2 launch oit_voicevox voicevox.launch.py \
  voicevox_path:=/home/ユーザー名/.voicevox/VOICEVOX.AppImage \
  no_sandbox:=true
```

利用可能な引数は、次のコマンドでも確認できます。

```bash
ros2 launch oit_voicevox voicevox.launch.py --show-args
```

## 終了方法

launchを実行しているターミナルで`Ctrl + C`を押してください。launchから起動したVOICEVOX EngineとROS 2ノードが終了します。

## よくあるエラー

### `Package 'oit_voicevox' not found`

ビルド後のワークスペースを読み込めていません。

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

改善しない場合は再ビルドします。

```bash
cd ~/ros2_ws
colcon build --packages-select oit_voicevox
source install/setup.bash
```

### launchファイルが見つからない

次のようなエラーが出る場合は、launchファイルを追加する前の状態がインストールされている可能性があります。

```text
file 'voicevox.launch.py' was not found
```

リポジトリを更新してから再ビルドします。

```bash
cd ~/ros2_ws/src/oit_voicevox
git pull

cd ~/ros2_ws
colcon build --packages-select oit_voicevox
source install/setup.bash
```

### `VOICEVOX.AppImage`が見つからない

指定したパスが間違っています。保存先を検索します。

```bash
find "$HOME" -maxdepth 4 -type f -name 'VOICEVOX*.AppImage' 2>/dev/null
```

表示された絶対パスを`voicevox_path`へ指定してください。

### `Permission denied`

AppImageに実行権限を付与します。

```bash
chmod +x /実際の保存先/VOICEVOX.AppImage
```

### VOICEVOX Engineの起動待ちから進まない

VOICEVOX AppImageの起動に失敗している可能性があります。まずlaunchを`Ctrl + C`で終了し、AppImageを単体で実行してエラーを確認してください。

```bash
/実際の保存先/VOICEVOX.AppImage
```

また、すでに別のVOICEVOXが起動している場合は、ポート`50021`が競合する可能性があります。手動で起動しているVOICEVOXを終了してから、もう一度launchを実行してください。

### サンドボックス関連のエラーが表示される

`no_sandbox:=true`を追加して起動します。

```bash
ros2 launch oit_voicevox voicevox.launch.py \
  voicevox_path:=/実際の保存先/VOICEVOX.AppImage \
  no_sandbox:=true
```

### メッセージを送信しても音が出ない

ノードとトピックを確認します。

```bash
ros2 node list
ros2 topic info /voicevox/speak
```

音声出力デバイスも確認してください。

```bash
aplay -l
```

PCがミュートになっていないか、正しい音声出力先が選択されているかも確認してください。

## ライセンス・利用上の注意

VOICEVOXおよび各音声キャラクターを利用する場合は、それぞれの利用規約を確認してください。

https://voicevox.hiroshiba.jp/term/
