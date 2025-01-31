// src/App.jsx
import { useState } from 'react';
import FileUploader from './components/FileUploader';
import JobDescriptionInput from './components/JobDescriptionInput';
import ResultDisplay from './components/ResultDisplay';
import { analyzeResume } from './services/apiService';
import { validateFileAndDescription } from './utils/validations';

function App() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (file) => {
    setResume(file);
    setError('');
  };

  const handleJobDescriptionChange = (description) => {
    setJobDescription(description);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate inputs
    const validationError = validateFileAndDescription(resume, jobDescription);
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('resume', resume);
      formData.append('jobDescription', jobDescription);

      const result = await analyzeResume(formData);
      setAnalysisResult(result);
    } catch (err) {
      setError('Failed to analyze resume. Please try again.');
      console.error('Resume analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white shadow-md rounded-lg p-8">
        <h1 className="text-2xl font-bold text-center mb-6">
          Resume ATS Score Checker
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <FileUploader 
            onFileUpload={handleFileUpload} 
            selectedFile={resume}
          />

          <JobDescriptionInput 
            jobDescription={jobDescription}
            onDescriptionChange={handleJobDescriptionChange}
          />

          {error && (
            <div className="text-red-500 text-sm text-center">
              {error}
            </div>
          )}

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 
                       transition-colors duration-300 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Check ATS Score'}
          </button>
        </form>

        {analysisResult && (
          <ResultDisplay 
            score={analysisResult.score} 
            details={analysisResult.details}
          />
        )}
      </div>
    </div>
  );
}

export default App;