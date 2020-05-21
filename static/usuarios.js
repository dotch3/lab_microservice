// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
  "use strict";

  let $event_pump = $("body");

  // Return the API
  return {
    read: function() {
      let ajax_options = {
        type: "GET",
        url: "api/usuarios",
        accepts: "application/json",
        dataType: "json",
      };
      $.ajax(ajax_options)
        .done(function(data) {
          $event_pump.trigger("model_read_success", [data]);
        })
        .fail(function(xhr, textStatus, errorThrown) {
          $event_pump.trigger("model_error", [xhr, textStatus, errorThrown]);
        });
    },
    create: function(fname, lname) {
      let ajax_options = {
        type: "POST",
        url: "api/usuarios",
        accepts: "application/json",
        contentType: "application/json",
        //dataType: 'json',
        data: JSON.stringify({
          fname: fname,
          lname: lname,
        }),
      };
      $.ajax(ajax_options)
        .done(function(data) {
          $event_pump.trigger("model_create_success", [data]);
        })
        .fail(function(xhr, textStatus, errorThrown) {
          $event_pump.trigger("model_error", [xhr, textStatus, errorThrown]);
        });
    },
    update: function(fname, lname) {
      let ajax_options = {
        type: "PUT",
        url: "api/usuarios/" + lname,
        accepts: "application/json",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
          fname: fname,
          lname: lname,
        }),
      };
      $.ajax(ajax_options)
        .done(function(data) {
          $event_pump.trigger("model_update_success", [data]);
        })
        .fail(function(xhr, textStatus, errorThrown) {
          $event_pump.trigger("model_error", [xhr, textStatus, errorThrown]);
        });
    },
    delete: function(lname) {
      let ajax_options = {
        type: "DELETE",
        url: "api/usuarios/" + lname,
        accepts: "application/json",
        contentType: "plain/text",
      };
      $.ajax(ajax_options)
        .done(function(data) {
          $event_pump.trigger("model_delete_success", [data]);
        })
        .fail(function(xhr, textStatus, errorThrown) {
          $event_pump.trigger("model_error", [xhr, textStatus, errorThrown]);
        });
    },
  };
})();

// Create the view instance
ns.view = (function() {
  "use strict";

  let $nome = $("#nome"),
    $sobrenome = $("#sobrenome"),
    $email = $("#email");

  // return the API
  return {
    reset: function() {
      $nome.val("");
      $sobrenome.val("").focus();
    },
    update_editor: function(nome, sobrenome) {
      $nome.val(nome);
      $sobrenome.val(sobrenome).focus();
    },
    build_table: function(usuario) {
      let rows = "";

      // clear the table
      $(".conteudo table > tbody").empty();

      // did we get a user array?
      if (usuario) {
        for (let i = 0, l = usuario.length; i < l; i++) {
          rows += `<tr><td class="nome">${usuario[i].nome}</td><td class="sobrenome">${usuario[i].sobrenome}</td><td class="email">${usuario[i].email}</td></tr>`;
        }
        $("table > tbody").append(rows);
      }
    },
    error: function(error_msg) {
      $(".error")
        .text(error_msg)
        .css("visibility", "visible");
      setTimeout(function() {
        $(".error").css("visibility", "hidden");
      }, 3000);
    },
  };
})();

// Create the controller
ns.controller = (function(m, v) {
  "use strict";

  let model = m,
    view = v,
    $event_pump = $("body"),
    $nome = $("#nome"),
    $sobrenome = $("#sobrenome"),
    $email = $("#email");

  // Get the data from the model after the controller is done initializing
  setTimeout(function() {
    model.read();
  }, 100);

  // Validate input
  function validate(nome, sobrenome) {
    return nome !== "" && sobrenome !== "";
  }

  // Create our event handlers
  $("#create").click(function(e) {
    let fname = $fname.val(),
      lname = $lname.val();

    e.preventDefault();

    if (validate(fname, lname)) {
      model.create(fname, lname);
    } else {
      alert("Problema com os parâmetros: primeiro ou último nome");
    }
  });

  $("#update").click(function(e) {
    let fname = $fname.val(),
      lname = $lname.val();

    e.preventDefault();

    if (validate(fname, lname)) {
      model.update(fname, lname);
    } else {
      alert("Problema com os parâmetros: primeiro ou último nome");
    }
    e.preventDefault();
  });

  $("#delete").click(function(e) {
    let lname = $lname.val();

    e.preventDefault();

    if (validate("placeholder", lname)) {
      model.delete(lname);
    } else {
      alert("Problema com os parâmetros: primeiro ou último nome");
    }
    e.preventDefault();
  });

  $("#reset").click(function() {
    //location.reload();
    //model.read();
    window.location.reload();
    view.reset();
  });

  $("table > tbody").on("dblclick", "tr", function(e) {
    let $target = $(e.target),
      nome,
      sobrenome;

    nome = $target
      .parent()
      .find("td.nome")
      .text();

    sobrenome = $target
      .parent()
      .find("td.sobrenome")
      .text();

    email = $target
      .parent()
      .find("td.email")
      .text();

    view.update_editor(nome, sobrenome, email);
  });

  // Handle the model events
  $event_pump.on("model_read_success", function(e, data) {
    view.build_table(data);
    view.reset();
  });

  $event_pump.on("model_create_success", function(e, data) {
    model.read();
  });

  $event_pump.on("model_update_success", function(e, data) {
    model.read();
  });

  $event_pump.on("model_delete_success", function(e, data) {
    model.read();
  });

  $event_pump.on("model_error", function(e, xhr, textStatus, errorThrown) {
    let error_msg =
      "Msg de Erro:" +
      textStatus +
      ": " +
      errorThrown +
      " - " +
      xhr.responseJSON.detail;
    view.error(error_msg);
    console.log(error_msg);
  });
})(ns.model, ns.view);
