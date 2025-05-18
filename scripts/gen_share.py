#!/usr/bin/env python3
# scripts/gen_share.py

import os
import re
from jinja2 import Template

# 1) 설정
IMAGES_DIR = "images"
SHARE_DIR  = "share"
INDEX_FILE = "index.html"

# 2) HTML 템플릿 ({{n}}에 숫자 삽입)
OG_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta property="og:title" content="맞는 말!">
  <meta property="og:description" content="맞는 말 시리즈">
  <meta property="og:image" content="/images/{{n}}.jpg">
  <meta property="og:url"   content="/share/{{n}}.html">
  <meta name="twitter:card" content="summary_large_image">
  <title>이재명의 말을 들어보세요!</title>
  <meta http-equiv="refresh" content="0; url=/index.html?img={{n}}">
</head>
<body>
  <p>공유 페이지로 이동 중입니다...</p>
</body>
</html>
"""

# 3) images 폴더에서 숫자만 골라서 정렬
nums = sorted(
    int(fname.split(".")[0])
    for fname in os.listdir(IMAGES_DIR)
    if fname.endswith(".jpg") and fname.split(".")[0].isdigit()
)

# 4) share 디렉토리 보장
os.makedirs(SHARE_DIR, exist_ok=True)

# 5) 각 번호별로 share/{n}.html 파일 생성
tpl = Template(OG_TEMPLATE)
for n in nums:
    out_path = os.path.join(SHARE_DIR, f"{n}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(tpl.render(n=n))

# 6) index.html의 totalImages 값 갱신
with open(INDEX_FILE, "r+", encoding="utf-8") as f:
    content = f.read()
    # const totalImages = X;
    new_content = re.sub(
        r"(const\s+totalImages\s*=\s*)\d+;",
        rf"\1{len(nums)};",
        content
    )
    f.seek(0)
    f.write(new_content)
    f.truncate()
