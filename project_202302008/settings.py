from pathlib import Path
import os

# 🔧 BASE_DIR proyek
BASE_DIR = Path(__file__).resolve().parent.parent

# 🚨 Keamanan
SECRET_KEY = 'django-insecure-6gm%o_zunaon=!yt-bzu#&fkh@)9wg7!5$empr^=fh44c-24_3'
DEBUG = True
ALLOWED_HOSTS = []

# ✅ Aplikasi yang digunakan
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'widget_tweaks',
    'django_extensions',  # ← Tambahkan ini agar show_urls berfungsi

    'pembelian',
]


# 🔒 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔗 Routing utama
ROOT_URLCONF = 'project_202302008.urls'

# 🧩 Konfigurasi Template
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'project_202302008', 'templates'),  # folder global template
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # ✅ Agar kategori tersedia di semua template
                'pembelian.context_processors.kategori_list',
            ],
        },
    },
]

# ⚙️ WSGI
WSGI_APPLICATION = 'project_202302008.wsgi.application'

# 🗂️ Database (default SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔐 Validasi Password
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Internasionalisasi
LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 🖼️ File Statis
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 🔑 Primary Key Default
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🚪 Redirect setelah login/logout
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
