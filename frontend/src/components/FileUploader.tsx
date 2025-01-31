function FileUploader({ onFileUpload, selectedFile }) {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    onFileUpload(file);
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
          <span className="ml-2 text-sm text-green-600">
            {selectedFile.name}
          </span>
        )}
      </div>
    </div>
  );
}

export default FileUploader;