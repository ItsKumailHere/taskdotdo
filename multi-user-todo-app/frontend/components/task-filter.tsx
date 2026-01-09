"use client";

import { TaskStatus } from "@/lib/types";

interface TaskFilterProps {
  currentFilter: TaskStatus | "all";
  onFilterChange: (filter: TaskStatus | "all") => void;
}

export function TaskFilter({ currentFilter, onFilterChange }: TaskFilterProps) {
  return (
    <div className="flex space-x-2 mb-4">
      {(["all", "pending", "completed"] as const).map((filter) => (
        <button
          key={filter}
          className={`px-4 py-2 rounded-md ${
            currentFilter === filter
              ? "bg-blue-500 text-white"
              : "bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200"
          }`}
          onClick={() => onFilterChange(filter)}
        >
          {filter.charAt(0).toUpperCase() + filter.slice(1)}
        </button>
      ))}
    </div>
  );
}