document.getElementById('userInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        const chat = document.getElementById('chat');
        const input = this.value;
        chat.innerHTML += `<p><b>You:</b> ${input}</p>`;
        chat.innerHTML += `<p><b>LianBot:</b> Processing: ${input}</p>`;
        this.value = '';
    }
});