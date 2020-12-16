<!DOCTYPE html>
<html>
<head><title> Tyler Barnes</title></head>
<H1>Chess AI Project</H1>
<p> This is a chess AI created in Python that utilizes the minimax search algorith as well as alpha-beta pruning in order to come up with the best moves </p>
<p> A killer huetristic was added to this alpha beta pruning for added efficiency </p>
<p> The player will always be white and move first</p>
<p> Castling, En Passant, and Promotion are all possible, however the game autopromotes to queen</p>
<p> The game does not prevent the player from making an illegal move while in check</p>
<p> The AI will always avoid check if possible but if the player does not they will lose</p>
<h1> How to play:</h1>
<p> Click the download link to get a zip with all the necessary Python files</p>
<p> (All files are also on <a href="https://github.com/trbarnes/Website/tree/main/ChessEngine">github</a> however some of the files there are test files)</p>
<a href="/static/ChessAi.zip" download>
  <img src="/static/download.png" alt="Dowload">
</a>
</html>
<p> Make sure you have Python 3 installed and then in the same directory as the files type: python main.py</p>
<p> You should see the game start and look like this</p>
<img src="/static/start.png">
<p> Format your moves in coordinate form (EX: e2e4)</p>
<img src="/static/middle.png">
<p> After each of your moves the AI will make its own move</p>
<img src="/static/end.png">
<p> And that's it, the rest is just trying to win!</p>