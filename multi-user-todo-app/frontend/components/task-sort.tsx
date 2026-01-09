"use client";

interface TaskSortProps {
  currentSort: string;
  currentOrder: string;
  onSortChange: (sort: string, order: string) => void;
}

export function TaskSort({ currentSort, currentOrder, onSortChange }: TaskSortProps) {
  return (
    <div className="flex space-x-2 mb-4">
      <select
        value={currentSort}
        onChange={(e) => onSortChange(e.target.value, currentOrder)}
        className="border rounded-md p-2 dark:bg-gray-700 dark:text-white"
      >
        <option value="created_at">Sort by Date</option>
        <option value="title">Sort by Title</option>
        <option value="due_date">Sort by Due Date</option>
      </select>
      
      <select
        value={currentOrder}
        onChange={(e) => onSortChange(currentSort, e.target.value)}
        className="border rounded-md p-2 dark:bg-gray-700 dark:text-white"
      >
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
      </select>
    </div>
  );
}