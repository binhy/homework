/**
 * Created by Administrator on 2017/1/17.
 */


group=[
    {'value':'1',txt:'开发组'},
    {'value':'2',txt:'运维组'},
    {'value':'3',txt:'测试组'}
];

stat = [
    {'value':'1',txt:'在线'},
    {'value':'2',txt:'离线'}
];


/*左侧菜单点击显示效果*/
$(".menu").click(function () {
    $(this).next('.menu-body').hide("normal").show("slow");
});


//错误消息提示
function alertMsg(message) {
    $("#err-msg").text(message);
    $("#err-msg").css('display','block');

    var t = setTimeout('$("#err-msg").css("display","none")',1500);
}

//点击菜单
$("#menu-1-1").click(function () {
    $(".content").show();
    $(".readme").hide();
});


$("#menu-1-2").click(function () {
    $(".readme").show();
    $(".content").hide();

});


// 全选/取消
function selectAll() {
    if($('#editstatus').attr("status") == "true"){
        $(".chk_id").each(function () {
            var editlist = $(this).parent().nextAll();
            if ($(this).prop("checked")){   //true
                trToViewModule(editlist);
                $(this).removeAttr("checked");
            }else {                         //false
                $(this).prop("checked", true);
                trToEditModule(editlist);
            }
        });


        //
        var chk_num=0;
        $(".chk_id").each(function () {
            if($(this).prop("checked")){
                chk_num +=1;
            }
        });

        if (chk_num == 0){
            backInitStatus();
        }


    }else {
        $(".chk_id").each(function () {
            if ($(this).prop("checked")){
                $(this).removeAttr("checked");
            }else {
                $(this).prop("checked",true);
            }
        });


    }
}


// 单行编辑
function editCurrTr(ths) {
    var result={};    //定义一个对象
    var edilist=$(ths).parent().prevAll();  //获取所有的td对象

    $(edilist).each(function () {
        if ($(this).attr('edit') == '1'){
            var key=$(this).attr('col');
            var vals=$(this).text();
            result[key]=vals;
        }
    });


    //显示遮罩图层
    $("#show_bg").css({'display':'block'});
    $(".show").css({
        'display':'block',
        'left':($("body").width()/2 - $(".show").width()/2)+'px',
        'top':($(document).height()/2 - $(".show").height()/2)-30+'px'
    });


    //填充值
    $("#host").val(result.host);
    $("#ip").val(result.ip);
    $("#cpu").val(result.cpu);
    $("#disk").val(result.disk);
    $("#mem").val(result.mem);


    //填充两个select
    var tmpa=['group','stat'];
    for(var i in tmpa){
        var def_content=window[tmpa[i]];
        var optionstr='';

        $(def_content).each(function () {
            if (($(this).attr('txt') == result.group )||($(this).attr('txt') == result.stat )) {
               optionstr += "<option value='" + $(this).attr('value') + "' selected>" + $(this).attr('txt') + "</option>";
            }else{
               optionstr += "<option value='" + $(this).attr('value') + "' >" + $(this).attr('txt') + "</option>";
            }
        });

        optionstr="<select class='edit-input'>" + optionstr + "</select>";
        $("#"+tmpa[i]).html(optionstr);

    }
}


/*将选中的所有行的指定列进入编辑模式*/
function editAllTr() {
    var check_num=0;
    if($("#editstatus").attr("status") == "true"){
        alertMsg("已经是编辑模式");
        return false;
    }

    $(".chk_id").each(function () {
        if($(this).prop('checked')){
            //若改行已经选中，找它后面的所有兄弟td标签
            var edistlist=$(this).parent().nextAll();
            trToEditModule(edistlist);
            check_num+=1;
        }
    });


    //如果未找到选中的记录则无法进入编辑模式
    if(check_num == 0){
        alertMsg('请选择要编辑的记录！');
        return false;
    }else {
        //设置编辑状态为true
        $("#editstatus").attr("status",true);
        //改变颜色
        $("#a-edit").css({'background':'lawngreen'});
        $("#a-save").css({'background':'lawngreen'});
    }
}


/*保存修改*/
function saveAllTr() {
    if($("#editstatus").attr("status") == "false"){
        alertMsg("编辑模式未启用");
        return false
    }else {
        //如果是编辑模式
        $(".chk_id").each(function () {
            if($(this).prop('checked')){
                //若改行已经选中，找它后面的所有兄弟td标签
                var edistlist=$(this).parent().nextAll();
                //改为view模式
                trToViewModule(edistlist);
                //修改完将选中的标签取消
                $(this).removeAttr("checked");
            }
        });
        backInitStatus();
    }
    alertMsg("修改成功")
}






/*关闭遮罩层*/
function hideShow() {
    $(".show").css({'display':'none'});
    $("#show_bg").css({'display':'none'});
}


//将tr转换为编辑模式函数
function trToEditModule(editlist) {
    $(editlist).each(function () {
        if($(this).attr('edit') == '1'){
            var td_value=$(this).text();  //获取td的text值

            if ($(this).attr('isselect') == '1'){
                var select_name=$(this).attr('col');
                var select_content=window[select_name];
                var optionstr='';
                $(select_content).each(function () {
                    if($(this).attr('txt') == td_value){
                        optionstr +="<option value='" + $(this).attr('value') + "' selected>" + $(this).attr('txt') + "</option>";
                    }else
                        optionstr +="<option value='" + $(this).attr('value') +"' >" +$(this).attr('txt') + "</option>";
                });


                optionstr="<select class='edit-input'>" + optionstr+"</select>";
                $(this).html(optionstr);

            }else {

                $(this).html("<input type='text' class='edit-input' value='" + td_value + "'/>")
            }
        }

    });
}



//将当前行由编辑模式变为浏览模式
function trToViewModule(edilist){
    $(edilist).each(function () {
        if ($(this).attr('edit') == '1') {
            //如果是select标签获取text值
            if ($(this).attr('isselect') == '1'){
               //console.log($(this).children(":first").children(":selected"));
                var td_value = $(this).children(":first").children(":selected").text();

            }else {
                var td_value = $(this).children(":first").val();
            }
            $(this).html(td_value);
        }
    });

}






// 取消编辑模式并恢复初始状态
function backInitStatus() {
    //保存完成后将编辑按钮的颜色恢复
    $("#a-edit").css({'background':'#ffffff'});
    $("#a-save").css({'background':'#ffffff'});
    //将编辑模式置为初始状态
    $("#editstatus").attr("status",false);
    //全选chkbox取消选中
    $("#checkall").removeAttr("checked");
}


/* 单独点击每个checkbox框时触发事件 */
function chkChoose(ths) {
    if($(this).prop("checked")){
        if($("#editstatus").attr("status")=="true"){
            var edistlist=$(this).parent().nextAll();
            trToEditModule(edistlist)
        }
    }else {
        if($("#editstatus").attr("status")=="true"){
            var edistlist=$(this).parent().nextAll();
            trToViewModule(edistlist)
        }


        var chk_num=0;
        $(".chk_id").each(function () {
            if($(this).prop("checked")){
                chk_num +=1;
            }
        });

        if (chk_num>0){
            return false
        }else {
            backInitStatus()
        }

    }

}