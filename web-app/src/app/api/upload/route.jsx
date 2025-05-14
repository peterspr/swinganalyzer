import fs from 'fs';
import path from 'path';


// TODO: Changed to uploading to S3.

export async function POST(req) {
  const formData = await req.formData();
  const file = formData.get('file');

  const arrayBuffer = await file.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);

  const uploadDir = path.join(process.cwd(), 'uploads');
  const filePath = path.join(uploadDir, `${Date.now()}_${file.name}`);

  fs.writeFileSync(filePath, buffer);

  const userID = 'local-dev';
  const timestamp = new Date().toISOString();

  return Response.json({ userID, timestamp, filePath });
}