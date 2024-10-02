import * as React from 'react';
import Card from './Card';

const Player = (props) => {
  const data = props;
  const { cards, value, playerName, gameOver } = data;

  let playerValue = <></>;

  if (value === 21 && cards.length === 2 && playerName === 'Player') {
    playerValue = <p>Blackjack! Your hand value is 21</p>;
  } else if (playerName === 'Player') {
    playerValue = <p>Your hand value is {value}</p>;
  } else if (!gameOver) {
    playerValue = <p>The dealers cards:</p>;
  } else {
    playerValue = <p>The dealers value was {value}, and the dealers cards were:</p>;
  }

  return (
    <div className="Player">
      <div>{playerValue}</div>
      <div className="Player-cards">
        {cards.map((card) => (
          <Card value={card[0]} suit={card[1]} visibility={card[2]} />
        ))}
      </div>
    </div>
  );
};

export default Player;
