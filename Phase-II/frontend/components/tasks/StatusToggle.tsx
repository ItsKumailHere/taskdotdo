'use client';

import React from 'react';

interface StatusToggleProps {
  taskId: string;
  completed: boolean;
  onStatusChange: (taskId: string, completed: boolean) => void;
  className?: string;
}

export const StatusToggle: React.FC<StatusToggleProps> = ({
  taskId,
  completed,
  onStatusChange,
  className = ''
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onStatusChange(taskId, e.target.checked);
  };

  return (
    <div className={`flex items-center ${className}`}>
      <label className="inline-flex items-center cursor-pointer">
        <input
          type="checkbox"
          checked={completed}
          onChange={handleChange}
          className="sr-only peer"
        />
        <div className="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
      </label>
    </div>
  );
};