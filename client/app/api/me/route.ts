// app/api/posts/route.ts

import { getMe, login } from '@/lib/auth';
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  
  let res = await getMe();
  console.log(res);

  return NextResponse.json(res.data)
}
