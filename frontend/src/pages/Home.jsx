import { useEffect, useState } from "react";
import SearchBar from "../components/Header/searchBar"; // ✅ FIXED casing
import UploadPanel from "../components/Header/UploadPanel";
import FileSidebar from "../components/Sidebar/FileSidebar";
import { searchDocuments } from "../api/searchApi";
import { fetchDocuments } from "../api/documentsApi";

export default function Home() {
  // 🔹 Document library state (sidebar)
  const [documents, setDocuments] = useState([]);
  const [selectedDocId, setSelectedDocId] = useState(null);

  // 🔹 Search state (kept for next phases)
  const [results, setResults] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(null);

  // 🔹 Load documents for sidebar
  const loadDocuments = async () => {
    try {
      const docs = await fetchDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error("Failed to load documents:", err);
    }
  };

  // 🔹 Load document list on app start
  useEffect(() => {
    loadDocuments();
  }, []);

  // 🔹 Search handler (NO auto-select, by design)
  const handleSearch = async (query) => {
    try {
      const data = await searchDocuments(query);
      setResults(data);
      setSelectedIndex(null);
      // DO NOT auto-select document here
    } catch (err) {
      console.error("Search failed:", err);
    }
  };

  return (
    <div>
      <h2>Document Search Engine</h2>

      {/* Search is independent */}
      <SearchBar onSearch={handleSearch} />

      {/* Deferred upload with explicit Upload button */}
      <UploadPanel onUploadComplete={loadDocuments} />

      {/* Persistent document library */}
      <FileSidebar
        documents={documents}
        selectedDocId={selectedDocId}
        onSelectDoc={setSelectedDocId}
        onRefresh={loadDocuments}
      />

      {/* TEMP DEBUG (safe to remove later) */}
      {selectedDocId && (
        <div style={{ marginTop: "10px" }}>
          Selected document: <b>{selectedDocId}</b>
        </div>
      )}
    </div>
  );
}
