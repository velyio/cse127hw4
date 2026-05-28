import sys, urllib.parse
from pymd5 import md5, padding
from urllib.parse import urlparse
url = sys.argv[1]

# http://bank.cse127.ucsd.edu/pa4/api?token=d6613c382dbb78b5592091e08f6f41fe&user=earlence&command1=ListSquirrels&command2=NoOp

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

#new token
h = md5(
    state=bytes.fromhex(known_token),
    count=padded_len * 8
)
suffix = b"&command3=UnlockAllSafes"
h.update(suffix)
new_token = h.hexdigest()

# new url
message_encoded = urllib.parse.quote(message, safe='=&+')
pad_encoded = urllib.parse.quote(pad, safe='')
suffix_encoded = urllib.parse.quote(suffix, safe='=&')

base = url[:url.index("?")]
new_url = f"{base}?token={new_token}&{message_encoded}{pad_encoded}{suffix_encoded}"

print(new_url)