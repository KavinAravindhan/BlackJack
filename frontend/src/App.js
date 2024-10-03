import * as React from 'react';
import { useState } from 'react';
import './App.css';
import Player from './components/Player';

const App = () => {
  // general game states
  const [gameId, setGameId] = useState(0);
  const [gameHasStarted, setGameStart] = useState(false);
  const [gameStatus, setGameStatus] = useState(true);

  const [winner, setWinner] = useState(false);

  // player and dealer card states
  const [playerCards, setPlayerCards] = useState([]);
  const [dealerCards, setDealerCards] = useState([]);

  // player and dealer hand value states
  const [playerValue, setPlayerValue] = useState(0);
  const [dealerValue, setDealerValue] = useState(0);

  /**
   * This function handles updating the cards and hand values of the players
   * @param data data returned from flask
   */
  const updateGameState = (data) => {
    setPlayerCards(data.player.cards);
    setDealerCards(data.dealer.cards);

    setPlayerValue(data.player.value);
    setDealerValue(data.dealer.value);

    setGameStatus(data.status);
    setWinner(data.winner);
  };

  const sendAction = async (event) => {
    event.preventDefault();
    const playerAction = event.target.value;

    // api call here
    const res = await fetch(`api/game_action/${gameId}`, {
      method: 'POST',
      type: 'JSON',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: playerAction,
      }),
    });

    const data = await res.json();
    updateGameState(data);
  };

  const gameStart = async (event) => {
    // check if the game has already started
    if (gameHasStarted) {
      return;
    }

    event.preventDefault();

    const res = await fetch('/api/start');
    const data = await res.json();
    setGameId(data.game_id);
    updateGameState(data);

    setGameStart(true);
  };

  const resetGame = () => {
    // reset game states
    setGameStart(false);

    // call gameStart
    gameStart();
  };

  let game = <></>;

  if (!gameHasStarted) {
    game = (
      <button className="NewandStartGameButton" type="button" onClick={gameStart}>
        Start Game!
      </button>
    );
  } else if (gameHasStarted && gameStatus) {
    game = (
      <div>
        <button className="HitStayButtons" type="button" onClick={sendAction} value="hit">
          Hit
        </button>

        <button className="HitStayButtons" type="button" onClick={sendAction} value="stay">
          Stay
        </button>

        {/* print out players information */}
        <Player value={playerValue} cards={playerCards} playerName="Player" gameOver={false} />
        <Player value={dealerValue} cards={dealerCards} playerName="Dealer" gameOver={false} />
      </div>
    );
    // game is over, display everything
  } else {
    let displayWinner = '';
    if (winner === 'player') {
      displayWinner = 'The winner is you!';
    } else if (winner === 'dealer') {
      displayWinner = 'The winner is the dealer!';
    } else {
      displayWinner = 'It was a tie!';
    }

    game = (
      <div>
        <p>{displayWinner}</p>
        <button className="NewandStartGameButton" type="button" onClick={resetGame}>
          New Game
        </button>

        {/* print out players information */}
        <Player value={playerValue} cards={playerCards} playerName="Player" gameOver />
        <Player value={dealerValue} cards={dealerCards} playerName="Dealer" gameOver />
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <p> COMS 4153 - Cloud Casino Blackjack!</p>
      </header>
      <main className="App-main">
        <p>The game ID is {gameId}</p>
        {game}
      </main>
    </div>
  );
};

export default App;
