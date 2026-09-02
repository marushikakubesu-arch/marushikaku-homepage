# homepage プロジェクト

## 概要
就労継続支援B型事業所「まるしかくベース」の紹介ホームページ。
三重県鈴鹿市で運営する就労継続支援B型事業所で、利用者に就労機会や生産活動の場を提供している。
障害福祉サービスの報酬を主な収益とし、生産活動として観葉植物の育成・販売も行う（オンラインショップ: https://marushikaku.base.ec/）。

## 技術スタック
- フレームワークなし（プレーンなHTML / CSS / JavaScript）
- ビルドツール不使用
- デザインはInstagram（@marushikakube_su）のロゴ・トーンに合わせたオレンジ主体の配色
- GitHub Actions（`.github/workflows/deploy.yml`）で`homepage/`フォルダをGitHub Pagesへ自動デプロイ（mainにpushされるたび自動反映）

## 重要なID・設定値
- 電話番号: 059-358-8866
- 住所: 〒513-0801 三重県鈴鹿市神戸八丁目6-16
- メールアドレス: marushikaku.besu@gmail.com
- オンラインショップ（BASE）: https://marushikaku.base.ec/
- Instagram: https://www.instagram.com/marushikakube_su/
- GitHubリポジトリ（Public）: https://github.com/marushikakubesu-arch/marushikaku-homepage
- 公開URL（GitHub Pages）: https://marushikakubesu-arch.github.io/marushikaku-homepage/

## ファイル構成
```
homepage/
├── CLAUDE.md
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   ├── logo.png
│   └── shop-*.jpg    # 事業所外観・店内・作業風景の実写真
├── blog/             # 利用者ブログの記事ページ（1記事1HTML）
│   ├── post-1.html〜post-3.html（サンプル記事）
│   └── post-4.html（実際の投稿）
└── archive/           # 使わなくなった素材の退避先
```
リポジトリ直下の `.github/workflows/deploy.yml` がGitHub Pagesへの自動公開を担当（`homepage/`フォルダ配下の変更をトリガーに実行）。

## 設計の意図
- 事業所概要／サービス内容／活動の様子／ご利用について／利用者の声／利用者ブログ／よくある質問／オンラインショップ／アクセス・お問い合わせ、の1ページ構成
- フレームワーク不使用でシンプルに保守できるようにする
- オンラインショップの商品表示はBASE公式の「商品ウィジェット」（iframe埋め込み、`商品詳細ページURL/widget`）を使用。価格・在庫は自動で最新化されるが、新商品の追加・削除は手動でiframeを追加/削除する必要がある（BASEはショップ全体の埋め込みを2025年10月よりセキュリティ上禁止しており、一覧の自動取得はできない）
- 利用者ブログはCMS等を使わず、`blog/post-N.html`を1記事ずつ追加する静的な方式（キャリカク社サイトの日付＋カテゴリタグ＋タイトルの一覧表示を参考）。新しい記事を追加する際は、既存の`blog/post-*.html`を複製して内容を書き換え、`index.html`の`#blog`セクションのリストに1行追加する
- お問い合わせフォームはGoogleフォームを埋め込み（ログイン不要で誰でも回答可能な設定を確認済み）
- リポジトリはGitHub Pages公開のためPublicにしている（顧客の個人情報・APIキー等は含めない）

## TODO
- [ ] 利用者の声セクションの一部（プレースホルダー3件）を、実際にいただいた声（同意取得済みのもの）に差し替え
- [ ] 利用者ブログのサンプル3記事（post-1〜3）を、実際の活動記録に差し替え
- [ ] BASEで商品の入れ替えがあった際は、shopセクションのiframe（items/xxxxx/widget）を更新
- [ ] （任意）Googleマップの埋め込みをしたい場合はGoogle Maps Embed APIキーの発行が必要（現在はリンクボタンのみ）
- [ ] （任意）独自ドメインの取得・接続

## 最終更新日
2026-09-02
