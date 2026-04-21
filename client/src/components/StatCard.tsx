export default function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div style={{
      background: '#ffffff',
      border: '1px solid var(--border-color)',
      borderRadius: '8px',
      padding: '1.5rem',
      boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
    }}>
      <div style={{ 
        fontSize: '0.75rem', textTransform: 'uppercase', 
        letterSpacing: '1px', color: 'var(--text-muted)', marginBottom: '0.5rem' 
      }}>
        {label}
      </div>
      <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--text-main)' }}>
        {value}
      </div>
    </div>
  );
}