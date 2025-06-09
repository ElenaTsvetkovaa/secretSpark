
document.addEventListener('DOMContentLoaded', function() {
    const moodTracker = document.getElementById('mood-tracker');
    const moodDisplay = document.getElementById('mood-display');
    const apiUrl = moodDisplay.dataset.apiUrl;
    const moodImage = document.getElementById('mood-image');
    const moodLabel = document.getElementById('mood-label');
    const moodSlider = document.getElementById('mood-slider');
    const continueBtn = document.getElementById('continue-btn');
    const reminderContainer = document.getElementById('reminder-container');
    const reminderMessage = document.getElementById('reminder-message');
    const reminderLabel = document.getElementById('reminder-label');

    let selectedMood = null;
    let moods = [];

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            moods = data;
            let currentMoodIndex = 0;

            loadMoodDisplay();

            moodSlider.addEventListener('input', (event) => {
                event.preventDefault();

                const rawValue = parseInt(moodSlider.value);
                const moodIndex = getMoodIndexFromSlider(rawValue);

                if (moodIndex !== currentMoodIndex) {
                    currentMoodIndex = moodIndex;
                    setMood(moodIndex);
                }
            });

            continueBtn.addEventListener('click', (event) => {
                event.preventDefault();
                if (!selectedMood) return;

                reminderMessage.textContent = selectedMood.reminder;

                if (!reminderContainer.classList.contains('hidden')) {
                    // Fade out first
                    reminderMessage.classList.add('opacity-0');

                    setTimeout(() => {

                        reminderMessage.classList.remove('opacity-0');

                        setTimeout(() => {
                            reminderMessage.classList.remove('opacity-0');
                        }, 10);
                    }, 300);
                } else {
                    // Show reminder
                    reminderContainer.classList.remove('hidden');

                    setTimeout(() => {
                        reminderContainer.classList.remove('opacity-0');
                        reminderLabel.classList.remove('opacity-0');
                        reminderMessage.classList.remove('opacity-0');
                    }, 10);
                }
            });
        });

        function setMood(index) {
            selectedMood = moods[index];

            // Fade out
            moodImage.classList.remove('opacity-100');
            moodImage.classList.add('opacity-0');
            moodLabel.classList.remove('opacity-100');
            moodLabel.classList.add('opacity-0');

            setTimeout(() => {
                moodImage.src = selectedMood.image;
                moodLabel.textContent = selectedMood.mood;

                // Fade in *after* image is fully loaded
                moodImage.classList.remove('opacity-0');
                moodImage.classList.add('opacity-100');
                moodLabel.classList.remove('opacity-0');
                moodLabel.classList.add('opacity-100');
            }, 250);
        }
        function getMoodIndexFromSlider(value) {
            const percent = value / 100;
            const moodIndex = Math.floor(percent * moods.length); // or tweak to bias happy earlier
            return Math.min(moodIndex, moods.length - 1);
        }
        function loadMoodDisplay() {

            const defaultIndex = moods.findIndex(m => m.is_default);
            selectedMood = moods[defaultIndex];

            moodImage.src = selectedMood.image;
            moodLabel.textContent = selectedMood.mood;
            moodSlider.value = defaultIndex * 20;

            setTimeout(() => {
                moodImage.classList.remove("opacity-0");
                moodLabel.classList.remove("opacity-0");
                moodSlider.classList.remove("opacity-0");
            }, 250);
        }
});











