$(function(context) {
    return function(){$(".thumb").mouseover(function(){
    var newsource = event.target.src
    $("#main_image").attr("src",newsource)
    });
    };
    }(DMP_CONTEXT.get()));
