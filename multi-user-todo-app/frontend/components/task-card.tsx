import { Todo } from "@/lib/types";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";

interface TaskCardProps {
  task: Todo;
  onToggleComplete: (id: string, completed: boolean) => void;
  onDelete: (id: string) => void;
}

export function TaskCard({ task, onToggleComplete, onDelete }: TaskCardProps) {
  return (
    <div className={`task-card border rounded-lg p-4 bg-white dark:bg-gray-800 flex items-start ${task.status === 'completed' ? 'task-completed' : ''}`}>
      <Checkbox
        checked={task.status === 'completed'}
        onCheckedChange={(checked) => onToggleComplete(task.id, checked as boolean)}
        className="mt-1 mr-3"
      />
      <div className="flex-1">
        <h3 className={`task-title text-lg font-medium ${task.status === 'completed' ? 'line-through text-gray-500' : ''}`}>
          {task.title}
        </h3>
        {task.description && (
          <p className="text-gray-600 dark:text-gray-300 mt-1">{task.description}</p>
        )}
        {task.due_date && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Due: {new Date(task.due_date).toLocaleDateString()}
          </p>
        )}
      </div>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => onDelete(task.id)}
        className="text-red-500 hover:text-red-700"
      >
        <Trash2 className="h-4 w-4" />
      </Button>
    </div>
  );
}