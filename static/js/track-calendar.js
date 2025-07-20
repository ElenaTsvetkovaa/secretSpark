document.addEventListener('DOMContentLoaded', function () {
    const API_ENDPOINTS = {
        tracker: "api/track-period/",
        results: "api/show-results/"
    };

    const PHASE_CONFIG = {
        menstrual: { color: "bg-pink-200", label: "Menstrual" },
        follicular: { color: "bg-blue-200", label: "Follicular" },
        ovulation: { color: "bg-yellow-200", label: "Ovulation" },
        luteal: { color: "bg-purple-200", label: "Luteal" },
        default: { color: "bg-gray-100", label: "" }
    };

    const lastPeriodDate = document.querySelector("[name='last_period_date']");
    const cycleLength = document.getElementById('cycleLength');
    const periodLength = document.getElementById('periodLength');
    const phaseDiv = document.getElementById("currentPhase");
    let monthOffset = 0;

    // Helper function to populate select options
    function populateSelectOptions(selectElement, start, end) {
        for (let i = start; i <= end; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            selectElement.appendChild(option);
        }
    }

    // Generate phase legend
    function generatePhaseLegend() {
        const legendDiv = document.getElementById("phaseLegend");
        legendDiv.innerHTML = Object.entries(PHASE_CONFIG)
            .filter(([key]) => key !== 'default')
            .map(([key, config]) => `
                <div class="flex items-center gap-1">
                    <div class="w-3 h-3 ${config.color} rounded-full"></div>
                    <span class="text-sm">${config.label}</span>
                </div>
            `).join('');
    }

    populateSelectOptions(cycleLength, 21, 39);
    populateSelectOptions(periodLength, 1, 10);
    generatePhaseLegend();

    // Helper function for API calls
    function apiCall(url, options = {}) {
        return fetch(url, {
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            ...options
        }).then(response => response.json());
    }

    // Helper function to update calendar and phase
    function updateCalendarData() {
        return apiCall(`${API_ENDPOINTS.results}?offset=${monthOffset}`)
            .then(results => {
                renderCalendar(results.phases, monthOffset);
                displayCurrentPhase(results.current_phase);
            });
    }

    apiCall(API_ENDPOINTS.tracker)
        .then(data => {
            lastPeriodDate.value = data.last_period_date || '';
            cycleLength.value = data.cycle_length || '';
            periodLength.value = data.period_length || '';

            if (data) {
                updateCalendarData();
            }
        });

    // Form submission handler
    document.getElementById("cycleForm").addEventListener("submit", function (e) {
        e.preventDefault();
        const payload = {
            last_period_date: lastPeriodDate.value,
            cycle_length: cycleLength.value,
            period_length: periodLength.value
        };

        fetch(API_ENDPOINTS.tracker, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify(payload),
            credentials: "include"
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    console.error("PUT error response:", data);
                    throw new Error("Failed to update cycle data.");
                });
            }
            return updateCalendarData();
        });
    });

    // Navigation handlers
    function handleNavigation(offsetChange) {
        monthOffset += offsetChange;
        updateCalendarData();
    }

    document.getElementById("prevBtn").addEventListener("click", () => handleNavigation(-3));
    document.getElementById("nextBtn").addEventListener("click", () => handleNavigation(3));

    function renderCalendar(phases, offset=0) {
        const calendarDiv = document.getElementById("calendar");
        calendarDiv.innerHTML = "";

        const today = new Date();
        const months = [];

        const baseMonth = new Date(today.getFullYear(), today.getMonth() + offset, 1);

        // Calculating 3 calendar months
        for (let i = 0; i < 3; i++) {
            const month = new Date(baseMonth.getFullYear(), baseMonth.getMonth() + i, 1);
            months.push(month);
        }

        // Generating the months
        months.forEach(month => {
            const year = month.getFullYear();
            const monthIndex = month.getMonth();
            const firstDay = new Date(year, monthIndex, 1);
            const lastDay = new Date(year, monthIndex + 1, 0);

            const daysInMonth = lastDay.getDate();
            const monthName = month.toLocaleString('default', { month: 'long' });

            let html = `<div class="bg-white shadow p-4 rounded-xl m-4 w-[22rem]">
                <h2 class="text-center text-lg font-bold text-[#721f49]">${monthName} ${year}</h2>
                <div class="grid grid-cols-7 gap-1.5 text-center text-sm font-semibold mt-2">
                    <div>Mon</div>
                    <div>Tue</div>
                    <div>Wed</div>
                    <div>Thu</div>
                    <div>Fri</div>
                    <div>Sat</div>
                    <div>Sun</div>
                </div>
                <div class="grid grid-cols-7 grid-rows-6 gap-1 text-center mt-2">
            `;

            // The calendar days start from Mon not Sun
            const startDay = (firstDay.getDay() + 6) % 7;
            for (let i = 0; i < startDay; i++) {
                html += `<div></div>`;
            }

            for (let day = 1; day <= daysInMonth; day++) {
                const date = new Date(year, monthIndex, day);
                const dateStr = date.toISOString().split('T')[0];

                const phase = phases.find(
                    p => dateStr >= p.start && dateStr <= p.end
                );

                const bgColor = phase ? PHASE_CONFIG[phase.name].color : PHASE_CONFIG.default.color;
                html += `<div class="${bgColor} rounded p-1" title="${phase?.name || ''}">${day}</div>`;
            }

            const totalCells = startDay + daysInMonth;
            const fullGridCells = 6 * 7;
            for (let i = totalCells; i < fullGridCells; i++) {
                html += `<div></div>`;
            }

            html += `</div></div>`;
            calendarDiv.innerHTML += html;
        })
    }

    function displayCurrentPhase(phaseData) {
           phaseDiv.innerHTML = `
                 <h2 class="text-3xl font-bold text-[#721f49] text-center mb-6 flex items-center justify-center gap-2">
                    <img src="/static/images/noto--lotus.svg" class="size-20">
                    Current Phase
                </h2>
                <div class="relative border border-pink-300 p-6 rounded-xl shadow-md bg-white overflow-hidden">
                    <h3 class="text-2xl font-semibold text-[#a1366c] mb-3 text-center z-10 relative">${phaseData.name}</h3>
                    <p class="text-gray-700 text-base leading-relaxed font-['Open_Sans'] text-center z-10 relative">
                        ${phaseData.description}
                    </p>
                </div>
            `;
    }

    const observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("opacity-100");
                entry.target.classList.remove("opacity-0");
            }
        },
        { threshold: 0.1 }
    );
    
    const cycleResultsDiv = document.getElementById("cycleResults");
    observer.observe(cycleResultsDiv);

});
