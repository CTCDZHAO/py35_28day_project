from time import time
# 时间戳获取
ts=int(time())
print(ts)

# 签名的获取
# token前50位+加时间戳，然后进行RSA加密
token='kdjsklfjskdlfjkldjflkdjfffkldjlkdjgkdjfgkjdfgkjdshjkdhhjgdhfjgdfjhgkdfjhgkjdhgjkdhgjkhkgj'
data=token[:50]+str(ts)
