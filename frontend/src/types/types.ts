export interface FileUploaderProps {
  onFileUpload: (file: File | null) => void;
  selectedFile: File | null;
}

export interface JobDescriptionInputProps {
  jobDescription: string;
  onDescriptionChange: (description: string) => void;
}

export interface ResultDisplayProps {
  score: number;
  details?: string[];
}

export interface ApiResponse {
  score: number;
  details: string[];
}

