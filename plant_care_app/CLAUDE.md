# plant_care_app

## 概要
ケータイで使う植物管理アプリ（PWA）。植物の登録、成長記録（写真・草丈）、水やり/肥料の予定管理、置き場所、LUX記録、空気循環記録、JSONバックアップ。

## 技術スタック
HTML/CSS/JavaScript単体（ライブラリなし）、IndexedDBで端末内保存、Service Workerでオフライン対応。

## 重要なID設定値
なし（APIキー・外部サービス不使用。データは端末内のみ）。

## ファイル構成
- index.html：画面と処理すべて
- manifest.json：ホーム画面追加の設定
- sw.js：オフライン用キャッシュ
- icon.svg：アイコン

## 設計の意図
- サーバー不要・個人情報なし。データは端末のブラウザ内にだけ保存し、機種変更用に書き出し/読み込みを用意。
- 写真は縮小してJPEG化して保存（容量節約）。
- 記録は1つのlogs配列に種類(type)で統一：water/fert/growth/lux/air。LUXと空気循環は置き場所にも紐づく。
- スマホへの導入にはHTTPS公開が必要。公開用の別リポジトリ（marushikakubesu-arch/plant_care_app、GitHub Pages）から公開。公開URL: https://marushikakubesu-arch.github.io/plant_care_app/
- 更新時はこのフォルダの内容を公開用リポジトリへ反映する（ホームページとは別管理）。

## TODO
- 【次の作業】複数端末の同期機能（方針決定済み）
  - 方式：Googleドライブのアプリデータ領域（appDataFolder、スコープ drive.appdata）に全データ(JSON、写真含む)を保存。サーバー不要・無料
  - 競合：記録ごとの更新日時を持たせ、新しいほうを残して統合。削除は印(tombstone)を残す
  - 同期のタイミング：起動時と保存時。設定タブに同期ボタンと最終同期時刻を表示
  - 変更は index.html のみ（新規ファイルなし）。OAuthクライアントIDは公開されても問題ない種類なのでコードに書いてよい（パスワード・トークンは書かない）
  - 事前準備（ボスが実施、案内する）：Google Cloudでプロジェクト作成→Google Drive API有効化→OAuth同意画面→OAuthクライアントID(ウェブ)作成。承認済みJavaScript生成元に https://marushikakubesu-arch.github.io を追加
  - 着手前に、設定タブから現在のデータを書き出してバックアップを取る
- スマホ実機での使い勝手確認
- 必要なら成長・LUXの推移グラフ、置き場所の移動履歴

## 最終更新日
2026-10-08
