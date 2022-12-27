/**
 *
 */

//地域のプルダウンボタンが変更された際の処理
function CheckSelectedRegion(obj) {

    let region = obj.value;
    let prefecture_selector = document.getElementById('prefecture');

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