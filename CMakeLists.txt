cmake_minimum_required(VERSION 3.8)
project(oit_voicevox)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# =============================================================================
# 1. 依存パッケージの検索 (必要に応じてコメントを外す)
# =============================================================================
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

# 【B: Pythonモジュール/Pythonノードを同梱する場合】
find_package(ament_cmake_python REQUIRED)

# =============================================================================
# 5. インストール設定 (コピペ用ターゲットの配置)
# =============================================================================

# (4) 実行用スクリプト (scripts/*.py, *.sh) のインストール 【B】
file(GLOB ALL_SCRIPTS "scripts/*.sh" "scripts/*.py")
if(ALL_SCRIPTS)
  install(PROGRAMS
    ${ALL_SCRIPTS}
    DESTINATION lib/${PROJECT_NAME}
  )
endif()

# (5) 設定ファイル・ローンチファイルのインストール
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# =============================================================================
# 6. エクスポートとパッケージ化 (締め)
# =============================================================================
ament_package()
