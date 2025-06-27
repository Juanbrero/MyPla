import './StarCard.css';

export const StarCard = ({ index, isFilled, onClick, onMouseEnter, onMouseLeave }) => {
  return (
    <div
      className="star-card"
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      <i className={`fa-star ${isFilled ? 'fa-solid star-filled' : 'fa-regular star-empty'}`}></i>
    </div>
  );
};




