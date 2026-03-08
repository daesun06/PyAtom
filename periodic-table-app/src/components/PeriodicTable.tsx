import React from 'react';
import { elements, getCategoryColor } from '../data/elements';
import type { Element } from '../data/elements';

interface PeriodicTableProps {
  onElementClick: (element: Element) => void;
}

const PeriodicTable: React.FC<PeriodicTableProps> = ({ onElementClick }) => {
  // Create a grid map: period -> group -> element
  const gridMap = new Map<number, Map<number, Element>>();

  elements.forEach((element) => {
    if (!gridMap.has(element.period)) {
      gridMap.set(element.period, new Map());
    }
    gridMap.get(element.period)!.set(element.group, element);
  });

  // Lanthanides and Actinides positions (periods 8-9 for display, groups 3-17)
  const lanthanides = elements.filter((e) => e.category === 'lanthanide');
  const actinides = elements.filter((e) => e.category === 'actinide');

  return (
    <div className="periodic-table-container">
      <div className="periodic-table">
        {/* Main table - periods 1-7 */}
        {[1, 2, 3, 4, 5, 6, 7].map((period) => (
          <div key={period} className="period-row">
            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18].map((group) => {
              const element = gridMap.get(period)?.get(group);

              // Special handling for lanthanides/actinides placeholder
              if (period === 6 && group === 3) {
                return (
                  <div
                    key={`${period}-${group}`}
                    className="element-cell placeholder-cell"
                    style={{ backgroundColor: '#ffbfff' }}
                    title="Lanthanides"
                  >
                    <span className="placeholder-text">57-71</span>
                  </div>
                );
              }

              if (period === 7 && group === 3) {
                return (
                  <div
                    key={`${period}-${group}`}
                    className="element-cell placeholder-cell"
                    style={{ backgroundColor: '#ff99cc' }}
                    title="Actinides"
                  >
                    <span className="placeholder-text">89-103</span>
                  </div>
                );
              }

              // Skip lanthanides and actinides from main grid
              if (element?.category === 'lanthanide' || element?.category === 'actinide') {
                return <div key={`${period}-${group}`} className="element-cell empty-cell" />;
              }

              if (element) {
                return (
                  <div
                    key={element.atomicNumber}
                    className="element-cell"
                    style={{ backgroundColor: getCategoryColor(element.category) }}
                    onClick={() => onElementClick(element)}
                    title={`${element.name} (${element.symbol})`}
                  >
                    <span className="atomic-number">{element.atomicNumber}</span>
                    <span className="symbol">{element.symbol}</span>
                    <span className="name">{element.name}</span>
                  </div>
                );
              }

              return <div key={`${period}-${group}`} className="element-cell empty-cell" />;
            })}
          </div>
        ))}

        {/* Spacer row */}
        <div className="spacer-row" />

        {/* Lanthanides row */}
        <div className="period-row lanthanide-row">
          <div className="element-cell empty-cell" />
          <div className="element-cell empty-cell" />
          {lanthanides.map((element) => (
            <div
              key={element.atomicNumber}
              className="element-cell"
              style={{ backgroundColor: getCategoryColor(element.category) }}
              onClick={() => onElementClick(element)}
              title={`${element.name} (${element.symbol})`}
            >
              <span className="atomic-number">{element.atomicNumber}</span>
              <span className="symbol">{element.symbol}</span>
              <span className="name">{element.name}</span>
            </div>
          ))}
        </div>

        {/* Actinides row */}
        <div className="period-row actinide-row">
          <div className="element-cell empty-cell" />
          <div className="element-cell empty-cell" />
          {actinides.map((element) => (
            <div
              key={element.atomicNumber}
              className="element-cell"
              style={{ backgroundColor: getCategoryColor(element.category) }}
              onClick={() => onElementClick(element)}
              title={`${element.name} (${element.symbol})`}
            >
              <span className="atomic-number">{element.atomicNumber}</span>
              <span className="symbol">{element.symbol}</span>
              <span className="name">{element.name}</span>
            </div>
          ))}
        </div>
      </div>

      <style>{`
        .periodic-table-container {
          width: 100%;
          overflow-x: auto;
          padding: 20px;
          box-sizing: border-box;
        }

        .periodic-table {
          display: flex;
          flex-direction: column;
          gap: 4px;
          min-width: 1200px;
        }

        .period-row {
          display: grid;
          grid-template-columns: repeat(18, 1fr);
          gap: 4px;
        }

        .spacer-row {
          height: 20px;
        }

        .element-cell {
          aspect-ratio: 1;
          border: 1px solid #333;
          border-radius: 4px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 4px;
          cursor: pointer;
          transition: transform 0.2s ease, box-shadow 0.2s ease;
          position: relative;
          min-height: 60px;
        }

        .element-cell:hover {
          transform: scale(1.1);
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
          z-index: 10;
        }

        .element-cell.empty-cell {
          border: none;
          background: transparent;
          cursor: default;
          pointer-events: none;
        }

        .element-cell.empty-cell:hover {
          transform: none;
          box-shadow: none;
        }

        .element-cell.placeholder-cell {
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.75rem;
          font-weight: bold;
          color: #333;
          cursor: default;
        }

        .element-cell.placeholder-cell:hover {
          transform: scale(1.05);
        }

        .atomic-number {
          position: absolute;
          top: 4px;
          left: 4px;
          font-size: 0.7rem;
          color: #333;
        }

        .symbol {
          font-size: 1.2rem;
          font-weight: bold;
          color: #000;
          margin-top: 8px;
        }

        .name {
          font-size: 0.6rem;
          color: #333;
          text-align: center;
          line-height: 1.2;
          margin-top: 2px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          max-width: 100%;
        }

        .placeholder-text {
          font-size: 0.8rem;
          font-weight: bold;
        }

        /* Responsive adjustments */
        @media (max-width: 1400px) {
          .periodic-table {
            min-width: 1000px;
          }

          .element-cell {
            min-height: 50px;
          }

          .symbol {
            font-size: 1rem;
          }

          .name {
            font-size: 0.5rem;
          }

          .atomic-number {
            font-size: 0.6rem;
          }
        }

        @media (max-width: 768px) {
          .periodic-table-container {
            padding: 10px;
          }

          .periodic-table {
            min-width: 800px;
            gap: 2px;
          }

          .period-row {
            gap: 2px;
          }

          .element-cell {
            min-height: 40px;
            padding: 2px;
          }

          .symbol {
            font-size: 0.9rem;
            margin-top: 4px;
          }

          .name {
            font-size: 0.45rem;
          }

          .atomic-number {
            font-size: 0.5rem;
            top: 2px;
            left: 2px;
          }
        }
      `}</style>
    </div>
  );
};

export default PeriodicTable;
