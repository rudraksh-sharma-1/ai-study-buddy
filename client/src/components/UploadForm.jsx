import React, { useState } from 'react';
import axios from 'axios';

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState("");
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) return alert("Please select a file.");

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResponse(`Uploaded: ${res.data.filename}`);
      setText(res.data.text || "No text extracted from PDF.");
      setSummary(res.data.summary || "No summary available.");
    } catch (err) {
      console.error("Upload error:", err);
      setResponse("Failed to upload");
    }finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <form onSubmit={handleUpload} className="space-y-4">
        <input type="file" onChange={handleFileChange} className='input' />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          {loading ? <span className="loading loading-ring loading-lg"></span>: "Upload PDF"}
        </button>
      </form>
      {response && <h1 className="mt-4">{response}</h1>}
      {text && <p className="mt-4">{text}</p>}
      {summary && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h2 className="text-lg font-semibold text-black">Summary:</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
};

export default UploadForm;
