# RTSP使用YOLOv8的專案

這個專案是用於使用YOLOv8進行RTSP影像辨識並呼叫API的工作。下面是有關如何在Docker中設定和運行這個專案的指南。

## Docker設定範例

以下是一個Docker Compose設定的範例，用於運行YOLOv8的容器。請確保你已經安裝了Docker和Docker Compose。

```yaml
version: '3'

services:
  yolov8cpu:
    container_name: yolov8cpu
    image: raidavidyang/yolov8cpu:v1
    restart: always
    privileged: true
    stdin_open: true
    environment:
      - APIURL=http://220.132.208.73:5170/rail
      - SOURCE=rail_cam1
      - CAPTION=萬華工地
      - RTSP_URL=rtsp://user:user123456@125.228.247.68:7001/797e5e39-dcf7-7613-2279-8a16f39e7ff8?ch01.264?dev=1
      - DETECTION_COUNT=7
    tty: true
    # volumes:
    #   - ./:/app
    logging:
      driver: json-file
      options:
        max-size: "1m"
    command: /bin/bash -c "cd /app && python app.py"
