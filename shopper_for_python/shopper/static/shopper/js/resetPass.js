/**
 * パスワード再設定画面
 */

// 作動させたいボタンを取得
let btn = document.getElementById('subm1');

// ボタン押下の処理
btn.addEventListener('click', () => {
    let pass = $('input[name="newpassword"]').val()
    console.log(pass);
    $('#modal_newpassword').text(pass);
})