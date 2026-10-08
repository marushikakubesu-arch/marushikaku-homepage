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
- スマホ実機での使い勝手確認
- 必要なら成長・LUXの推移グラフ、置き場所の移動履歴

## 最終更新日
2026-10-08
