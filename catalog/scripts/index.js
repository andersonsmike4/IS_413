$(function (context) {
    return function () {
        var p_container = $('#products')
        p_container.load('/catalog/index.product/')
    }
}(DMP_CONTEXT.get()))
