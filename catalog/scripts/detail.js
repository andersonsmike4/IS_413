// ready function
$(function()
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
})
