from software_shop_webapp import app
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
this_machine = s.getsockname()[0]
s.close()
print(f"my ip: {this_machine}")

app.run(debug=True, host=this_machine,port=8888)
