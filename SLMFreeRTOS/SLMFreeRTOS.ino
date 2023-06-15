#include "slm.h"
#include "wifi.h"

void setup() {
  Serial.begin(115200);
  setup_wifi();

  if (WiFi.status() != WL_CONNECTED) {
    setup_wifi();
  }

  task_slm();
  delay(500);
  // task_record();
}

void task_slm() {
  samples_queue = xQueueCreate(8, sizeof(sum_queue_t));
  xTaskCreate(mic_i2s_reader_task, "Mic I2S Reader", I2S_TASK_STACK, NULL, I2S_TASK_PRI, NULL);
  double _Leq_dB;

  while(xQueueReceive(samples_queue, &_Leq_dB, portMAX_DELAY)) {
    Serial.printf("%.1f\n", _Leq_dB);
  }
}

void loop() {

}
