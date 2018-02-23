(function(context) {
    
$("#id_ProductType").on('change', function(){

var Type = $("#id_ProductType").val()

if(Type == 'B'){
$("#id_Quantity").closest('p').show(300)
$("#id_ReorderTrigger").closest('p').show(300)
$("#id_ReorderQuantity").closest('p').show(300)
$("#id_ItemID").closest('p').hide(300)
$("#id_MaxRental").closest('p').hide(300)
$("#id_RetireDate").closest('p').hide(300)
}

if(Type == 'I'){
$("#id_Quantity").closest('p').hide(300)
$("#id_ReorderTrigger").closest('p').hide(300)
$("#id_ReorderQuantity").closest('p').hide(300)
$("#id_ItemID").closest('p').show(300)
$("#id_MaxRental").closest('p').hide(300)
$("#id_RetireDate").closest('p').hide(300)
}

if(Type == 'R'){
$("#id_Quantity").closest('p').hide(300)
$("#id_ReorderTrigger").closest('p').hide(300)
$("#id_ReorderQuantity").closest('p').hide(300)
$("#id_ItemID").closest('p').show(300)
$("#id_MaxRental").closest('p').show(300)
$("#id_RetireDate").closest('p').show(300)
}


})

$( document ).ready(function() {
var Type = $("#id_ProductType").val()

if(Type == 'B'){
$("#id_Quantity").closest('p').show(300)
$("#id_ReorderTrigger").closest('p').show(300)
$("#id_ReorderQuantity").closest('p').show(300)
$("#id_ItemID").closest('p').hide(300)
$("#id_MaxRental").closest('p').hide(300)
$("#id_RetireDate").closest('p').hide(300)
}

if(Type == 'I'){
$("#id_Quantity").closest('p').hide(300)
$("#id_ReorderTrigger").closest('p').hide(300)
$("#id_ReorderQuantity").closest('p').hide(300)
$("#id_ItemID").closest('p').show(300)
$("#id_MaxRental").closest('p').hide(300)
$("#id_RetireDate").closest('p').hide(300)
}

if(Type == 'R'){
$("#id_Quantity").closest('p').hide(300)
$("#id_ReorderTrigger").closest('p').hide(300)
$("#id_ReorderQuantity").closest('p').hide(300)
$("#id_ItemID").closest('p').show(300)
$("#id_MaxRental").closest('p').show(300)
$("#id_RetireDate").closest('p').show(300)
}
});


    
})(DMP_CONTEXT.get());
