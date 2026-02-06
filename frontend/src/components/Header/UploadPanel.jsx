import { useState } from "react";
import { uploadFiles } from "../../api/uploadApi";

export default function UploadPanel({ onUploadComplete }) {
  // 🔹 Files selected but NOT uploaded yet
  const [selectedFiles, setSelectedFiles] = useState([]);

  // 🔹 When user selects files
  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    if (!files.length) return;

    // Append files (allow multiple selections)
    setSelectedFiles((prev) => [...prev, ...files]);

    // Reset input so same file can be chosen again if needed
    e.target.value = "";
  };

  // 🔹 When user clicks Upload
  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;

    try {
      await uploadFiles(selectedFiles);
      console.log("Upload successful");

      // Clear frontend state
      setSelectedFiles([]);

      // Refresh sidebar (Home.jsx)
      if (typeof onUploadComplete === "function") {
        onUploadComplete();
      }
    } catch (err) {
      console.error("Upload error:", err);
    }
  };

  return (
    <div>
      {/* Choose files */}
      <input
        type="file"
        multiple
        onChange={handleFileSelect}
      />

      {/* Upload button appears ONLY if files are selected */}
      {selectedFiles.length > 0 && (
        <div style={{ marginTop: "8px" }}>
          <button onClick={handleUpload}>
            Upload ({selectedFiles.length})
          </button>
        </div>
      )}
    </div>
  );
}
