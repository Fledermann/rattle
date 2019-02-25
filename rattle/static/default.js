$(document).on('click', '.widget-cl', (function(event) {
    postit(this, event);
}));

$(document).on('change input', '.widget-ch-in', (function(event) {
    postit(this, event);
}));

$(document).on('change click', '.widget-ch-cl', (function(event) {
    postit(this, event);
}));

$( document ).ready(function() {
    postit(null, null);
});

/*$(window).bind('beforeunload', function(e) { 
    e.preventDefault();
    return "Unloading this page may lose data. What do you want to do..."
});*/

function get_props(obj) {
    return {
        'value': obj.val()
    };
}

function postit(this_, event) {
    var json_post = {'event' : 'None'};
    if (this_) {
        json_post = {'event' : event.type,
                     'id_' : $(this_).attr('id'),
                     'props' : JSON.stringify(get_props($(this_)))};
    }
    $.post('/', json_post,
      function(response){
        json_ = JSON.parse(response);
        for (var k in json_) {
            if (json_[k].type_ == 'attr') {
                $('#'+json_[k].id_).prop(json_[k].key, json_[k].value);
            }
            else {
                console.log('Received function call:');
                console.log(json_[k].id_);
                $('#'+json_[k].id_)[json_[k].key](json_[k].value);
            }
        }
   });
}