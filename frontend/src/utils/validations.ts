export const validateFileAndDescription = (resume: File | null, jobDescription: string) => {
  if (!resume) return 'Please upload a resume';
  if (!jobDescription.trim()) return 'Please provide a job description';
  
  const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  
  const allowedExtensions = ['.pdf', '.docx'];
  const fileName = resume.name.toLowerCase();

  if (!allowedTypes.includes(resume.type)) {
    return 'Invalid file type. Please upload PDF or Word document';
  }

  if (!allowedExtensions.some(ext => fileName.endsWith(ext))) {
    return 'Invalid file extension. Use .pdf or .docx';
  }

  if (resume.size > 5 * 1024 * 1024) {
    return 'File size exceeds 5MB limit';
  }

  return null;
};