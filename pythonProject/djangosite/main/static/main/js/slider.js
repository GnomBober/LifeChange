const track = document.querySelector('.carousel-track');
const leftButton = document.querySelector('.carousel-btn.left');
const rightButton = document.querySelector('.carousel-btn.right');
const cards = document.querySelectorAll('.test-card');

const cardWidth = cards[0].offsetWidth + 20; // Ширина карточки с учетом margin
const visibleCards = 6; // Количество видимых карточек
let currentPosition = 0; // Начальная позиция

rightButton.addEventListener('click', () => {
    const maxPosition = -(cards.length - visibleCards) * cardWidth;
    currentPosition -= cardWidth * visibleCards;
    if (currentPosition < maxPosition) {
        currentPosition = maxPosition; // Остановить на последней группе карточек
    }
    track.style.transform = `translateX(${currentPosition}px)`;
});

leftButton.addEventListener('click', () => {
    currentPosition += cardWidth * visibleCards;
    if (currentPosition > 0) {
        currentPosition = 0; // Остановить на первой группе карточек
    }
    track.style.transform = `translateX(${currentPosition}px)`;
});

document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.test-card');
    if (cards.length > 0) {
        const cardWidth = cards[0].offsetWidth + 20;
        console.log(cardWidth); // Проверьте значение cardWidth
    } else {
        console.log("Карточки не найдены");
    }
});

const cards = document.querySelectorAll('.test-card');
if (cards.length > 0) {
    const cardWidth = cards[0].offsetWidth + 20;
    console.log(cardWidth); // Значение ширины первой карточки
} else {
    console.log("Карточки с классом 'test-card' не найдены");
}
