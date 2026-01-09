import { NextRequest, NextResponse } from 'next/server';

// List of public routes that don't require authentication
const publicRoutes = ['/', '/login', '/register'];

export function middleware(request: NextRequest) {
  // Check if the current route is public
  const isPublicRoute = publicRoutes.some(route =>
    request.nextUrl.pathname === route ||
    request.nextUrl.pathname.startsWith(`${route}/`)
  );

  // Get the Better Auth session token from cookies
  const sessionToken = request.cookies.get('better-auth.session_token')?.value;

  // If the route is protected and user is not authenticated, redirect to login
  if (!isPublicRoute && !sessionToken) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Allow the request to proceed
  return NextResponse.next();
}

// Apply middleware to all routes except static assets
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    {
      source: '/((?!api|_next/static|_next/image|favicon.ico).*)',
      missing: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },
  ],
};