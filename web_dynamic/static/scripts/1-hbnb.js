$(document).ready(function () {
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
