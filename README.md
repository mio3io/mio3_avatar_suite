# Mio3 Avatar Tools

アバター編集用のサポートツール「Mio3 Bones」からに名前を変更してアバター編集まわりの統合ツールになる予定。現在の名前は暫定です。

## 導入方法

[Code > Download ZIP](https://github.com/mio3io/Mio3Bones/archive/master.zip) から ZIP ファイルをダウンロードします。
Blender の `Edit > Preferences > Addons > Install` を開き、ダウンロードしたアドオンの ZIP ファイルを選択してインストールボタンを押します。インストール後、該当するアドオンの左側についているチェックボックスを ON にします。

## 機能

右クリックメニューと、アーマチュアのメニューに追加されます

### 追加＞アーマチュア

VRChat用の Humanoid アーマチュアを追加しまう

### アーマチュア＞トランスフォーム

-   ボーンを均等にする
-   ボーンを整列する（先頭と末端ボーンを基準）

### アーマチュア＞名前

-   ボーンに通し番号をふる

### サイドバー＞ Mio3 タブ

-   ボーン名のフォーマットの一括変換（実験的）ポーズモードで表示されているボーンを任意のフォーマットに変換

実験的に追加しています。うまく変換されるかわからないため変換後に確認してください。

元の名前が一定のパターンにあてはまるものでないとうまく変換されないことがあります。
表示されているものだけを変換する仕様になっているため、必要な部分のみ変換してください。

変換後のフォーマットは現在「UpperArm_L」と「UpperArm.L」のみになっています。

認識されるパターン例

-   UpperArm_L
-   Upper Arm_L
-   Upper_Arm_L
-   UpperArm.L
-   Upper Arm.L
-   Upper_Arm.L
-   L_UpperArm
-   LeftUpperArm
-   UpperArmLeft
-   Hair
-   HairFront.001
-   HairFront.end
-   HairFront_L.001
-   (CustomPrefix\_)Arm_L

カスタムプレフィックス

-   IK_UpperArm_L を IK_UpperArm.L のように変換したい場合は、カスタムプレフィックスに「IK_」を登録するとそのまま使用されます。また、不要なプレフィックスを削除することもできます。

<!--
おそらく期待どおりに変換されないパターン

-   IK_Arm_L のような大文字が続くパターンは I と K は分離され I_K_Arm_L のように扱われるため、カスタムプレフィックスとして登録してください（IK_を登録するとそのまま使用されます）
-->