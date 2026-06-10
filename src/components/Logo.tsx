export function Logo({ className = "" }: { className?: string }) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className="flex items-center gap-1">
        {/* Pink angle brackets */}
        <span className="text-2xl font-bold text-primary">&lt;</span>
        <span className="text-2xl font-bold text-primary">&gt;</span>
        {/* Brand text */}
        <span className="text-xl font-semibold tracking-tight ml-1">CodeCraft</span>
      </div>
    </div>
  )
}
