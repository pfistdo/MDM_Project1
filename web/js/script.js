function classify_image(event, text) {
  // Preview
  if (file) {
    preview.src = URL.createObjectURL(files[0]);
  }
  // Upload
  const formData = new FormData();
  for (const name in files) {
    formData.append(name, files[name]);
  }
  fetch("/model/image", {
    method: "POST",
    headers: {},
    body: formData,
  })
    .then((response) => {
      console.log(response);
      response.text().then(function (text) {
        answer.innerHTML = text;
      });
    })
    .then((success) => console.log(success))
    .catch((error) => console.log(error));
}

// Upload image to server using AJAX Post
function upload_image() {
  var form_data = new FormData();
  var ins = document.getElementById("upload_image").files[0];
  form_data.append("file", ins);

  if (ins != undefined) {
    $.ajax({
      url: "upload", // point to server-side URL
      dataType: "text", // what to expect back from server
      cache: false,
      contentType: false,
      processData: false,
      data: form_data,
      type: "post",
      success: function (response) {
        alert(response, "success");
      },
      error: function (response) {
        alert(response, "danger");
      },
    });
  } else {
    alert("Please select an image to upload!", "danger");
  }
}

function preview_image() {
  const preview = document.querySelector("#imagePreview");
  const file = document.querySelector("input[type=file]").files[0];
  const reader = new FileReader();

  reader.addEventListener(
    "load",
    function () {
      preview.innerHTML = '<img src="' + reader.result + '" class="img-fluid">';
    },
    false
  );

  if (file) {
    reader.readAsDataURL(file);
  }
}

// Bootstrap alert
const alert = (message, type) => {
const alertPlaceholder = document.getElementById('alerts')
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}