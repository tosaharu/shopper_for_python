/**
 *
 */

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

// 登録ボタンを押下した際にモーダルにデータを送る

// 対象のボタンを取得
let btn = document.getElementById('subm1');

// ボタン押下時の処理
btn.addEventListener('click', () => {
  selectAndInsertData("email", "modal_email");
  selectAndInsertData("password2", "modal_password");
  selectAndInsertData("name", "modal_name");
  selectAndInsertGender("gender", "modal_gender");
  selectAndInsertBirthday("year-select", "month-select", "day-select", "modal_birthday");
  selectAndInsertArea("region", "prefecture", "area", "modal_area");
})

// 第一引数の要素の値を、第二引数で選択した要素のなかに挿入する
function selectAndInsertData(getFrom, insertInto) {
  let val = document.getElementById(getFrom).value;
  document.getElementById(insertInto).innerHTML = val;
}

// （性別チェックボックス用）第一引数の要素の値を、第二引数で選択した要素のなかに挿入する
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

// （誕生日セレクトボックス用）第一引数の要素の値を、第二引数で選択した要素のなかに挿入する
function selectAndInsertBirthday(getFrom1, getFrom2, getFrom3, insertInto) {
  let year = document.getElementById(getFrom1).value;
  let month = document.getElementById(getFrom2).value;
  let day = document.getElementById(getFrom3).value;
  document.getElementById(insertInto).innerHTML = year + " 年 " + month + " 月 " + day + " 日 ";
}

// （エリアセレクトボックス用）第一引数の要素の値を、第二引数で選択した要素のなかに挿入する
function selectAndInsertArea(getFrom1, getFrom2, getFrom3, insertInto) {
  let r_index = document.getElementById(getFrom1).selectedIndex
  let region = document.getElementById(getFrom1).children[r_index].innerHTML;
  let p_index = document.getElementById(getFrom2).selectedIndex
  let prefecture = document.getElementById(getFrom2).children[p_index].innerHTML;
  let a_index = document.getElementById(getFrom3).selectedIndex
  let area = document.getElementById(getFrom3).children[a_index].innerHTML;

  document.getElementById(insertInto).innerHTML = region + " - " + prefecture + " - " + area;
}
