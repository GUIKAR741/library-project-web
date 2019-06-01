$(document).ready(function (){
    $('#cpf').mask('000.000.000-00');
    $('#telefone').mask('(00)00000-0000');
    $("#formValidate").validate({
        rules: {
            nome: {
                required: true
            },
            email: {
                required: true,
                email: true
            },
            telefone: {
                required: false,
                minlength: 11
            },
            senha: {
                required: true,
                minlength: 6
            },
            nova_senha: {
                required: false,
                minlength: 6
            },
            conf_nova_senha: {
                required: false,
                minlength: 6,
                equalTo: "#nova_senha"
            },
        },
        //For custom messages
        messages: {
            nome: {
                required: "Nome obrigatório!",
            },
            email: {
                required: "Email obrigatório!",
                email: "Email inválido!"
            },
            telefone: {
                minlength: "Telefone inválido! Tamanho no mínimo 11 caracteres."
            },
            senha: {
                required: "Senha obrigatória!",
                minlength: "Senha inválida! Tamanho no mínimo 6 caracteres."
            },
            nova_senha: {
                minlength: "Senha inválida! Tamanho no mínimo 6 caracteres."
            },
            conf_nova_senha: {
                minlength: "Senha inválida! Tamanho no mínimo 6 caracteres.",
                equalTo: "Senha diferentes!"
            },
        },
        errorElement: 'div',
        errorPlacement: function (error, element) {
            var placement = $(element).data('error');
            if (placement) {
                $(placement).append(error)
            } else {
                error.insertAfter(element);
            }
        },
        submitHandler: function (form) {
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
                    $.ajax({
                        url: '/library/perfil/',
                        type: 'post',
                        data: $(form).serialize(),
                        success: function (data) {
                            if (data.status == 'ok') {
                                sucesso(data.msg, ' ');
                            } else {
                                login_error_msg(data.msg)
                            }
                        }
                    })
                } else {
                    swal(" ", {
                        title: "Cancelado!",
                        icon: "error",
                        timer: 1500,
                        buttons: false
                    });
                }
            });
        }
    });
});

