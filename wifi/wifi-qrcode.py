from segno import helpers

def makeWifiQrd(qrd_path, wifi_name, passwd, security='WPA/WPA2 PSK', hidden=False, scale=10):
    """
    生成 WIFI 二维码图片
    :param qrd_path: 生成二维码图片的保存路径
    :param wifi_name:
    :param passwd:
    :param security: 身份验证类型;值应为 WEP 或 WPA。设置为 None则省略该值。nopass 相当于将该值设置为None，但在前一种情况下，该值不会被省略。
    :param hidden: 网络是否隐藏, 默认为 False, True-隐藏 False-未隐藏
    :param scale: 表示单个模块的大小(默认为1), 即指定生成图片的尺寸大小
    :return:
    """
    wf = helpers.make_wifi(ssid=wifi_name,
                           password=passwd,
                           security=security,
                           hidden=hidden)
    wf.save(qrd_path, scale=10)


if __name__ == '__main__':
    #qrd_path = 'C:\\Users\\lenovo\\Pictures\\wifi_qrd2.png'
    makeWifiQrd("qr-wifi.png", 'D-Link_DIR-629', '123456789')