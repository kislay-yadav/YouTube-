async function download() {
  const url = document.getElementById('url').value;
  const message = document.getElementById('message');
  const loader = document.getElementById('loader');

  if (!url) {
    message.textContent = "Please enter a YouTube URL.";
    return;
  }

  loader.style.display = 'block';
  message.textContent = "";

  try {
    const response = await fetch('/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    const data = await response.json();
    loader.style.display = 'none';

    if (response.ok) {
      message.innerHTML = `✅ Downloading <b>${data.title}</b>...`;
      window.location.href = `/get/${data.filename}`;
    } else {
      message.textContent = `❌ Error: ${data.error}`;
    }
  } catch (err) {
    loader.style.display = 'none';
    message.textContent = `❌ Error: ${err.message}`;
  }
}
