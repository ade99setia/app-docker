$ErrorActionPreference = 'Stop'

$uri = 'http://localhost:8088/api/hf/hf01'
$headers = @{ 'Content-Type' = 'application/json' }
$body = '{"device_id":"G013524JZXDD784","product_key":"uniwin","time":"1776344825"}'

Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body