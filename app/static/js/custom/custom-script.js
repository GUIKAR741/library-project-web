/*================================================================================
	Item Name: Materialize - Material Design Admin Template
	Version: 5.0
	Author: PIXINVENT
	Author URL: https://themeforest.net/user/pixinvent/portfolio
================================================================================

NOTE:
------
PLACE HERE YOUR OWN JS CODES AND IF NEEDED.
WE WILL RELEASE FUTURE UPDATES SO IN ORDER TO NOT OVERWRITE YOUR CUSTOM SCRIPT IT'S BETTER LIKE THIS. */
$('.swal-erro').click(function () {
	swal({
		title: "Tente novamente!",
		text: "Por algum motivo, não foi possível alterar seus dados.",
		icon: "error",
		timer: 1500,
		buttons: false
	});
});

$('.swal-alert').click(function () {
	swal({
		title: "Preencha os campos obrigatórios!",
		text: " ",
		icon: "warning",
		timer: 1500,
		buttons: false
	});
});

$('.swal-info').click(function () {
	swal({
		title: "Reserva disponível!",
		text: "Nome do Livro, você tem 24 horas para realizar o empréstimo.",
		icon: "info"
	});
});

$('.swal-reserva').click(function () {
	swal({
		title: "Reserva realizada com sucesso!",
		text: " ",
		icon: "success",
		timer: 1500,
		buttons: false
	});
});

$('.swal-reserva-falha').click(function () {
	swal({
		title: "Tente novamente!",
		text: "Por algum motivo, não foi possível realizar sua reserva.",
		icon: "error",
		timer: 1500,
		buttons: false
	});
});

$('.swal-renovacao').click(function () {
	swal({
		title: "Renovação realizada com sucesso!",
		text: " ",
		icon: "success",
		timer: 1500,
		buttons: false
	});
});

$('.swal-renovacao-falha').click(function () {
	swal({
		title: "Tente novamente!",
		text: "Por algum motivo, não foi possível realizar sua renovação.",
		icon: "error",
		timer: 1500,
		buttons: false
	});
});

$('.swal-cancelar').click(function () {
	swal({
		title: "Reserva cancelada com sucesso!",
		text: " ",
		icon: "success",
		timer: 1500,
		buttons: false
	});
});

$('.swal-cancelar-falha').click(function () {
	swal({
		title: "Tente novamente!",
		text: "Por algum motivo, não foi possível realizar o cancelamento da sua reserva.",
		icon: "error",
		timer: 1500,
		buttons: false
	});
});

function login_error_msg(texto = ' ') {
	swal({
		title: "Dados inválidos!",
		text: texto,
		icon: "error",
		timer: 1500,
		buttons: false
	});
};

function sucesso(titulo = '' , texto = ''){
	swal({
		title: titulo,
		text: texto,
		icon: "success",
		timer: 1500,
		buttons: false
	});
}

$('.swal-login-falha').click(function () {
	swal({
		title: "Tente novamente!",
		text: "Por algum motivo, não foi possível logar na sua conta.",
		icon: "error",
		timer: 1500,
		buttons: false
	});
});

$('.swal-esqueceu-senha').click(function () {
	swal({
		title: "Email enviado!",
		text: "Verifique sua caixa de entrada.",
		icon: "success",
		timer: 1500,
		buttons: false
	});
});

$('.swal-esqueceu-error').click(function () {
	swal({
		title: "Email inválido!",
		text: "Email não cadastrado.",
		icon: "error",
		timer: 1500,
		buttons: false
	});
});

$('.swal-esqueceu-falha').click(function () {
	swal({
		title: "Tente novamente!",
		text: "Por algum motivo, não foi possível resetar sua senha.",
		icon: "error",
		timer: 1500,
		buttons: false
	});
});

$('.swal-confirmacao').click(function () {
	swal({
		title: "Deseja alterar os dados?",
		icon: 'warning',
		dangerMode: true,
		buttons: {
			cancel: 'Cancelar',
			delete: 'Confirmar'
		}
	}).then(function (willDelete) {
		if (willDelete) {
			swal(" ", {
				title: "Seus dados foram alterados com sucesso!",
				icon: "success",
				timer: 1500,
				buttons: false
			});
		} else {
			swal(" ", {
				title: "Cancelado!",
				icon: "error",
				timer: 1500,
				buttons: false
			});
		}
	});
});
