#!/bin/bash

while sleep 10;
    do 
        api_key=`cat /openmlconfig/api_key.txt`; 
        echo "API key:$api_key";  
        java -Xmx4G -jar /openmlsource/Java/evaluate.jar -config "server = http://website/;api_key = $api_key" -f process_dataset;
        java -Xmx4G -jar /openmlsource/Java/evaluate.jar -config "server = http://website/;api_key = $api_key" -f evaluate_run;
    done