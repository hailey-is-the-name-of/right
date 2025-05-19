#!/usr/bin/env python3
# scripts/gen_share.py

import os
import re
from jinja2 import Template

# ======== 경로 설정 ========
# 이 스크립트 파일 위치를 기준으로 상위 디렉토리(ROOT) 찾기
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# images, share 폴더 및 index.html 경로
IMAGES_DIR = os.path.join(BASE_DIR, "images")
SHARE_DIR  = os.path.join(BASE_DIR, "share")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
# 사용 중인 사이트 기본 URL (GitHub Pages 또는 커스텀 도메인)
BASE_URL   = "https://bluenew.life/right"

# ======== HTML 템플릿 ========
# {{n}}, {{base}} 변수로 이미지 번호와 사이트 URL을 삽입
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
    # 1. images 폴더에서 .jpg 파일 추출 (파일명은 숫자여야 함)
    try:
        entries = os.listdir(IMAGES_DIR)
    except FileNotFoundError:
        print(f"Error: '{IMAGES_DIR}' 폴더를 찾을 수 없습니다.")
        return

    nums = sorted(
        int(os.path.splitext(f)[0])
        for f in entries
        if f.lower().endswith('.jpg') and os.path.splitext(f)[0].isdigit()
    )

    # 2. share 디렉토리 생성
    os.makedirs(SHARE_DIR, exist_ok=True)

    # 3. share/{n}.html 생성
    tpl = Template(OG_TEMPLATE)
    for n in nums:
        html = tpl.render(n=n, base=BASE_URL)
        out_path = os.path.join(SHARE_DIR, f"{n}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated share page: {out_path}")

    # 4. index.html 안의 totalImages 값 갱신
    total = len(nums)
    pattern = r"(const\s+totalImages\s*=\s*)\d+;"
    replacement = rf"\1{total};"
    try:
        with open(INDEX_FILE, 'r+', encoding='utf-8') as f:
            content = f.read()
            new_content = re.sub(pattern, replacement, content)
            f.seek(0)
            f.write(new_content)
            f.truncate()
        print(f"Updated totalImages to {total} in {INDEX_FILE}")
    except FileNotFoundError:
        print(f"Error: '{INDEX_FILE}' 파일을 찾을 수 없습니다.")

if __name__ == '__main__':
    main()
