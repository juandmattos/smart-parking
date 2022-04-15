 #include <DHT.h>
#include <XBee.h>
#include <Adafruit_Sensor.h>

#define DHTTYPE DHT11

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();


uint8_t payloadBienvenida[] = { 0x48, 0x69, 0x20, 0x58, 0x62, 0x65, 0x65, 0x20, 0x4e, 0x65, 0x74, 0x77, 0x6f, 0x72, 0x6b, 0x21 };
uint8_t  payloadData[] = { 0x53, 0x50, 0, 0x54, 0, 0x48, 0, 0x48, 0x53, 0, 0 };

boolean bienvenida = true;
const int PIR = 10;
const int TH = 9;
const int HS = A5; //mido la humedad al analogico 0
int HS_VAL = 0;
int statusLed = 13;
int errorLed = 13;
int dataLed = 13;

int pirState = LOW;           // de inicio no hay movimiento
int mov = 0;                  // estado del pin


XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x4147a057);
ZBTxRequest zbTxBienvenida = ZBTxRequest(addr64, payloadBienvenida, sizeof(payloadBienvenida));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

ZBTxRequest zbTx = ZBTxRequest(addr64, payloadData, sizeof(payloadData));

DHT dht(TH, DHTTYPE);

void flashLed(int pin, int times, int wait) {

  for (int i = 0; i < times; i++) {
    digitalWrite(pin, HIGH);
    delay(wait);
    digitalWrite(pin, LOW);

    if (i + 1 < times) {
      delay(wait);
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  pinMode(statusLed, OUTPUT);
  pinMode(errorLed, OUTPUT);
  pinMode(dataLed,  OUTPUT);
  pinMode(PIR, INPUT);
  pinMode(HS, INPUT);
  
  Serial.begin(9600);
  xbee.setSerial(Serial);
  dht.begin();

  flashLed(statusLed, 3, 50);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (bienvenida) {
    Serial.println("Se envio Bienvenida");
    xbee.send(zbTxBienvenida);
    bienvenida = false;
    // flash TX indicator
    delay(2000);
  }

  float H = dht.readHumidity();
  float T = dht.readTemperature();
  HS_VAL = analogRead(HS);
//GET SENSOR DATA

  // Get PIR state
  mov = digitalRead(PIR);
  Serial.println(mov);
  if (mov == HIGH) {
    payloadData[2] = 0x01;
    mov = LOW;
  } else {
    payloadData[2] = 0x00;
  }
  // Get DHT11 data
  if (isnan(T)) {
    payloadData[4] = 'E';
  } else {
    //data collect
  }
  
  if (isnan(H)) {
    payloadData[6] = 'E';
  } else {
    //data collect
  }
  payloadData[9] = HS_VAL >> 8 & 0xff;
  payloadData[10] = HS_VAL & 0xff;
  if (isnan(HS_VAL)) {
    payloadData[9] = 0x45;
    payloadData[10] = 0x45;
  } else {
    payloadData[9] = HS_VAL >> 8 & 0xff;
    payloadData[10] = HS_VAL & 0xff;
  }

  delay(500);
  xbee.send(zbTx);

  // flash TX indicator
  flashLed(statusLed, 1, 100);

  // after sending a tx request, we expect a status response
  // wait up to half second for the status response
  if (xbee.readPacket(500)) {
    // got a response!

    // should be a znet tx status              
    if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
      xbee.getResponse().getZBTxStatusResponse(txStatus);

      // get the delivery status, the fifth byte
      if (txStatus.getDeliveryStatus() == SUCCESS) {
        // success.  time to celebrate
        flashLed(statusLed, 5, 50);
      } else {
        // the remote XBee did not receive our packet. is it powered on?
        //Serial.println(txStatus.getDeliveryStatus());
        flashLed(errorLed, 3, 500);
      }
    }
  } else if (xbee.getResponse().isError()) {
    //nss.print("Error reading packet.  Error code: ");  
    //nss.println(xbee.getResponse().getErrorCode());
  } else {
    // local XBee did not provide a timely TX Status Response -- should not happen
    flashLed(errorLed, 2, 50);
  }
}
