
document.addEventListener('DOMContentLoaded', function() {
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
        // Setting the mood
        function setMood(index) {
            selectedMood = moods[index];
            // document.getElementById("selectedMoodInput").value = selectedMood.id;

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
        // Calculate the idx of mood because i use larger range
        function getMoodIndexFromSlider(value) {
            const percent = value / 100; // v = 30; percent = 0.3
            const moodIndex = Math.floor(percent * moods.length); // idx = 1 -> which is mood at idx 2
            return Math.min(moodIndex, moods.length - 1);
        }
        // Loading the Mood tracker elements
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


        const dateInput = document.getElementById("dateInput");
        const diaryForm = document.getElementById("diaryForm");
        const formDate =   document.getElementById("selectedDateInput");
        const formMood =  document.getElementById("selectedMoodInput");
        // Instantiating date Flatpickr calendar
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

        dateInput.addEventListener('change', function (event){
            formDate.value = this.value;

            fetch(`/diary/entry/?date=${formDate}`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        window.location.href = `/diary/${data.diary_id}`
                    } else {
                        window.location.href = `/diary`
                    }
                });
        });
});
        // Make a post request
        // let postTimeOut;
        // diaryForm.addEventListener('change', () => {
        //     clearTimeout(postTimeOut);
        //     postTimeOut = setTimeout(sendPostRequest, 500);
        // });
        //
        // function sendPostRequest() {
        //     formMood.value = selectedMood.id;
        //
        //     const form = new FormData(diaryForm);
        //     fetch('/diary/', {
        //         method: 'POST',
        //         body: form,
        //     })
        //         .then(res => res.json())
        //         .catch(error => console.log('Error:', error));
        // }


        // function sendGetRequest() {
        //
        //     fetch('/diary/', {
        //         method: "GET",
        //         date:  fp.input.value,
        //     })
        //         .then(res => res.json())
        //         .catch(error => console.error('Error:', error));
        // }
        //
        // const diaryForm = document.getElementById('diaryForm');
        // let postTimeOut;
        //
        // diaryForm.addEventListener('input', () => {
        //     clearTimeout(postTimeOut);
        //     postTimeOut = setTimeout(sendPostRequest, 500);
        // });
        //


        //
        // datePicker.addEventListener("click", () => {
        //     fp.open();
        //     document.getElementById("selectedDateInput").value = fp.input.value;
        //     sendGetRequest();
        // });



        // don't have submit button
        // sendPostRequest();

        //   saveButton.click = () => {
        //         const selectedDate = fp.input.value;
        //         document.getElementById("selectedDateInput").value = fp.input.value;
        //         document.getElementById("selectedMoodInput").value = selectedMood.id;
        // }













