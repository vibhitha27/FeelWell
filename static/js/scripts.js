function playAudio(text) {
    let audio = new Audio(`/speak/${encodeURIComponent(text)}`);
    audio.play();
}
