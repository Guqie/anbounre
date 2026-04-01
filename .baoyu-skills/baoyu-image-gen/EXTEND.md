# baoyu-image-gen preferences
version: 1.0.0

# Default provider (google, openai, dashscope, replicate)
default_provider: google

# Default models per provider
default_models:
  google: gemini-3-pro-image-preview
  openai: gpt-image-1.5
  dashscope: z-image-turbo
  replicate: google/nano-banana-pro

# Default quality (normal=1024, 2k=2048)
default_quality: normal

# Default aspect ratio
default_ar: "16:9"

# API Base URL (optional override)
# api_base: https://api.openai.com/v1
