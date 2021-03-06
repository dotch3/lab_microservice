// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        read: function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/usuarios',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('usuario_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('usuario_model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(lname, lsobr, lende, lemai, ltele, ltipo, luser, lpass) {
            
            let ajax_options = {
                type: 'POST',
                url: 'api/usuario',
                accepts: 'application/json',
                contentType: 'application/json',
                //dataType: 'json',
                data: JSON.stringify({
                    'nome': lname,
                    'sobrenome': lsobr,
                    'email': lemai,
                    'address': lende,
                    'tipo_usuario': ltipo,
                    'password': lpass,
                    'username': luser,
                    'celular': ltele,
                    
                })
            };
                        
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('usuario_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('usuario_model_error', [xhr, textStatus, errorThrown]);
            })
        },
                 
        update: function(lname, lsobr, lende, ltele, lemai, ltipo, luser, lpass) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/usuario',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'nome': lname,
                    'sobrenome': lsobr,
                    'address': lende,
                    'celular': ltele,
                    'email': lemai,
                    'tipo_usuario': ltipo,
                    'username': luser,
                    'password': lpass,
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('usuario_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('usuario_model_error', [xhr, textStatus, errorThrown]);
            })
        },
        delete: function(lname) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api/usuario',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'nome': lname
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                console.log('model_delete_success')
                $event_pump.trigger('usuario_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_delete_success', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    // return the API
    return {
        reset: function() {
            let $lname = $('#uname').val('').focus(),
                $lende = $('#uende').val(''),
                $ltele = $('#utele').val(''),
                $lemai = $('#uemai').val(''),
                $ltipo = $('#utipo').val(''),
                $luser = $('#uuser').val(''),
                $lpass = $('#upass').val('');
        },
        build_table_usuario: function(usuario) {
            let rowsUsuario = ''
            
            if (usuario) {
                // clear the table
                $('#tableUsuario tbody').empty();
                // did we get a people array?
                for (let i=0, l=usuario.length; i < l; i++) {
                    rowsUsuario += `<tr><td>${usuario[i][1].nome}</td><td>${usuario[i][1].address}</td><td>${usuario[i][1].celular}</td></tr>`;
                }
                $('#tableUsuario tbody').append(rowsUsuario);
            }
        },
        error: function(error_msg) {
            $('.error').text(error_msg).css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $fname = $('#fname'),
        $lname = $('#lname');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100);

    // Validate input
    function validate(lname, luser, lpass) {
        return lname !== "" && luser !== "" && lpass !== "";
    }
    
    function validateSenha(luser, lpass) {
        return luser.length >= 5 && lpass.length >= 4;
    }

    // Create our event handlers
    $('#ucreate').click(function(e) {
        
        let $lname = $('#uname').val(),
            $lende = $('#uende').val(),
            $ltele = $('#utele').val(),
            $lemai = $('#uemai').val(),
            $ltipo = $('#utipo').val(),
            $luser = $('#uuser').val(),
            $lpass = $('#upass').val();
        
        e.preventDefault();

       if (validate($lname, $luser, $lpass)) {
            if (validateSenha($luser, $lpass)) {
                
                var resultado = $lname.split(" ");
                $lname = resultado[0];
                
               var lsobr = "";
                for (var i = 1; i < resultado.length; i++) {
                     var prop = resultado[i];
                     lsobr = lsobr + " " + prop;
                }
                model.create($lname, lsobr, $lende, $ltele, $lemai, $ltipo, $luser, $lpass);
                $('#form_incl_usuario').each (function(){
                    this.reset();
                });
            } else {
                alert('Usuario e Senha devem ter o mínimo de caracteres exigido');
            }
        } else {
            alert('Nome, Usuário e Senha não podem ser vazios!');
        }
    });

    $('#uupdate').click(function(e) {
       let $lname = $('#uname').val(),
            $lende = $('#uende').val(),
            $ltele = $('#utele').val(),
            $lemai = $('#uemai').val(),
            $ltipo = $('#utipo').val(),
            $luser = $('#uuser').val(),
            $lpass = $('#upass').val();
        
        e.preventDefault();

       if (validate($lname, $luser, $lpass)) {
            if (validateSenha($luser, $lpass)) {
                
                var resultado = $lname.split(" ");
                $lname = resultado[0];
                
                var lsobr = "";
                for (var i = 1; i < resultado.length; i++) {
                     var prop = resultado[i];
                     lsobr = lsobr + " " + prop;
                }
                model.update($lname, lsobr, $lende, $ltele, $lemai, $ltipo, $luser, $lpass);
                $('#form_incl_usuario').each (function(){
                    this.reset();
                });
            } else {
                alert('Usuario e Senha devem ter o mínimo de caracteres exigido');
            }
        } else {
            alert('Nome, Usuário e Senha não podem ser vazios!');
        }
    });

    $('#udelete').click(function(e) {
      
        let $lname = $('#uname').val();

        e.preventDefault();

        if (validate($lname, 'placeholder', 'placeholder')) {
            var resultado = $lname.split(" ");
            $lname = resultado[0];
            model.delete($lname)
            $('#form_incl_usuario').each (function(){
                this.reset();
            });
        } else {
            alert('Problema com os parâmetros: primeiro ou último nome');
        }
        e.preventDefault();
    });

    // Handle the model events
    $event_pump.on('usuario_read_success', function(e, data) {
        console.log("$event_pump.on('usuario_read_success - usuario')")
        console.log(data)
        view.build_table_usuario(data);
        view.reset();
    });

    $event_pump.on('usuario_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('usuario_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('usuario_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('usuario_model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = "Msg de Erro:" + textStatus + ': ' + errorThrown;
        view.error(error_msg);
    })
}(ns.model, ns.view));