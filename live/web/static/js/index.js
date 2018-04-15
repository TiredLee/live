
$(function () {
    var category = $('h3').attr('category');
    var lis = $("li[role='presentation']");
    $(".active").removeClass('active');
    for (var i = 0; i < lis.length; i ++)
    {
        if ($(lis[i]).attr('category') == category){
            $(lis[i]).addClass('active');
        }
    }
});








