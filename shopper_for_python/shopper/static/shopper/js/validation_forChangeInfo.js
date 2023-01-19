/**
 * validation.jsで作成したバリデーションを会員情報変更画面に設定
 */
// 各選択肢にバリデーションをかける
activateExistingMailValidation('email_outline', 'email', 'main_form', 'subm1');
activateValidation('name_outline', 'name', 'main_form', 'subm1');
activateRadioValidation('gender_outline', 'gender', 'invalid-feedback-gender', 'main_form', 'subm1');
activateValidation('region_outline', 'region', 'main_form', 'subm1');
activateValidation('prefecture_outline', 'prefecture', 'main_form', 'subm1');
activateValidation('area_outline', 'area', 'main_form', 'subm1');

// 会員情報変更でのみ必要なバリデーション
activateValidation('pass_outline', 'password', 'sub_form', 'subm2');
activateValidation('newpass_outline', 'newpassword1', 'sub_form', 'subm2');
activateDoublePassValidation('newpass2_outline', 'newpassword2', 'newpassword1', 'sub_form', 'subm2');