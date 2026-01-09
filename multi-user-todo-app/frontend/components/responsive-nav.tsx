"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Menu, X } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ThemeToggle } from "@/components/theme-toggle";

export function ResponsiveNav() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const pathname = usePathname();

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  return (
    <nav className="bg-white dark:bg-gray-800 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="text-xl font-bold text-blue-500">
              TaskDo
            </Link>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <Link href="/dashboard">
              <Button variant={pathname === '/dashboard' ? 'default' : 'ghost'}>
                Dashboard
              </Button>
            </Link>
            <Link href="/tasks">
              <Button variant={pathname === '/tasks' ? 'default' : 'ghost'}>
                Tasks
              </Button>
            </Link>
            <ThemeToggle />
          </div>
          
          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <ThemeToggle />
            <Button variant="ghost" onClick={toggleMenu} className="ml-2">
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>
        
        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <Link href="/dashboard">
                <Button 
                  variant={pathname === '/dashboard' ? 'default' : 'ghost'} 
                  className="w-full justify-start mb-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Dashboard
                </Button>
              </Link>
              <Link href="/tasks">
                <Button 
                  variant={pathname === '/tasks' ? 'default' : 'ghost'} 
                  className="w-full justify-start"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Tasks
                </Button>
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}