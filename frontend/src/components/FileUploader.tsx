import { FileUploaderProps } from "../types/types";

function FileUploader({ onFileUpload, selectedFile }:FileUploaderProps) {
  const handleFileChange = (e:React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileUpload(e.target.files[0]);
    }
     e.target.value = '';
  };

  const handleClearFile = () => {
    onFileUpload(null);
  };

  return (
    <div className="mb-4">
      <label 
        htmlFor="resume-upload" 
        className="block text-sm font-medium text-gray-700 mb-2"
      >
        Upload Resume
      </label>
      <div className="flex items-center">
        <input 
          id="resume-upload"
          type="file" 
          accept=".pdf,.doc,.docx"
          onChange={handleFileChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md 
                     focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {selectedFile && (
          <button
            type="button"
            onClick={handleClearFile}
            className="ml-2 text-sm text-red-600 hover:text-red-800"
          >
            Clear
          </button>
        )}
        </div>
        {selectedFile && (
          <span className="ml-2 text-sm text-green-600">
            {selectedFile.name}
          </span>
        )}
    </div>
  );
}

export default FileUploader;