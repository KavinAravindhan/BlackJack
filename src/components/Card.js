import * as React from 'react';
// import backside from '../card.png';

const Card = (props) => {
  const data = props;
  const { value, suit, visibility } = data;

  let card = <></>;
  /* switch case for suits */
  let cSuit = '';

  switch (suit) {
    case 'Hearts':
      cSuit = <>&hearts;</>;
      break;

    case 'Diamonds':
      cSuit = <>&diams;</>;
      break;

    case 'Spades':
      cSuit = <>&spades;</>;
      break;

    case 'Clubs':
      cSuit = <>&clubs;</>;
      break;

    default:
      break;
  }

  if (visibility === false) {
    card = (
      <>
        <div className="Card-front Card-backside-test">
          <div className="Card-wrapper">
            <div className="Top-value">
              {' '}
              {value}
              <br /> {cSuit}{' '}
            </div>
            <div className="Suit"> {cSuit} </div>
            <div className="Bottom-value">
              {' '}
              {value}
              <br /> {cSuit}
            </div>
          </div>
        </div>
      </>
    );
  } else {
    card = (
      <>
        <div className="Card-front">
          <div className="Top-value">
            {' '}
            {value}
            <br /> {cSuit}{' '}
          </div>
          <div className="Suit"> {cSuit} </div>
          <div className="Bottom-value">
            {' '}
            {value}
            <br /> {cSuit}
          </div>
        </div>
      </>
    );
  }

  return <div className="Card">{card}</div>;
};

export default Card;
