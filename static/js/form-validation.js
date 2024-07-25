document.addEventListener('DOMContentLoaded', function() {
    const cityInput = document.getElementById('city-input');
    const submitButton = document.getElementById('submit-button');
    const cityName = document.getElementById('city-name');
    const weatherDate = document.getElementById('weather-date');
    const weatherTime = document.getElementById('weather-time');
    const temperature = document.getElementById('temperature');
    const conditionText = document.getElementById('condition-text');
    const weatherIcon = document.getElementById('weather-icon');
    const resultDiv = document.getElementById('main');

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const cityForm = document.getElementById('city-form');

    function validateInput() {
        submitButton.disabled = cityInput.value.trim() === '';
    }

    async function fetchWeatherData(city) {
        try {
            const response = await fetch(cityForm.action, {
                method: 'POST',
                body: new URLSearchParams({ city: city }),
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });

            const data = await response.json();

            if (data.error) {
                resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                cityName.textContent = `City: ${data.city}`;
                temperature.textContent = `Temperature: ${data.temperature}°C`;
                conditionText.textContent = `Condition: ${data.condition_text}`;
                weatherIcon.src = `http:${data.condition_icon}`;
                weatherIcon.alt = data.condition_text;

                weatherDate.textContent = `Date: ${data.date}`;
                weatherTime.textContent = `Time: ${data.time}`;

            }
        } catch (error) {
            console.error('Error:', error);
            resultDiv.innerHTML = `<p>An error occurred. Please try again later.</p>`;
        }
    }

    // Изначально устанавливаем состояние кнопки
    validateInput();

    // Устанавливаем обработчик событий для изменения поля ввода
    cityInput.addEventListener('input', validateInput);

    // Устанавливаем обработчик событий для отправки формы
    cityForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Предотвращаем стандартное действие формы

        var city = cityInput.value.trim();
        if (city) {
            if (window.location.pathname !== indexUrl) {
                localStorage.setItem('city', city);
                window.location.href = indexUrl;
            } else {
                fetchWeatherData(city);
            }
        }
    });

    const storedCity = localStorage.getItem('city');
    if (storedCity) {
        cityInput.value = storedCity;
        fetchWeatherData(storedCity);
        localStorage.removeItem('city');
    }
});
