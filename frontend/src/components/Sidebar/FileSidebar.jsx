import { deleteDocument } from "../../api/documentsApi";

export default function FileSidebar(props) {
  const {
    documents = [],
    selectedDocId,
    onSelectDoc,
    onRefresh,
  } = props;

  // ✅ SAFE: documents always an array
  if (documents.length === 0) {
    return <div>No documents available</div>;
  }

  const handleDelete = async (docId) => {
    if (!window.confirm(`Delete ${docId}?`)) return;

    try {
      await deleteDocument(docId);
      onRefresh();
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  return (
    <div>
      <h3>Documents</h3>
      <ul>
        {documents.map((doc) => (
          <li
            key={doc.doc_id}
            style={{
              fontWeight:
                selectedDocId === doc.doc_id ? "bold" : "normal",
            }}
          >
            <span
              style={{ cursor: "pointer" }}
              onClick={() => onSelectDoc(doc.doc_id)}
            >
              {doc.doc_id}
            </span>

            <button
              style={{ marginLeft: 8 }}
              onClick={() => handleDelete(doc.doc_id)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
