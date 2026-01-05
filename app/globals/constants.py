ROOT_ROLE_CODE = "ROOT"
ROOT_ROUTER_PARENT_ID = 0
UPLOAD_RESPONSE_FIELD_KEY = "X-File-Path"


# 常见的视频文件类型
VIDEO_MIME_TYPES = [
    "video/mp4",
    "video/x-matroska",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/quicktime",
    "video/webm",
    "video/ogg",
    "video/mpeg",
    "video/3gpp",
    "video/x-flv",
]


SUBSCRIPTION_TYPE_MAP = {
    "trial_7_days": "七天试用",
    "unpaid": "未付费",
    "paid": "付费会员",
    "expired": "付费会员过期",
}


SITE_CONFIG = {
    "code": 1,
    "msg": "",
    "time": 1719875136,
    "data": {
        "adminInfo": {
            "id": 1,
            "username": "admin",
            "nickname": "Admin",
            "avatar": "\/static\/images\/avatar.png",
            "last_login_time": "2024-07-02 07:05:36",
            "super": True,
        },
        "siteConfig": {
            "siteName": "BuildAdmin演示站",
            "version": "v1.0.0",
            "cdnUrl": "https:\/\/demo.buildadmin.com",
            "apiUrl": "https:\/\/buildadmin.com",
            "upload": {
                "maxsize": 10485760,
                "savename": "\/storage\/{topic}\/{year}{mon}{day}\/{filename}{filesha1}{.suffix}",
                "mimetype": "jpg,png,bmp,jpeg,gif,webp,zip,rar,xls,xlsx,doc,docx,wav,mp4,mp3,txt",
                "mode": "local",
            },
        },
        "terminal": {"installServicePort": "8000", "npmPackageManager": "pnpm"},
    },
}
