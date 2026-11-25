export const API='http://127.0.0.1:8000/api';
export function token(){return localStorage.getItem('cc_token')||''}
export async function api(path:string,options:RequestInit={}){const res=await fetch(API+path,{...options,headers:{'Content-Type':'application/json',Authorization:`Bearer ${token()}`,...options.headers}});if(!res.ok)throw new Error(await res.text());return res.json()}
