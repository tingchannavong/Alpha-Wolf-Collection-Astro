const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');
const images = document.querySelectorAll('.carousel img');
let currentImageIndex = 0;

function showImage(index) {
  images.forEach((img, i) => {
    img.classList.toggle('active', i === index);
  });
}

prevButton.addEventListener('click', () => {
  currentImageIndex = (currentImageIndex > 0) ? currentImageIndex - 1 : images.length - 1;
  showImage(currentImageIndex);
});

nextButton.addEventListener('click', () => {
  currentImageIndex = (currentImageIndex < images.length - 1) ? currentImageIndex + 1 : 0;
  showImage(currentImageIndex);
});

showImage(currentImageIndex); // Show the first image initially

const dots = document.querySelectorAll('.dot');

function updateDots(index) {
  dots.forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
  });
}

function showImage(index) {
  images.forEach((img, i) => {
    img.classList.toggle('active', i === index);
  });
  updateDots(index); // Update dots based on the current image
}

prevButton.addEventListener('click', () => {
  currentImageIndex = (currentImageIndex > 0) ? currentImageIndex - 1 : images.length - 1;
  showImage(currentImageIndex);
});

nextButton.addEventListener('click', () => {
  currentImageIndex = (currentImageIndex < images.length - 1) ? currentImageIndex + 1 : 0;
  showImage(currentImageIndex);
});

showImage(currentImageIndex); // Show the first image and the corresponding dot initially

