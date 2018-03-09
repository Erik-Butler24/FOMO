$(function(context) {
    return function(){
    var container = $('#tiles_container')
    container.load('/catalog/tiles/' + context.CatID+ '/' + context.Pagenum)
    }
}(DMP_CONTEXT.get()));


$(function(context) {
    return function(){$("#Pageup").on('click', function(){
    if(context.Pagenum < context.MaxPages){
    var container = $('#tiles_container')
    context.Pagenum ++
    container.fadeOut('fast',  function() {container.load('/catalog/tiles/' + context.CatID + '/' + context.Pagenum, function() {container.fadeIn()})})
    $("#DisplayPageNumber").text(context.Pagenum)}
    });
    };
    }(DMP_CONTEXT.get()));

$(function(context) {
    $(function(){$("#Pagedn").on('click', function(){
    if(context.Pagenum > 1){
    var container = $('#tiles_container')
    container.fadeOut('fast',  function() {container.load('/catalog/tiles/' + context.CatID + '/' + context.Pagenum, function() {container.fadeIn()})})
    context.Pagenum --
    $("#DisplayPageNumber").text(context.Pagenum)}
    });
    });
    }(DMP_CONTEXT.get()));
