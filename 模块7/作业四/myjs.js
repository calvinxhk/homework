$("#guidelist").click(function () {

    $("#guidelist1").toggle()
});
$(" .main-head").click(function () {
    $(" .main-head").css({"background":"blue","color":"white"});
    $(this).css({"background":"white","color":"black"})
});
$("#main-searchb").click(function () {
    var id=$("#main-searchid").val(),
     date=$("#main-searchdate").val(),
     status=$("#main-searchstatus").find("option:selected").text(),
     resourse=$("#main-searchresourse").find("option:selected").text();

$(".result").each(function () {
    var listTarget=$(this).children("ul").eq(0).children("li");
    if ((listTarget.eq(1).text() || !id) &&
        (listTarget.eq(2).text()===date||!date)&&
        (listTarget.eq(3).text()===status||!status)&&
        (listTarget.eq(4).text()===resourse||!resourse)
    )
    {$(this).css("display","block")}
    else {$(this).css("display","none")}
})
});
$("#selectall").change(function () {
    var target=$(".first-checkbox").children("input");
    if ($(this).prop("checked")){
        target.prop("checked",true)
    }
    else {target.prop("checked",false)}

   });
$("#selectopp").change(function () {
    var target=$(".first-checkbox").children("input");
    target.each(function () {
        if ($(this).prop("checked")){
            $(this).prop("checked",false)
        }
        else {$(this).prop("checked",true)}
    })

});
$(".editor").click(function () {
    var record = $(this).parent().parent().siblings("input"),
        target = $(this).parent().siblings(),
        recive = $(this).parent().parent().next().children().children();
    if (record.val() === '0') {
        record.val('1');
        $(this).parent().parent().css("display", 'none');
        $(this).parent().parent().next().css("display", "block");
        var id=target.eq(1).text(),date=target.eq(2).text(),status=target.eq(3).text(),source=target.eq(4).text();
        recive.eq(1).val(id);
        recive.eq(2).val(date);
        recive.eq(3).val(status);
        recive.eq(4).val(source);
    }
    else {
        var answer = confirm("点击确认键不保存退出，点击取消返回编辑模式。（若需保存，请点击保存按钮）");
        if (answer) {
            $(this).parent().parent().prev().css("display", 'block');
            $(this).parent().parent().css("display", "none");
            record.val('0');
        }
    }
});
$(".save").click(function () {
    var record = $(this).parent().parent().siblings("input"),
        target = $(this).parent().siblings().children(),
        recive = $(this).parent().parent().prev().children();
    if (record.val()){
    var answer = confirm("确认保存?");
    if (answer){
        $(this).parent().parent().prev().css("display", 'block');
        $(this).parent().parent().css("display", "none");
        record.val('0');
        var newId= target.eq(1).val(),
        newDate = target.eq(2).val(),
        newstatus = target.eq(3).val(),
        newsource = target.eq(4).val();
        recive.eq(1).text(newId);recive.eq(2).text(newDate);
        recive.eq(3).text(newstatus);recive.eq(4).text(newsource);

    }
}});
$(".delete").click(function () {
    $(".result").each(function () {
        if($(this).children().eq(1).children().eq(0).children().prop("checked"))
        {
            $(this).remove()
        }

    })
})