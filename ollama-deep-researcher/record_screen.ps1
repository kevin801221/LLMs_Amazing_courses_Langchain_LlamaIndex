Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds

$outputPath = "screen_recording_$(Get-Date -Format 'yyyyMMdd_HHmmss').mp4"
$ffmpeg = "ffmpeg"

Write-Host "Starting screen recording... Press Ctrl+C to stop."
& $ffmpeg -f gdigrab -framerate 30 -offset_x 0 -offset_y 0 -video_size "$($screen.Width)x$($screen.Height)" -i desktop -c:v libx264 -preset ultrafast -qp 0 $outputPath
