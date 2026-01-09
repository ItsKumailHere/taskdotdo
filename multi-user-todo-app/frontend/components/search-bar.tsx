"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";

interface SearchBarProps {
  onSearch: (query: string) => void;
}

export function SearchBar({ onSearch }: SearchBarProps) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      onSearch(query);
    }, 300); // Debounce search by 300ms

    return () => clearTimeout(timeoutId);
  }, [query, onSearch]);

  return (
    <div className="mb-4">
      <Input
        type="text"
        placeholder="Search tasks..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full"
      />
    </div>
  );
}