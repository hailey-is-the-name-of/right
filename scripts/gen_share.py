#!/usr/bin/env python3
# scripts/gen_share.py

import os
import re
from jinja2 import Template

# ==== 설정 영역 ====  
# 이미지가 올라가는 폴더
IMAGES_DIR = "images"
# 공유 페이지(.html)를 생성할 폴더
SHARE_DIR  = "share"
# index.html 파일 경로
INDEX_FILE = "index.html"
# 사이트의 기본 URL (GitHub Pages, custom domain 등)
# 예: https://hailey-is-the-name-of.github.io/right
BASE_URL = "https://bluenew.life/right"

# HTML 템플릿: {{n}} 자리에 이미지 번호가 들어갑니다
OG_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta property="og:title" content="맞는 말 시리즈">
  <meta property="og:description" content="맞는 말 시리즈">
  <meta property="og:image" content="{{ base }}/images/{{n}}.jpg">
  <meta property="og:url"   content="{{ base }}/share/{{n}}.html">
  <meta name="twitter:card" content="summary_large_image">
  <title>맞는 말 시리즈</title>
  <meta http-equiv="refresh" content="0; url={{ base }}/index.html?img={{n}}">
</head>
<body>
  <p>공유 페이지로 이동 중입니다...</p>
</body>
</html>
"""

def main():
    # 1) images 폴더 내 숫자형 파일명을 추출
    entries = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith('.jpg')]
    nums = sorted(
        int(os.path.splitext(f)[0])
        for f in entries
        if os.path.splitext(f)[0].isdigit()
    )

    # 2) share 디렉토리 생성
    os.makedirs(SHARE_DIR, exist_ok=True)

    # 3) share/{n}.html 생성
    tpl = Template(OG_TEMPLATE)
    for n in nums:
        html = tpl.render(n=n, base=BASE_URL)
        out_path = os.path.join(SHARE_DIR, f"{n}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated: {out_path}")

    # 4) index.html에서 totalImages 값 갱신
    total = len(nums)
    pattern = r"(const\s+totalImages\s*=\s*)\d+;"
    replacement = rf"\1{total};"
    with open(INDEX_FILE, 'r+', encoding='utf-8') as f:
        content = f.read()
        new_content = re.sub(pattern, replacement, content)
        f.seek(0)
        f.write(new_content)
        f.truncate()
    print(f"Updated totalImages to {total} in {INDEX_FILE}")

if __name__ == '__main__':
    main()
