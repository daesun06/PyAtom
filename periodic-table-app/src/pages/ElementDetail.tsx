import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getElementByAtomicNumber, calculateNeutrons } from '../data/elements';
import AtomicModel from '../components/AtomicModel';
import './ElementDetail.css';

const ElementDetail: React.FC = () => {
  const { atomicNumber } = useParams<{ atomicNumber: string }>();
  const navigate = useNavigate();

  const element = atomicNumber 
    ? getElementByAtomicNumber(parseInt(atomicNumber, 10))
    : undefined;

  if (!element) {
    return (
      <div className="element-detail-error">
        <h1>Element Not Found</h1>
        <p>Sorry, we couldn't find an element with atomic number {atomicNumber}.</p>
        <button className="back-button" onClick={() => navigate('/')}>Back to Periodic Table</button>
      </div>
    );
  }

  const neutrons = calculateNeutrons(element.atomicMass, element.atomicNumber);
  const totalElectrons = element.electronShells.reduce((sum, count) => sum + count, 0);

  return (
    <div className="element-detail-page">
      <div className="element-detail-header">
        <button className="back-button" onClick={() => navigate('/')}>
          <span className="arrow">←</span> Back to Periodic Table
        </button>
      </div>

      <div className="element-detail-content">
        <div className="element-info-section">
          <div className="element-header">
            <div className="element-symbol-container">
              <span className="element-symbol">{element.symbol}</span>
              <span className="atomic-number-badge">{element.atomicNumber}</span>
            </div>
            <h1 className="element-name">{element.name}</h1>
            <span className="element-category">{element.category}</span>
          </div>

          <div className="element-properties">
            <div className="property-card">
              <h3>Atomic Number</h3>
              <p className="property-value">{element.atomicNumber}</p>
            </div>
            <div className="property-card">
              <h3>Atomic Mass</h3>
              <p className="property-value">{element.atomicMass.toFixed(3)} u</p>
            </div>
            <div className="property-card">
              <h3>Protons</h3>
              <p className="property-value">{element.atomicNumber}</p>
            </div>
            <div className="property-card">
              <h3>Neutrons</h3>
              <p className="property-value">{neutrons}</p>
            </div>
            <div className="property-card">
              <h3>Electrons</h3>
              <p className="property-value">{totalElectrons}</p>
            </div>
          </div>

          <div className="electron-configuration">
            <h3>Electron Configuration</h3>
            <p className="configuration-text">{element.electronConfiguration}</p>
            <div className="electron-shells">
              {element.electronShells.map((count, index) => (
                <div key={index} className="shell-item">
                  <span className="shell-label">Shell {index + 1}:</span>
                  <span className="shell-value">{count} electron{count !== 1 ? 's' : ''}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="element-model-section">
          <h2>Atomic Model</h2>
          <p className="model-instructions">Drag to rotate • Scroll to zoom</p>
          <div className="model-container">
            <AtomicModel 
              protons={element.atomicNumber}
              neutrons={neutrons}
              electronShells={element.electronShells}
            />
          </div>
          <div className="model-legend">
            <div className="legend-item">
              <span className="legend-color proton"></span>
              <span>Protons</span>
            </div>
            <div className="legend-item">
              <span className="legend-color neutron"></span>
              <span>Neutrons</span>
            </div>
            <div className="legend-item">
              <span className="legend-color electron"></span>
              <span>Electrons</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ElementDetail;
