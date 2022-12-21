/**
 *
 */
// 'use strict';

// モーダルにパラメータ渡し
$('#subm').on('click', function () {
  const text = $('#typeText1').val();
  $('.modal-body').text(text);
})

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
  }
}

//年月日の選択肢を生成
console.log("年月日生成処理");
let yearSelections = document.querySelector('#year-select');
let monthSelections = document.querySelector('#month-select');
let daySelections = document.querySelector('#day-select');

createFirstOptionElements(yearSelections);
for (let i = 1920; i <= 2020; i++) {
  createOptionElements(yearSelections, i);
}

createFirstOptionElements(monthSelections);
for (let i = 1; i <= 12; i++) {
  createOptionElements(monthSelections, i);
}

createFirstOptionElements(daySelections);
for (let i = 1; i <= 31; i++) {
  createOptionElements(daySelections, i);
}

function createOptionElements(el, val) {
  let op = document.createElement("option");
  op.value = val;
  op.text = val;
  el.appendChild(op);
}

function createFirstOptionElements(el) {
  let op = document.createElement("option");
  op.value = "";
  op.text = "--";
  el.appendChild(op);
}

// function getElementByValue(year) {
//   let el = document.querySelector(`#year-select>option[value='${year}']`);
//   console.log("valueの値によって要素を持ってくるテスト");
//   console.log(el.value);
// }
// getElementByValue(1989);

//年月の選択に応じて、選択可能な日を表示する
function CheckSelectedMonth() {
  let year = document.getElementById('year-select').value;
  let month = document.getElementById('month-select').value;
  console.log(year);
  console.log(month);

  let day_list = document.getElementById('day-select').children;
  for (let i = 0; i < day_list.length; i++) {
    day_list[i].removeAttribute("hidden");
    day_list[i].removeAttribute("disabled");
  }

  let array_day_list = Array.from(day_list);

  if (month == 4 || month == 6 || month == 9 || month == 11) {
    let target_list = array_day_list.slice(31);
    hideTargetList(target_list);
  } else if (month == 2) {
    if (year % 100 == 0 && year % 400 != 0) {
      let target_list = array_day_list.slice(29);
      console.log("１００年ごとの例外")
      hideTargetList(target_list);
    } else if (year % 4 == 0) {
      let target_list = array_day_list.slice(30);
      console.log("うるう年")
      hideTargetList(target_list);
    } else {
      let target_list = array_day_list.slice(29);
      console.log("通常の２月")
      hideTargetList(target_list);
    }
  }
}

function hideTargetList(list) {
  for (let i = 0; i < list.length; i++) {
    list[i].setAttribute("hidden", "");
    list[i].setAttribute("disabled", "");
  }
}

function sendFormData() {
  selectAndInsertData("email", "modal_email");
  selectAndInsertData("password2", "modal_password");
  selectAndInsertData("name", "modal_name");
  selectAndInsertGender("gender", "modal_gender");
  selectAndInsertBirthday("year-select", "month-select", "day-select", "modal_birthday");
  selectAndInsertArea("region", "prefecture", "area", "modal_area");
}

// 第二引数で選択した要素のあとに、第一引数の内容を挿入する
function selectAndInsertData(getFrom, insertInto) {
  let val = document.getElementById(getFrom).value;
  document.getElementById(insertInto).innerHTML = val;
}

function selectAndInsertGender(getFrom, insertInto) {
  let val;
  let elements = document.getElementsByName(getFrom);
  for (let i = 0; i <= elements.length; i++) {
    if (elements[i].checked) {
      val = elements[i].value;
      break;
    }
  }
  console.log(val)
  switch (val) {
    case "1":
      val = "男性";
      break;
    case "2":
      val = "女性";
      break;
    case "3":
      val = "回答しない";
      break;
  }
  document.getElementById(insertInto).innerHTML = val;
}

function selectAndInsertBirthday(getFrom1, getFrom2, getFrom3, insertInto) {
  let year = document.getElementById(getFrom1).value;
  let month = document.getElementById(getFrom2).value;
  let day = document.getElementById(getFrom3).value;
  document.getElementById(insertInto).innerHTML = year + " 年 " + month + " 月 " + day + " 日 ";
}

function selectAndInsertArea(getFrom1, getFrom2, getFrom3, insertInto) {
  let r_index = document.getElementById(getFrom1).selectedIndex
  let region = document.getElementById(getFrom1).children[r_index].innerHTML;
  let p_index = document.getElementById(getFrom2).selectedIndex
  let prefecture = document.getElementById(getFrom2).children[p_index].innerHTML;
  let a_index = document.getElementById(getFrom3).selectedIndex
  let area = document.getElementById(getFrom3).children[a_index].innerHTML;

  document.getElementById(insertInto).innerHTML = region + " - " + prefecture + " - " + area;
}
