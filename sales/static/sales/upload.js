const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

Dropzone.autoDiscover = false;
const myDropzone = new Dropzone("#my-dropzone", {
    url: '/sales/upload/',
    init: function() {
        this.on('sending', function(file, xhr, formData) {
            console.log('Sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    accepedFiles: 'csv'
});