// components/SymbolCard.jsx
import React from 'react';
import './SymbolCard.css';

const SymbolCard = ({ symbol }) => (
  <div className="symbol-card">
    <p className='symbol-currency'>{symbol.base_currency}</p>
    <p className="symbol-id">{symbol.id}</p>
    <p className="symbol-status">Status: {symbol.status}</p>
  </div>
);

export default SymbolCard;
