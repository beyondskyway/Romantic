// 输入数据检测
/*commom use */
function checkData(idname, alertnospace) {
    var str = document.getElementById(idname);
    var val = str.value;
    var instruction = document.getElementById(alertnospace);
    if (val.indexOf(" ") >= 0) {
        instruction.innerHTML = "[请不要输入空格]";
    } else {
        instruction.innerHTML = " ";
    }
}
function focusClearWarn(id) {
    var instruction = document.getElementById(id);
    //var instruction1 = document.getElementById(aa);
    instruction.innerHTML = " ";
    //instruction1.innerHTML = " ";
}
/* page_one check  start*/
function format_qq() {
    var z = $("#qq").val();
    var atposy = z.length;
    if (atposy > 13 || atposy < 5 || isNaN(z)) {
        $("#qqRight").append("[请输入5到13位数值]");
    }
}

function format_pwd() {
    var z = $("#password").val();
    var atposy = z.length;
    if (atposy > 20 || atposy < 5) {
        $("#passwordRight").append("[请输入5-20位字符]");
    }
}

$(document).ready(function () {
    $("#qq").blur(function () {
        checkData('qq', 'qqRight');
        format_qq();
    }).focus(function () {
        focusClearWarn('qqRight');
    });
    $("#password").blur(function () {
        checkData('password', 'passwordRight');
        format_pwd();
    }).focus(function () {
        focusClearWarn('passwordRight');
    });
    $("#next_btn").click(function () {
        var qq = $("#qq").val();
        var pwd = $("#password").val();
        var pwd_len = pwd.length;
        var qq_len = qq.length;
        if (qq_len > 13 || qq_len < 5 || isNaN(qq)) {
            $("#qq").focus();
        }
        else if(pwd_len < 5 || pwd_len > 20 || pwd.indexOf(" ") >= 0 ) {
            $("#password").focus();
        }
        else{
            $("#page_one").hide().next().show();
        }
    });
});
/* page_one check  end*/
/* page_two check  start*/
function format_height() {
    var y = document.forms["edit"]["height"].value;
    if (y > 250 || y < 100 || isNaN(y)) {
        $("#heightRight").append("[请输入100-250cm的数值]");
    }
}
function format_phone() {
    var x = document.forms["edit"]["phone"].value;
    var atpos = x.length;
    if (atpos !== 11 || isNaN(x)) {
        $("#phoneRight").append("[请输入11位手机号]");
    }
}
function format_age() {
    var y = document.forms["edit"]["age"].value;
    if (y > 60 || y < 16 || isNaN(y)) {
        $("#ageRight").append("[请输入16-60间年龄]");
    }
}
function format_nickname() {
    var y = document.forms["edit"]["nickname"].value.length;
    if (y < 2 || y > 20) {
        $("#nicknameRight").append("[请输入2-20个字]");
    }
}
function format_department() {
    var y = document.forms["edit"]["department"].value.length;
    if (y < 2 || y > 20) {
        $("#departmentRight").append("[请输入2-20个字]");
    }
}
function format_name() {
    var y = document.forms["edit"]["name"].value.length;
    if (y < 2 || y > 20) {
        $("#nameRight").append("[请输入2-20个字]");
    }
}
function format_identity() {
    var y = document.forms["edit"]["identity_id"].value.length;
    if (y != 18) {
        $("#identityRight").append("[请输入18位身份证号]");
    }
}

$(document).ready(function () {
    $("#nickname").blur(function () {
        checkData('nickname', 'nicknameRight');
        format_nickname();
    }).focus(function () {
        focusClearWarn('nicknameRight');
    });
    $("#age").blur(function () {
        checkData('age', 'ageRight');
        format_age();
    }).focus(function () {
        focusClearWarn('ageRight');
    });
    $("#height").blur(function () {
        //checkData('height', 'heightRight');
        format_height();
    }).focus(function () {
        focusClearWarn('heightRight');
    });
    $("#department").blur(function () {
        checkData('department', 'departmentRight');
        format_department();
    }).focus(function () {
        focusClearWarn('departmentRight');
    });
    $("#name").blur(function () {
        checkData('name', 'nameRight');
        format_name();
    }).focus(function () {
        focusClearWarn('nameRight');
    });
    $("#phone").blur(function () {
        checkData('phone', 'phoneRight');
        format_phone();
    }).focus(function () {
        focusClearWarn('phoneRight');
    });
    $("#identity_id").blur(function () {
        checkData('identity_id', 'identityRight');
        format_identity();
    }).focus(function () {
        focusClearWarn('identityRight');
    });
    $("#submit").click(function () {
        var nickname = $("#nickname").val();
        var nickname_len = nickname.length;
        var department = $("#department").val();
        var department_len = department.length;
        var name = $("#name").val();
        var name_len = name.length;
        var height = $("#height").val();
        var phone = $("#phone").val();
        var phone_len = phone.length;
        var age = $("#age").val();
        var identity_len = $("#identity_id").val().length;
        if(nickname_len < 2 || nickname_len > 20 || nickname.indexOf(" ") >= 0){
            $("#nickname").focus();
            return false;
        }
        else if(age < 16 || age > 60 || isNaN(age) || age.indexOf(" ") >= 0){
            $("#age").focus();
            return false;
        }
        else if (100 > height || height > 250 || isNaN(height) || height.indexOf(" ") >= 0) {
            $("#height").focus();
            return false;
        }
        else if (department_len < 2 || department_len > 20 || department.indexOf(" ") >= 0){
            $("#department").focus();
            return false;
        }
        else if (name_len < 2 || name_len > 20 || name.indexOf(" ") >= 0){
            $("#name").focus();
            return false;
        }
        else if (phone_len != 11 || isNaN(phone) || phone.indexOf(" ") >= 0) {
            $("#phone").focus();
            return false;
        }
        else if (identity_len != 18) {
            $("#identity_id").focus();
            return false;
        }
        else{
            return true;
        }
    })
});
