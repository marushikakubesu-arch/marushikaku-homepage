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
- Googleビジネスプロフィール: 登録済み（ホームページ・SNSリンク設定済み、Googleマップにも反映済み）
- Google Search Console: 登録・所有権確認済み（HTMLファイル方式、`homepage/googlec0e21ed30566cb09.html`）

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
│   └── post-4.html（実際の投稿。水やりについて）
└── archive/           # 使わなくなった素材の退避先（post-1〜3.htmlはサンプル記事のため退避済み）
```
リポジトリ直下の `.github/workflows/deploy.yml` がGitHub Pagesへの自動公開を担当（`homepage/`フォルダ配下の変更をトリガーに実行）。

## 設計の意図
- 1ページ構成のセクション順（2026-09-03改訂）：トップ(#top) → まるしかくベースについて(#about) → 活動の様子(#gallery) → まるしかくベースでできること(#service) → 1日の流れ(#schedule) → こんな方におすすめです(#recommend) → 就労継続支援B型とは？(#btype) → ご利用までの流れ(#flow) → 育てた植物を、あなたのもとへ。＝植物販売について(#plants、旧オンラインショップ・Instagramセクションを統合) → 利用者ブログ(#blog) → よくある質問(#faq) → アクセス・お問い合わせ(#contact)
- 「利用者の声」は実際の利用者から集めた正式な声ではなかったため、「こんな方におすすめです」（利用対象者チェックリスト）に差し替え済み
- フレームワーク不使用でシンプルに保守できるようにする
- オンラインショップの商品表示はBASE公式の「商品ウィジェット」（iframe埋め込み、`商品詳細ページURL/widget`）を使用。価格・在庫は自動で最新化されるが、新商品の追加・削除は手動でiframeを追加/削除する必要がある（BASEはショップ全体の埋め込みを2025年10月よりセキュリティ上禁止しており、一覧の自動取得はできない）
- 利用者ブログはCMS等を使わず、`blog/post-N.html`を1記事ずつ追加する静的な方式（キャリカク社サイトの日付＋カテゴリタグ＋タイトルの一覧表示を参考）。新しい記事を追加する際は、既存の`blog/post-*.html`を複製して内容を書き換え、`index.html`の`#blog`セクションのリストに1行追加する
- お問い合わせフォームはGoogleフォームを埋め込み（ログイン不要で誰でも回答可能な設定を確認済み）
- リポジトリはGitHub Pages公開のためPublicにしている（顧客の個人情報・APIキー等は含めない）

## TODO
- [ ] 利用者ブログは現在post-4（水やりについて）のみ公開中。サンプル記事（post-1〜3）はarchiveへ退避済み。新しい記事が集まり次第、随時追加
- [ ] BASEで商品の入れ替えがあった際は、shopセクションのiframe（items/xxxxx/widget）を更新
- [ ] （任意）独自ドメインの取得・接続

## 完了した公開・SEO対応（2026-09-02）
- GitHub Pagesで公開、Google Search Console登録・インデックス登録リクエスト済み
- Googleビジネスプロフィール登録済み（Googleマップに反映済みのため、サイト内への地図埋め込みは不要と判断）
- Instagram・Googleビジネスプロフィールにホームページリンクを設定済み

## 最終更新日
2026-09-03
