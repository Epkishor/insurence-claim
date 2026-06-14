export default function StatusBadge({ status }) {
  const colors = {
    PENDING_DOCUMENTS: "#f59e0b",
    DOCUMENTS_UPLOADED: "#3b82f6",
    PROCESSING: "#8b5cf6",
    UNDER_REVIEW: "#6366f1",
    APPROVED: "#22c55e",
    PARTIALLY_APPROVED: "#14b8a6",
    REJECTED: "#ef4444",
    MORE_DOCUMENTS_REQUIRED: "#f97316",
  };

  return (
    <span
      style={{
        background: colors[status] || "#64748b",
        color: "white",
        padding: "4px 8px",
        borderRadius: 5,
        fontSize: 13,
      }}
    >
      {status}
    </span>
  );
}