const MapElement = document.querySelector("#Map");
const Map = new google.maps.Map(MapElement, {
  "zoom": 12.,
  "center": new google.maps.LatLng(MapElement.dataset.lat, MapElement.dataset.lng),
  "mapTypeId": google.maps.MapTypeId.ROADMAP
});

let SelectedMarker = null;

google.maps.event.addListener(Map, "click", function(Event){
  //Set values of hidden latitude and longitude inputs to make form submission easier
  document.querySelector("#HiddenLatitudeInput").value = Event.latLng.lat();
  document.querySelector("#HiddenLongitudeInput").value = Event.latLng.lng();

  //Hide map selection hint
  document.querySelector("#MapTitleExplanation").style.opacity = "0";

  //Create a marker if it doesn't exist and move it to the clicked location
  SelectedMarker ??= new google.maps.Marker({
    "map": Map,
    "title": "Place location"
  });
  SelectedMarker.setPosition(Event.latLng);
});

document.querySelector("#ImageDropWrapper").addEventListener("dragover", function(Event){
  Event.preventDefault(); //Prevent browser from opening the file as usual. Both dragover and drop events need to be preventDefault-ed.
});
document.querySelector("#ImageDropWrapper").addEventListener("drop", function(Event){
  Event.preventDefault(); //Prevent browser from opening the file as usual. Both dragover and drop events need to be preventDefault-ed.
  debugger;
});
