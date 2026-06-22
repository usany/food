export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname === "/api/test") {
      const result = await env.DB.prepare("SELECT 1 as test").all();
      return Response.json(result);
    }
    
    return new Response("Django app runs separately. Use SQLite locally or deploy to Workers.");
  }
};