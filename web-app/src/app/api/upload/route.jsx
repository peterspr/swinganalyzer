import { v4 as uuidv4 } from 'uuid';

export async function POST(req) {
  const formData = await req.formData();
  const file = formData.get('file');

  const userID = uuidv4();
  const timestamp = new Date().toISOString();

  // TODO: Actually upload file to S3 here
  // Simulate upload for now

  return Response.json({ userID, timestamp });
}