import React from 'react';

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  className = '',
  type = 'button',
  fullWidth = false,
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed border';

  const variants = {
    primary: 'bg-primary hover:bg-primary/90 text-primary-foreground border-primary focus:ring-primary shadow-sm',
    secondary: 'bg-secondary hover:bg-secondary/90 text-secondary-foreground border-secondary focus:ring-secondary shadow-sm',
    outline: 'bg-transparent hover:bg-muted text-foreground border-border focus:ring-ring',
    ghost: 'bg-transparent hover:bg-muted text-foreground border-transparent focus:ring-ring',
    destructive: 'bg-destructive hover:bg-destructive/90 text-destructive-foreground border-destructive focus:ring-destructive shadow-sm',
    card: 'bg-card hover:bg-card/80 text-card-foreground border-border shadow-md hover:shadow-lg'
  };

  const sizes = {
    sm: 'px-3 py-2 text-sm rounded-md',
    md: 'px-4 py-2.5 text-sm rounded-lg',
    lg: 'px-6 py-3 text-base rounded-lg',
    xl: 'px-8 py-4 text-lg rounded-xl'
  };

  const widthClass = fullWidth ? 'w-full' : '';

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${widthClass} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;