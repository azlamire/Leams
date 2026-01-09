# Настройка стриминга

## Обзор

Leams поддерживает несколько протоколов стриминга для обеспечения низкой задержки и высокого качества трансляций.

### Поддерживаемые протоколы

| Протокол | Латентность | Качество | Поддержка браузеров |
|----------|-------------|----------|---------------------|
| **RTMP** | 3-5s | Высокое | Требует плеер |
| **HLS** | 6-30s | Высокое | Все современные |
| **WebRTC** | <1s | Среднее-Высокое | Chrome, Firefox, Safari |
| **DASH** | 6-30s | Высокое | Все современные |

---

## Настройка RTMP стриминга

### Для стримеров (OBS Studio)

#### 1. Получение Stream Key

Войдите в ваш аккаунт Leams и перейдите в Dashboard:

```
https://leams.com/dashboard/stream-settings
```

Ваш Stream Key выглядит примерно так:
```
live_sk_abc123xyz789def456
```

⚠️ **Важно**: Никогда не делитесь вашим Stream Key публично!

#### 2. Настройка OBS Studio

**Шаг 1**: Откройте OBS Studio → Settings → Stream

**Шаг 2**: Выберите настройки:
```
Service: Custom
Server: rtmp://ingest.leams.com/live
Stream Key: [ваш stream key]
```

**Шаг 3**: Настройте Output (Output → Output Mode: Advanced):

```
Encoder: x264 (или NVENC/AMD если есть GPU)
Rate Control: CBR
Bitrate: 
  - 1080p60: 6000 Kbps
  - 1080p30: 4500 Kbps
  - 720p60: 4500 Kbps
  - 720p30: 3000 Kbps
Keyframe Interval: 2
CPU Usage Preset: veryfast (для x264)
Profile: high
Tune: zerolatency
```

**Шаг 4**: Настройте Video:

```
Base Resolution: 1920x1080
Output Resolution: 1920x1080 (или 1280x720)
FPS: 60 (или 30)
```

**Шаг 5**: Настройте Audio:

```
Sample Rate: 48 kHz
Channels: Stereo
Bitrate: 160 kbps
```

#### 3. Тестирование соединения

Нажмите "Start Streaming" в OBS. Если всё настроено правильно:

- ✅ OBS покажет зелёный индикатор
- ✅ На Leams Dashboard появится "🔴 LIVE"
- ✅ Зрители смогут видеть ваш стрим с задержкой ~5-10 секунд

### Для стримеров (Streamlabs Desktop)

```
Stream Type: Streaming Services
Service: Custom RTMP
RTMP URL: rtmp://ingest.leams.com/live
Stream Key: [ваш stream key]
```

### Для стримеров (XSplit)

```
Outputs → Add Output → Custom RTMP
Name: Leams
RTMP URL: rtmp://ingest.leams.com/live/[stream_key]
```

---

## Рекомендуемые настройки битрейта

### Видео битрейт

| Разрешение | FPS | Битрейт (Kbps) | Интернет (Upload) |
|------------|-----|----------------|-------------------|
| 1920x1080 | 60 | 6000 | 8+ Mbps |
| 1920x1080 | 30 | 4500 | 6+ Mbps |
| 1280x720 | 60 | 4500 | 6+ Mbps |
| 1280x720 | 30 | 3000 | 4+ Mbps |
| 854x480 | 30 | 2000 | 3+ Mbps |

### Аудио битрейт

```
Музыка/подкасты: 256 kbps
Обычный стрим: 160 kbps
Низкая пропускная способность: 128 kbps
```

---

## Настройка HLS (для просмотра)

HLS автоматически генерируется из RTMP потока. Никаких дополнительных настроек не требуется.

### Adaptive Bitrate Streaming

Leams автоматически создаёт несколько качеств:

```
1080p60 - 6000 Kbps
720p60  - 4500 Kbps
720p30  - 3000 Kbps
480p30  - 2000 Kbps
360p30  - 1000 Kbps
```

Плеер автоматически выбирает оптимальное качество на основе:
- Скорости интернета зрителя
- Размера окна плеера
- Производительности устройства

---

## WebRTC стриминг (Low Latency)

⚠️ **Экспериментальная функция**

Для стриминга с минимальной задержкой (<1s) используйте WebRTC.

### Настройка в OBS (через WHIP)

**Требования**:
- OBS Studio 30.0+
- Плагин OBS-WHIP

**Настройка**:
```
Service: WHIP
Server: https://webrtc.leams.com/whip
Bearer Token: [ваш access token]
```

### Для просмотра

Включите "Low Latency Mode" в настройках плеера на странице стрима.

---

## Настройка RTMP сервера (для self-hosted)

### nginx-rtmp конфигурация

```nginx
rtmp {
    server {
        listen 1935;
        chunk_size 4096;
        
        application live {
            live on;
            record off;
            
            # Аутентификация
            on_publish http://backend:8000/api/streams/verify;
            on_publish_done http://backend:8000/api/streams/end;
            
            # HLS настройки
            hls on;
            hls_path /tmp/hls;
            hls_fragment 2s;
            hls_playlist_length 10s;
            hls_nested on;
            
            # Adaptive bitrate
            hls_variant _high BANDWIDTH=6000000;
            hls_variant _mid BANDWIDTH=3000000;
            hls_variant _low BANDWIDTH=1000000;
            
            # DASH (опционально)
            dash on;
            dash_path /tmp/dash;
            dash_fragment 2s;
            
            # Запись VODs
            record all;
            record_path /var/rec;
            record_unique on;
            record_suffix -%Y%m%d-%H%M%S.flv;
            
            # Callback'и
            on_record_done http://backend:8000/api/vods/process;
        }
    }
}

http {
    server {
        listen 8080;
        
        # HLS
        location /hls {
            types {
                application/vnd.apple.mpegurl m3u8;
                video/mp2t ts;
            }
            root /tmp;
            add_header Cache-Control no-cache;
            add_header Access-Control-Allow-Origin *;
        }
        
        # DASH
        location /dash {
            root /tmp;
            add_header Cache-Control no-cache;
            add_header Access-Control-Allow-Origin *;
        }
    }
}
```

### Запуск nginx-rtmp в Docker

```yaml
# docker-compose.yml
services:
  rtmp:
    image: alfg/nginx-rtmp
    ports:
      - "1935:1935"
      - "8080:8080"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./hls:/tmp/hls
      - ./recordings:/var/rec
    restart: unless-stopped
```

---

## Video Transcoding

### FFmpeg конфигурация

```bash
ffmpeg -i rtmp://localhost/live/stream_key \
  -c:v libx264 -preset veryfast -tune zerolatency \
  -b:v 6000k -maxrate 6000k -bufsize 12000k \
  -s 1920x1080 -r 60 -g 120 \
  -c:a aac -b:a 160k -ar 48000 \
  -f hls -hls_time 2 -hls_list_size 5 \
  -hls_flags delete_segments+append_list \
  /tmp/hls/stream_key/index.m3u8
```

### Adaptive Bitrate Transcoding

```bash
#!/bin/bash
INPUT="rtmp://localhost/live/$1"
OUTPUT_PATH="/tmp/hls/$1"

ffmpeg -i "$INPUT" \
  # 1080p60
  -c:v:0 libx264 -preset veryfast -b:v:0 6000k -s:v:0 1920x1080 -r:v:0 60 \
  # 720p60
  -c:v:1 libx264 -preset veryfast -b:v:1 4500k -s:v:1 1280x720 -r:v:1 60 \
  # 720p30
  -c:v:2 libx264 -preset veryfast -b:v:2 3000k -s:v:2 1280x720 -r:v:2 30 \
  # 480p30
  -c:v:3 libx264 -preset veryfast -b:v:3 2000k -s:v:3 854x480 -r:v:3 30 \
  # Audio
  -c:a aac -b:a 160k -ar 48000 \
  # HLS output
  -f hls -hls_time 2 -hls_list_size 5 \
  -master_pl_name master.m3u8 \
  -var_stream_map "v:0,a:0 v:1,a:0 v:2,a:0 v:3,a:0" \
  "$OUTPUT_PATH/stream_%v.m3u8"
```

---

## CDN интеграция

### CloudFlare Stream

```javascript
// Конфигурация
const CLOUDFLARE_ACCOUNT_ID = 'your_account_id';
const CLOUDFLARE_API_TOKEN = 'your_api_token';

// Загрузка VOD
async function uploadVOD(videoPath) {
  const formData = new FormData();
  formData.append('file', fs.createReadStream(videoPath));
  
  const response = await axios.post(
    `https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/stream`,
    formData,
    {
      headers: {
        'Authorization': `Bearer ${CLOUDFLARE_API_TOKEN}`,
      }
    }
  );
  
  return response.data.result.uid;
}
```

### AWS CloudFront

```python
# S3 + CloudFront для VODs
import boto3

s3 = boto3.client('s3')
cloudfront = boto3.client('cloudfront')

def upload_vod(file_path, stream_id):
    # Загрузка в S3
    s3.upload_file(
        file_path,
        'leams-vods',
        f'vods/{stream_id}/index.m3u8',
        ExtraArgs={'ContentType': 'application/x-mpegURL'}
    )
    
    # Инвалидация CloudFront cache
    cloudfront.create_invalidation(
        DistributionId='YOUR_DISTRIBUTION_ID',
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [f'/vods/{stream_id}/*']
            },
            'CallerReference': str(time.time())
        }
    )
```

---

## Мониторинг стримов

### Проверка статуса

```bash
# Проверка RTMP соединения
curl http://localhost:8080/stat

# Проверка HLS сегментов
ls -lh /tmp/hls/stream_key/

# Мониторинг битрейта
ffprobe rtmp://localhost/live/stream_key
```

### Метрики

- **Viewer count**: Количество активных зрителей
- **Bitrate**: Текущий битрейт стрима
- **Frame drops**: Потерянные кадры
- **Buffer health**: Состояние буфера
- **Latency**: Задержка от стримера до зрителя

---

## Troubleshooting

### Проблема: "Failed to connect to server"

**Решение**:
1. Проверьте firewall (порт 1935 должен быть открыт)
2. Убедитесь в правильности Stream Key
3. Проверьте RTMP URL: `rtmp://ingest.leams.com/live`

### Проблема: Высокая задержка

**Решение**:
1. Уменьшите буфер в OBS: Advanced → Network Buffering → 400ms
2. Используйте WebRTC вместо HLS для просмотра
3. Оптимизируйте keyframe interval: 2 секунды

### Проблема: Низкое качество видео

**Решение**:
1. Увеличьте битрейт
2. Проверьте скорость upload интернета
3. Измените preset на "faster" или "medium"
4. Используйте GPU encoding (NVENC/AMD)

### Проблема: Stream "лагает" у зрителей

**Решение**:
1. Проверьте стабильность upload соединения
2. Включите CBR (Constant Bitrate) mode
3. Уменьшите разрешение или FPS
4. Проверьте логи сервера на packet loss

---

## Дополнительные ресурсы

- [OBS Studio настройки](https://obsproject.com/wiki/)
- [FFmpeg документация](https://ffmpeg.org/documentation.html)
- [HLS спецификация](https://datatracker.ietf.org/doc/html/rfc8216)
- [WebRTC overview](https://webrtc.org/getting-started/overview)
