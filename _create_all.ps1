# -*- coding: utf-8 -*-
$ErrorActionPreference = "Stop"
$base = "D:\ming_software\my-tool\my-tool\pkgTools\pages"
function w($name, $content) {
    $path = Join-Path $base ($name + "\" + $name + ".vue")
    [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
    Write-Host "Created: $name"
}

