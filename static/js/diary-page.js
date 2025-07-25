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

                fetch(`/diary/by-date/?date=${selectedDate}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.exists) {
                            // If record exists, populate the form with REST API data
                            const diaryData = data.data;
                            document.querySelector('[name="content"]').value = diaryData.content;
                            formMood.value = diaryData.mood;

                            // Use mood_data from the enhanced serializer
                            const moodIndex = moods.findIndex(m => m.id === diaryData.mood_data.id);
                            if (moodIndex !== -1) {
                                setMood(moodIndex);
                                moodSlider.value = moodIndex * 20;
                            }
                            continueBtn.click();
                            
                            // Store diary ID for updates
                            diaryForm.dataset.diaryId = diaryData.id;
                            diaryForm.dataset.isUpdate = 'true';
                        } else {
                            // No existing entry - prepare for creation
                            reminderContainer.classList.add('hidden');
                            document.querySelector('[name="content"]').value = '';
                            formMood.value = '';
                            
                            // Clear update flags
                            delete diaryForm.dataset.diaryId;
                            delete diaryForm.dataset.isUpdate;

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

        const content = document.querySelector('[name="content"]').value;
        const selectedDate = formDate.value;
        const moodId = formMood.value;

        // Prepare JSON data for REST API - use default mood if none selected  
        const requestData = {
            date: selectedDate ? selectedDate : new Date(),
            content: content,
            mood: moodId ? parseInt(moodId) : selectedMood.id  // Default to mood ID 4 (Calm)
        };

        // Determine if this is create or update
        const isUpdate = diaryForm.dataset.isUpdate === 'true';
        const diaryId = diaryForm.dataset.diaryId;

        let url, method;
        if (isUpdate && diaryId) {
            url = `/diary/${diaryId}/`;
            method = 'PUT';
        } else {
            url = `/diary/`;
            method = 'POST';
        }

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(requestData)
        })
            .then(response => response.json())
            .then(data => {
                showSuccessMessage();
                // Store the ID for future updates
                diaryForm.dataset.diaryId = data.id;
                diaryForm.dataset.isUpdate = 'true';
            })
            .catch(err => {
                console.error("Error saving diary entry:", err);
                alert("Error saving entry");
            })

    })

    function showSuccessMessage() {
        const msg = document.getElementById('successMessage');
        if (msg) {
            msg.style.opacity = '1';
            msg.style.transition = 'opacity 0.5s ease';
            
            setTimeout(() => {
                msg.style.opacity = '0';
            }, 2000);
        }
    }


});
