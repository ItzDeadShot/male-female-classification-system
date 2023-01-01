// Configure a few settings and attach camera 250x187
Webcam.set({
  width: 350,
  height: 267,
  image_format: "jpeg",
  jpeg_quality: 90,
});
Webcam.attach("#my_camera");

function take_snapshot() {
  // play sound effect
  //shutter.play();
  // take snapshot and get image data
  Webcam.snap(function (data_uri) {
    // display results in page
    document.getElementById("results").innerHTML =
      '<img class="after_capture_frame" src="' + data_uri + '"/>';
    $("#captured_image_data").val(data_uri);
  });
}

function saveSnap() {
  var base64data = $("#captured_image_data").val();
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/predict",
    data: { image: base64data },
    success: function (response) {
      $("#capture_result").css("display", "block");
        var prediction = response.prediction;
      var image = response.image;
      $("#capture_prediction").html(prediction);
    },
  });
}
