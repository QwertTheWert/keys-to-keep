document.addEventListener("DOMContentLoaded", () => {
  const stars = document.querySelectorAll(".interactive-star");
  const hiddenInput = document.getElementById("selected-rating");
  const submitButton = document.getElementById("submit-button");
  let selectedRating = 0;

  stars.forEach((star, index) => {
    star.addEventListener("mouseover", () => {
      highlightStars(index + 1);
    });

    star.addEventListener("mouseout", () => {
      highlightStars(selectedRating);
    });

    star.addEventListener("click", () => {
      selectedRating = index + 1;
      hiddenInput.value = selectedRating;
      submitButton.disabled = hiddenInput.value == 0;

      highlightStars(selectedRating);
    });
  });

  function highlightStars(rating) {
    stars.forEach((star, i) => {
      star.classList.toggle("hover", i < rating);
      star.classList.toggle("selected", i < selectedRating);
    });
  }
});``

