$(function(context) {
    return function(){
    var container = $('#tiles_container')
    console.log(DMP_CONTEXT.lastContext.CatID)
    container.load('/catalog/tiles/' + DMP_CONTEXT.lastContext.CatID)

    }



}(DMP_CONTEXT.get()));



