// app/api/posts/route.ts

import { getMe, login } from '@/lib/auth';
import { NextResponse } from 'next/server'

import { cookies } from 'next/headers'

export async function POST(request: Request) {
  
  let username = 'devminhphuc';
  let password = '123123';

  let res = await login(username, password);
  if (res.data) {
    
    const access_token = res.data.access_token;
    let my = await cookies();
    my.set('access_token', access_token);
  }

  return NextResponse.json(res.data)
}
