// Create the namespace instance
let nsa = {};

// Create the model instance
nsa.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        read: function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/items',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(lname, lsobr, lende, lemai, ltele, ltipo, luser, lpass) {
            
            let ajax_options = {
                type: 'POST',
                url: 'api/item/' + lname,
                accepts: 'application/json',
                contentType: 'application/json',
                //dataType: 'json',
                data: JSON.stringify({
                    'nome': lname,
                    'sobrenome': lsobr,
                    'email': lemai,
                    'address': lende,
                    'password': lpass,
                    'username': luser,
                    'celular': ltele,
                })
            };
            
            console.log(ajax_options)
                        
            $.ajax(ajax_options)
            .done(function(data) {
                 console.log("model_create_success "+ data);
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(lname, lsobr, lende, lemai, ltele, ltipo, luser, lpass) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/item/' + lname,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'nome': lname,
                    'sobrenome': lsobr,
                    'email': lemai,
                    'address': lende,
                    'password': lpass,
                    'username': luser,
                    'celular': ltele,
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        delete: function(lname) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api/item/' + lname,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
nsa.view = (function() {
    'use strict';

    let $fname = $('#fname'),
        $lname = $('#lname');

    // return the API
    return {
        reset: function() {
            $lname.val('');
            $fname.val('').focus();
        },
        update_editor: function(fname, lname) {
            $lname.val(lname);
            $fname.val(fname).focus();
        },
        build_table: function(people) {
            let rows = ''

            // clear the table
            $('#tableItem tbody').empty();

            // did we get a people array?
            if (people) {
                for (let i=0, l=people.length; i < l; i++) {
                    rows += `<tr><td>${people[i][1].nome}</td><td>${people[i][1].descricao}</td><td>${people[i][1].status}</td></tr>`;
                }
                $('#tableItem tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
nsa.controller = (function(m, v) {
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
    $('#icreate').click(function(e) {
        
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

    $('#iupdate').click(function(e) {
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

    $('#idelete').click(function(e) {
      
        let $itName = $('#liname').val();
        console.log($itName)
        e.preventDefault();

        if (validate($itName, 'placeholder', 'placeholder')) {
            model.delete($itName)
            $('#form_incl_item').each (function(){
                this.reset();
            });
        } else {
            alert('Problema com os parâmetros: primeiro ou último nome');
        }
        e.preventDefault();
    });

    $('#ireset').click(function() {
        //location.reload();
        //model.read();
        window.location.reload();
        view.reset();
    })

    $('#tableItem tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            fname,
            lname;

        fname = $target
            .parent()
            .find('td.fname')
            .text();

        lname = $target
            .parent()
            .find('td.lname')
            .text();

        view.update_editor(fname, lname);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = "Msg de Erro:" + textStatus + ': ' + errorThrown;
        view.error(error_msg);
        console.log(error_msg);
    })
}(nsa.model, nsa.view));