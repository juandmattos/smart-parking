#!/bin/bash
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p PuntaCarretasShopping -l 1 -ai 1 -an A -d 1450F8D346D80142 -q 8 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p PuntaCarretasShopping -l 1 -ai 2 -an B -d 6CD5B69AA55A998F -q 15 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p PuntaCarretasShopping -l 1 -ai 3 -an C -d F169C92836C6BD61 -q 9 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p PuntaCarretasShopping -l 2 -ai 1 -an A -d 8EC1B2C496D79789 -q 8 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p PuntaCarretasShopping -l 2 -ai 2 -an B -d 0587422811790E54 -q 20 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p PuntaCarretasShopping -l 2 -ai 3 -an C -d 3B6C05ACE681A093 -q 16 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p PuntaCarretasShopping -l 2 -ai 4 -an D -d 17665E7B44E5EFDC -q 5 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p PuntaCarretasShopping -l 3 -ai 1 -an A -d 7E1C75F22B089FB9 -q 12 > /dev/null 2>&1 &
nohup python Producer-Parkings-Kafka-Streaming_V5.py -p PuntaCarretasShopping -l 3 -ai 2 -an B -d 7A7C63A8F2813646 -q 7 > /dev/null 2>&1 &