/**
 * 商品登録画面
 * 
 * ・日付入力関連の処理
 * ・入力エリアに即した店舗を表示する処理
 * ・店舗新規登録時の入力サジェスト処理
 * ・店舗新規登録処理
 * ・品目新規登録処理
 */

// 日付入力欄を今日までしか選択できないように制限
window.addEventListener('DOMContentLoaded', () => {
    let today = new Date();
    today.setDate(today.getDate());
    let yyyy = today.getFullYear();
    let mm = ("0" + (today.getMonth() + 1)).slice(-2);
    let dd = ("0" + today.getDate()).slice(-2);
    let formatDate = yyyy + '-' + mm + '-' + dd;
    let dateInput = document.getElementById('date');
    dateInput.setAttribute('max', formatDate);
})

// 今日を選択するボタンを作成
function today_select() {
    var today = new Date();
    today.setDate(today.getDate());
    var yyyy = today.getFullYear();
    var mm = ("0" + (today.getMonth() + 1)).slice(-2);
    var dd = ("0" + today.getDate()).slice(-2);
    document.getElementById("date").value = yyyy + '-' + mm + '-' + dd;
}

// エリア選択に関する処理
let area_select_button = document.getElementById('area');
area_select_button.addEventListener('input', function () {
    ShowSelectedAreaStoreSelection();
});


// 選択していているエリアに合わせた店舗を表示する
function ShowSelectedAreaStoreSelection() {
    $.ajax({
        url: "Ajax_GetStore/",
        type: "GET",
        data: { area: $('#area').val() }
    }).done(function (result) {
        //通信成功時のコールバック
        console.log(result);
        console.log($('#store'));

        // 既存リストの削除
        $('#store').children().remove();
        // 選択都道府県のリストを挿入
        $('#store').append(result);


    }).fail(function () {
        //通信失敗時のコールバック
        console.log("通信失敗");

    }).always(function () {
        //常に実行する処理
    })
};

/**
 * 店舗登録モーダルに関する処理
 */

// モーダル起動ボタンの取得
let register_store_subm = document.getElementById('register_store_subm');


//モーダル起動ボタンを押下した際にエリアデータをモーダルに反映する処理
register_store_subm.addEventListener('click', () => {
    let region = document.getElementById('region').value;
    let prefecture = document.getElementById('prefecture').value;
    let area = document.getElementById('area').value;
    console.log(region);
    console.log(prefecture);
    console.log(area);

    let targetRegion = document.querySelector('#store_region>option[value="' + region + '"]');
    targetRegion.selected = true;
    let targetPrefecture = document.querySelector('#store_prefecture>option[value="' + prefecture + '"]');
    targetPrefecture.selected = true;
    let targetArea = document.querySelector('#store_area>option[value="' + area + '"]');
    targetArea.selected = true;
})


// モーダル内の地域選択に関する処理
let store_region_select_button = document.getElementById('store_region');
store_region_select_button.addEventListener('input', function () {
    Store_ShowSelectedRegionPrefectureSelection(this);
})

// モーダル内の都道府県選択に関する処理
let store_prefecture_select_button = document.getElementById('store_prefecture');
store_prefecture_select_button.addEventListener('input', function () {
    Store_ShowSelectedPrefectureAreaSelection();
});

//モーダル内の、地域のプルダウンボタンが変更された際の処理
function Store_ShowSelectedRegionPrefectureSelection(obj) {

    let region = obj.value;
    let prefecture_selector = document.getElementById('store_prefecture');

    // 選択地域の変更に応じて、選択可能な都道府県を表示する
    hidden_list = document.querySelectorAll('#store_prefecture>[data-region_id]');
    for (let i = 0; i < hidden_list.length; i++) {
        hidden_list[i].setAttribute("hidden", "");
        hidden_list[i].setAttribute("disabled", "");
    }
    display_list = document.querySelectorAll('#store_prefecture>[data-region_id="' + region + '"]')
    for (let i = 0; i < display_list.length; i++) {
        display_list[i].removeAttribute("hidden");
        display_list[i].removeAttribute("disabled");
    }

    // 選択地域を変更した際に、対象外の都道府県・エリア・店舗の選択をリセットする
    let index = prefecture_selector.selectedIndex;
    let p_region = document.querySelectorAll('#store_prefecture>[data-region_id]')[index].dataset.region_id;
    console.log(p_region);
    if (p_region != region) {
        // 都道府県の選択をリセット
        prefecture_selector.options[0].selected = true;
        // エリアの選択をリセット
        Store_ShowSelectedPrefectureAreaSelection()
    }
}


// モーダル内の、選択していている都道府県に合わせたエリアを表示する
function Store_ShowSelectedPrefectureAreaSelection() {
    $.ajax({
        url: "Ajax_GetArea/",
        type: "GET",
        data: { prefecture: $('#store_prefecture').val() }
    }).done(function (result) {
        //通信成功時のコールバック
        console.log(result);
        console.log($('#store_area'));

        // 既存リストの削除
        $('#store_area').children().remove();
        // 選択都道府県のリストを挿入
        $('#store_area').append(result);

    }).fail(function () {
        //通信失敗時のコールバック
        console.log("通信失敗");

    }).always(function () {
        //常に実行する処理
    })
};

/**
 * 新規店舗登録のサジェストに関する処理
 * ※デプロイ先が対応していなかったのでOFFに
 */

// //店舗名をサジェストをする
// store_name_form = document.getElementById("store_name");

// store_name_form.addEventListener('input', () => {
//     Ajax_SearchStoreName();
// })
// function Ajax_SearchStoreName() {
//     let store_area = $('#store_area').children(":selected").text();
//     console.log(store_area)
//     $.ajax({
//         url: "Ajax_SearchStoreName/",
//         type: "GET",
//         data: {
//             store_area: store_area,
//             store_name: store_name_form.value,
//         }
//     }).done(function (result) {
//         //通信成功時のコールバック
//         console.log("通信成功");
//         console.log(result);
//         $("#name-candidate").children().remove();
//         $("#name-candidate").append(result);

//     }).fail(function () {
//         //通信失敗時のコールバック
//         console.log("通信失敗");

//     }).always(function () {
//         //常に実行する処理
//     })
// };

// //店舗住所のサジェストをする
// store_name_form.addEventListener('blur', () => {
//     Ajax_SearchStoreAddress();
// })
// function Ajax_SearchStoreAddress() {
//     let store_area = $('#store_area').children(":selected").text();
//     console.log(store_area)
//     $.ajax({
//         url: "Ajax_SearchStoreAddress/",
//         type: "GET",
//         data: {
//             store_name: store_name_form.value,
//             store_area: store_area,
//         }
//     }).done(function (result) {
//         //通信成功時のコールバック
//         console.log("通信成功");
//         console.log(result);
//         $("#address-candidate").children().remove();
//         $("#address-candidate").append(result);

//     }).fail(function () {
//         //通信失敗時のコールバック
//         console.log("通信失敗");

//     }).always(function () {
//         //常に実行する処理
//     })
// };

/**
 * 新規店舗登録に関する処理
 * １．類似情報をチェックし、あれば確認モーダルを表示
 * ２．記載の情報をDB登録
 * ３．店舗を今登録したもので選択済みにする
 * ４．モーダルを閉じる
 * ５．モーダルの値をリセット
 */

// 店舗登録モーダルに、bsのモーダル用functionを使用できるように（参考元ではmodule化=>impotして使用していたが、bootstrap.クラス名でも呼び出し可なのでそちらで）
let register_store_modal = document.getElementById('register_store_modal');
let register_store_modal_obj = new bootstrap.Modal(register_store_modal);

// 店舗登録確認モーダルに、bsのモーダル用functionを使用できるように（参考元ではmodule化=>impotして使用していたが、bootstrap.クラス名でも呼び出し可なのでそちらで）
let confirm_store_modal = document.getElementById('confirm_store_modal');
let confirm_store_modal_obj = new bootstrap.Modal(confirm_store_modal);

// 起動ボタンの取得
let register_store_modal_subm = document.getElementById('register_store_modal_subm');

// 登録しようとしている店舗名をチェックし、類似情報があれば警告のモーダルを表示
register_store_modal_subm.addEventListener('click', () => {
    // store_idが存在する場合に設定（店舗情報画面でも使用するため）
    let store_id = 0;
    if ($('#store_id').length) {
        store_id = $('#store_id').val();
    }
    let store_name = $('#store_name').val();
    $.ajax({
        url: "Ajax_CheckSimilarStoreInfo/",
        type: "GET",
        data: {
            store_name: store_name,
            store_id: store_id,
        },
    }).done(function (result_list) {
        //通信成功時のコールバック
        console.log(result_list);
        if (result_list.length > 0) {
            console.log("類似情報があります");
            console.log(document.getElementById('registering_store_name'));
            document.getElementById('registering_store_name').innerHTML = "「" + store_name.replace(/\s+/g, "") + "」";
            let target = document.getElementById('similar_storelist');
            while (target.lastChild) {
                target.removeChild(target.lastChild);
            }
            for (result of result_list) {
                let li_element = document.createElement('li');
                li_element.textContent = result;
                target.appendChild(li_element);
            }
            confirm_store_modal_obj.show();

        } else {
            console.log("類似情報がありません");
            // そのまま登録処理へ
            Ajax_RegisterStoreInfo()
        }

    }).fail(function (result) {
        console.log("通信失敗");

    }).always(function (result) {
        //常に実行する処理
        console.log("通信完了");
    })
})

// 店舗確認モーダルの登録ボタンに設定
let confirm_store_modal_subm = document.getElementById("confirm_store_modal_subm");

confirm_store_modal_subm.addEventListener('click', () => {
    Ajax_RegisterStoreInfo();
})

/**
 * 店舗データ登録処理
 * ・データの登録
 * ・登録した店舗を選択状態にする
 * ・店舗登録モーダルと、確認モーダルがる場合はそれを閉じる
 * ・モーダルの値をリセットする
 */
function Ajax_RegisterStoreInfo() {
    let store_name = $('input[name="store_name"]').val().replace(/\s+/g, "");
    let store_region = $('select[name="store_region"]').val();
    let store_prefecture = $('select[name="store_prefecture"]').val();
    let store_area = $('select[name="store_area"]').val();
    $.ajax({
        url: "Ajax_RegisterStoreInfo/",
        type: "POST",
        data: {
            store_name: store_name,
            store_area: store_area,
            store_address: $('input[name="store_address"]').val(),
            store_start_hour: $('input[name="store_start_hour"]').val(),
            store_end_hour: $('input[name="store_end_hour"]').val(),
            store_URL: $('input[name="store_URL"]').val(),
            store_tel: $('input[name="store_tel"]').val(),
            store_payment: $('input[name="store_payment"]').val(),
            store_facility: $('input[name="store_facility"]').val(),
            store_service: $('input[name="store_service"]').val(),
        },
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }).done(function (result) {
        //通信成功時のコールバック

        // モーダルで入力したエリア情報を選択済にする
        let targetRegion = document.querySelector('#region>option[value="' + store_region + '"]');
        targetRegion.selected = true;
        let targetPrefecture = document.querySelector('#prefecture>option[value="' + store_prefecture + '"]');
        targetPrefecture.selected = true;
        let targetArea = document.querySelector('#area>option[value="' + store_area + '"]');
        targetArea.selected = true;

        // 店舗情報を選択済にする

        // 新規登録完了した店舗idを取得する
        let storeId = Number(result);

        // selectタグを取得する
        let select = document.getElementById("store");
        // optionタグを作成する
        let option = document.createElement("option");
        // optionタグのテキストにstoreNameを設定する
        option.text = store_name;
        // optionタグのvalueにstoreIdを設定する
        option.value = storeId;
        // optionタグにselected属性を追加する
        option.setAttribute('selected', true);
        // selectタグの子要素にoptionタグを追加する
        select.appendChild(option);

        // モーダルを閉じる
        confirm_store_modal_obj.hide();
        register_store_modal_obj.hide();

        // モーダルのフォームを空に
        let form_element = document.getElementById('register_store_modal_form');
        form_element.reset();

        // バリデーション解除
        let validated = $('div.register_store_modal_outline')
        validated.removeClass('was-validated');
        // 自作バリデーションは、is-valid/is-invalidをフォーム自体に持っているので除去
        let input = $('#store_name');
        if (input.hasClass('is-valid')) {
            input.removeClass('is-valid');
        }
        if (input.hasClass('is-invalid')) {
            input.removeClass('is-invalid');
        }

    }).fail(function (result) {
        console.log("通信失敗");

    }).always(function (result) {
        //常に実行する処理
        console.log("通信完了");
    })
}

/**
 * 品目登録モーダル内の登録ボタンを押下した際の流れ
 * １．類似情報をチェックし、あれば確認モーダルを表示
 * ２．記載の情報をDB登録
 * ３．品目を今登録したもので選択済みにする
 * ４．モーダルを閉じる
 * ５．モーダルの値をリセット（余裕があれば）
 */

// 品目登録モーダルに、bsのモーダル用functionを使用できるように（参考元ではmodule化=>impotして使用していたが、bootstrap.クラス名でも呼び出し可なのでそちらで）
let register_item_modal = document.getElementById('register_item_modal');
let register_item_modal_obj = new bootstrap.Modal(register_item_modal);

// 品目登録確認モーダルに、bsのモーダル用functionを使用できるように（参考元ではmodule化=>impotして使用していたが、bootstrap.クラス名でも呼び出し可なのでそちらで）
let confirm_item_modal = document.getElementById('confirm_item_modal');
let confirm_item_modal_obj = new bootstrap.Modal(confirm_item_modal);

// 起動ボタンの取得
let register_item_modal_subm = document.getElementById('register_item_modal_subm');

// 登録しようとしている品目をチェックし、類似情報があれば警告のモーダルを表示
register_item_modal_subm.addEventListener('click', () => {
    let item_name = $('#item_name').val();
    let item_unit_name = $('#item_unit').children(':selected').text();
    $.ajax({
        url: "Ajax_CheckSimilarItemInfo/",
        type: "GET",
        data: {
            item_name: item_name,
        }
    }).done(function (result_list) {
        //通信成功時のコールバック
        console.log(result_list);
        if (result_list.length > 0) {
            console.log("類似情報があります");
            console.log(document.getElementById('registering_item_name'));
            document.getElementById('registering_item_name').innerHTML = "「" + item_name + " /" + item_unit_name + "」";
            let target = document.getElementById('similar_itemlist');
            while (target.lastChild) {
                target.removeChild(target.lastChild);
            }
            for (result of result_list) {
                let li_element = document.createElement('li');
                li_element.textContent = result;
                target.appendChild(li_element);
            }
            confirm_item_modal_obj.show();

        } else {
            console.log("類似情報がありません");
            // そのまま登録処理へ
            Ajax_RegisterItemInfo()
        }

    }).fail(function (result) {
        console.log("通信失敗");

    }).always(function (result) {
        //常に実行する処理
        console.log("通信完了");
    })
})

// 品目確認モーダルの登録ボタンに設定
let confirm_item_modal_subm = document.getElementById("confirm_item_modal_subm");

confirm_item_modal_subm.addEventListener('click', () => {
    Ajax_RegisterItemInfo();
})

/**
 * 品目データ登録処理
 * ・データの登録
 * ・モーダルの値をリセットする
 * ・品目登録モーダルと、確認モーダルがる場合はそれを閉じる
 * ・登録した品目を選択状態にする
 */
function Ajax_RegisterItemInfo() {
    $.ajax({
        url: "Ajax_RegisterItemInfo/",
        type: "POST",
        data: {
            item_name: $('#item_name').val(),
            item_unit: $('#item_unit').val()
        },
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }).done(function (result) {
        //通信成功時のコールバック

        // 新規登録完了した品目idを取得する
        let itemId = Number(result);

        // selectタグを取得する
        let select = document.getElementById("item");
        // optionタグを作成する
        let option = document.createElement("option");
        // optionタグ用テキストの生成
        item_name_text = $('#item_name').val() + "/" + $('#item_unit').children(':selected').text();
        // optionタグのテキストにstoreNameを設定する
        option.text = item_name_text;
        // optionタグのvalueにitemIdを設定する
        option.value = itemId;
        // optionタグにselected属性を追加する
        option.setAttribute('selected', true);
        // selectタグの子要素にoptionタグを追加する
        select.appendChild(option);

        // モーダルを閉じる
        confirm_item_modal_obj.hide();
        register_item_modal_obj.hide();

        // モーダルのフォームを空に
        let form_element = document.getElementById('register_item_modal_form');
        form_element.reset();

        // バリデーション解除
        let validated = $('div.register_item_modal_outline')
        validated.removeClass('was-validated');
        // 自作バリデーションは、is-valid/is-invalidをフォーム自体に持っているので除去
        let input = $('#item_name,#item_unit');
        if (input.hasClass('is-valid')) {
            input.removeClass('is-valid');
        }
        if (input.hasClass('is-invalid')) {
            input.removeClass('is-invalid');
        }

    }).fail(function (result) {
        console.log("通信失敗");

    }).always(function (result) {
        //常に実行する処理
        console.log("通信完了");
    })
}

// 2重モーダル表示
$(document).ready(function () {
    $(document).on('show.bs.modal', '.modal', e => {
        const $currentModal = $(e.currentTarget);
        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $currentModal.css('z-index', zIndex);
        setTimeout(function () {
            $('.modal-backdrop')
                .not('.modal-stack')
                .css('z-index', zIndex - 1)
                .addClass('modal-stack');
        }, 0);
    });
});