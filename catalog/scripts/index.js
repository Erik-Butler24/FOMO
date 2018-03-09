$(function(context) {
    return function(){
    var container = $('#tiles_container')
    container.load('/catalog/tiles/' + context.CatID+ '/' + context.Pagenum)
    }
}(DMP_CONTEXT.get()));


$(function(context) {
    return function(){$("#Pageup").on('click', function(){
    if(context.Pagenum < context.MaxPages){
    context.Pagenum ++
    var container = $('#tiles_container')
    container.fadeOut()
    container.load('/catalog/tiles/' + context.CatID + '/' + context.Pagenum)
    $("#DisplayPageNumber").text(context.Pagenum)
    container.fadeIn()}
    });
    };
    }(DMP_CONTEXT.get()));

$(function(context) {
    $(function(){$("#Pagedn").on('click', function(){
    if(context.Pagenum > 1){
    context.Pagenum --
    var container = $('#tiles_container')
    container.fadeOut()
    container.load('/catalog/tiles/' + context.CatID + '/' + context.Pagenum)
    $("#DisplayPageNumber").text(context.Pagenum)
    container.fadeIn()}
    });
    });
    }(DMP_CONTEXT.get()));
