from segno import helpers

#制作二维码名片
qr = helpers.make_mecard(name="优酷视频",email="youku@sina.com",phone="18091241241")

qr.save("card.png",scale=10)