const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
const alertBox = document.getElementById('alert-box');

const handleAlerts = (type, message) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${message}
    </div>
    `;
}

Dropzone.autoDiscover = false;
const myDropzone = new Dropzone("#my-dropzone", {
    url: '/sales/upload/',
    init: function() {
        this.on('sending', function(file, xhr, formData) {
            console.log('Sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function(file, response) {
            const ex = response.ex;
            if (ex) {                
                handleAlerts('success', 'CSV uploaded');
            } else {
                handleAlerts('warning', 'CSV already uploaded');
            }
        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    accepedFiles: 'csv'
});