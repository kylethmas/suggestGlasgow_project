const MapElement = $("#Map")[0];
const Map = new google.maps.Map(MapElement, {
  "zoom": 12.,
  "center": new google.maps.LatLng(MapElement.dataset.lat, MapElement.dataset.lng),
  "mapTypeId": google.maps.MapTypeId.ROADMAP
});

new google.maps.Marker({
  "map": Map,
  "title": "Place location"
}).setPosition(new google.maps.LatLng(MapElement.dataset.lat, MapElement.dataset.lng));

const ThisPlaceSlug = $("#ThisPlaceSlug")[0].innerText;
async function GetCommentsFrom(Index){ //This would contain a database call
  return await (await fetch(`${window.origin}/suggestGlasgow/GetComments?slug=${ThisPlaceSlug}&start=${Index}`)).json();
}

async function* GetNextCommentGenerator(){
  let LoadedCommentsCount = 0;
  let LoadedComments;
  do{
    LoadedComments = await GetCommentsFrom(LoadedCommentsCount);
    yield* LoadedComments;
    LoadedCommentsCount += LoadedComments.length;
  } while(LoadedComments.length !== 0);
}


const TComment = $("#TComment")[0];
const CommentsPreviewContainer = $("#OverflowWrapper")[0];

//Loads top comments preview
void async function(){
  const GetNextComment = GetNextCommentGenerator();
  for(let i = 0; i < 5; ++i){
    const TCommentClone = TComment.content.firstElementChild.cloneNode(true);
    const CommentData = (await GetNextComment.next()).value;
    TCommentClone.querySelector(".Title").innerText = CommentData.Title;
    TCommentClone.querySelector(".UserDate").innerText = `by ${CommentData.Username} on ${CommentData.Date}`;
    TCommentClone.querySelector(".Text").innerText = CommentData.Comment;
    CommentsPreviewContainer.appendChild(TCommentClone);
  }
}();

let LoadingComments = false;
const LoadMoreComments = function(){
  const GetNextComment = GetNextCommentGenerator();
  const CommentsWrapper = $("#CommentsWrapper")[0];
  const LoadCommentsButton = $("#LoadMoreCommentsButton")[0];
  return async function(){
    if(LoadingComments) return;
    LoadingComments = true;
    LoadCommentsButton.classList.add("Disabled");
    for(let i = 0; i < 300; ++i){
      const CommentData = (await GetNextComment.next()).value;
      if(!CommentData) break;
      const TCommentClone = TComment.content.firstElementChild.cloneNode(true);
      if(CommentData === undefined){
        LoadCommentsButton.style.display = "none";
        LoadingComments = false;
        return;
      }
      TCommentClone.querySelector(".Title").innerText = CommentData.Title;
      TCommentClone.querySelector(".UserDate").innerText = `by ${CommentData.Username} on ${CommentData.Date}`;
      TCommentClone.querySelector(".Text").innerText = CommentData.Comment;
      CommentsWrapper.appendChild(TCommentClone);
    }
    LoadingComments = false;
    LoadCommentsButton.classList.remove("Disabled");
  };
}();

function OpenCommentsView(){
  $("#CommentsOverlayBackground")[0].style.display = "block";
  if($("#CommentsWrapper")[0].childNodes.length === 0) LoadMoreComments();
}
function CloseCommentsView(){
  $("#CommentsOverlayBackground")[0].style.display = "none";
}

$("#CommentsOverlayBackground").click(function(Event){
  if(Event.target === this) CloseCommentsView(); //Only trigger if the background is clicked
});
$(document).keydown(function(Event){
  if(Event.code === "Escape") CloseCommentsView();
});

$("#CommentButton, #OverflowWrapper").each(function(){
  $(this).mousedown(function(Event){//This has to be mousedown because click sometimes misfires on the map
    if(!MapElement.contains(Event.target)) OpenCommentsView();
  });
});

$("#LoadMoreCommentsButton").click(LoadMoreComments);

$("#Ratings > form").each($(this).click(function(Event){
  this.querySelector("button").click();
}));