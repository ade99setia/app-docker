curl.exe -X POST "http://localhost:8080/webhook/set/ade-setia" -H "apikey: KunciRahasiaSaya999" -H "Content-Type: application/json" -d "{\"webhook\":{\"enabled\":true,\"url\":\"http://host.docker.internal:8000/api/webhook/wa\",\"webhookByEvents\":false,\"webhookBase64\":false,\"events\":[\"MESSAGES_UPSERT\",\"MESSAGES_UPDATE\",\"MESSAGES_DELETE\",\"SEND_MESSAGE\"]}}"

curl -X POST "http://localhost:8080/webhook/set/ade-setia" \
  -H "apikey: KunciRahasiaSaya999" \
  -H "Content-Type: application/json" \
  -d '{"webhook":{"enabled":true,"url":"http://host.docker.internal:8000/api/webhook/wa","webhookByEvents":false,"webhookBase64":false,"events":["MESSAGES_UPSERT","MESSAGES_UPDATE","MESSAGES_DELETE","SEND_MESSAGE"]}}'

curl -X POST "http://localhost:8080/webhook/set/ade-setia" \
  -H "apikey: KunciRahasiaSaya999" \
  -H "Content-Type: application/json" \
  -d '{"webhook":{"enabled":true,"url":"http://localhost:18084/api/webhook/evolution/K9fTQ2mXvL8aWzP1sRj6UdYhC0nBqE4gM7Vw3JtAkc5ZxDpNHyFrbSuOlIeiG2","webhookByEvents":false,"webhookBase64":false,"events":["MESSAGES_UPSERT","MESSAGES_UPDATE","MESSAGES_DELETE","SEND_MESSAGE"]}}'

<!-- =========================================================================== -->
<!-- Connect to IP Local / Tailscale -->

IDN SOLO
api/webhook/evolution/K9fTQ2mXvL8aWzP1sRj6UdYhC0nBqE4gM7Vw3JtAkc5ZxDpNHyFrbSuOlIeiG2

BDN KARANGANYAR
api/webhook/evolution/M3zKJc2YQWf8sL7G1B0xE4tH9RdaUuVw6iP5AyrnDkXhSCTbFvNjZpOlImeqg

curl -X POST "http://localhost:8080/webhook/set/ade-setia" \
  -H "apikey: KunciRahasiaSaya999" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook": {
      "enabled": true,
      "url": "http://100.125.217.5:8888/api/webhook/evolution/K9fTQ2mXvL8aWzP1sRj6UdYhC0nBqE4gM7Vw3JtAkc5ZxDpNHyFrbSuOlIeiG2",
      "webhookByEvents": false,
      "webhookBase64": false,
      "events": [
        "MESSAGES_UPSERT",
        "MESSAGES_UPDATE",
        "MESSAGES_DELETE",
        "SEND_MESSAGE"
      ]
    }
  }'