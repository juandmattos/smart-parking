#!/bin/bash

python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p PuntaCarretasShopping -l 1 -i 1 -a A --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p PuntaCarretasShopping -l 1 -i 2 -a B --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p PuntaCarretasShopping -l 1 -i 3 -a C --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p PuntaCarretasShopping -l 2 -i 1 -a A --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p PuntaCarretasShopping -l 2 -i 2 -a B --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p PuntaCarretasShopping -l 2 -i 3 -a C --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p PuntaCarretasShopping -l 2 -i 4 -a D --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p PuntaCarretasShopping -l 3 -i 1 -a A --device --qt-slots 7 &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p PuntaCarretasShopping -l 3 -i 2 -a B --device --qt-slots 5 &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p TresCrucesShopping -l 1 -i 1 -a A --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p TresCrucesShopping -l 1 -i 2 -a B --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p TresCrucesShopping -l 1 -i 3 -a C --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p TresCrucesShopping -l 2 -i 1 -a A --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p TresCrucesShopping -l 2 -i 2 -a B --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p TresCrucesShopping -l 2 -i 3 -a C --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p TresCrucesShopping -l 2 -i 4 -a D --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p TresCrucesShopping -l 3 -i 1 -a A --device --qt-slots &
sleep 10
python /opt/smart-parking/Python/Generator/Producer-Parkings-Kafka-Streaming_V4.py -p TresCrucesShopping -l 3 -i 2 -a B --device --qt-slots &
