
/** from https://www.freecodecamp.org/news/upload-files-with-javascript/ */
/** @param {Event} event */
function uploadFile(event) {

  console.log("uploadFile");
  const form = document.getElementById('uploadForm');
  const formData = new FormData(form);
  const searchParams = new URLSearchParams(formData);

  /** @type {Parameters<fetch>[1]} */
  const fetchOptions = {
    method: form.method,
    headers: {'Access-Control-Allow-Origin':'*'}
  };

  if (form.method.toLowerCase() === 'post') {
    if (form.enctype === 'multipart/form-data') {
      fetchOptions.body = formData;
    } else {
      fetchOptions.body = searchParams;
    }
  } else {
    url.search = searchParams;
  }

  fetch('http://localhost:5000/upload', fetchOptions)
    .then(response => {
      if (response.ok) return response.json()
      else throw new Error('Upload failed');
    })
    .then(json => {
      responseElement = document.getElementById('loader-download');
      switchToLoader(responseElement);
      responseElement.removeEventListener('click', responseElement.fn, false);

      let interval = setInterval( async() => {
        await fetch('http://localhost:5000/status?model_id='+json.model_id, {cache: "no-cache"})
        .then(async(response) => {
        if (response.ok) {

          response_json = await response.json();
          console.log(response_json);

          if (response_json.status==0) {

            console.log('successful conversion');

            switchToDownload(responseElement);

            responseElement.addEventListener('click', responseElement.fn = function() {
              location.href = 'http://localhost:5000/get_model?model_id='+response_json.model_id;
            }, false);

          } else {
            console.log('failed conversion');

            // responseElement.removeEventListener('click', responseElement.fn, false);
            
            switchToFailed(responseElement);
          }
          clearInterval(interval);
        }
      })}, 1000);
    })
    .catch(error => console.error('Error:', error));
}

function switchToLoader(element) {
  element.innerText = '';
  element.classList.remove('failed');
  element.classList.remove('button');
  element.classList.add('loader');
}

function switchToDownload(element) {
  element.classList.remove('loader');
  element.classList.remove('failed');
  element.classList.add('button');
  element.innerText = 'Download';
}

function switchToFailed(element) {
  element.classList.remove('loader');
  element.classList.remove('button');
  element.classList.add('failed');
  element.innerHTML = '<b>Failed conversion!</b><br>upload a zip file including<br>the .pb files and the folder \"variables\".';
}