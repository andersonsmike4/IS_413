// #1 delayed
// #2 clasure (for scope)

// ready function
$(function()
{
    // assign variable to the product type
    var choice = $('#id_type')

    // hide and show fields depending on type
    choice.on('change', function()
    {
        choice.val() == 'BulkProduct'
        if (choice.val() == 'IndividualProduct')
        {
            $('#id_pid').closest('p').show(400)
            $('.Rental').closest('p').hide(400)
            $('.Bulk').closest('p').hide(400)
        }
        else if (choice.val() == 'RentalProduct')
        {
            $('#id_pid').closest('p').show(400)
            $('.Rental').closest('p').show(400)
            $('.Bulk').closest('p').hide(400)
        }
        else if (choice.val() == 'BulkProduct')
        {
            $('#id_pid').closest('p').hide(400)
            $('.Rental').closest('p').hide(400)
            $('.Bulk').closest('p').show(400)
        }
        else {
            $('#id_pid').closest('p').hide(400)
            $('.Rental').closest('p').hide(400)
            $('.Bulk').closest('p').hide(400)
        }
    })
    //trigger change immediately
    $('#id_type').trigger('change')
})
