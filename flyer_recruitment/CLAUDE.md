# flyer_recruitment（利用者募集チラシ）

## 概要
就労継続支援B型事業所「まるしかくベース」の利用者募集用チラシ（A4縦・印刷配布用）。
見学・体験希望者やご家族、相談支援専門員に向けて、植物に囲まれた明るい事業所の雰囲気と、
育成→撮影→商品化→販売→梱包発送までの作業内容を直感的に伝えることを目的とする。

## 技術スタック
- HTML + CSS（単一ファイル index.html、外部フレームワーク不使用）
- QRコード生成: `qrcode` npm パッケージ v1.4.4 の browser 向けビルドをローカル同梱（vendor/qrcode.min.js、オフラインで動作・外部送信なし）
- アクセスマップ: 外部地図サービスは使わず、道路・ランドマークを手描き風に表現した簡易SVGマップを自作（index.html内に直接記述）
- 印刷対応: `@page { size: A4; }` ＋ `.page` を 210mm×297mm 固定で実装。ブラウザの印刷機能でPDF化・印刷する想定
- 画像: homepage側の実写真・ロゴ、およびユーザーから追加で受け取った実写真を使用（images/配下にコピーして同梱、homepageフォルダへの相互参照はしていない）

## 重要なID設定値
- Instagram遷移先URL: `https://www.instagram.com/marushikakube_su/`（index.html内のQRコード生成スクリプトに直書き）
- 住所: 〒513-0801 三重県鈴鹿市神戸8丁目6-16
- TEL: 059-358-8866
- Web: marushikakubase.com
- アクセス: 鈴鹿市駅から徒歩4分（アクセスマップ・見出しに記載）

## ファイル構成
- `index.html` … チラシ本体（レイアウト・スタイル・QRコード生成スクリプト・アクセスマップSVGを含む）
- `vendor/qrcode.min.js` … QRコード生成ライブラリ（ローカル同梱、オフライン動作）
- `images/logo.png` … ロゴ画像（homepage/images/logo.pngと同一ファイルをコピー）
- `images/hero-exterior.jpg` … メインビジュアル4枚のうち「事業所外観」（homepage/images/shop-exterior.jpgと同一）
- `images/hero-plants.jpg` … メインビジュアル4枚のうち「事業所内販売スペース」（モンステラ等が並ぶ事務所内のようす）
- `images/hero-studio.jpg` … メインビジュアル4枚のうち「商品撮影スペース」（旧step-photo.jpg。撮るアイコンの写真差し替えにあわせ分離）
- `images/hero-pc.jpg` … メインビジュアル4枚のうち「PC作業スペース」（旧step-pc.jpg、モニターが並ぶ作業スペース。PCで作業するアイコンの写真差し替えにあわせ分離）
- `images/step-grow.jpg` … 「育てる」工程の写真（homepage/images/shop-watering.jpg、水やりのようす）
- `images/step-photo.jpg` … 「撮る」工程の写真（スマートフォンで商品の植物を撮影しているようす）
- `images/step-sell.jpg` … 「売る」工程の写真（お客様に商品の植物をお渡ししているようす。顔部分はユーザー側で絵文字により加工済み）
- `images/step-ship.jpg` … 「届ける」工程の写真（homepage/images/shop-packing.jpg、梱包のようす）
- `images/step-pc.jpg` … 「PCで作業する」工程の写真（1人でモニターに向かい作業しているようす）
- `archive/hero-placeholder.svg` … 初版で使用していたヒーロー用イラスト（実写真に差し替え済みのため退避）
- `archive/hero-photo-shelf.jpg` … メインビジュアルで使っていた「店内の植物棚」の写真（5枚→4枚化にともない削除、参考用に保持）

## 設計の意図
- 一般的な福祉施設チラシの堅い印象を避け、植物ショップ／クリエイティブワークスペースのような明るく親しみやすいデザインを意図（余白を多く確保）
- 配色はhomepage（homepage/css/style.css の`:root`変数）と完全に統一している：
  --accent #EF9D2E（homepageの--color-primary）／--accent-dark #C97A17（同--color-primary-dark）／
  --accent-tint #FCE6BD（同--color-accent-soft）／--paper #FFFAF3（同--color-bg）／
  --ink #4A3F35（同--color-text）／--ink-soft #7A6F63（同--color-text-light）／--border #F0DDB8（同--color-border）。
  homepageの配色を変更した場合はこちらも合わせて更新すること
- ロゴ画像（.mark）は丸型にトリミングして表示（border-radius:50%）
- メインビジュアルは1枚の横長写真ではなく、写真4枚（事業所外観・事業所内販売スペース・商品撮影スペース・PC作業スペース、この順で左から）を横一列4列のグリッドで配置し、各写真の下にキャプション（figcaption）を添えている
- 「作業の流れ」は 育てる→撮る→PCで作業する→売る→届ける の順（当初は売る・届けるの後にPCで作業するを置いていたが、「撮るの後にもってきて」との指示で並び替え）
- 「作業の流れ」の売る・撮る・PCで作業するの3アイコンは、メインビジュアルとは別の写真をそれぞれ使用している（images/step-sell.jpg・step-photo.jpg・step-pc.jpg）。
  これらは当初メインビジュアルと共用していたが、都度「ヒーロー部分はさっきのまま」との指示があったため、メインビジュアル側は元の写真を別ファイル（hero-exterior.jpg／hero-studio.jpg／hero-pc.jpg）として保持し、作業の流れアイコン側だけ新しい写真に差し替える、という方針で統一している。今後さらに写真を差し替える依頼が来た場合もこの方針（ヒーローとアイコンは別ファイルで管理）を踏襲すること
- 写真が正方形（1280×1280）なのに対しメインビジュアルの1セル（.photo-frame）は横長のため、`background-size:cover`だと写真の大部分が切れてしまう。「写真全体が見えるように」という指示に合わせ`background-size:contain`を採用し、セル背景色（--accent-tint）を余白として見せることで、トリミングなしで全体を表示している。
  実装はCSS Gridの各セル（.photo-frame）に背景画像（background-image/background-position/background-size:contain）を敷く方式。`<img>`+`object-fit`ではなく背景画像方式にしているのは、CSS Gridの行高さが画像の縦横比の影響で意図通りに計算されない不具合が確認されたため（`.photo-frame`の高さを`45mm`のように絶対値で固定した上で背景画像方式にすることで回避）
- アクセスマップは、ユーザーが提示した既存チラシの手描き風マップ（道路・河川・最寄り駅／市役所／小学校などのランドマーク・方位磁針・目的地への赤矢印）を参考に、同じ構成要素をSVGで再現。CTAバナーとフッターの間に専用セクション（.access）として配置し、見出しに「鈴鹿市駅から徒歩4分」を明記
- QRコードは外部サービスに情報を送らず、ローカルのJSライブラリでオフライン生成
- 画像を今後差し替える場合は、`images/`内の同名ファイルを上書きするだけでよい構造にしている

## TODO
- [ ] 印刷時の発色・QRコードの読み取り精度を実機プリンタで確認する
- [ ] 内容確定後、marushikakubase.com のトップページ等からもチラシPDFへのリンクを検討
- [ ] アクセスマップは簡易的な手描き風の模式図であり、正確な縮尺・全ての道路は反映していない。掲載後に周辺情報（道路形状・ランドマークの位置関係）に誤りがないか実際の地図と照らして確認する

## 最終更新日
2026-09-16（メインビジュアルを実写真4枚・横一列・キャプション付き・トリミングなし表示に変更、作業の流れの順序変更とPC作業アイコンの写真差し替え、手描き風アクセスマップを追加、配色をhomepageと完全統一、ロゴを丸型トリミングに変更）
