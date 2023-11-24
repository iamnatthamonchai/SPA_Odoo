odoo.define("backend_font_style", function (require) {
  "use strict";
  var ajax = require('web.ajax');
  ajax.jsonRpc("/bfs_config", 'call', {}, {'async': false}).then(function (data) {
    var obj = eval(data);
    if(obj.backend_font_style != 'Odoo'){
      $("body").css("font-family", "'" + obj.backend_font_style + "', sans-serif");
    }
  });
  
  $(document).on("change", ".bfs_config", function (){
    var selected = $(this).find('option:selected').val().replace(/\"/g, '');
    if(selected != 'Odoo' && selected != 'false'){
      $("body").css("font-family", "'" + selected + "', sans-serif");
    } else {
      $("body").css("font-family", '');
    }
  });
});