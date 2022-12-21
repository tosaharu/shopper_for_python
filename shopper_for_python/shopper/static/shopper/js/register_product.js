/**
 *
 */


//地域のプルダウンボタンが変更された際の処理
function CheckSelectedRegion(obj) {

    let region = obj.value;
    let prefecture_selector = document.getElementById('prefecture');

    // エリアが選択された際に、都道府県を選択可能にする
    if (region >= 1) {
        prefecture_selector.removeAttribute("disabled");
    } else {
        console.log("else処理");
        prefecture_selector.setAttribute("disabled", "disabled");
    }

    // 選択エリアの変更に応じて、選択可能な都道府県を表示する
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

    // 選択エリアを変更した際に、対象外の都道府県・エリアの選択をリセットする
    let index = prefecture_selector.selectedIndex;
    let p_region = document.querySelectorAll('[data-region_id]')[index].dataset.region_id;
    console.log(p_region);
    if (p_region != region) {
        prefecture_selector.options[0].selected = true;
        let area_selector = document.getElementById('area');
        area_selector.options[0].selected = true;
        let store_selector = document.getElementById('store');
        store_selector.options[0].selected = true;
    }
}

//都道府県のプルダウンボタンが変更された際の処理
function CheckSelectedPrefecture(obj) {
    let prefecture = obj.value;
    console.log(prefecture);
    let area_selector = document.getElementById('area');

    // 都道府県が選択された際に、エリアを選択可能にする
    if (prefecture >= 1) {
        area_selector.removeAttribute("disabled");
    } else {
        console.log("else処理");
        area_selector.setAttribute("disabled", "disabled");
    }

    // 選択都道府県の変更に応じて、選択可能なエリアを表示する
    hidden_list = document.querySelectorAll('[data-prefecture_id]');
    for (let i = 0; i < hidden_list.length; i++) {
        hidden_list[i].setAttribute("hidden", "");
        hidden_list[i].setAttribute("disabled", "");
    }
    display_list = document.querySelectorAll('[data-prefecture_id="' + prefecture + '"]')
    for (let i = 0; i < display_list.length; i++) {
        display_list[i].removeAttribute("hidden");
        display_list[i].removeAttribute("disabled");
    }

    // 選択都道府県を変更した際に、対象外のエリアの選択をリセットする
    let index = area_selector.selectedIndex;
    let a_prefecture = document.querySelectorAll('[data-prefecture_id]')[index].dataset.prefecture_id;
    console.log(a_prefecture);
    if (a_prefecture != prefecture) {
        area_selector.options[0].selected = true;
        let store_selector = document.getElementById('store');
        store_selector.options[0].selected = true;
    }
}

// ここから下は登録画面用js
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

//エリアのプルダウンボタンが変更された際の処理
function CheckSelectedArea(obj) {
    let area = obj.value;
    console.log(area);
    let store_selector = document.getElementById('store');
    console.log(store_selector);


    // エリアが選択された際に、店舗を選択可能にする
    if (area >= 1) {
        store_selector.removeAttribute("disabled");
    } else {
        console.log("else処理");
        store_selector.setAttribute("disabled", "disabled");
    }

    // 選択エリアの変更に応じて、選択可能な店舗を表示する
    hidden_list = document.querySelectorAll('[data-area_id]');
    for (let i = 0; i < hidden_list.length; i++) {
        hidden_list[i].setAttribute("hidden", "");
        hidden_list[i].setAttribute("disabled", "");
    }
    display_list = document.querySelectorAll('[data-area_id="' + area + '"]')
    for (let i = 0; i < display_list.length; i++) {
        display_list[i].removeAttribute("hidden");
        display_list[i].removeAttribute("disabled");
    }

    // 選択エリアを変更した際に、対象外の店舗選択をリセットする
    let index = store_selector.selectedIndex;
    let s_area = document.querySelectorAll('[data-area_id]')[index].dataset.area_id;
    console.log(s_area);
    if (s_area != area) {
        store_selector.options[0].selected = true;
    }
}

//大品目のプルダウンボタンが変更された際の処理
function CheckSelectedMainItem(obj) {
    let main_item = obj.value;
    console.log(main_item);
    let sub_item_selector = document.getElementById('subitem');
    console.log(sub_item_selector);


    // 大品目が選択された際に、中品目を選択可能にする
    if (main_item >= 1) {
        sub_item_selector.removeAttribute("disabled");
    } else {
        console.log("else処理");
        sub_item_selector.setAttribute("disabled", "disabled");
    }

    // 大品目の変更に応じて、選択可能な中品目を表示する
    hidden_list = document.querySelectorAll('[data-main_item_id]');
    for (let i = 0; i < hidden_list.length; i++) {
        hidden_list[i].setAttribute("hidden", "");
        hidden_list[i].setAttribute("disabled", "");
    }
    display_list = document.querySelectorAll('[data-main_item_id="' + main_item + '"]')
    for (let i = 0; i < display_list.length; i++) {
        display_list[i].removeAttribute("hidden");
        display_list[i].removeAttribute("disabled");
    }

    // 大品目を変更した際に、対象外の品目選択をリセットする
    let index = sub_item_selector.selectedIndex;
    let s_main_item = document.querySelectorAll('[data-main_item_id]')[index].dataset.main_item_id;
    console.log(s_main_item);
    if (s_main_item != main_item) {
        sub_item_selector.options[0].selected = true;
        let item_selector = document.getElementById('item');
        item_selector.options[0].selected = true;
    }
}

//中品目のプルダウンボタンが変更された際の処理
function CheckSelectedSubItem(obj) {
    let sub_item = obj.value;
    console.log(sub_item);
    let item_selector = document.getElementById('item');
    console.log(item_selector);


    // 中品目が選択された際に、中品目を選択可能にする
    if (sub_item >= 1) {
        item_selector.removeAttribute("disabled");
    } else {
        console.log("else処理");
        item_selector.setAttribute("disabled", "disabled");
    }

    // 中品目の変更に応じて、選択可能な品目を表示する
    hidden_list = document.querySelectorAll('[data-sub_item_id]');
    for (let i = 0; i < hidden_list.length; i++) {
        hidden_list[i].setAttribute("hidden", "");
        hidden_list[i].setAttribute("disabled", "");
    }
    display_list = document.querySelectorAll('[data-sub_item_id="' + sub_item + '"]')
    for (let i = 0; i < display_list.length; i++) {
        display_list[i].removeAttribute("hidden");
        display_list[i].removeAttribute("disabled");
    }

    // 中品目を変更した際に、対象外の品目選択をリセットする
    let index = item_selector.selectedIndex;
    let i_sub_item = document.querySelectorAll('[data-sub_item_id]')[index].dataset.sub_item_id;
    console.log(i_sub_item);
    if (i_sub_item != sub_item) {
        item_selector.options[0].selected = true;
    }
}

//店舗登録モーダルに関する処理
//新規登録ボタンを押下した際にエリアデータをモーダルに反映する処理

// 起動ボタンの取得
let btn1 = document.getElementById('subm2');

btn1.addEventListener('click', () => {
    let region = document.getElementById('region').value;
    let prefecture = document.getElementById('prefecture').value;
    let area = document.getElementById('area').value;

    let targetRegion = document.querySelector('#store_region>option[value="' + region + '"]');
    targetRegion.selected = true;
    let targetPrefecture = document.querySelector('#store_prefecture>option[value="' + prefecture + '"]');
    targetPrefecture.selected = true;
    let targetArea = document.querySelector('#store_area>option[value="' + area + '"]');
    targetArea.selected = true;
})

//登録ボタンを押下した際に、１．記載の情報をDB登録　２．店舗を今登録したもので選択済みにする　３．モーダルを閉じてリセットする　４．登録完了or失敗の表示（余裕があれば）

// bsのモーダル用functionを使用できるように（参考元ではmodule化=>impotして使用していたが、bootstrap.クラス名でも呼び出し可なのでそちらで）
let modal = document.getElementById('modal');
let modalObj = new bootstrap.Modal(modal);

// 起動ボタンの取得
let btn3 = document.getElementById('subm3');

btn3.addEventListener('click', () => {
    let store_name = $('input[name="store_name"]').val();
    let store_region = $('select[name="store_region"]').val();
    let store_prefecture = $('select[name="store_prefecture"]').val();
    let store_area = $('select[name="store_area"]').val();
    $.ajax({
        url: "Ajax_RegisterStoreInfo/",
        type: "POST",
        data: {
            store_name: store_name,
            store_region: store_region,
            store_prefecture: store_prefecture,
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
        let targetRegion = document.querySelector('#region>option[value="' + store_region + '"]');
        targetRegion.selected = true;
        let targetPrefecture = document.querySelector('#prefecture>option[value="' + store_prefecture + '"]');
        targetPrefecture.selected = true;
        let targetArea = document.querySelector('#area>option[value="' + store_area + '"]');
        targetArea.selected = true;

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

    }).fail(function (result) {
        console.log("通信失敗");

    }).always(function (result) {
        //常に実行する処理
        console.log("通信完了");
        modalObj.hide()
    })
})