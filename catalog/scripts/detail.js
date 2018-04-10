// ready function
$(function(context)
{
    // assign variable to the product type
    var thumbnail = $('.thumbnails_img')

    // hide and show fields depending on type
    thumbnail.on('mouseover', function()
    {
        var srcimg = $(this).attr('src')
        // var src = $(this).attr('src')
        console.log(srcimg)
        $('#big_img').attr('src', srcimg)


    })
    //
    // // assogn variable
    // var quantity = $('#id_quantity')
    //
    // var price = context.price * 2
    // // update price on quantity change
    // quantity.on('change', function(){
    //     // price = price * parseInt(quantity.val())
    //     $('#tot_prod_price').text(parseFloat(price.toFixed(2)))
    // })
})
