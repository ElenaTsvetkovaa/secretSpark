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
    const cycleResultsDiv = document.getElementById("cycleResults");
    const cycleForm = document.getElementById("cycleForm");
    const deleteDataBtn = document.getElementById("deleteDataBtn");
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
    function updateCalendarData(animate = false) {
        return apiCall(`${API_ENDPOINTS.results}?offset=${monthOffset}`)
            .then(results => {
                renderCalendar(results.phases, monthOffset, animate);
                displayCurrentPhase(results.current_phase);
            });
    }

    apiCall(API_ENDPOINTS.tracker)
        .then(data => {
            lastPeriodDate.value = data.last_period_date || new Date();
            cycleLength.value = data.cycle_length || '28';
            periodLength.value = data.period_length || '5';

            if (data && data.last_period_date) {
                // Add fade-in animation for results
                cycleResultsDiv.style.opacity = "0";
                cycleResultsDiv.classList.remove("hidden");
                deleteDataBtn.classList.remove("hidden");
                document.getElementById("resultsBtn").classList.remove("col-span-3");
                document.getElementById("resultsBtn").classList.add("col-span-2");
                
                setTimeout(() => {
                    cycleResultsDiv.style.transition = "opacity 0.5s ease-in-out";
                    cycleResultsDiv.style.opacity = "1";
                }, 50);
                
                return updateCalendarData();
            }
        })
        .then(() => {
            observer.observe(cycleResultsDiv);
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
            // Add fade-in animation for results
            cycleResultsDiv.style.opacity = "0";
            cycleResultsDiv.classList.remove("hidden");
            deleteDataBtn.classList.remove("hidden");
            document.getElementById("resultsBtn").classList.remove("col-span-3");
            document.getElementById("resultsBtn").classList.add("col-span-2");
            
            setTimeout(() => {
                cycleResultsDiv.style.transition = "opacity 0.5s ease-in-out";
                cycleResultsDiv.style.opacity = "1";
            }, 50);
            
            return updateCalendarData();
        })
        .then(() => {
            observer.observe(cycleResultsDiv);
        });
    });

    // Navigation handlers
    function handleNavigation(offsetChange) {
        monthOffset += offsetChange;
        updateCalendarData();
    }

    document.getElementById("prevBtn").addEventListener("click", () => handleNavigation(-3));
    document.getElementById("nextBtn").addEventListener("click", () => handleNavigation(3));

    // Custom confirmation dialog
    function showCustomConfirm(message, onConfirm) {
        const overlay = document.createElement('div');
        overlay.className = 'fixed inset-0 bg-black bg-opacity-0 flex items-center justify-center z-50 transition-all duration-300';

        const dialog = document.createElement('div');
        dialog.className = 'bg-white p-6 rounded-xl shadow-lg max-w-md mx-4 transform scale-75 opacity-0 transition-all duration-300';

        dialog.innerHTML = `
            <div class="text-center">
                <div class="mb-4">
                    <svg class="mx-auto h-12 w-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.962-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                    </svg>
                </div>
                <h3 class="text-lg font-semibold text-gray-900 mb-2">Delete Period Data</h3>
                <p class="text-gray-600 mb-6">${message}</p>
                <div class="flex gap-3 justify-center">
                    <button id="cancelBtn" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 font-medium">
                        Cancel
                    </button>
                    <button id="confirmBtn" class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium">
                        Delete Data
                    </button>
                </div>
            </div>
        `;

        overlay.appendChild(dialog);
        document.body.appendChild(overlay);

        // Trigger animations
        setTimeout(() => {
            overlay.classList.remove('bg-opacity-0');
            overlay.classList.add('bg-opacity-50');
            dialog.classList.remove('scale-75', 'opacity-0');
            dialog.classList.add('scale-100', 'opacity-100');
        }, 10);

        function closeDialog() {
            overlay.classList.add('bg-opacity-0');
            overlay.classList.remove('bg-opacity-50');
            dialog.classList.add('scale-75', 'opacity-0');
            dialog.classList.remove('scale-100', 'opacity-100');

            setTimeout(() => {
                document.body.removeChild(overlay);
            }, 300);
        }

        dialog.querySelector('#cancelBtn').onclick = closeDialog;

        dialog.querySelector('#confirmBtn').onclick = () => {
            closeDialog();
            setTimeout(onConfirm, 300);
        };

        overlay.onclick = (e) => {
            if (e.target === overlay) {
                closeDialog();
            }
        };
    }

    // Delete data handler
    document.getElementById("deleteDataBtn").addEventListener("click", function() {
        showCustomConfirm("Are you sure you want to delete all your period tracking data? This action cannot be undone.", () => {
            fetch(API_ENDPOINTS.tracker, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                },
                credentials: "include"
            })
            .then(response => {
                if (response.ok) {
                    // Reset form
                    lastPeriodDate.value = "";
                    cycleLength.value = "28";
                    periodLength.value = "5";

                    // Hide results and delete button
                    cycleResultsDiv.classList.add("hidden");
                    deleteDataBtn.classList.add("hidden");
                    document.getElementById("resultsBtn").classList.remove("col-span-2");
                    document.getElementById("resultsBtn").classList.add("col-span-3");
                } else {
                    throw new Error("Failed to delete data");
                }
            })
            .catch(error => {
                console.error("Delete error:", error);
                alert("Failed to delete data. Please try again.");
            });
        });
    });

    function renderCalendar(phases, offset=0, animate=false) {
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
        months.forEach((month, index) => {
            const year = month.getFullYear();
            const monthIndex = month.getMonth();
            const firstDay = new Date(year, monthIndex, 1);
            const lastDay = new Date(year, monthIndex + 1, 0);

            const daysInMonth = lastDay.getDate();
            const monthName = month.toLocaleString('default', { month: 'long' });

            const animationClasses = '';
            const animationStyle = '';
            
            let html = `<div class="bg-white shadow p-4 rounded-xl m-4 w-[22rem] ${animationClasses}" style="${animationStyle}">
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
        });

    }

    function displayCurrentPhase(phaseData) {
        phaseDiv.style.opacity = "0";
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
        
        // Add subtle fade-in animation
        setTimeout(() => {
            phaseDiv.style.transition = "opacity 0.4s ease-in-out";
            phaseDiv.style.opacity = "1";
        }, 100);
    }

    const observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting && !entry.target.classList.contains("hidden")) {
                // Observer is working but results are already visible
                // This observer was meant to detect when results come into view
                // but we're already handling visibility with the hidden class
            }
        },
        { threshold: 0.1 }
    );

});
