$(document).ready(function () {
  checkApiStatus();
  fetchPlaces();

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

function fetchPlaces () {
  $.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    contentType: 'application/json',
    data: JSON.stringify({}),
    success: function (data) {
      $.each(data, function (index, place) {
        const article = $('<article>');
        // TITLE BOX
        const titleDiv = $('<div>').addClass('title_box');
        // Name
        titleDiv.append(`<h2>${place.name}</h2>`);
        // Price
        const priceDiv = $('<div>').addClass('price_by_night');
        priceDiv.text(`$${place.price_by_night}`);
        titleDiv.append(priceDiv);

        // INFORMATION
        const infoDiv = $('<div>').addClass('information');
        // Number of guests
        const guestDiv = $('<div>').addClass('max_guest');
        const _gs = place.max_guest > 1 ? 's' : '';
        guestDiv.text(`${place.max_guest} Guest${_gs}`);
        // Number of rooms
        const roomsDiv = $('<div>').addClass('number_rooms');
        const _rs = place.number_rooms > 1 ? 's' : '';
        roomsDiv.text(`${place.number_rooms} Room${_rs}`);
        // Number of bathrooms
        const bathroomsDiv = $('<div>').addClass('number_bathrooms');
        const _bs = place.number_bathrooms > 1 ? 's' : '';
        bathroomsDiv.text(`${place.number_bathrooms} bathroom${_bs}`);

        // Append all to Information
        $.each([guestDiv, roomsDiv, bathroomsDiv], function (index, div) {
          infoDiv.append(div);
        });

        // USER
        const userDiv = $('<div>').addClass('user');
        // TODO
        // const firstName = place.user_id;
        // const lastName = place.user_id;
        userDiv.append('<b>Owner:</b> firstName lastName');

        // DESCRIPTION
        const descDiv = $('<div>').addClass('description');
        descDiv.append(place.description);

        // Attach all place DIVs to article
        $.each([titleDiv, infoDiv, userDiv, descDiv], function (index, div) {
          article.append(div);
        });

        $('.places').append(article);
      });
    }
  });
}
