let currentSlides = {};

function showSlides(sliderId, slideIndex) {
    const slides = document.querySelectorAll(`#${sliderId} .month-statistics`);
    if (slides.length === 0) return;
    
    if (!currentSlides[sliderId]) {
        currentSlides[sliderId] = 0;
    }
    
    slides.forEach((slide, index) => {
        slide.style.display = index === slideIndex ? 'flex' : 'none';
    });
}

function nextSlide(sliderId) {
    const slides = document.querySelectorAll(`#${sliderId} .month-statistics`);
    if (slides.length === 0) return;

    currentSlides[sliderId] = (currentSlides[sliderId] + 1) % slides.length;
    showSlides(sliderId, currentSlides[sliderId]);
}

function prevSlide(sliderId) {
    const slides = document.querySelectorAll(`#${sliderId} .month-statistics`);
    if (slides.length === 0) return;

    currentSlides[sliderId] = (currentSlides[sliderId] - 1 + slides.length) % slides.length;
    showSlides(sliderId, currentSlides[sliderId]);
}

// Initialize all sliders
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.slider').forEach(slider => {
        const sliderId = slider.id;
        currentSlides[sliderId] = 0;
        showSlides(sliderId, currentSlides[sliderId]);
    });
});


// let slideIndex = {};
// showSlide(slideIndex);

// function nextSlide(sliderID) {
//   showSlide((slideIndex += 1));
// }

// function prevSlide(sliderID) {
//   showSlide((slideIndex -= 1));
// }

// function showSlide(index, sliderId) {
//   const slides = document
//     .getElementsByClassName("slides")[0]
//     .getElementsByTagName("img");

//   const slides_month = document
//   .getElementsByClassName("slides")[0]
//   .getElementsByClassName("month-name");

//   if (index >= slides.length) {
//     slideIndex = 0;
//   }

//   if (index < 0) {
//     slideIndex = slides.length - 1;
//   }

//   for (let i = 0; i < slides.length; i++) {
//     slides[i].style.display = "none";
//     slides_month[i].style.display = "none";
//   }

//   slides[slideIndex].style.display = "flex";
//   slides_month[slideIndex].style.display = "flex";

//   // slides[slideIndex].style.objectFit = "cover";
//   // slides[slideIndex].style.objectFit = "cover";
//   // slides[slideIndex].style.width = "100%";
//   // slides[slideIndex].style.height = "100%";
// }
