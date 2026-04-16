import os


class Config:
    # ==============================
    # معلومات الأداة الأساسية
    # ==============================
    APP_NAME = "NOMIX CLONER"
    VERSION = "v1.0.0"  # يجب أن يطابق إصدار GitHub Tag
    VERSION_NAME = "NOMIX CLONER v1.0.0"
    GITHUB_REPO = "Abdallah1959/NOMIX-CLONER"
    GITHUB_API_LATEST = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    SUPPORT_LINK = "https://discord.gg/5AHucVEZ8p"
    DEVELOPER = "Body"

    # ==============================
    # إعدادات محرك الحماية (Rate Limiter)
    # ==============================
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 10))
    BASE_DELAY = float(os.getenv("BASE_DELAY", 5.0))

    # ==============================
    # سرعات النسخ الافتراضية
    # ==============================
    DELAY_ROLE = float(os.getenv("DELAY_ROLE", 0.8))
    DELAY_CATEGORY = float(os.getenv("DELAY_CATEGORY", 0.5))
    DELAY_CHANNEL = float(os.getenv("DELAY_CHANNEL", 0.5))
    DELAY_EMOJI = float(os.getenv("DELAY_EMOJI", 0.8))
    DELAY_STICKER = float(os.getenv("DELAY_STICKER", 1.5))
    DELAY_DELETE = float(os.getenv("DELAY_DELETE", 0.3))

    # ==============================
    # إعدادات التحديث التلقائي
    # ==============================
    ENABLE_AUTO_UPDATE_CHECK = True
    REQUEST_TIMEOUT = 10

    # ==============================
    # بيانات العرض داخل البرنامج
    # ==============================
    USER_AGENT = f"{APP_NAME}/{VERSION}"
