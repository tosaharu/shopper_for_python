/**
 * validation.jsで作成したバリデーションを店舗情報画面に設定
 */

// 店舗情報編集で必要なバリデーション
activateValidation('store_region_outline', 'store_region', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_prefecture_outline', 'store_prefecture', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_area_outline', 'store_area', 'register_store_modal_form', 'register_store_modal_subm');
activateExistingStoreValidation('store_name_outline', 'store_name', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_address_outline', 'store_address', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_start_hour_outline', 'store_start_hour', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_end_hour_outline', 'store_end_hour', 'register_store_modal_form', 'register_store_modal_subm');