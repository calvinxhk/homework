$(".header1 a").click(function () {
    $(".user-login-mask").css("display","block")
});
$("#phone-login").click(function(){ $(".box-login .phone-login").css("display","block"); $(this).css("color","blue"); $("#user-login").css("color","#abb6d2");$(".box-login .id-login").css("display","none")});
$("#user-login").click(function(){$(".box-login .phone-login").css("display","none"); $(this).css("color","blue");$("#phone-login").css("color","#abb6d2");$(".box-login .id-login").css("display","block")});
$(" .exit").click(function(){$(".user-login-mask").css("display","none")});
intervalID=0;
 function lunbo (id) {
    var trueindex =id||5;
    intervalID=setInterval(function () {
        $(".img .lunbo-img").eq(trueindex).css("display","none");
        $(".lunbo-foot").eq(trueindex).css("background-color","rgba(0,0,0,0.6)");
        if(trueindex ===5){trueindex=0}
        else {trueindex++}
        $(".img .lunbo-img").eq(trueindex).css("display","block");
        $(".lunbo-foot").eq(trueindex).css("background-color","white");
    },1000)
}
lunbo();
$(".lunbo-foot").hover(function (){
    clearInterval(intervalID);
    $(".lunbo-foot").css('background-color','rgba(0,0,0,0.6)');
    $(".lunbo .lunbo-img").css("display",'none');
    $(this).css("background-color","white");
    $(".lunbo-img").eq($(this).index()).css("display","block");
},function () {
    lunbo($(this).index())
});

$(".guide-list-first").not($("#list-first")[0]).mouseenter(function () {
    $(this).css("background-color","black");
    $(".guide-list .second-floor").eq($(this).index()-1).css("display","block")
});
$(".guide-list .guide-list-first").not($("#list-first")[0]).mouseleave(function () {
    $(this).css("background-color","rgba(0,0,0,0.5)");
    $(".guide-list .second-floor").eq($(this).index()-1).css("display","none")
});
$(".phone-login #phoneLogin").blur(function () {
   if($(this).val().length !==11 || $(this).val().match(/[^0-9]/)  )
   { if($(this).next()){$(this).next().remove()}
   $(this).after("<b style='color: red;border:0 transparent solid'>请输入正确手机号码！</b>")
   }
   else {{ if($(this).next()){$(this).next().remove()}
       $(this).after("<b title='ok' style='color: green;border:0 transparent solid'>格式正确！</b>")}
}});
$(" #phonePassword,#IdUser,#Idpassword ").blur(function () {
    if($(this).val().length <=6 || $(this).val().length >=16 ||$(this).val().match(/[^a-zA-Z0-9_]/)  )
    { if($(this).next()){$(this).next().remove()}
        $(this).after("<b style='color: red;border:0 transparent solid'>由6-16位字母数字下划线组成!</b>")
    }
    else {{ if($(this).next()){$(this).next().remove()}
        $(this).after("<b title='ok' style='color: green;border:0 transparent solid'>格式正确！</b>")}
    }});
$(".phone-login #phoneButton").click(function () {
    if($(".phone-login #phoneLogin").next().attr("title")!=="ok" || $(".phone-login #phonePassword").next().attr("title")!=="ok")
    {    alert("请输入正确手机号和密码！");
        return false}
});
$(" #IdBotton").click(function () {
    if($(" #IdUser").next().attr("title")!=="ok" || $(" #Idpassword").next().attr("title")!=="ok")
    {    alert("请输入正确用户名和密码！");
        return false}
});
$("#bigpic").mousemove(function (event) {
    $(this).css("cursor","move");
    var X = event.pageX-80,Y= event.pageY-500;
    var newpositon = -2*X + 'px'+ ' '+ -2*Y +'px';
    if(X > 320 || Y<=-80 ||Y>320) {$("#picarea").css("display","none");$("#showarea").css("display","none")}
    else {$("#picarea").css({"left":X,"top":Y,"display":"block"});$("#showarea").css({"display":"block","background-position":newpositon})}

});
$(".smallpicList").hover(function () {

$("#bigpicpic").attr("src",$(this)[0].src);
$("#showarea").css("background-image","url("+$(this)[0].src+")")
});
$("#banbenlist ").children("li").hover(function () {
    $(this).css("border","1px solid #FF0036")
},function () {
    $(this).css("border","1px solid #999")
});
$("#goodchoiceadd").click(function () {
    var date =Number($("#goodchoiceares").attr("placeholder")) ;
    $("#goodchoiceares").attr("placeholder",date+1)
});
$("#goodchoiceamin").click(function () {
    var date =Number($("#goodchoiceares").attr("placeholder"));
    console.log(date)
    if (date >=1){$("#goodchoiceares").attr("placeholder",date-1)}

});


$("#goodbuybutton2").click(function () {
    var shoppingcar = $("#shoppingCar");
    var bX = shoppingcar.offset().left, bY = shoppingcar.offset().top, aX = $(this).offset().left,
        aY = $(this).offset().top;
    var reX = bX - aX, reY = bY - aY;
    var m = 0.05, t=1, n = reY / reX - m * reX;x0=reX/60/t;
    newpic = "<img id='newpic' src=" + $("#bigpicpic")[0].src + " style='width:50px;height:50px;position:absolute;left:0;top:-50px;z-index:999'>";
    $(this).append(newpic);
    //创造图片节点
    //ax,ay 图片开始坐标,bx,by终点坐标
    //默认为抛物线轨迹,y=mx*x+nx,x是left的数值,y是top的数值,m>0,y'=2mx+n,y0=(2mx+n)*x0,m代表运动幅度,x0代表运动速度
    //终点相对坐标(bX-aX,bY-aY)-->(reX,reY)
    var target = $("#newpic");
    console.log(aX, aY, bX, bY, reX, reY);
    window.requestAnimationFrame(move);

    function move() {
        if (target.offset().left <= bX) {
            var picleftold = target.offset().left - aX;
            var picleft = picleftold + x0;
            //计算向左移动到达的相对坐标
            var pictopold = target.offset().top - aY;
            var pictop = pictopold + (2 * m * picleftold + n);
            //计算向上移动到达的相对坐标
            target.css("left", picleft + "px");
            target.css("top", pictop + "px");
            window.requestAnimationFrame(move);
        } else{target.remove();$("#shoppingCaricon").css('color','red ')}
        console.log(target.offset().left, target.offset().top);

        // console.log(aX,aY,bX,bY,reX,reY)
    }
});

