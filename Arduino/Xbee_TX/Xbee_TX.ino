#include <XBee.h>

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();

uint8_t payloadBienvenida[] = { 72, 111, 108, 97, 32, 120, 98, 101, 101, 32, 114, 111, 117, 116, 101, 114, 33 };
uint8_t  payloadData[] = { 72 };

boolean bienvenida = true;
int statusLed = 13;
int errorLed = 13;
int dataLed = 13;

XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x4147a057);
ZBTxRequest zbTxBienvenida = ZBTxRequest(addr64, payloadBienvenida, sizeof(payloadBienvenida));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

ZBTxRequest zbTx = ZBTxRequest(addr64, payloadData, sizeof(payloadData));

//// create reusable response objects for responses we expect to handle 
//ZBRxResponse rx = ZBRxResponse();
//ModemStatusResponse msr = ModemStatusResponse();

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

  Serial.begin(9600);
  xbee.setSerial(Serial);

  flashLed(statusLed, 3, 50);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (bienvenida) {
    Serial.println("Se envio Bienvenida");
    xbee.send(zbTxBienvenida);
    bienvenida = false;
    // flash TX indicator
    flashLed(statusLed, 1, 100);
  }

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
        Serial.println(txStatus.getDeliveryStatus());
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
  delay(5000);
}
