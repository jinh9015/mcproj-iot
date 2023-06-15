#include <WiFi.h>

// #define WIFI_SSID "TECHBREW_2G"    // WiFi SSID
// #define WIFI_PWD "tech1234!"             // WiFi 비밀번호
#define WIFI_SSID "SK_WiFiGIGA5E36_2.4G"    // WiFi SSID
#define WIFI_PWD "AWM15@3832"

void setup_wifi() {
  delay(10);                              // 안정성을 위한 딜레이 설정.
  Serial.println();
  Serial.print("WiFi 연결 시도중 : ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PWD);                // 와이파이 연결 시도

  while (WiFi.status() != WL_CONNECTED) {         // 와이파이가 연결중이 아닐 때
    delay(500);
    Serial.print(".");                            
  }

  // 와이파이 연결 성공 시
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());              // WiFi IP 출력
}

/*
void wifi_task(void *pvParameter) {

  double _Leq_dB;
  
  while(1) {
    if(xQueueReceive(samples_queue, &_Leq_dB, 0)) { // If there is data in the queue
      if (WiFi.status() == WL_CONNECTED) {
        Serial.printf("%.1f\n", _Leq_dB);
      }
    }
    else { // If the queue is empty, check WiFi status
      if(WiFi.status() != WL_CONNECTED) {
        setup_wifi();
      }
    }
    
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}
*/