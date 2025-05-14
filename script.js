const TOTAL = 64;
let index = 1;
let texts = [];

// DOM 참조
const wrapper = document.getElementById('wrapper');
const templateCard = document.getElementById('template-card');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');

// 카드 클릭 토글 핸들러
function flipHandler(e) {
  e.currentTarget.classList.toggle('flipped');
}

// 새 카드 만들어서 반환
function makeCard(idx) {
  const newCard = templateCard.cloneNode(true);
  newCard.removeAttribute('id');
  // front/back 요소
  const img = newCard.querySelector('.card-img');
  const txt = newCard.querySelector('.card-text');
  img.src = `images/${idx}.jpg`;
  txt.textContent = texts[idx - 1] || '';
  // 클릭 시 뒤집기
  newCard.addEventListener('click', flipHandler);
  return newCard;
}

// 카드 슬라이드 인 애니메이션
function slideIn(idx) {
  const distance = window.innerHeight * 0.14; // 80%만큼 아래에서 시작
  const newCard = makeCard(idx);

  // 1) 초기 설정: 화면 아래(보이지 않게)
  newCard.style.transition = 'none';
  newCard.style.transform = `translateY(${distance}px)`;
  wrapper.appendChild(newCard);

  // 이미지 로드 완료 후 wrapper 크기 동기화 및 애니 실행
  const img = newCard.querySelector('.card-img');
  img.onload = () => {
    // 래퍼 크기를 카드 크기와 동기화
    wrapper.style.width = img.clientWidth + 'px';
    wrapper.style.height = img.clientHeight + 'px';
    // 래퍼 보이기
    wrapper.style.visibility = 'visible';

    // 애니메이션: 아래→원위치
    requestAnimationFrame(() => {
      newCard.style.transition = 'transform 0.7s ease-out';
      newCard.style.transform = 'translateY(0)';
    });

    // 애니 끝나면, 아래 카드(첫 번째 노드)를 제거
    newCard.addEventListener('transitionend', () => {
      const old = wrapper.querySelector('.card:not(.flipped), .card.flipped');
      if (old && old !== newCard) {
        wrapper.removeChild(old);
      }
    }, { once: true });
  };
  // slideIn 함수 img.onload 내부 가장 마지막에:
wrapper.style.visibility = 'visible';

}

// contents.txt 로딩
fetch('contents.txt')
  .then(r => r.text())
  .then(raw => {
    // "\n숫자." 패턴으로 분리
    const parts = raw.split(/\n(?=\d+\.)/);
    texts = parts.map(t => t.replace(/^\d+\.\s*/, '').trim());
    // 초기 카드 슬라이드 인
    slideIn(index);
  });

// 이전 버튼
prevBtn.onclick = () => {
  index = index > 1 ? index - 1 : TOTAL;
  slideIn(index);
};

// 다음 버튼
nextBtn.onclick = () => {
  index = Math.floor(Math.random() * TOTAL) + 1;
  slideIn(index);
};
