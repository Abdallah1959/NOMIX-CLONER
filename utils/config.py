import os

class Config:
    # معلومات الأداة
    VERSION = "v3.0 Enterprise"
    GITHUB_REPO = "Abdallah1959/NOMIX-CLONER"
    SUPPORT_LINK = "https://discord.gg/5AHucVEZ8p"
    DEVELOPER = "Body"

    # إعدادات محرك الحماية (Rate Limiter)
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 10))
    BASE_DELAY = float(os.getenv("BASE_DELAY", 5.0))
    
    # سرعات النسخ الافتراضية
    DELAY_ROLE = 0.8
    DELAY_CATEGORY = 0.5
    DELAY_CHANNEL = 0.5
    DELAY_EMOJI = 0.8
    DELAY_STICKER = 1.5
    DELAY_DELETE = 0.3