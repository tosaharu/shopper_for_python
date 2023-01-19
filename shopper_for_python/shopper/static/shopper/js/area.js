/**
 * エリア選択の選択肢を制御する
 * 
 * area.jsでは、商品登録画面の画面&モーダルのように[data-region_id]を使用した
 * hidden_listやdisplay_listが複数ある場合、一括で処理される
 * ⇒商品登録画面での選択による絞り込みは、モーダル側にも反映される
 */

// 最初に必要な処理
window.addEventListener('load', () => {
    // 選択済の地域に応じて、選択可能な都道府県を表示する
    let region = document.getElementById('region').value;

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

// 地域選択に関する処理
let region_select_button = document.getElementById('region');
region_select_button.addEventListener('input', function () {
    ShowSelectedRegionPrefectureSelection(this);
})

// 都道府県選択に関する処理
let prefecture_select_button = document.getElementById('prefecture');
prefecture_select_button.addEventListener('input', function () {
    ShowSelectedPrefectureAreaSelection();
});


// 地域のプルダウンボタンが変更された際の処理
function ShowSelectedRegionPrefectureSelection(obj) {

    let region = obj.value;
    let prefecture_selector = document.getElementById('prefecture');

    // 選択地域の変更に応じて、選択可能な都道府県を表示する
    hidden_list = document.querySelectorAll('[data-region_id]');
    for (let i = 0; i < hidden_list.length; i++) {
        hidden_list[i].setAttribute("hidden", "");
        hidden_list[i].setAttribute("disabled", "");
    }
    display_list = document.querySelectorAll('[data-region_id="' + region + '"]')
    for (let i = 0; i < display_list.length; i++) {
        display_list[i].removeAttribute("hidden");
        display_list[i].removeAttribute("disabled");
    }

    // 選択地域を変更した際に、対象外の都道府県・エリア・店舗の選択をリセットする
    let index = prefecture_selector.selectedIndex;
    let p_region = document.querySelectorAll('[data-region_id]')[index].dataset.region_id;
    console.log(p_region);
    console.log(p_region);

    if (p_region != region) {
        // 都道府県の選択をリセット
        prefecture_selector.options[0].selected = true;
        // エリアの選択をリセット
        ShowSelectedPrefectureAreaSelection()
        // 店舗情報があるページの場合、店舗情報をリセット
        if (typeof ShowSelectedAreaStoreSelection == 'function') {
            ShowSelectedAreaStoreSelection()
        }
    }
}


// 選択していている都道府県に合わせたエリアを表示する
function ShowSelectedPrefectureAreaSelection() {
    $.ajax({
        url: "Ajax_GetArea/",
        type: "GET",
        data: { prefecture: $('#prefecture').val() }
    }).done(function (result) {
        //通信成功時のコールバック
        console.log(result);
        console.log($('#area'));

        // 既存リストの削除
        $('#area').children().remove();
        // 選択都道府県のリストを挿入
        $('#area').append(result);

        // 店舗情報があるページ（商品投稿ページ）の場合、店舗情報をリセット
        if (typeof ShowSelectedAreaStoreSelection == 'function') {
            ShowSelectedAreaStoreSelection()

            // 商品投稿のモーダルにもエリア選択肢を反映
            // 既存リストの削除
            $('#store_area').children().remove();
            // 選択都道府県のリストを挿入
            $('#store_area').append(result);
        }
    }).fail(function () {
        //通信失敗時のコールバック
        console.log("通信失敗");

    }).always(function () {
        //常に実行する処理
    })
};