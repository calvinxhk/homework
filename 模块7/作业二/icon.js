$("#phone-login").click(function(){ $(".box-login .phone-login").css("display","block"); $(this).css("color","blue"); $("#user-login").css("color","#abb6d2");$(".box-login .id-login").css("display","none")});
$("#user-login").click(function(){$(".box-login .phone-login").css("display","none"); $(this).css("color","blue");$("#phone-login").css("color","#abb6d2");$(".box-login .id-login").css("display","block")});
$(".user-login-mask .exit").click(function(){$(".user-login-mask").css("display","none")})
$(".digg-a").mouseover(function(){if ($(".icon-hand").css("background-position")!="0px -20px"){$(".icon-hand").css("background-position","0 0")}});
$(".digg-a").mouseout(function(){if ($(".icon-hand").css("background-position")!="0px -20px"){$(".icon-hand").css("background-position","0 -40px")}});
$(".discus-a").mouseover(function(){if ($(".icon-note").css("background-position")!="0px -80px"){$(".icon-note").css("background-position","0 -60px")}});
$(".discus-a").mouseout(function(){if ($(".icon-note").css("background-position")!="0px -80px"){$(".icon-note").css("background-position","0 -100px")}});
$(".collect-a").mouseover(function(){if ($(".icon-collect").css("background-position")!="0px -140px"){$(".icon-collect").css("background-position","0 -120px")}});
$(".collect-a").mouseout(function(){if ($(".icon-collect").css("background-position")!="0px -140px"){$(".icon-collect").css("background-position","0 -160px")}});
$(".content-item").mouseover(function(){$(".share-site-to").css("display","inline")});
$(".content-item").mouseout(function(){$(".share-site-to").css("display","none")});
$(".icon-sina").mouseover(function(){$(this).css("background-position","0px -90px")});
$(".icon-sina").mouseout(function(){$(this).css("background-position","0px 0px")});
$(".icon-douban").mouseover(function(){$(this).css("background-position","0px -105px")});
$(".icon-douban").mouseout(function(){$(this).css("background-position","0px -15px")});
$(".icon-qqzone").mouseover(function(){$(this).css("background-position","0px -120px")});
$(".icon-qqzone").mouseout(function(){$(this).css("background-position","0px -30px")});
$(".icon-renren").mouseover(function(){$(this).css("background-position","0px -150px")});
$(".icon-renren").mouseout(function(){$(this).css("background-position","0px -60px")});
$("a").mouseover(function(){$(this).css("text-decoration","underline")});
$("a").mouseout(function(){$(this).css("text-decoration","none")});
$(".ct_pagepa").mouseover(function(){$(this).css("background-color","#369");$(this).css("color","white")});
$(".ct_pagepa").mouseout(function(){$(this).css("background-color","white");$(this).css("color","#369")});
$(window).scroll(function(){if($(document).scrollTop()>'300'){$(".back-to-top").css("display","block")}else{$(".back-to-top").css("display","none")}});
$(".back-to-top").mouseover(function(){$(this).css("background-position","0px -39px")});
$(".back-to-top").mouseout(function(){$(this).css("background-position","0px 0px")});
$(".back-to-top").click(function(){$("html,body").animate({scrollTop:0},500)});
$(".action-menu a").mouseover(function(){$(this).css("background-color","#9F79EE");$(this).css("color","white")});
$(".action-menu a").mouseout(function(){$(this).css("background-color","transparent");$(this).css("color","#c0cddf")});
$(".digg-a").click(function(){if ($(".icon-hand").css("background-position")!="0px -20px"){$("#plus1").css("display","inline");$(".icon-hand").css("background-position","0px -20px");var a = $("#like").html();$("#like").html(Number(a)+1);$("#plus1").animate({bottom:'50px',fontSize:"35px", opacity:'0.2'},300,function(){$(this).css({"display":"none","bottom":"0","font-size":"12px","opacity":"1","left":"0"})});}else{$("#minus1").css("display","inline");$(".icon-hand").css("background-position","0px -40px");var a = $("#like").html();$("#like").html(a-1);$("#minus1").animate({bottom:'50px',fontSize:"35px", opacity:'0.2'},300,function(){$(this).css({"display":"none","bottom":"0","font-size":"12px","opacity":"1","left":"0"})});}});
$(".discus-a").click(function(){$(".comment-area-box").toggle()});
$("#comment-exit").mouseover(function(){$(this).css("background-position","0px -38px")});
$("#comment-exit").mouseout(function(){$(this).css("background-position","0px -28px")});
$("#comment-exit").click(function(){$(".comment-area-box").toggle()});
$(".news-image").mouseenter(function(){if ($(this).parent().children("input").val() ==0){$(this).css("cursor","zoom-in")}else {$(this).css("cursor","zoom-out")}});
$(".news-image").click(function(){
if($(this).parent().children("input").val() ==0)
{$(this).animate({width:"200px",height:"200px",right:"131px"},500);
$(this).parent().children("input").val(1) }
else{$(this).animate({width:"65px",height:"65px",right:"0px"},500);
$(this).parent().children("input").val(0)}
});
$(".comment-bottom .view").click(function(){$(".comment-bottom .waiting").toggle()})