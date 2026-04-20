document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('[data-like-form]');

    if (!form) {
        return;
    }

    const button = form.querySelector('[data-like-button]');
    const count = document.querySelector('[data-like-count]');
    const status = form.querySelector('[data-like-status]');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        button.disabled = true;
        status.textContent = 'Сохраняем...';

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });

            if (!response.ok) {
                throw new Error('Request failed');
            }

            const data = await response.json();
            button.textContent = data.button_text;
            count.textContent = data.likes_count;
            status.textContent = data.liked ? 'Лайк поставлен' : 'Лайк убран';
        } catch (error) {
            status.textContent = 'Не удалось сохранить лайк';
        } finally {
            button.disabled = false;
        }
    });
});
