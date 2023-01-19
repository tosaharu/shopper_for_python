/**
 * フォームで生年月日入力欄を使用する画面
 * 
 * ・生年月日の選択肢生成処理
 * ・年月に応じた月日の選択肢に絞る処理
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