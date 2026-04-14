import base64
import time
from uuid import uuid4

from captcha.image import ImageCaptcha

# 简单的内存缓存用于存储验证码 (生产环境建议使用 Redis)
# 格式: { "uuid": {"code": "1234", "expire": 1234567890} }
_captcha_cache = {}

def generate_captcha(length: int = 4, expire_seconds: int = 120):
    """
    生成图片验证码及标识
    """
    image = ImageCaptcha(width=160, height=60)
    # 生成随机验证码内容
    import random
    import string
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    # 生成图片内容
    data = image.generate(code)
    img_b64 = base64.b64encode(data.getvalue()).decode()
    
    # 生成唯一标识
    captcha_uuid = str(uuid4())
    
    # 存入缓存
    _captcha_cache[captcha_uuid] = {
        "code": code.lower(),
        "expire": time.time() + expire_seconds
    }
    
    # 清理过期验证码 (避免内存泄漏)
    cleanup_expired_captcha()
    
    return {
        "uuid": captcha_uuid,
        "img": f"data:image/png;base64,{img_b64}"
    }

def verify_captcha(captcha_uuid: str, code: str) -> bool:
    """
    验证图片验证码
    """
    # 检查是否存在
    cache_item = _captcha_cache.get(captcha_uuid)
    if not cache_item:
        return False
    
    # 检查是否过期
    if time.time() > cache_item["expire"]:
        del _captcha_cache[captcha_uuid]
        return False
    
    # 验证并删除 (一次性)
    is_valid = cache_item["code"] == code.lower()
    del _captcha_cache[captcha_uuid]
    
    return is_valid

def cleanup_expired_captcha():
    """清理过期的验证码"""
    now = time.time()
    expired_keys = [k for k, v in _captcha_cache.items() if now > v["expire"]]
    for k in expired_keys:
        del _captcha_cache[k]
