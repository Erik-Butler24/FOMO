//Load initial sub-page
$(function(context) {
    return function(){
    //set "container" to my HTML tag
    var container = $('#tiles_container')
    //load URL of my sub-page
    container.load('/catalog/tiles/' + context.CatID+ '/' + context.Pagenum)
    }
}(DMP_CONTEXT.get()));


//Page up function
$(function(context) {
    return function(){$("#Pageup").on('click', function(){
    if(context.Pagenum < context.MaxPages){
    //set "container" to my HTML tag
    var container = $('#tiles_container')
    //increment page number
    context.Pagenum ++
    //Fade out, Load, then fade back in (3 nested functions)
    container.fadeOut('fast',  function() {container.load('/catalog/tiles/' + context.CatID + '/' + context.Pagenum, function() {container.fadeIn()})})
    //Update HTML page number
    $("#DisplayPageNumber").text(context.Pagenum)}
    });
    };
    }(DMP_CONTEXT.get()));


//page down function
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
