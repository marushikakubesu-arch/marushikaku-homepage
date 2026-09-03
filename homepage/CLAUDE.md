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
- 独自ドメイン: marushikakubase.com（2026-09-03取得、お名前.comで管理。`homepage/CNAME`で設定）
- 公開URL（GitHub Pages・旧URL）: https://marushikakubesu-arch.github.io/marushikaku-homepage/（独自ドメイン設定後はこちらから自動転送）
- Googleビジネスプロフィール: 登録済み（ホームページ・SNSリンク設定済み、Googleマップにも反映済み）
- Google Search Console: 登録・所有権確認済み（HTMLファイル方式、`homepage/googlec0e21ed30566cb09.html`）

## ファイル構成
```
homepage/
├── CLAUDE.md
├── CNAME              # 独自ドメイン(marushikakubase.com)設定用。GitHub Pagesが参照
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
- 1ページ構成のセクション順（2026-09-03改訂）：トップ(#top) → まるしかくベースについて(#about) → 活動の様子(#gallery) → まるしかくベースでできること(#service) → 1日の流れ(#schedule) → こんな方におすすめです(#recommend) → 就労継続支援B型とは？(#btype) → ご利用までの流れ(#flow) → 利用者ブログ(#blog) → よくある質問(#faq) → 育てた植物を、あなたのもとへ。＝植物販売について(#plants、旧オンラインショップ・Instagramセクションを統合、アクセスの直前に配置) → アクセス・お問い合わせ(#contact)
- 「利用者の声」は実際の利用者から集めた正式な声ではなかったため、「こんな方におすすめです」（利用対象者チェックリスト）に差し替え済み
- フレームワーク不使用でシンプルに保守できるようにする
- オンラインショップの商品表示はBASE公式の「商品ウィジェット」（iframe埋め込み、`商品詳細ページURL/widget`）を使用。価格・在庫は自動で最新化されるが、新商品の追加・削除は手動でiframeを追加/削除する必要がある（BASEはショップ全体の埋め込みを2025年10月よりセキュリティ上禁止しており、一覧の自動取得はできない）
- 利用者ブログはCMS等を使わず、`blog/post-N.html`を1記事ずつ追加する静的な方式（キャリカク社サイトの日付＋カテゴリタグ＋タイトルの一覧表示を参考）。新しい記事を追加する際は、既存の`blog/post-*.html`を複製して内容を書き換え、`index.html`の`#blog`セクションのリストに1行追加する
- お問い合わせフォームは、サイトのデザインに合わせた自作フォーム（`#contactForm`）からGoogleフォームの送信先(`/formResponse`)へ直接POSTする方式（hidden iframeで送信し、`js/main.js`が送信後に完了メッセージを表示）。Googleフォーム標準の見た目は使っていない
  - フォーム項目とentry ID：お名前=entry.112423487（必須）／メールアドレス=entry.911916954（必須）／電話番号=entry.1613386452（必須）／ご希望の種類（体験・見学・相談）=entry.1329975269（任意）／お問い合わせ内容=entry.270639122（任意）
  - 元のGoogleフォーム側で質問の追加・削除・変更を行った場合、上記entry IDと`index.html`内のフォーム項目がずれるため、`index.html`のフォームも合わせて修正が必要
- リポジトリはGitHub Pages公開のためPublicにしている（顧客の個人情報・APIキー等は含めない）

## TODO
- [ ] 利用者ブログは現在post-4（水やりについて）のみ公開中。サンプル記事（post-1〜3）はarchiveへ退避済み。新しい記事が集まり次第、随時追加
- [ ] BASEで商品の入れ替えがあった際は、shopセクションのiframe（items/xxxxx/widget）を更新
- [ ] Google Search Consoleの所有権確認をmarushikakubase.comでも新規に行い、サイトマップ送信・インデックス登録リクエストを行う（旧github.io URLでの登録は残したままでよい）
- [ ] Instagram・Googleビジネスプロフィールのリンクを、旧github.io URLからmarushikakubase.comに更新する

## 完了した公開・SEO対応（2026-09-02）
- GitHub Pagesで公開、Google Search Console登録・インデックス登録リクエスト済み
- Googleビジネスプロフィール登録済み（Googleマップに反映済みのため、サイト内への地図埋め込みは不要と判断）
- Instagram・Googleビジネスプロフィールにホームページリンクを設定済み

## 独自ドメイン接続（2026-09-03〜04）
- marushikakubase.comを取得し、GitHub Pagesのカスタムドメインとして接続完了（HTTPS化・DNS checkも成功）
- つまずいたポイント：お名前.comは「ドメインDNS設定」（Aレコード等の登録）と「ネームサーバー設定」（お名前.comのネームサーバーを実際に使うかの選択）が別画面になっており、後者を選択していなかったためDNSがいつまでも反映されなかった。「ネームサーバー設定」で「お名前.comのネームサーバーを使う」を選択したことで解決
- 今後、同じ現象（DNSレコードを設定したのに何時間経っても反映されない）が起きた場合は、まず「ネームサーバー設定」が正しく選択されているか確認する

## 最終更新日
2026-09-03
