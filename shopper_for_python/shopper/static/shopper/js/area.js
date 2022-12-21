/**
 *
 */
window.onload = PrefectureAreaOpener()

function PrefectureAreaOpener() {
  // エリアが選択された際に、都道府県を選択可能にする
  let region = document.getElementById('header_region').value;
  let prefecture_selector = document.getElementById('header_prefecture');
  if (region >= 1) {
    prefecture_selector.removeAttribute("disabled");
  } else {
    prefecture_selector.setAttribute("disabled", "disabled");
  }
  // 選択エリアの変更に応じて、選択可能な都道府県を表示する
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

  let prefecture = document.getElementById('header_prefecture').value;
  let area_selector = document.getElementById('header_area');
  // 都道府県が選択された際に、エリアを選択可能にする
  if (prefecture >= 1) {
    area_selector.removeAttribute("disabled");
  } else {
    area_selector.setAttribute("disabled", "disabled");
  }
  // 選択都道府県の変更に応じて、選択可能なエリアを表示する
  hidden_list = document.querySelectorAll('[data-header_prefecture_id]');
  for (let i = 0; i < hidden_list.length; i++) {
    hidden_list[i].setAttribute("hidden", "");
    hidden_list[i].setAttribute("disabled", "");
  }
  display_list = document.querySelectorAll('[data-header_prefecture_id="' + prefecture + '"]')
  for (let i = 0; i < display_list.length; i++) {
    display_list[i].removeAttribute("hidden");
    display_list[i].removeAttribute("disabled");
  }
}



//地域のプルダウンボタンが変更された際の処理
function CheckSelectedHeaderRegion(obj) {

  let region = obj.value;
  let prefecture_selector = document.getElementById('header_prefecture');

  // エリアが選択された際に、都道府県を選択可能にする
  if (region >= 1) {
    prefecture_selector.removeAttribute("disabled");
  } else {
    prefecture_selector.setAttribute("disabled", "disabled");
  }

  // 選択エリアの変更に応じて、選択可能な都道府県を表示する
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

  // 選択エリアを変更した際に、対象外の都道府県・エリアの選択をリセットする
  let index = prefecture_selector.selectedIndex;
  let p_region = document.querySelectorAll('[data-header_region_id]')[index].dataset.header_region_id;
  console.log(region);
  console.log(p_region);

  if (p_region != region) {
    prefecture_selector.options[0].selected = true;
    let area_selector = document.getElementById('header_area');
    area_selector.options[0].selected = true;
  }
}

//都道府県のプルダウンボタンが変更された際の処理
function CheckSelectedHeaderPrefecture(obj) {
  let prefecture = obj.value;
  let area_selector = document.getElementById('header_area');

  // 都道府県が選択された際に、エリアを選択可能にする
  if (prefecture >= 1) {
    area_selector.removeAttribute("disabled");
  } else {
    area_selector.setAttribute("disabled", "disabled");
  }

  // 選択都道府県の変更に応じて、選択可能なエリアを表示する
  hidden_list = document.querySelectorAll('[data-header_prefecture_id]');
  for (let i = 0; i < hidden_list.length; i++) {
    hidden_list[i].setAttribute("hidden", "");
    hidden_list[i].setAttribute("disabled", "");
  }
  display_list = document.querySelectorAll('[data-header_prefecture_id="' + prefecture + '"]')
  for (let i = 0; i < display_list.length; i++) {
    display_list[i].removeAttribute("hidden");
    display_list[i].removeAttribute("disabled");
  }

  // 選択都道府県を変更した際に、対象外のエリアの選択をリセットする
  let index = area_selector.selectedIndex;
  let a_prefecture = document.querySelectorAll('[data-header_prefecture_id]')[index].dataset.header_prefecture_id;
  if (a_prefecture != prefecture) {
    area_selector.options[0].selected = true;
  }
}