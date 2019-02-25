/* Load function when ready */
$(document).ready(function () {
    
    /* add timeout since SP adds webpater after page is loaded */
    setTimeout(function () {
        $("div[title*='Blocked']").css("background-color", "#696969'");
        $("div[title*='Lunch']").css("background-color", "#696969'");
        $("div[title*='TSC WG']").css("background-color", "#DDA0DD'");
        $("div[title*='JEC']").css("background-color", "#DDA0DD'");
        $("div[title*='JWWG']").css("background-color", "#DDA0DD'");
        $("div[title*='EKMWG']").css("background-color", "#DDA0DD'");
        $("div[title*='CUB']").css("background-color", "#CCCC00'");
        $("div[title*='MUB']").css("background-color", "#CCCC00'");
        $("div[title*='PMB WG']").css("background-color", "#DDA0DD'");
        $("div[title*='4-Star']").css("background-color", "#666600'");
        $("div[title*='2-Star']").css("background-color", "#666600'");
        $("div[title*='OPT']").css("background-color", "#666600'");
        $("div[title*='Roundtable']").css("background-color", "#666600'");
        $("div[title*='PLN']").css("background-color", "#666600'");
        $("div[title*='TCP JPG']").css("background-color", "#00FA9A'");

    }, 1000);
});
