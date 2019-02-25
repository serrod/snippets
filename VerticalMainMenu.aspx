<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:mso="urn:schemas-microsoft-com:office:office" xmlns:msdt="uuid:C2F41010-65B3-11d1-A29F-00AA00C14882">
<head id="Head1" runat="server">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" x-undefined="" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<title>Vertical Main Navigation:Dynamic Menu Template</title>


<!--[if gte mso 9]><SharePoint:CTFieldRefs runat=server Prefix="mso:" FieldList="FileLeafRef,_dlc_DocId,_dlc_DocIdUrl,_dlc_DocIdPersistId"><xml>
<mso:CustomDocumentProperties>
<mso:_dlc_DocId msdt:dt="string">VAZUKHW3ZV4A-949061940-2</mso:_dlc_DocId>
<mso:_dlc_DocIdItemGuid msdt:dt="string">7ab8fe76-98e7-4b7e-a0f8-9d2ca4d9145b</mso:_dlc_DocIdItemGuid>
<mso:_dlc_DocIdUrl msdt:dt="string">https://intranet.ent.southcom.mil/sites/j3/j34/_layouts/DocIdRedir.aspx?ID=VAZUKHW3ZV4A-949061940-2, VAZUKHW3ZV4A-949061940-2</mso:_dlc_DocIdUrl>
</mso:CustomDocumentProperties>
</xml></SharePoint:CTFieldRefs><![endif]-->
</head>

<body>
 <script>


     // get site information, url, path, and empty arrays
     var vSharePointLibrary = "VerticalNavigationMenu";
     var vSharePointUrl = window.location.protocol + "//" + window.location.host + _spPageContextInfo.webServerRelativeUrl;
     var vSharePointFullPath = vSharePointUrl + "/_vti_bin/listdata.svc/" + vSharePointLibrary;
     var vResultsListAllArr = [];

     // functions to check for data types int and float
     function IsInt(x) {
         return !isNaN(x) && eval(x).toString().length == parseInt(eval(x)).toString().length
     }
     function IsFloat(x) {
         return !isNaN(x) && !IsInt(eval(x)) && x.toString().length > 0
     }
     function StrUrl(str) {
         return str.split(",", vMylistSortedArr[i].Url)[0];
     }

     // access JSON string url, parse results into array,sort by group, and split url
     $.ajax({
         url: vSharePointFullPath,
         type: "GET",
         headers: { "Accept": "application/json; odata=verbose" },
         success: function (vdata) {
             $.each(vdata.d.results, function (index, item) {
                 vResultsListAllArr.push({ Title: item.Title, Group: item.GroupValue, Order: item.Order, Url: item.URL });
             });

             // sort by order id
             var vResultslistSortedArr = vResultsListAllArr.sort(function (a, b) { return a.Order - b.Order });

             for (var i = 0; i < vResultslistSortedArr.length; i++) {

                 var vResultsFullUrl = String(vResultslistSortedArr[i].Url);
                 var vResultsUrl = vResultsFullUrl.split(",");


                 if (vResultslistSortedArr[i].Group == 'NO' && IsInt(vResultslistSortedArr[i].Order)) {

                     $("#vDynamicMenuRoot").append('<li role="presentation"><a href="' + vResultsUrl[0] + '" target="_blank"> &#8921 ' + vResultslistSortedArr[i].Title + '</a></li>');
                 }
                 if (vResultslistSortedArr[i].Group == 'YES' && IsInt(vResultslistSortedArr[i].Order)) {
                     $("#vDynamicMenuRoot").append('<li class="dropdown" role="presentation"><a class="dropdown-toggle" role="button" aria-expanded="false" aria-haspopup="true" href="#" data-toggle="dropdown"> &#8921 ' + vResultslistSortedArr[i].Title + '<span class="caret"></span></a><ul class="dropdown-menu" id="vMenu-' + vResultslistSortedArr[i].Order + '"></ul></li>');
                 }
                 if (vResultslistSortedArr[i].Group == 'NO' && IsFloat(vResultslistSortedArr[i].Order)) {
                     $("#vMenu-" + Math.floor(vResultslistSortedArr[i].Order)).append('<li role="presentation"><span class="glyphicon glyphicon-menu-right"></span><a href="' + vResultsUrl[0] + '" target="_blank" title="' + vResultsUrl[1] + '"> ' + vResultslistSortedArr[i].Title + '</a></li>');
                 }
             }

         },
         error: function (error) {
             alert("ERROR: Library (" + MyLibrary + ") JSON Failing");
         }
     });
        
    </script>
    <!-- START NAV -->
    <div class="container-fluid col-md-4">
        <div class="row">
            <ul class="nav nav-tabs nav-stacked" id="vDynamicMenuRoot" style="text-transform:uppercase;">
                
                <!-- JS CONTENT -->
            </ul>
        </div>
    </div>

</body>
</html>