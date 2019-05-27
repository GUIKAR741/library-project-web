$(document).ready(function(){
    $("#loginValidate").validate({
        rules: {
            usuario: {
                required: true,
                email: true
            },
            senha: {
                required: true,
            },
        },
        //For custom messages
        messages: {
            usuario: {
                required: "Email obrigatório!",
                email: "Email inválido!"
            },
            senha: {
                required: "Senha obrigatória!",
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
            $.ajax({
                url: '/',
                type: 'post',
                data: $(form).serialize(),
                success: function (data) {
                    if (data.logado) {
                        window.location = '/';
                    }else{
                        login_error_msg(data.msg)
                    }
                }
            })
        }
    });
})