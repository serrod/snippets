<?php


function getDirContents($dir){
        $results = array();
        $files = scandir($dir);

            foreach($files as $key => $value){
                if(!is_dir($dir. DIRECTORY_SEPARATOR .$value)){
                    $results[] = $value;
                } else if(is_dir($dir. DIRECTORY_SEPARATOR .$value)) {
                    $results[] = $value;
                    getDirContents($dir. DIRECTORY_SEPARATOR .$value);
                }
            }
    }

# 
print_r(getDirContents('/home/srodriguez/Documents/php-file-parser'));


?>
