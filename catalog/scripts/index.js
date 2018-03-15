$(function (context) {
    return function () {
        var p_container = $('#products')
        p_container.load('/catalog/index.product/' + context.categoryid)
        $('#previous_page').click(function(){
            if ($('#current_page').text() != 1)
            {
                var new_page = parseInt($('#current_page').text()) - 1
                $('#current_page').text(new_page)
                p_container.load('/catalog/index.product/' + context.categoryid + '/' + new_page)
            }

            // return False
        })
        $('#next_page').click(function(){
            if ($('#current_page').text() != context.total_pages)
            {
                var new_page = parseInt($('#current_page').text()) + 1
                $('#current_page').text(new_page)
                p_container.load('/catalog/index.product/' + context.categoryid + '/' + new_page)
            }

            // return False
        })
    }
}(DMP_CONTEXT.get()))
