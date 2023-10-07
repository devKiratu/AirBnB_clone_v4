$(document).ready(function () {
  checkApiStatus();

  $('input:checkbox:checked').prop('checked', false);
  const data = {};
  $('input:checkbox').on('click', function () {
    if ($(this).prop('checked') === true) {
      data[$(this).attr('data-id')] = $(this).attr('data-name');
    } else if ($(this).attr('data-id') in data) {
      delete data[$(this).attr('data-id')];
    }
    if (Object.values(data).length > 0) {
      $('div.amenities h4').text(Object.values(data).join(', '));
    } else {
      $('div.amenities h4').html('&nbsp;');
    }
  });
});

function checkApiStatus () {
  $.get('http://0.0.0.0:5001/api/v1/status/', function (res) {
    if (res.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  });
}
