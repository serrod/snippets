<?php
/*
 load small JSON files to fake JSON API for testing
*/
header("Access-Control-Allow-Origin: *");
header('Content-Type: application/json');

$myfile = fopen("Crm.json", "r") or die("Unable to open file!");
while(!feof($myfile)) {
	echo fgets($myfile);
}
fclose($myfile);  
?>
