import { ResultDisplayProps } from "../types/types";

function ResultDisplay({ score, details }:ResultDisplayProps) {
  const getScoreColor = (score: number) => {
    if (score > 70) return 'text-green-600';
    if (score > 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="mt-6 text-center">
      <h2 className="text-xl font-semibold mb-2">ATS Score</h2>
      <div 
        className={`text-4xl font-bold ${getScoreColor(score)}`}
      >
        {score.toFixed(2)}%
      </div>
      
      {details && (
        <div className="mt-4 text-sm text-gray-600">
          <h3 className="font-medium mb-2">Analysis Details</h3>
          <ul className="list-disc list-inside text-left">
            {details.map((detail, index) => (
              <li key={index}>{detail}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default ResultDisplay;