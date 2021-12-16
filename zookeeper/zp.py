from registerservice import RegisterCenter

rs = RegisterCenter("127.0.0.1:2181")

rs.service_register("fill", "provider", {"ip": "192.168.1.33", "port": "8000"})

rs.service_register("fill", "provider", {"ip": "192.168.2.33", "port": "9000"})


