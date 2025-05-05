import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

import {getMe} from './lib/auth'

const protectedRoutes = ['/admin']

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  const isProtected = protectedRoutes.some((route) =>
    pathname.startsWith(route)
  )

  if (isProtected) {
    let me = await getMe();
    console.log(me.data);
    
    // if (!token) {
    //   const loginUrl = new URL('/login', request.url)
    //   loginUrl.searchParams.set('redirect', pathname)
    //   return NextResponse.redirect(loginUrl)
    // }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/admin/:path*'],
}