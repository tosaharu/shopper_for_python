/**
 * validation.jsで作成したバリデーションをパスワード再設定画面に設定
 */
// パスワード再設定でのみ必要なバリデーション
activateValidation('newpass_outline', 'newpassword1', 'main_form', 'subm1');
activateDoublePassValidation('newpass2_outline', 'newpassword2', 'newpassword1', 'main_form', 'subm1');