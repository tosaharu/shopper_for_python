/**
 *　validation.jsで作成したバリデーションを新規登録画面に設定
 */
// 各選択肢にバリデーションをかける
activateExistingMailValidation('email_outline', 'email', 'main_form', 'subm1');
activateValidation('name_outline', 'name', 'main_form', 'subm1');
activateRadioValidation('gender_outline', 'gender', 'invalid-feedback-gender', 'main_form', 'subm1');
activateValidation('region_outline', 'region', 'main_form', 'subm1');
activateValidation('prefecture_outline', 'prefecture', 'main_form', 'subm1');
activateValidation('area_outline', 'area', 'main_form', 'subm1');

// 新規登録でのみ必要なバリデーション
activateValidation('pass_outline', 'password1', 'main_form', 'subm1');
activateDoublePassValidation('pass2_outline', 'password2', 'password1', 'main_form', 'subm1');
activateValidation('year-select_outline', 'year-select', 'main_form', 'subm1');
activateValidation('month-select_outline', 'month-select', 'main_form', 'subm1');
activateValidation('day-select_outline', 'day-select', 'main_form', 'subm1');