# Shopper(Python)  
  
β版リリース: 2023/1/19  
開発期間: 1か月  
URL: https://hasa.pythonanywhere.com/shopper/  
  
  
## アプリ概要  
  
自分のお得な買い物リストを作れる、家計応援アプリです。  
  
「なるべくおトクに買えるお店を知りたい・・・」  
「商品ごとに行くべきお店の一覧が欲しい・・・」  
  
  
そんな **とにかく安く、効率よく** 買い物をしたいあなたにピッタリ！  
  
## 使い方

1. 自分が買った/気になっている商品の情報を投稿する
1. その商品の品目ごとに、自分の投稿情報と他のユーザーの投稿情報リストが生成される

## 使用技術

- フロントエンド

  - Javascript / jQuery 3.6.0
  - HTML / CSS / SCSS / Bootstrap 5.0
  
- バックエンド

  - Python 3.11.0 / Django 4.1.5
  
- インフラ

  - Docker 20.10.21 / docker-compose 3.9
  - MySQL 8.0.3 / MySQLWorkbench 8.0.31
  
- その他ツール

  - Visual Studio Code

※もともとJava 11(JavaEE,Eclipse)で作成したアプリケーションを、Python(Django)で作り直し機能改修しています。  
　（無料のデプロイ先を使用したい、今後機械学習等のライブラリも使用してみたいという理由）  
　Javaでも同等のアプリケーションを作成することが可能です。  
　https://github.com/tosaharu/open

## 機能一覧

- ユーザー登録関連
  - 新規登録
  - パスワード再設定
    - 2段階認証
  - ログイン/ログアウト
  - 登録情報変更
  - 退会（論理削除）
 
 - 管理画面

 - 商品情報投稿
   - 商品新規登録
   - 店舗新規登録
     - 入力サジェスト機能　※デプロイ先でスクレイピング使用不可の関係で現在停止中
     - 類似登録防止機能
   - 商品品目新規登録
     - 類似登録防止機能
   
 - メイン画面
     - 品目ごと安値投稿リスト表示（自分/他人それぞれ5件ずつ）
       - エリア絞り込み（複数選択可能）
       - ソート切り替え

 - 店舗情報
     - 店舗情報編集

 - 問い合わせフォーム
 
 - レスポンシブル対応
 
 - リアルタイムバリデーション

## こだわった点

 - ユーザビリティを向上に力を入れました  
   
   - フロントでのバリデーションを充実
     - ajaxを利用したDB参照
     - pattern属性での正規表現指定
     - 2項目を参照したうえで発生する等のやや特殊なバリデーション  
     …etc
   - ページ内でのデータ更新には基本的にajax通信を利用
     - メイン画面でのエリア変更やソート変更時
     - 商品登録時の店舗・品目の新規登録時  
     …etc
   - 入力フォーム補助
     - ユーザー情報をもとにしたデフォルト表示
     - スクレイピングを利用した入力サジェストを実装
   - 重いクエリの調整
     - メイン画面の描画時間を2.4秒⇒0.5秒に向上
       - N+1問題の緩和
       - distinct()不使用
 - データの作成・更新方法を工夫しました
   - 当初、ユーザーが投稿する商品の品目は運営側で分類・網羅する予定だったが工数的に現実的ではなかったため、一定数を用意しつつあとはユーザーがそれに倣っていれていく形式を取りました
     - 上記のようにユーザーが更新するため、DB既存データとの完全一致を除外し、類似を警告するという形で、登録不可バグが発生しないように注力しつつ重複登録を避ける仕様を実装
 
 - レスポンシブル対応に注力しました
   - PCサイズ・スマホどちらでも視認性、操作性が保てるように
   - スマホはiOS/Android両方の実機でチェックと不具合修正を実施

## 画面イメージ

- アプリトップ  
<img src="https://user-images.githubusercontent.com/115526019/213859881-cc3512e4-c9fa-495e-8663-c9ec4dc51fd9.png" alt="shopper_" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213859898-fe99f0f1-0d92-4f4d-b32b-812c31c47626.png" alt="shopper_ (1)" width="50%">

- 新規会員登録画面  
<img src="https://user-images.githubusercontent.com/115526019/213859912-7f7f16df-a5a1-4b01-92ab-22bea7a7dc34.png" alt="u_RegisterUser_" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213859924-7c90020e-a9b5-40c6-98e8-5c2aea70ca8f.png" alt="u_RegisterUser__ (1)" width="50%">

- メイン画面  
<img src="https://user-images.githubusercontent.com/115526019/213859941-226a3185-2806-40b5-9b8c-7a19a622a82e.png" alt="u_Main_" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213859955-85b4144c-bd75-4dd9-bcc0-bda7c9cb7eb2.png" alt="u_Main_ (1)" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213861137-1b4144a5-4675-4798-acf7-e15d56886430.png" alt="u_Main_ (2)" width="50%">

- 商品登録画面  
<img src="https://user-images.githubusercontent.com/115526019/213859992-90ad3604-2c41-48dc-a7d9-a606798ae1c1.png" alt="u_RegisterProduct_" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213860005-bef0af68-3316-400f-8024-dce45a07972a.png" alt="u_RegisterProduct_ (1)" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213860004-6761c7db-76fc-4c05-9838-e126cbbebde2.png" alt="u_RegisterProduct_ (2)" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213860003-13d26feb-bd26-4899-b416-e6f69711810a.png" alt="u_RegisterProduct_ (3)" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213860001-b5fd2430-9742-4536-b5dd-fab941886355.png" alt="u_RegisterProduct_ (4)" width="50%">

- 店舗情報画面  
<img src="https://user-images.githubusercontent.com/115526019/213860033-7d309b87-e80a-49c5-b0e1-b3842290e332.png" alt="u_StoreInfo_7" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213860039-0ca027de-d758-4a95-80dd-6e792ce16f13.png" alt="u_StoreInfo_7 (1)" width="50%">

- 会員情報画面  
<img src="https://user-images.githubusercontent.com/115526019/213860048-a8476f8b-6ad8-4c61-997e-291528a4e97b.png" alt="u_ChangeInfo_" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213860050-acad55c4-8c98-436d-87de-9d002b6a5271.png" alt="u_ChangeInfo_ (1)" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213860056-857b39bf-2bd1-4597-8bd7-2a9c99244a4f.png" alt="u_ChangeInfo_ (2)" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213860065-407d0c5b-0f61-470e-85cb-6f20397568d5.png" alt="u_ChangeInfo_ (3)" width="50%">

- 退会画面  
<img src="https://user-images.githubusercontent.com/115526019/213860082-0c20b2f1-128a-491c-a382-7d623ef8c5d7.png" alt="u_Quit_" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213860093-0f18e3ba-a923-4dee-b474-7e2f61665f9e.png" alt="u_Quit_ (1)" width="50%">

- お問い合わせ画面  
<img src="https://user-images.githubusercontent.com/115526019/213860113-d010de5e-11f3-41ac-9e4d-ddb75b275bb2.png" alt="u_Inquiry_" width="50%">

- ログイン/ログアウト画面  
<img src="https://user-images.githubusercontent.com/115526019/213860122-c65697f5-fd4f-4588-b1e2-171ef3fc37bf.png" alt="u_Login_" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213862690-df7c165e-6a99-4a1d-93ab-12edb0d149dd.png" alt="u_Logout_" width="50%">

- パスワード再設定画面  
<img src="https://user-images.githubusercontent.com/115526019/213863065-ee255a0d-8ce1-4e61-bf06-b1937d6a8135.png" alt="u_ResetPasswordAuth_" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213863123-6717ede1-7e20-48a3-ba30-f5defde1faf9.jpg" alt="u_ResetPasswordAuth_ (1)" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213862405-b3d8f23a-8a65-43c5-9a46-0c750c05aa36.png" alt="u_ResetPasswordAuth_ (2)" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213862404-b74d3de9-0705-4058-ad06-3df782906288.png" alt="u_ResetPassword_" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213863182-59bdecc2-1fb2-4622-9bab-5d13a4943866.jpg" alt="u_ResetPassword_ (1)" width="50%"><img src="https://user-images.githubusercontent.com/115526019/213862402-a16d44ee-9a3a-4068-8b9c-d4bc6fd6cba5.png" alt="u_ResetPassword_ (2)" width="50%">
