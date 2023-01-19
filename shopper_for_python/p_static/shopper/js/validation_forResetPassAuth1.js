/**
 * validation.jsで作成したバリデーションをパスワード再設定認証画面に設定
 */
// パスワード債発行用選択肢にバリデーションをかける
activateValidation('email_outline', 'email', 'main_form', 'subm1');
activateValidation('year-select_outline', 'year-select', 'main_form', 'subm1');
activateValidation('month-select_outline', 'month-select', 'main_form', 'subm1');
activateValidation('day-select_outline', 'day-select', 'main_form', 'subm1');