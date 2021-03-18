import base64
import rsa


def generate_keys():
    """生成公私钥对象, 写入文件"""
    pub_key, pri_key = rsa.newkeys(2048)
    pubkey_str = pub_key.save_pkcs1().decode()
    prikey_str = pri_key.save_pkcs1().decode()
    with open('public.pem', 'w', encoding='utf-8') as f:  # win系统环境下也可以兼容 / 目录分隔符
        f.write(pubkey_str)
    with open('private.pem', 'w', encoding='utf-8') as f:
        f.write(prikey_str)


def get_keys1():
    """获取公私钥对象"""
    with open('public.pem', 'r', encoding='utf-8') as f:
        pubkey_str = f.read()
    with open('private.pem', 'r', encoding='utf-8') as f:
        private_str = f.read()

    pubkey = rsa.PublicKey.load_pkcs1(pubkey_str.encode())
    private = rsa.PrivateKey.load_pkcs1(private_str.encode())

    return pubkey, private

def get_keys2():
    """获取公私钥对象"""
    with open('alipay_pub.pem', 'r', encoding='utf-8') as f:
        pubkey_str = f.read()
    with open('alipay_pri.pem', 'r', encoding='utf-8') as f:
        private_str = f.read()

    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey_str.encode())
    private = rsa.PrivateKey.load_pkcs1(private_str.encode())

    return pubkey, private


def encrypt_decrypt(message: str, pub_key, pri_key):
    # <1> 加密
    origin_cipher = rsa.encrypt(message.encode(), pub_key)
    print('origin_cipher:', origin_cipher)
    cipher_text = base64.b64encode(origin_cipher).decode()
    print('cipher_text:', cipher_text)
    # <2> 解密
    message2 = rsa.decrypt(base64.b64decode(cipher_text), pri_key).decode()
    print('message2:', message2)


def convert_number():
    """进制转换"""
    # two = 0b1100
    # print(bin(two))
    # print(oct(two))
    # print(hex(two))
    # print('-'*30)
    eight = '11'
    print(int(eight, 16))


def signature_verify(message, pub_key, pri_key):
    # 签名
    buff = rsa.sign(message.encode(), pri_key, 'SHA-256')
    sign = base64.b64encode(buff).decode()
    print(sign)

    # 验签
    alg = rsa.verify(message.encode(), base64.b64decode(sign), pub_key)
    print(alg)


if __name__ == '__main__':
    # generate_keys()
    pub_key, pri_key = get_keys2()
    message1 = '密码-hahaha'
    print('message1:', message1)
    encrypt_decrypt(message1, pub_key, pri_key)
    signature_verify(message1, pub_key, pri_key)


"""
body: {
    "app_id": app_id,
    "charset": "utf-8",
    "sign_type": "RSA2",
    "timestamp": timestamp,
    "sign": sign,
    "method": xxx,
    "biz_content": {},
    
}
"""

"""
GET: https://域名?app_id=xxx&charset=utf-8&sign_type&=xxx&timestamp=xxx&version=xxx&sign=xxx&method=xxx,

POST: http://域名?app_id=xxx&charset=utf-8&sign_type&=xxx&timestamp=xxx&version=xxx&sign=xxx

body = raw_data: dict
"""
