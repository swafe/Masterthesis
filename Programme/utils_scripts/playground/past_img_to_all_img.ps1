#powershellISE öffnen, cd 'path of script' und .\past_img_to_all_img.ps1 (script ausführen)
#vorher folder dataset_9091 mit IMG in Subordner kobieren
$source = 'E:\Datasets_GGU_Bodenproben_orig\Bodenproben_recognition\9091\*\*.jpg'
$direction = 'E:\Datasets_GGU_Bodenproben_orig\Bodenproben_recognition\dataset\dataset_9091\all_img2'
#gci hauptordner -file -recurse -Filter .jpg | Move-Item -Destination direction
copy-Item -Path $source -Destination $direction
#echo 'naem'