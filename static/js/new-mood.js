document.addEventListener('DOMContentLoaded', function () {
    const moodDisplay = document.getElementById('mood-display');
    const apiUrl = moodDisplay.dataset.apiUrl;
    const moodImage = document.getElementById('mood-image');
    const moodLabel = document.getElementById('mood-label');
    const moodSlider = document.getElementById('mood-slider');
    const continueBtn = document.getElementById('continue-btn');
    const reminderContainer = document.getElementById('reminder-container');
    const reminderMessage = document.getElementById('reminder-message');
    const reminderLabel = document.getElementById('reminder-label');
    const saveButton = document.getElementById('saveButton');

    // form fields to populate
    const dateInput = document.getElementById("dateInput");
    const diaryForm = document.getElementById("diaryForm");
    const formDate = document.getElementById("selectedDateInput");
    const formMood = document.getElementById("selectedMoodInput");

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

                formMood.value = selectedMood.id;
                reminderMessage.textContent = selectedMood.reminder;

                 if (reminderContainer.classList.contains('hidden')) {
                    reminderContainer.classList.remove('hidden');
                    setTimeout(() => {
                        reminderContainer.classList.remove('opacity-0');
                        reminderLabel.classList.remove('opacity-0');
                        reminderMessage.classList.remove('opacity-0');
                    }, 10);
                } else {
                    // If it's already visible, briefly fade out + back in for updated message
                    reminderMessage.classList.add('opacity-0');
                    setTimeout(() => {
                        reminderMessage.classList.remove('opacity-0');
                    }, 250);
                }
            });

            //  When the date changes
            dateInput.addEventListener('change', function () {
                const selectedDate = this.value;
                formDate.value = selectedDate;

                fetch(`/diary/entry/?date=${selectedDate}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.exists) {
                            // If record exist we add populate the form
                            document.querySelector('[name="content"]').value = data.content;
                            formMood.value = data.mood_id;

                            const moodIndex = moods.findIndex(m => m.id === data.mood_id);
                            if (moodIndex !== -1) {
                                setMood(moodIndex);
                                moodSlider.value = moodIndex * 20;
                            }
                            continueBtn.click();
                            diaryForm.action = `/diary/${data.diary_id}/`;
                        } else {
                            // fetch empty form
                            reminderContainer.classList.add('hidden');
                            document.querySelector('[name="content"]').value = '';
                            formMood.value = '';
                            diaryForm.action = `/diary/`;

                            const defaultIndex = moods.findIndex(m => m.is_default);
                            setMood(defaultIndex);
                            moodSlider.value = defaultIndex * 20;
                        }
                    })
                    .catch(err => {
                        console.error("Error fetching diary entry:", err);
                    });
            });
        });

    // Loading initial mood
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

    // Setting the mood
    function setMood(index) {
        if (selectedMood && selectedMood.id === moods[index].id) return;

        selectedMood = moods[index];

        // Fade out current content
        moodImage.classList.add('opacity-0', 'scale-95');
        moodLabel.classList.add('opacity-0');

        setTimeout(() => {
            moodImage.src = selectedMood.image;
            moodLabel.textContent = selectedMood.mood;

            // Fade in updated content
            moodImage.onload = () => {
                moodImage.classList.remove('opacity-0', 'scale-95');
            };
            moodLabel.classList.remove('opacity-0');
        }, 200);
    }
    // Calculate idx from slider
    function getMoodIndexFromSlider(value) {
        const percent = value / 100;
        const moodIndex = Math.floor(percent * moods.length);
        return Math.min(moodIndex, moods.length - 1);
    }

    // Flatpickr
    const fp = flatpickr(dateInput, {
        appendTo: document.getElementById("calendarDisplay"),
        inline: true,
        defaultDate: new Date(),
        altInput: true,
        altFormat: "J M Y",
        dateFormat: "Y-m-d",
        onReady: () => {
            dateInput.classList.add("opacity-100")
        },
    });

    // saving the form
    saveButton.addEventListener("click", function (event) {
        event.preventDefault();

        const formData = new FormData(diaryForm);
        const url = diaryForm.action;

        fetch(url, {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                 alert("Saved ✅");
                 diaryForm.action = `/diary/${data.diary_id}/`;
            })

    })


});
