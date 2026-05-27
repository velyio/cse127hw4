import sys
import urllib.parse
from pymd5 import md5, padding
from urllib.parse import urlparse, parse_qs, unquote

url = "http://bank.cse127.ucsd.edu/pa4/api?token=d6613c382dbb78b5592091e08f6f41fe&user=earlence&command1=ListSquirrels&command2=NoOp"

parsed = urlparse(url)
params = parsed.query

#find the token
token_start = params.index("token=") + len("token=")
token_end = params.index("&", token_start)
known_token = params[token_start:token_end]

#find mssage: "user=earlence&command1=ListSquirrels&command2=NoOp"
msg_start = params.index("user=")
message = params[msg_start:]

#find message len
password_len = 8
total_len = password_len + len(message)

#find padding len
pad = padding(total_len * 8)
padded_len = total_len + len(pad)

h = md5(
    state=bytes.fromhex(known_token),
    count=padded_len * 8
)
suffix = "&command3=UnlockAllSafes"
h.update(suffix)
new_token = h.hexdigest()

forged = message.encode('latin-1') + pad + suffix.encode('latin-1')
encoded = urllib.parse.quote(forged, safe='=&')

#creating url new
base = url[:url.index("?")]
new_url = f"{base}?token={new_token}&{encoded}"
print(new_url)