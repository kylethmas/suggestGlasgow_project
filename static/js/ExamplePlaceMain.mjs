const MapElement = document.querySelector("#Map");
const Map = new google.maps.Map(MapElement, {
  "zoom": 12.,
  "center": new google.maps.LatLng(MapElement.dataset.lat, MapElement.dataset.lng),
  "mapTypeId": google.maps.MapTypeId.ROADMAP
});

new google.maps.Marker({
  "map": Map,
  "title": "Place location"
}).setPosition(new google.maps.LatLng(MapElement.dataset.lat, MapElement.dataset.lng));


async function GetCommentsFrom(Index){ //This would contain a database call
  return await (await fetch(window.origin + "/suggestGlasgow/GetComments?slug=sugo&start=" + Index)).json();
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


const TComment = document.querySelector("#TComment");
const CommentsPreviewContainer = document.querySelector("#OverflowWrapper");

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
  const CommentsWrapper = document.querySelector("#CommentsWrapper");
  const LoadCommentsButton = document.querySelector("#LoadMoreCommentsButton");
  return async function(){
    if(LoadingComments) return;
    LoadingComments = true;
    LoadCommentsButton.classList.add("Disabled");
    for(let i = 0; i < 5; ++i){
      const TCommentClone = TComment.content.firstElementChild.cloneNode(true);
      const CommentData = (await GetNextComment.next()).value;
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
  document.querySelector("#CommentsOverlayBackground").style.display = "block";
  if(document.querySelector("#CommentsWrapper").childNodes.length === 0) LoadMoreComments();
}
function CloseCommentsView(){
  document.querySelector("#CommentsOverlayBackground").style.display = "none";
}

document.querySelector("#CommentsOverlayBackground").addEventListener("click", function(Event){
  if(Event.target === this) CloseCommentsView(); //Only trigger if the background is clicked
});
document.addEventListener("keydown", function(Event){
  if(Event.code === "Escape") CloseCommentsView();
});

for(const Element of document.querySelectorAll("#CommentButton, #OverflowWrapper")){
  Element.addEventListener("mousedown", function(Event){ //This has to be mousedown because click sometimes misfires on the map
    if(!MapElement.contains(Event.target)) OpenCommentsView();
  });
}

document.querySelector("#LoadMoreCommentsButton").addEventListener("click", LoadMoreComments);

document.querySelectorAll("#Ratings > form").forEach(Element => Element.addEventListener("click", function(Event){
  this.querySelector("button").click();
}));