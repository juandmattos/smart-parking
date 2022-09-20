#!/bin/bash

nohup python Producer-Parkings-Kafka-Streaming_V5.py -p TresCrucesShopping -l 1 -ai 1 -an A -d 327671F2009776BE -q 7 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p TresCrucesShopping -l 1 -ai 2 -an B -d DD5F6C5BDA3D7A95 -q 17 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p TresCrucesShopping -l 1 -ai 3 -an C -d 4DE1C372D9293D6F -q 9 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p TresCrucesShopping -l 2 -ai 1 -an A -d 9AA1AD57EC8B8856 -q 13 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p TresCrucesShopping -l 2 -ai 2 -an B -d 64ED8BB2354F293B -q 15 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p TresCrucesShopping -l 2 -ai 3 -an C -d 51FE29B1E7DACCB6 -q 8 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p TresCrucesShopping -l 2 -ai 4 -an D -d 5AF3A94B18BC85EC -q 5 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p TresCrucesShopping -l 3 -ai 1 -an A -d CE6EFF5988ECBF74 -q 10 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p TresCrucesShopping -l 3 -ai 2 -an B -d FCB85470B7C0E0CC -q 12 > /dev/null 2>&1 &