let lastClickedButton = document.querySelector('.buy.active'); // Ищем кнопку с классом 'active' при загрузке

function changeButtonState(button) {
  // Если была нажата другая кнопка, сбрасываем состояние предыдущей
  if (lastClickedButton && lastClickedButton !== button) {
    lastClickedButton.classList.remove('active');
  }

  // Добавляем класс 'active' для текущей кнопки
  button.classList.add('active');

  // Запоминаем текущую нажатую кнопку
  lastClickedButton = button;
}