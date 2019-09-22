from segno import helpers

qr = helpers.make_wifi(ssid="My WiFi",password="123456789",security="WPA")

qr.version

qr.designator

qr.save("qr-wifi.png",scale=10)