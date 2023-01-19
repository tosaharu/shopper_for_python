/**
 * 店舗情報画面
 * 
 * 商品登録画面>店舗登録モーダルで使用していた機能を流用する機能
 * ・店舗モーダルのselectの制御をする
 * ・類似店舗があった際の確認モーダル表示
 */

// 最初に必要な処理
window.addEventListener('load', () => {
    // 選択済の地域に応じて、選択可能な都道府県を表示する
    let region = document.getElementById('store_region').value;

    hidden_list = document.querySelectorAll('[data-region_id]');
    console.log(hidden_list);
    for (let i = 0; i < hidden_list.length; i++) {
        hidden_list[i].setAttribute("hidden", "");
        hidden_list[i].setAttribute("disabled", "");
    }
    display_list = document.querySelectorAll('[data-region_id="' + region + '"]')
    for (let i = 0; i < display_list.length; i++) {
        display_list[i].removeAttribute("hidden");
        display_list[i].removeAttribute("disabled");
    }
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

// 店舗登録確認モーダルに、bsのモーダル用functionを使用できるように（参考元ではmodule化=>impotして使用していたが、bootstrap.クラス名でも呼び出し可なのでそちらで）
let confirm_store_modal = document.getElementById('confirm_store_modal');
let confirm_store_modal_obj = new bootstrap.Modal(confirm_store_modal);

// 起動ボタンの取得
let register_store_modal_subm = document.getElementById('register_store_modal_subm');

// 登録しようとしている店舗名をチェックし、類似情報があれば警告のモーダルを表示
register_store_modal_subm.addEventListener('click', () => {
    // store_idが存在する場合に設定（店舗情報画面でも使用するため）
    let store_id = 0;
    if ($('#store_id')) {
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
            // そのまま更新処理へ
            document.register_store_modal_form.submit();
        }

    }).fail(function (result) {
        console.log("通信失敗");

    }).always(function (result) {
        //常に実行する処理
        console.log("通信完了");
    })
})

// 起動ボタンの取得
let confirm_store_modal_subm = document.getElementById('confirm_store_modal_subm');

// 確認ポップアップから更新処理を実行
confirm_store_modal_subm.addEventListener('click', () => {
    document.register_store_modal_form.submit();
})

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