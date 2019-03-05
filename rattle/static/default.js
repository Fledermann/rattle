$(document).on('change', '.change', (function(event) {
    console.log(this, event)
    postit(this, event);
}));

$(document).on('click', '.click', (function(event) {
    postit(this, event);
}));

$(document).on('input', '.input', (function(event) {
    postit(this, event);
}));

$( document ).ready(function() {
    postit(null, null);
});

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
                $('#'+json_[k].id_)[json_[k].key](json_[k].value);
            }
        }
   });
}