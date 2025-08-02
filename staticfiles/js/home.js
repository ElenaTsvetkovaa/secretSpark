
document.addEventListener("DOMContentLoaded", () => {
    const testimonial = document.getElementById("testimonial-section");

    function onScroll() {
        if (testimonial.classList.contains('opacity-0')) {
            testimonial.classList.remove('opacity-0');
            testimonial.classList.add('opacity-100');
            window.removeEventListener('scroll', onScroll);
        }
    }
      window.addEventListener('scroll', onScroll);
});



