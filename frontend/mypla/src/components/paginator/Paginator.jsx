import React from 'react';
import './Paginator.css';

export const Paginator = ({ currentPage, hasNextPage, onPageChange }) => {
  return (
    <div className="paginator-container">
      <button
        disabled={currentPage === 1}
        onClick={() => onPageChange(currentPage - 1)}
        className={`paginator-button ${currentPage === 1 ? 'disabled' : ''}`}
      >
        ‹ Anterior
      </button>

      <span className="paginator-page-indicator">Página {currentPage}</span>

      <button
        disabled={!hasNextPage}
        onClick={() => onPageChange(currentPage + 1)}
        className={`paginator-button ${!hasNextPage ? 'disabled' : ''}`}
      >
        Siguiente ›
      </button>
    </div>
  );
};
