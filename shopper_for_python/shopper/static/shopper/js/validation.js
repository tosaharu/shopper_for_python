/**
 *
 */

// バリデーションの警告文がチェック対象の直後にある場合（通常の配置）に、バリデーションの種類に合った警告文に更新する
function updateValidationMessage(input) {
	let validationMessage = input.validationMessage;
	console.log(validationMessage);
	let insertAt = input.nextElementSibling;
	console.log(insertAt);
	insertAt.innerHTML = validationMessage;
}

// フォームをチェックし、問題があればボタンは無効に、なければ有効に切り替える
function toggleFormButton(form_id, button_id) {
	let subm_form = document.getElementById(form_id);
	let subm = document.getElementById(button_id);
	if (subm_form.checkValidity()) {
		subm.removeAttribute('disabled');
	} else {
		subm.setAttribute('disabled', 'disabled');
	}
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// ラジオボタン以外の選択肢HTML構造用
function activateValidation(outline_id, input_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let input = document.getElementById(input_id);
	console.log(input)

	input.addEventListener('focus', function () {
		outline.classList.remove('was-validated');
	}, false)

	input.addEventListener('blur', function () {
		outline.classList.add('was-validated');
		toggleFormButton(form_id, button_id);
		updateValidationMessage(input)
	}, false)
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// ラジオボタンの選択肢HTML構造用
function activateRadioValidation(outline_id, input_name, invalid_feedback_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let forms = document.getElementsByName(input_name);
	console.log(forms)
	let insertAt = document.getElementById(invalid_feedback_id);
	console.log(insertAt)

	for (let input of forms) {
		input.addEventListener('focus', function () {
			outline.classList.remove('was-validated');
		}, false)

		input.addEventListener('blur', function () {
			outline.classList.add('was-validated');
			toggleFormButton(form_id, button_id);

			let validationMessage = input.validationMessage;
			console.log(validationMessage);
			insertAt.innerHTML = validationMessage;
		}, false)
	}
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// 2か所のパスワードの入力が一致していることをバリデートする
function activateDoublePassValidation(outline_id, input_id, reference_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let input = document.getElementById(input_id);
	console.log(input)
	let reference = document.getElementById(reference_id);
	console.log(reference)

	input.addEventListener('focus', function () {
		input.classList.remove('is-valid');
		input.classList.remove('is-invalid');
		outline.classList.remove('was-validated');
	}, false)

	input.addEventListener('blur', function () {
		console.log(input.value);
		console.log(reference.value);
		if (input.value == reference.value) {
			console.log("パス合致");
			input.classList.remove('is-invalid');
			input.classList.add('is-valid');
			input.setCustomValidity("")

		} else {
			console.log("パス不一致");
			input.classList.remove('is-valid');
			input.classList.add('is-invalid');
			input.setCustomValidity("パスワードが一致しません")

		}
		outline.classList.add('was-validated');
		toggleFormButton(form_id, button_id);
		updateValidationMessage(input)
	}, false)
}

// フォーカスが外れた際にバリデーションし、フォーカスされたときにバリデーションを解除する
// メールアドレスがDBに存在しないことをバリデートする
function activateExistingMailValidation(outline_id, input_id, form_id, button_id) {
	let outline = document.getElementById(outline_id);
	console.log(outline)
	let input = document.getElementById(input_id);
	console.log(input)

	input.addEventListener('focus', function () {
		input.classList.remove('is-valid');
		input.classList.remove('is-invalid');
		outline.classList.remove('was-validated');
	}, false)


	input.addEventListener('blur', function () {
		$.ajax({
			url: "Ajax_CheckUserMail",
			type: "GET",
			data: { mail: $('#email').val() }
		}).done(function (result) {
			//通信成功時のコールバック
			let checkMail = Number(result);
			if (checkMail == 1) {
				console.log("登録済のメールアドレス有り");
				input.classList.remove('is-valid');
				input.classList.add('is-invalid');
				input.setCustomValidity("そのメールアドレスは既に使用されています")
			} else {
				console.log("登録済のメールアドレス無し、または自分のメールアドレスの場合");
				input.classList.remove('is-invalid');
				input.classList.add('is-valid');
				input.setCustomValidity("")
			}
			outline.classList.add('was-validated');
			toggleFormButton(form_id, button_id);
			updateValidationMessage(input)
		}).fail(function () {
			//通信失敗時のコールバック
			console.log("通信失敗");
		}).always(function () {
			//常に実行する処理
		});

	}, false)
}
