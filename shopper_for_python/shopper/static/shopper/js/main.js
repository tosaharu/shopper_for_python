/**
 * メイン画面
 * 
 * ・エリア選択の選択肢を制御
 * ・選択したエリアに合わせた情報を取得する
 * ・選択したソートに合わせた情報を取得する
*/

// 最初に必要な処理
window.addEventListener('load', () => {
    // 選択済の地域に応じて、選択可能な都道府県を表示する
    let region = document.getElementById('header_region').value;

    hidden_list = document.querySelectorAll('[data-header_region_id]');
    for (let i = 0; i < hidden_list.length; i++) {
        hidden_list[i].setAttribute("hidden", "");
        hidden_list[i].setAttribute("disabled", "");
    }

    display_list = document.querySelectorAll('[data-header_region_id="' + region + '"]')
    for (let i = 0; i < display_list.length; i++) {
        display_list[i].removeAttribute("hidden");
        display_list[i].removeAttribute("disabled");
    }

    // 選択されているエリアをボタン上に表示する
    ShowSelectedArea()
})


// 地域選択に関する処理
let region_select_button = document.getElementById('header_region');
region_select_button.addEventListener('input', () => {
    ShowSelectedRegionPrefectureSelection();
})

// 都道府県選択に関する処理
let prefecture_select_button = document.getElementById('header_prefecture');
prefecture_select_button.addEventListener('input', () => {
    ShowSelectedPrefectureAreaSelection();
});


// 地域のプルダウンボタンが変更された際の処理
function ShowSelectedRegionPrefectureSelection() {

    let region = document.getElementById('header_region').value;
    let prefecture_selector = document.getElementById('header_prefecture');

    // 選択地域の変更に応じて、選択可能な都道府県を表示する
    hidden_list = document.querySelectorAll('[data-header_region_id]');
    for (let i = 0; i < hidden_list.length; i++) {
        hidden_list[i].setAttribute("hidden", "");
        hidden_list[i].setAttribute("disabled", "");
    }
    display_list = document.querySelectorAll('[data-header_region_id="' + region + '"]')
    for (let i = 0; i < display_list.length; i++) {
        display_list[i].removeAttribute("hidden");
        display_list[i].removeAttribute("disabled");
    }

    // 選択地域を変更した際に、対象外の都道府県の選択をリセットする
    let index = prefecture_selector.selectedIndex;
    let p_region = document.querySelectorAll('[data-header_region_id]')[index].dataset.header_region_id;
    console.log(region);
    console.log(p_region);

    if (p_region != region) {
        prefecture_selector.options[0].selected = true;
    }
    ShowSelectedPrefectureAreaSelection();
}


// 選択していている都道府県に合わせたエリアを表示する
function ShowSelectedPrefectureAreaSelection() {
    $.ajax({
        url: "Ajax_GetMultiSelectArea/",
        type: "GET",
        data: { header_prefecture: $('#header_prefecture').val() }
    }).done(function (result) {
        //通信成功時のコールバック
        console.log(result);
        console.log($('div.ms-drop>ul'));

        // 既存リストの削除
        $('div.ms-drop>ul>li').remove();
        // 選択都道府県のリストを挿入
        $('div.ms-drop>ul').append(result);


    }).fail(function () {
        //通信失敗時のコールバック
        console.log("通信失敗");

    }).always(function () {
        //常に実行する処理
        ShowSelectedArea();
    })
};

// 選択されているエリアをボタン上に表示する
function ShowSelectedArea() {
    let selected_area_text = "";

    let selected_area_list = document.querySelectorAll('.area_selection>label>input');
    console.log(selected_area_list);
    let cnt = 0;
    for (selected_area of selected_area_list) {
        console.log(selected_area);
        if (selected_area.checked) {
            if (cnt > 0) {
                selected_area_text = selected_area_text + ",";
            }
            selected_area_text = selected_area_text + selected_area.nextElementSibling.textContent;
            cnt++;
        }
    }
    console.log(selected_area_text);
    if (selected_area_text != null && selected_area_text != "") {
        $('#msbtn>span').text(selected_area_text);
    } else {
        $('#msbtn>span').text("");
    }
}

// エリア選択ボタン押下時に最安情報リスト更新
let GetSortedAreasProduct_btn = document.getElementById('submit_areas_selection');
GetSortedAreasProduct_btn.addEventListener('click', () => {
    GetAreaProduct();
});

// 選択エリアに応じた最安商品リストの取得
function GetAreaProduct() {
    // 初投稿前の初期表示の場合は何も処理せずに終了する
    if (document.getElementById('first_step_btn')) {
        console.log('未投稿なので商品リストを取得せず終了')
        return
    }

    // 選択されたエリアを取得する
    let header_areas = $('input[name="header_area"]').filter(":checked").map(function () {
        return $(this).val();
    }).get();
    console.log(header_areas);

    $.ajax({
        url: "Ajax_GetAreaProduct/",
        type: "GET",
        data: { header_areas: header_areas, },
    }).done(function (result) {
        //通信成功時のコールバック
        console.log(result);
        console.log($('div#area_selector').next());

        // 既存リストの削除
        $('ul#product_list').empty();
        // 選択都道府県のリストを挿入
        $('ul#product_list').append(result);


    }).fail(function () {
        //通信失敗時のコールバック
        console.log("通信失敗");

    }).always(function () {
        //常に実行する処理
    })
};

// ソートボタン押下時に最安情報リスト更新
let GetSortedProduct_btn = document.getElementById('submit_sort');
GetSortedProduct_btn.addEventListener('click', () => {
    GetSortedProduct();
});

// 選択したソート方式に応じた最安商品リストの取得
function GetSortedProduct() {
    // 初投稿前の初期表示の場合は何も処理せずに終了する
    if (document.getElementById('first_step_btn')) {
        console.log('未投稿なので商品リストを取得せず終了')
        return
    }

    $.ajax({
        url: "Ajax_GetSortedProduct/",
        type: "GET",
        data: { sort: $('#sort').val(), },
    }).done(function (result) {
        //通信成功時のコールバック
        console.log(result);
        console.log($('div#area_selector').next());

        // 既存リストの削除
        $('ul#product_list').empty();
        // 選択都道府県のリストを挿入
        $('ul#product_list').append(result);


    }).fail(function () {
        //通信失敗時のコールバック
        console.log("通信失敗");

    }).always(function () {
        //常に実行する処理
    })
};

/**
 * エリア選択ボックスのホバー表示対応
 */

// エリア選択ボタンのホバー時カーソル
let ms_parent = $('.ms-parent');
console.log(ms_parent);
let ms_button = $('.ms-button')
console.log(ms_button);

// ホバー時
ms_parent.mouseover(() => {
    ms_button.css(
        {
            'border-color': '#86b7fe',
            'outline': '0',
            'box-shadow': '0 0 0 0.25rem rgba(13, 110, 253, 0.25)'
        }
    )
})

// ホバー解除時
ms_parent.mouseout(() => {
    ms_button.css(
        {
            'border-color': '',
            'outline': '',
            'box-shadow': ''
        }
    )
})