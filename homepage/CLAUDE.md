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
- Google Search Console: 旧URL（github.io）・独自ドメイン（marushikakubase.com）ともに登録・所有権確認済み。marushikakubase.com側は2026-09-11に`sitemap.xml`を送信済み（ステータス「成功」）
- 事業所番号（facilityNumber）: 2410302323
- WAMNET事業所情報ページ: https://www.wam.go.jp/sfkohyoout/COP020100E00.do?_FORMID=COP000101&corporationNumber=A2420700000065&facilityNumber=2410302323&bunjoNumber=000000&serviceType=46&serviceSubNumber=A0000172440
- LITALICO仕事ナビ掲載ページ: https://snabi.jp/facility/38618

## ファイル構成
```
homepage/
├── CLAUDE.md
├── CNAME              # 独自ドメイン(marushikakubase.com)設定用。GitHub Pagesが参照
├── robots.txt         # 検索エンジン向けクロール許可設定、sitemap.xmlの場所を明記
├── sitemap.xml        # index.html・ブログ記事一覧のURLを記載
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   ├── logo.png
│   ├── shop-*.jpg    # 事業所外観・店内・作業風景の実写真
│   ├── shop-activity.mp4  # 活動の様子スライドショー用の実動画
│   └── shop-intro.mp4     # ヒーローセクション冒頭の紹介・採用動画（顔出しスタッフ2名、本人確認済み）
├── blog/             # 利用者ブログの記事ページ（1記事1HTML）
│   ├── post-4.html（実際の投稿。水やりについて）
│   ├── post-5.html（実際の投稿。写真撮影）
│   ├── post-6.html（実際の投稿。梱包について）
│   ├── post-7.html（実際の投稿。販売と写真撮影）
│   ├── post-8.html（実際の投稿。撮影デー）
│   ├── post-9.html（実際の投稿。今までの作業を通して思ったことと植物の紹介）
│   ├── post-10.html（実際の投稿。事業所の見学）
│   ├── post-11.html（実際の投稿。面談とこの前のサプライズ）
│   ├── post-12.html（実際の投稿。新しいことの挑戦）
│   ├── post-13.html（実際の投稿。今月ラスト）
│   ├── post-14.html（実際の投稿。初めての植え替え）
│   └── post-15.html（実際の投稿。水やりと商品カード作り）
└── archive/           # 使わなくなった素材の退避先（post-1〜3.htmlはサンプル記事のため退避済み）
```
リポジトリ直下の `.github/workflows/deploy.yml` がGitHub Pagesへの自動公開を担当（`homepage/`フォルダ配下の変更をトリガーに実行）。

## 設計の意図
- 1ページ構成のセクション順（2026-10-01改訂）：トップ(#top) → 3つの強み(#strengths、ヒーロー直後に新設) → まるしかくベースについて(#about) → 活動の様子(#gallery) → まるしかくベースでできること(#service) → 1日の流れ(#schedule) → こんな方におすすめです(#recommend) → 就労継続支援B型とは？(#btype) → ご利用までの流れ(#flow) → 利用者ブログ(#blog) → よくある質問(#faq) → 育てた植物を、あなたのもとへ。＝植物販売について(#plants、旧オンラインショップ・Instagramセクションを統合、アクセスの直前に配置) → アクセス・お問い合わせ(#contact)
- ヒーロー直後に「3つの強み」セクション(#strengths、`section-alt`)を新設（2026-10-01）。見出し上に`.eyebrow`バッジ「まるしかくベースの3つの強み」、`<h2>植物を育てながら、「できる」を増やしていく</h2>`（2026-10-01、当初の「ちゃんと働く」から変更）、リード文に続き、`.feature-row`（テキスト側`.feature-text`＋画像/ウィジェット側`.feature-media`の順で横並び、モバイルでは縦積み）を3段配置。STRENGTH 01「本物の商品として、お客様の元へ届く」は`.feature-media`に`#plants`と同じBASE商品ウィジェットiframeを2つ配置（items/157039851「ステファニア スベローサ」・items/157080526「アグラオネマ ワールドヘリテージ」の異なる植物2種、2026-10-01に見た目のバリエーションを出すため同一植物の個体違い2点から差し替え）。STRENGTH 02「次につながるスキルが身につく」は画像（`images/shop-pc-work.jpg`）を配置。STRENGTH 03「工賃もしっかり獲得できる」は画像なしで、`.ok-badge`（「利用は週1日からでもOK！」）と工賃シミュレーション（`.wage-sim`一式）を`#btype`セクションから移動して配置。各段の`.strength-num`に「強み01/02/03」ラベルを表示（2026-10-01、当初の英語表記「STRENGTH 01/02/03」から日本語表記に変更）。工賃シミュレーションのHTML構造・id（`wageSimDays`/`wageSimBreakdown`/`wageSimAmount`）・計算ロジック（`js/main.js`）は変更していないため、配置場所が変わっても動作は従来通り。これに伴い`#btype`セクションには元々あった3つの`<p>`の説明文のみが残る形に戻した
- `.feature-row`内の並びは「`.feature-text`→`.feature-media`」（テキストが先、画像・ウィジェットが後）に統一（2026-10-02）。以前はSTRENGTH 01が画像先、STRENGTH 02が`.feature-row.reverse`（`flex-direction: row-reverse`）でDOM順は画像先・見た目だけ反転という状態で、モバイル（flex-wrapで縦積み）では画像が先に表示されてしまっていたため統一した。`.feature-row.reverse`はどこからも参照されなくなったため、`css/style.css`からも削除済み（今後`.feature-row`の見た目を左右反転させたい場合は、同名クラスを再度CSSに追加する必要がある）
- `#strengths`のリード文（「単なる訓練ではなく〜」）とSTRENGTH 01の間に、実際の水やり作業の写真（`images/shop-watering.jpg`、`#gallery`で使用している素材を再利用）を1枚追加（2026-10-01）。`.strengths-intro-img`クラスで`.blog-post-photo`等と同じ丸み（`border-radius: 20px`）・影（`box-shadow: 0 10px 24px rgba(122, 96, 55, 0.1)`）を付け、`max-width: 480px; margin: 2em auto;`で中央寄せの適度なサイズに抑えている
- リード文の直後・水やり写真の直前に、3つの強みのタイトルだけを並べた概要ブロック`.strengths-overview`（`<ul>`、`<li>`3枚）を追加（2026-10-01）。詳細（本文・画像・BASE商品ウィジェット・工賃シミュレーション）を読む前に、全体像を一目で把握できるようにする狙い。各`<li>`の文言は後続の3つの`.feature-row`内`<h3>`と完全に一致させている（本物の商品として、お客様の元へ届く／次につながるスキルが身につく／工賃もしっかり獲得できる）。見た目は`.recommend-grid .card`を参考にしたコンパクトな白カード（`display:flex; flex-wrap:wrap; gap:14px`で横並び3カラム、画面が狭い場合は自動で折り返して縦積みになる）。ラベル部分は既存の`.strength-num`クラスをそのまま流用し、`.strengths-overview .strength-num`で`display:block`のみ上書き（色・太さ・文字間隔は共通定義を継承）。新しい色変数は追加せず、既存の`--color-border`とグレーのドロップシャドウ値（他のカード類と同じ`rgba(122, 96, 55, ...)`）のみ使用
- 「利用者の声」は実際の利用者から集めた正式な声ではなかったため、「こんな方におすすめです」（利用対象者チェックリスト）に差し替え済み
- 「こんな方におすすめです」(#recommend)のカード8枚は、2026-10-01にコンパクトなチェックリスト表示へ変更（スクロール量が多く間延びして見えたため）。HTML構造（`card-grid recommend-grid`/`card`/`card-icon`/`p`）は変更せず、`style.css`に`.recommend-grid`スコープの上書きスタイルを追加：カード内をアイコン左・テキスト右の横並びに変更、paddingを32px 28px→14px 18px、アイコンの丸を56px→32px、グリッド列幅の最小値を240px→170px、カード間gapを24px→14pxに縮小。`.card-grid`/`.card`/`.card-icon`のベース定義（#service等で共用）自体は変更していない
- フレームワーク不使用でシンプルに保守できるようにする
- ヒーローセクション（`.hero`）の一番上、ロゴより前に紹介・採用動画（`.hero-video`、`images/shop-intro.mp4`）を配置（2026-09-15追加）。再生ボタン付きでミュート・自動再生はしない（動画にナレーション・字幕があるため）。顔出しスタッフが映っているが本人確認済み
- 「活動の様子」(#gallery)は静的な写真グリッドではなく、写真8枚＋動画1本を自動送りする自作スライドショー（`.slideshow`、JSは`js/main.js`内）。矢印・ドットクリックでも切り替え可能。新しい写真・動画を追加する場合は`.slideshow-slide`を1つ追加し、`.slideshow-dot`も対応する数だけ追加する
- オンラインショップの商品表示はBASE公式の「商品ウィジェット」（iframe埋め込み、`商品詳細ページURL/widget`）を使用。価格・在庫は自動で最新化されるが、新商品の追加・削除は手動でiframeを追加/削除する必要がある（BASEはショップ全体の埋め込みを2025年10月よりセキュリティ上禁止しており、一覧の自動取得はできない）
- 利用者ブログはCMS等を使わず、`blog/post-N.html`を1記事ずつ追加する静的な方式（キャリカク社サイトの日付＋カテゴリタグ＋タイトルの一覧表示を参考）。新しい記事を追加する際は、既存の`blog/post-*.html`を複製して内容を書き換え、`index.html`の`#blog`セクションのリストに1行追加する
- `#blog`のブログ一覧は新しい順3件のみ初期表示し、「もっと見る」ボタン（`#blogMoreBtn`、JSは`js/main.js`内）で残りを展開／折りたたみできる。記事が3件以下の場合はボタン自体を自動で非表示にする。CSS側で`.blog-list li[hidden] { display: none; }`が必要（`.blog-list li`が`display:flex`のため、素の`[hidden]`属性だけでは打ち消される点に注意）
- お問い合わせフォームは、サイトのデザインに合わせた自作フォーム（`#contactForm`）からGoogleフォームの送信先(`/formResponse`)へ直接POSTする方式（hidden iframeで送信し、`js/main.js`が送信後に完了メッセージを表示）。Googleフォーム標準の見た目は使っていない
  - フォーム項目とentry ID：お名前=entry.112423487（必須）／メールアドレス=entry.911916954（必須）／電話番号=entry.1613386452（必須）／ご希望の種類（体験・見学・相談）=entry.1329975269（任意）／お問い合わせ内容=entry.270639122（任意）
  - 元のGoogleフォーム側で質問の追加・削除・変更を行った場合、上記entry IDと`index.html`内のフォーム項目がずれるため、`index.html`のフォームも合わせて修正が必要
- リポジトリはGitHub Pages公開のためPublicにしている（顧客の個人情報・APIキー等は含めない）
- 工賃シミュレーションは当初（2026-10-01）「就労継続支援B型とは？」(#btype)セクション内（静的なカードグリッドの「工賃の例」から変更）に追加したが、同日中に「3つの強み」(#strengths)のSTRENGTH 03へ移動済み（上記参照）。中身は「週に何日利用しますか？」の問いかけ＋週1〜5日のラジオボタン（`#wageSimDays`、既存の`.form-radio-group`/`.form-radio`クラスを流用）、選択に応じてJS（`js/main.js`）がリアルタイムに計算した月額目安を表示する`.wage-sim-result`（内訳`#wageSimBreakdown`＋金額`#wageSimAmount`）で構成。計算ルール：基本単価は1日利用900円、月の目安利用日数＝Math.round(週の利用日数×4.33週)（1年52週÷12ヶ月＝約4.33週で算出し、小数は四捨五入。2026-10-01、当初の「×4週」は月の週数を少なく見積もりすぎていたため修正）、基本額＝900円×月の目安利用日数（週1日＝4日／週2日＝9日／週3日＝13日／週4日＝17日／週5日＝22日）。これに加えて週の利用日数に応じた段階的なボーナスを加算する（週1日・週2日：ボーナスなし／週3日：10,000円／週4日：20,000円／週5日：30,000円）。ボーナスがある日数（週3〜5日）は内訳とボーナス込み合計の両方を表示し、ボーナスなし（週1〜2日）は基本額のみを表示する（2026-10-01に、週5日のみ特別扱いしていたボーナス方式から、週3日以上に段階的にボーナスを付与する方式へ修正）。ページ読み込み時は週3日がデフォルト選択（月額目安 合計約21,700円が初期表示）。半日利用（450円/日）の情報は`.wage-sim-sub`に「※半日利用の場合は1日あたり450円で計算されます」と一言だけ補足。下に`.section-note`（既存クラスを再利用）で「※あくまで目安です。実際の工賃は作業内容や実績により変動します。」の注意書きを表示。計算ルール自体を変更する場合は`js/main.js`内の`WAGE_PER_DAY`・`WEEKS_PER_MONTH`（現在4.33）定数と、週日数→ボーナス額のマッピングである`WAGE_BONUS`オブジェクト（`{1:0, 2:0, 3:10000, 4:20000, 5:30000}`）を修正すればよい
- フッター（`.site-footer .footer-links`）に、BASE・Instagramに加えてWAMNET事業所情報・LITALICO仕事ナビへの掲載リンクを追加（2026-10-02）。いずれも`target="_blank" rel="noopener noreferrer"`で外部サイトへ新規タブ遷移
- `#contact`の`.contact-info dl`に「送迎」（無料送迎あり）「お弁当」（注文可）の項目を「利用時間」の後・「電話番号」の前に追加（2026-10-02）。`#service`の`.highlight-badges`に既にあった「送迎あり」「食事提供あり」のバッジ表示とは別に、アクセス・お問い合わせセクションでも詳細情報として案内する形
- SEO対策（2026-09-11、「就労継続支援B型事業所 鈴鹿市」での検索順位向上を目的に実施）：`index.html`・ブログ記事(`blog/post-*.html`)にcanonical・OGP（og:title等）・Twitterカードを追加。`index.html`にはLocalBusinessのJSON-LD構造化データ（施設名・住所・電話番号・sameAs）も追加。あわせて`robots.txt`・`sitemap.xml`を新規作成。新しいページ（ブログ記事等）を追加する際は、同様にcanonical・OGP・meta descriptionを設定し、`sitemap.xml`にもURLを1行追加すること

## TODO
- [ ] 利用者ブログは現在post-4（水やりについて）・post-5（写真撮影）・post-6（梱包について）・post-7（販売と写真撮影）・post-8（撮影デー）・post-9（今までの作業を通して思ったことと植物の紹介）・post-10（事業所の見学）・post-11（面談とこの前のサプライズ）・post-12（新しいことの挑戦）・post-13（今月ラスト）・post-14（初めての植え替え）・post-15（水やりと商品カード作り）を公開中。サンプル記事（post-1〜3）はarchiveへ退避済み。新しい記事が集まり次第、随時追加
- [ ] BASEで商品の入れ替えがあった際は、shopセクションのiframe（items/xxxxx/widget）を更新
- [ ] Googleビジネスプロフィールの口コミ（クチコミ）を、利用者さん・ご家族に依頼して増やしていく（「就労継続支援B型事業所 鈴鹿市」のローカル検索対策として重要。件数が少ないほど効果が大きい）

## 2026-09-11時点で確認済み・完了（Googleビジネスプロフィール・Instagram）
- Googleビジネスプロフィール：カテゴリ「障害者向けサービス＆支援組織」、営業時間「月〜金10:00-16:00」、住所・電話番号、いずれもホームページと一致を確認
- Googleビジネスプロフィールのウェブサイトリンクは既にmarushikakubase.comに更新済みだった
- Instagramをソーシャルプロフィールとして新規追加（審査待ち）
- 事業所写真（外観・店内・植物棚など）は複数枚既に登録済みで十分な状態
- Instagramのプロフィール（bioリンク）も既にmarushikakubase.comになっていることを確認済み

## 完了した公開・SEO対応（2026-09-02）
- GitHub Pagesで公開、Google Search Console登録・インデックス登録リクエスト済み
- Googleビジネスプロフィール登録済み（Googleマップに反映済みのため、サイト内への地図埋め込みは不要と判断）
- Instagram・Googleビジネスプロフィールにホームページリンクを設定済み

## 独自ドメイン接続（2026-09-03〜04）
- marushikakubase.comを取得し、GitHub Pagesのカスタムドメインとして接続完了（HTTPS化・DNS checkも成功）
- つまずいたポイント：お名前.comは「ドメインDNS設定」（Aレコード等の登録）と「ネームサーバー設定」（お名前.comのネームサーバーを実際に使うかの選択）が別画面になっており、後者を選択していなかったためDNSがいつまでも反映されなかった。「ネームサーバー設定」で「お名前.comのネームサーバーを使う」を選択したことで解決
- 今後、同じ現象（DNSレコードを設定したのに何時間経っても反映されない）が起きた場合は、まず「ネームサーバー設定」が正しく選択されているか確認する

## Search Consoleサイトマップ送信（2026-09-11）
- marushikakubase.comプロパティに`sitemap.xml`を送信し、ステータス「成功」を確認

## 最終更新日
2026-10-07（利用者ブログに新規記事post-15「水やりと商品カード作り」を追加。`index.html`の一覧・`sitemap.xml`も更新。先にpost-14〔初めての植え替え〕が公開済みだったため、番号をpost-15に振り直した）

2026-10-05（利用者ブログにpost-14「初めての植え替え」を追加。`index.html`の一覧・`sitemap.xml`も更新）

2026-10-05（Search Console実績〔9/2〜10/2：表示1,040回・クリック41回・平均順位4.2位。一般検索はクリック0〜少数〕を受けて、`index.html`のtitle・meta description・og/twitterの文面を「鈴鹿市の就労継続支援B型｜見学・体験受付中｜まるしかくベース」へ変更し、JSON-LDに営業時間〔月〜金10:00-16:00〕を追加。効果は2〜4週間後にSearch ConsoleのCTRで確認する。旧URL〔github.io〕がGoogle検索に残っている件は、HP側は`marushikakubase.com`に統一済みのため、GitHub Pages設定とSearch ConsoleのURL検査での確認が必要）

2026-10-02（`#strengths`の`.feature-row`の並びを「テキストが先、画像・ウィジェットが後」に統一し、未使用になった`.feature-row.reverse`をCSSから削除／フッターにWAMNET事業所情報・LITALICO仕事ナビへのリンクを追加／`#contact`の`dl`に「送迎」「お弁当」の項目を追加）

2026-10-01（3つの強みセクションにSTRENGTH01の前に水やり写真を追加、STRENGTH01のBASE商品ウィジェットを異なる植物2種に差し替え、`.strength-num`の表記を「STRENGTH 01/02/03」から「強み01/02/03」に変更、`#strengths`の見出しを「植物を育てながら、ちゃんと働く」から「植物を育てながら、『できる』を増やしていく」に変更、リード文と水やり写真の間に3つの強みのタイトルだけをまとめた概要ブロック`.strengths-overview`を追加）
