import { cn } from '@/lib/utils'
import { AlertCircle, CheckCircle2, Info, AlertTriangle } from 'lucide-react'

export function Alert({ className, variant = 'default', children, ...props }) {
  const variants = {
    default: 'bg-background text-foreground border',
    success: 'bg-green-50 text-green-900 border-green-200',
    warning: 'bg-yellow-50 text-yellow-900 border-yellow-200',
    error: 'bg-red-50 text-red-900 border-red-200',
    info: 'bg-blue-50 text-blue-900 border-blue-200',
  }

  const icons = {
    default: Info,
    success: CheckCircle2,
    warning: AlertTriangle,
    error: AlertCircle,
    info: Info,
  }

  const Icon = icons[variant]

  return (
    <div
      role="alert"
      className={cn('relative w-full rounded-lg border p-4', variants[variant], className)}
      {...props}
    >
      <div className="flex gap-3">
        <Icon className="h-5 w-5 flex-shrink-0" />
        <div className="flex-1">{children}</div>
      </div>
    </div>
  )
}

export function AlertTitle({ className, children, ...props }) {
  return (
    <h5 className={cn('mb-1 font-medium leading-none tracking-tight', className)} {...props}>
      {children}
    </h5>
  )
}

export function AlertDescription({ className, children, ...props }) {
  return (
    <div className={cn('text-sm [&_p]:leading-relaxed', className)} {...props}>
      {children}
    </div>
  )
}
