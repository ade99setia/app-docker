<?php

$appEnv = getenv('APP_ENV') ?: 'development';
$currentTime = date('Y-m-d H:i:s');

?><!doctype html>
<html lang="id">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Docker Dev vs Prod</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 720px;
            margin: 40px auto;
            padding: 0 16px;
            line-height: 1.6;
        }
        code {
            background: #f2f2f2;
            padding: 2px 6px;
        }
    </style>
</head>
<body>
    <h1>Contoh Docker Development vs Production</h1>
    <p>Halaman ini disediakan sebagai contoh minimal untuk materi pembelajaran.</p>
    <ul>
        <li>APP_ENV: <code><?php echo htmlspecialchars($appEnv, ENT_QUOTES, 'UTF-8'); ?></code></li>
        <li>Waktu server: <code><?php echo htmlspecialchars($currentTime, ENT_QUOTES, 'UTF-8'); ?></code></li>
        <li>Mode development memakai bind mount folder project</li>
        <li>Mode production memakai image + named volume</li>
    </ul>
</body>
</html>
