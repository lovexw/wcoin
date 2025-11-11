"""
WCOIN Wallet
钱包模块 - 生成地址和管理密钥
"""

import hashlib
import json
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64


class Wallet:
    """钱包类 - 管理密钥对和地址"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None
        
    def generate_keypair(self):
        """生成新的密钥对"""
        key = RSA.generate(2048)
        self.private_key = key.export_key()
        self.public_key = key.publickey().export_key()
        self.address = self._generate_address(self.public_key)
        return self.address
        
    def _generate_address(self, public_key):
        """从公钥生成地址"""
        sha256_hash = hashlib.sha256(public_key).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        hashed = ripemd160.digest()
        address = base64.b64encode(hashed).decode('utf-8')[:34]
        return f"W{address}"
        
    def sign_transaction(self, transaction_data):
        """签名交易"""
        if not self.private_key:
            raise ValueError("No private key available")
            
        key = RSA.import_key(self.private_key)
        h = SHA256.new(json.dumps(transaction_data, sort_keys=True).encode())
        signature = pkcs1_15.new(key).sign(h)
        return base64.b64encode(signature).decode('utf-8')
        
    @staticmethod
    def verify_signature(public_key, transaction_data, signature):
        """验证交易签名"""
        try:
            key = RSA.import_key(public_key)
            h = SHA256.new(json.dumps(transaction_data, sort_keys=True).encode())
            sig_bytes = base64.b64decode(signature)
            pkcs1_15.new(key).verify(h, sig_bytes)
            return True
        except:
            return False
            
    def save_to_file(self, filepath):
        """保存钱包到文件"""
        wallet_data = {
            'private_key': self.private_key.decode('utf-8') if self.private_key else None,
            'public_key': self.public_key.decode('utf-8') if self.public_key else None,
            'address': self.address
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(wallet_data, f, indent=2)
            
    def load_from_file(self, filepath):
        """从文件加载钱包"""
        if not os.path.exists(filepath):
            return False
            
        with open(filepath, 'r') as f:
            wallet_data = json.load(f)
            
        self.private_key = wallet_data['private_key'].encode('utf-8') if wallet_data.get('private_key') else None
        self.public_key = wallet_data['public_key'].encode('utf-8') if wallet_data.get('public_key') else None
        self.address = wallet_data.get('address')
        return True
