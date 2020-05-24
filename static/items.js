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
                $event_pump.trigger('item_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('item_model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(liname, lidescription, listatus, liidate, lifdate, lipname) {
            
            let ajax_options = {
                type: 'POST',
                url: 'api/item',
                accepts: 'application/json',
                contentType: 'application/json',
                //dataType: 'json',
                data: JSON.stringify({
                    'nome': liname,
                    'descricao': lidescription,
                    'data_inicio': liidate,
                    'data_final': lifdate,
                    'status': listatus,
                    'proprietario': lipname,
                })
            };
             
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('item_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('item_model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(liname, lidescription, listatus, liidate, lifdate, lipname) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/item',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'nome': liname,
                    'descricao': lidescription,
                    'data_inicio': liidate,
                    'data_final': lifdate,
                    'status': listatus,
                    'proprietario': lipname,
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('item_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('item_model_error', [xhr, textStatus, errorThrown]);
            })
        },
        delete: function(lname) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api/item',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'nome': lname
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('item_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('item_model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
nsa.view = (function() {
    'use strict';


    // return the API
    return {
        reset: function() {
            let $liname = $('#liname').val('').focus(),
                $lidescription = $('#lidescription').val(''),
                $listatus = $('#listatus').val(''),
                $liidate = $('#liidate').val(''),
                $lifdate = $('#lifdate').val(''),
                $lipname = $('#lipname').val('');
        },
        build_table_item: function(item) {
            let rowsItem = ''
            
            if (item) {
                // clear the table
                $('#tableItem tbody').empty();
                // did we get a people array?
                for (let i=0, l=item.length; i < l; i++) {
                    rowsItem += `<tr><td>${item[i][1].nome}</td><td>${item[i][1].descricao}</td><td>${item[i][1].status}</td></tr>`;
                }
                $('#tableItem tbody').append(rowsItem);
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
        
        let $liname = $('#liname').val(),
            $lidescription = $('#lidescription').val(),
            $listatus = $('#listatus').val(),
            $liidate = $('#liidate').val(),
            $lifdate = $('#lifdate').val(),
            $lipname = $('#lipname').val();
        
        e.preventDefault();

       if (validate($liname, $lidescription, $lipname)) {
            model.create($liname, $lidescription, $listatus, $liidate, $lifdate, $lipname);
            $('#form_incl_item').each (function(){
                this.reset();
            });
        } else {
            alert('Nome, Descricao e Nome do Proprietario não podem ser vazios!');
        }
    });

    $('#iupdate').click(function(e) {
      let $liname = $('#liname').val(),
            $lidescription = $('#lidescription').val(),
            $listatus = $('#listatus').val(),
            $liidate = $('#liidate').val(),
            $lifdate = $('#lifdate').val(),
            $lipname = $('#lipname').val();
        
        e.preventDefault();

       if (validate($liname, $lidescription, $lipname)) {
            model.update($liname, $lidescription, $listatus, $liidate, $lifdate, $lipname);
            $('#form_incl_item').each (function(){
                this.reset();
            });
        } else {
            alert('Nome, Descricao e Nome do Proprietario não podem ser vazios!');
        }
    });

    $('#idelete').click(function(e) {
      
        let $liname = $('#liname').val();

        e.preventDefault();

        if (validate($liname, 'placeholder', 'placeholder')) {
            model.delete($liname)
            $('#form_incl_item').each (function(){
                this.reset();
            });
        } else {
            alert('Problema com os parâmetros: Nome');
        }
        e.preventDefault();
    });

    // Handle the model events
    $event_pump.on('item_read_success', function(e, data) {
        console.log("$event_pump.on('item_read_success - item')")
        console.log(data)
        view.build_table_item(data);
        view.reset();
    });

    $event_pump.on('item_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('item_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('item_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('item_model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = "Msg de Erro:" + textStatus + ': ' + errorThrown;
        view.error(error_msg);
    })
}(nsa.model, nsa.view));