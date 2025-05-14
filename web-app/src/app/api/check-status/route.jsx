// TODO: Change to S3 workflow.

export async function GET(Request) {
  const { searchParams } = new URL(req.url);
  const filePath = searchParams.get('filePath');

  const res = await fetch(`http://localhost:8000/process-video`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ file_path: filePath }),
  });

  const data = await res.json();
  return Response.json({ status: data.status });
}