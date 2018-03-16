// ready function
$(function()
{
    // assign variable to the product type
    var thumbnail = $('.thumbnails_img')

    // hide and show fields depending on type
    thumbnail.on('mouseover', function()
    {

        // var src = $(this).attr('src')
        console.log($(this).closest('img'))
        // $(#big_image).attr('src', this.attr('src'))
    })
})
