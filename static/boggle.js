"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();

  // loop over board and create the DOM tr/td structure
  const $body = $("<tbody>");
  $table.append($body);

  for (let i = 0; i < 5; i++) {
    const $row = $("<tr>");

    for (let j = 0; j < 5; j++) {
      const $cell = $("<td>")
        .text(board[i][j])
        .attr("id", `${i}-${j}`);

      $row.append($cell);
    }

    $table.append($row);
  }

}

/** Submit word to API */
async function submitWord(evt) {
  evt.preventDefault();

  const response = await fetch('/api/score-word', {
    method: "POST",
    body: JSON.stringify({ "gameId": `${gameId}`, "word": $(evt.target).val() }),
    headers: {
      "content-type": "application/json"
    }
  });

  const result = await response.json();
}

$form.on("submit", ".word-input-btn", submitWord);

start();