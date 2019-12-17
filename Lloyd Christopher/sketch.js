author = "replaceme1author"
score = "replaceme2score"
comment = "replaceme3comment"

function drawText( x, y, text_array ) {
  let positions = {"top": {"x":x,"y":y}, "bottom": {}};
  var pos_x = x;
  for ( var i = 0; i < text_array.length; ++ i ) {
    var part = text_array[i];var t = part[0];
    var c = part[1];var w = textWidth( t );
    fill(color(c));
    text( t, pos_x, y);
    pos_x += w;
    positions.bottom.x = pos_x;
    positions.bottom.y = y;
  }
}



index = 0
currentComment = {}

function setup() {
  lines = round(textWidth(comment)/500)+3;
  textSize(17);
  createCanvas(750, 54+lines*24);
  textFont("Verdana");
  textAlign(LEFT, TOP);
           
}

function draw() {
  //if (!a) {
  //  a = !a;
  //} else return;
  background(37);
  drawText(30, 30, [
    [author, [20, 141, 211]],
    ["  ", [0,0,0]],
    [score, [180]]
  ]);
  
  fill(255)
  
  text(comment, 30, 53, width-(width/12), height-(height/4))

}

function calculateLines() {
  let startWidth = width/12
  let endWidth = width-(width/12)
  let txtWidth = textWidth(currentComment.comment)
  let lines = txtWidth/(startWidth-endWidth);
  return Math.round(Math.abs(lines))+1
}

function keyPressed() {

  console.log(calculateLines())
  resizeCanvas(600, 33+calculateLines()*24+22);
}