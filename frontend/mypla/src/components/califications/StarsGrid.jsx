import { StarCard } from "./StarCard";
import './StarsGrid.css';

export const StarsGrid = ({ rating, hoverRating, onSelectEvent, onHover, onLeave }) => {
  const stars = [1, 2, 3, 4, 5];

  return (
    <fieldset className="stars-grid">
      <legend className="star-grid-label">Calificacion</legend>
      <div className="stars-grid-content">
        {stars.map((index) => (
          <StarCard
            key={index}
            index={index}
            isFilled={hoverRating >= index || (!hoverRating && rating >= index)}
            onClick={() => onSelectEvent(index)}
            onMouseEnter={() => onHover(index)}
            onMouseLeave={onLeave}
          />
        ))}
      </div>
    </fieldset>
  );
};
