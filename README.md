## 説明/使用方法
DiscordでBotとして利用できるプログラム群です。
* Requiment_Install.cmdを実行して必要なライブラリをインストールします。
* .envの Token here にDiscord Botのトークンを挿入します。
### filter.py
Discordでユーザーが送信したメッセージ内の単語をブロックできます。定義更新が必要なマルウェアURLリストなどに適しています。
* プログラム内にある FILTER URL HERE にフィルターのURLを挿入します。
### gban.py
Discordで特定のユーザーIDを持つユーザーを参加時に自動的にBANし、参加を阻止します。
* プログラム内にあるユーザーIDを記述する箇所にユーザーIDを追加します。