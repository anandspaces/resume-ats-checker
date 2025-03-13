import { JobDescriptionInputProps } from "../types/types";

function JobDescriptionInput({ jobDescription, onDescriptionChange }:JobDescriptionInputProps) {
  const handleChange = (e:React.ChangeEvent<HTMLTextAreaElement>) => {
    onDescriptionChange(e.target.value);
  };

  return (
    <div className="mb-4">
      <label 
        htmlFor="job-description" 
        className="block text-sm font-medium text-gray-700 mb-2"
      >
        Job Description
      </label>
      <textarea 
        id="job-description"
        value={jobDescription}
        onChange={handleChange}
        placeholder="Paste job description here"
        className="w-full px-3 py-2 border border-gray-300 rounded-md 
                   focus:outline-none focus:ring-2 focus:ring-blue-500 
                   h-32 resize-none"
      />
    </div>
  );
}

export default JobDescriptionInput;