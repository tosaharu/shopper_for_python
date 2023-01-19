/**
 * validation.jsで作成したバリデーションを商品登録画面に設定
 */
// 商品登録画面で必要なバリデーション
activateValidation('date_outline', 'date', 'main_form', 'main_subm');
activateValidation('region_outline', 'region', 'main_form', 'main_subm');
activateValidation('prefecture_outline', 'prefecture', 'main_form', 'main_subm');
activateValidation('area_outline', 'area', 'main_form', 'main_subm');
activateValidation('store_outline', 'store', 'main_form', 'main_subm');
activateSelect2Validation('item_outline', 'main_form', 'main_subm');
activateValidation('detail_outline', 'detail', 'main_form', 'main_subm');
activateValidation('price_outline', 'price', 'main_form', 'main_subm');
activateValidation('amount_outline', 'amount', 'main_form', 'main_subm');
activateValidation('discount_outline', 'discount', 'main_form', 'main_subm');
activateValidation('comment_outline', 'comment', 'main_form', 'main_subm');

// 店舗情報新規登録で必要なバリデーション
activateValidation('store_region_outline', 'store_region', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_prefecture_outline', 'store_prefecture', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_area_outline', 'store_area', 'register_store_modal_form', 'register_store_modal_subm');
activateExistingStoreValidation('store_name_outline', 'store_name', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_address_outline', 'store_address', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_start_hour_outline', 'store_start_hour', 'register_store_modal_form', 'register_store_modal_subm');
activateValidation('store_end_hour_outline', 'store_end_hour', 'register_store_modal_form', 'register_store_modal_subm');

// 品目新規登録で必要なバリデーション
activateExistingItemValidation('item_name_outline', 'item_unit_outline', 'item_name', 'item_unit', 'register_item_modal_form', 'register_item_modal_subm');
activateValidation('item_unit_outline', 'item_unit', 'register_item_modal_form', 'register_item_modal_subm');
