'use client';

import React, { useState } from 'react';

interface DeleteConfirmationProps {
  taskId: string;
  onDelete: (taskId: string) => void;
  taskTitle: string;
}

export const DeleteConfirmation: React.FC<DeleteConfirmationProps> = ({
  taskId,
  onDelete,
  taskTitle
}) => {
  const [showDialog, setShowDialog] = useState(false);

  const handleDelete = () => {
    onDelete(taskId);
    setShowDialog(false);
  };

  return (
    <>
      <button
        onClick={() => setShowDialog(true)}
        className="text-red-600 hover:text-red-800"
      >
        Delete
      </button>

      {showDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Confirm Deletion</h3>
            <p className="text-gray-600 mb-4">
              Are you sure you want to delete the task "{taskTitle}"? This action cannot be undone.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowDialog(false)}
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};