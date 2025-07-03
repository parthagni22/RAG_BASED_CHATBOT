import React from 'react';
import { Zap, ArrowRight } from 'lucide-react';
import { QUICK_ACTIONS } from '../../constants';

const WelcomeMessage = ({ onQuickAction }) => (
  <div className="max-w-4xl mx-auto space-y-8">
    {/* Welcome Header */}
    <div className="text-center space-y-4">
      <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-2xl shadow-lg">
        <Zap className="w-8 h-8 text-primary-foreground" />
      </div>
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">
          Welcome to Aggie Navigator
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Your intelligent Texas A&M course assistant. Get help with course information,
          prerequisites, degree planning, and academic recommendations.
        </p>
      </div>
    </div>

    {/* Quick Actions Grid */}
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {QUICK_ACTIONS.map((action) => (
        <div
          key={action.id}
          onClick={() => onQuickAction(action.title)}
          className="group bg-card border border-border rounded-xl p-6 cursor-pointer transition-all duration-200 hover:shadow-lg hover:border-primary/20 hover:-translate-y-1"
        >
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-muted rounded-lg flex items-center justify-center text-2xl group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                {action.icon}
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
                  {action.title}
                </h3>
                <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all" />
              </div>
              <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                {action.description}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>

    {/* Stats Cards */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
      <div className="bg-card border border-border rounded-xl p-4 text-center">
        <div className="text-2xl font-bold text-primary">500+</div>
        <div className="text-sm text-muted-foreground">Courses Available</div>
      </div>
      <div className="bg-card border border-border rounded-xl p-4 text-center">
        <div className="text-2xl font-bold text-secondary">24/7</div>
        <div className="text-sm text-muted-foreground">Always Available</div>
      </div>
      <div className="bg-card border border-border rounded-xl p-4 text-center">
        <div className="text-2xl font-bold text-accent">AI Powered</div>
        <div className="text-sm text-muted-foreground">Smart Assistance</div>
      </div>
    </div>
  </div>
);

export default WelcomeMessage;